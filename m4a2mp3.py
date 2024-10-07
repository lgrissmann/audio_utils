import os
import sys
from pydub import AudioSegment
import subprocess
import shutil
from mutagen.easymp4 import EasyMP4  # Para ler tags do m4a
from mutagen.flac import FLAC        # Para ler tags do flac
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TDRC, TCON, ID3NoHeaderError

# Função para obter o bitrate do arquivo de entrada usando ffmpeg
def get_audio_bitrate(file_path):
    command = ["ffmpeg", "-i", file_path, "-f", "ffmetadata", "-"]
    result = subprocess.run(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    output = result.stderr.decode()
    
    for line in output.splitlines():
        if "bitrate:" in line:
            bitrate = line.split("bitrate:")[1].strip().split(" ")[0] + "k"
            return bitrate
    return None

# Função para copiar tags de .m4a e .flac para .mp3
def copy_tags(source_file, mp3_file):
    try:
        if source_file.endswith('.m4a'):
            source_tags = EasyMP4(source_file)
        elif source_file.endswith('.flac'):
            source_tags = FLAC(source_file)
        else:
            return
        
        mp3_tags = ID3(mp3_file)
        
        # Copiando tags
        if 'title' in source_tags:
            mp3_tags.add(TIT2(encoding=3, text=source_tags['title'][0]))
        if 'artist' in source_tags:
            mp3_tags.add(TPE1(encoding=3, text=source_tags['artist'][0]))
        if 'album' in source_tags:
            mp3_tags.add(TALB(encoding=3, text=source_tags['album'][0]))
        if 'date' in source_tags:
            mp3_tags.add(TDRC(encoding=3, text=source_tags['date'][0]))
        if 'genre' in source_tags:
            mp3_tags.add(TCON(encoding=3, text=source_tags['genre'][0]))
        
        mp3_tags.save(v2_version=3)
        # print(f"Tags copiadas de {source_file} para {mp3_file}")
    except ID3NoHeaderError:
        print(f"Não foi possível adicionar tags ao arquivo {mp3_file}")

# Função para converter arquivo .m4a ou .flac para .mp3 mantendo o bitrate da entrada
def convert_to_mp3(source_file, output_file, bitrate="192k"):
    audio = AudioSegment.from_file(source_file)
    audio.export(output_file, format="mp3", bitrate=bitrate)
    print(f"Convertido: {source_file} -> {output_file} (bitrate: {bitrate})")

# Função para buscar arquivos .m4a e .flac em um diretório recursivamente e processá-los
def convert_and_copy_music_in_directory(root_dir, output_dir):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            # Se for arquivo .m4a ou .flac, converte para .mp3
            if file.endswith(".m4a") or file.endswith(".flac"):
                source_file = os.path.join(subdir, file)
                
                # Caminho relativo para manter a estrutura de diretórios
                relative_path = os.path.relpath(subdir, root_dir)
                output_subdir = os.path.join(output_dir, relative_path)
                os.makedirs(output_subdir, exist_ok=True)
                
                mp3_file = os.path.join(output_subdir, os.path.splitext(file)[0] + ".mp3")
                
                # Obtém o bitrate do arquivo de entrada
                bitrate = get_audio_bitrate(source_file)
                if bitrate is None:
                    print(f"Não foi possível obter o bitrate de {source_file}. Usando 192k.")
                    bitrate = "192k"
                
                # Converte o arquivo para .mp3
                convert_to_mp3(source_file, mp3_file, bitrate)
                
                # Copia as tags do arquivo de origem para o arquivo .mp3
                copy_tags(source_file, mp3_file)

            # Se for arquivo .mp3, copia diretamente mantendo a estrutura de diretórios
            elif file.endswith(".mp3"):
                mp3_file = os.path.join(subdir, file)
                
                relative_path = os.path.relpath(subdir, root_dir)
                output_subdir = os.path.join(output_dir, relative_path)
                os.makedirs(output_subdir, exist_ok=True)
                
                output_mp3_file = os.path.join(output_subdir, file)
                shutil.copy2(mp3_file, output_mp3_file)
                print(f"Copiado: {mp3_file} -> {output_mp3_file}")

# Verifica se os argumentos de linha de comando foram passados
if len(sys.argv) != 3:
    print("Uso: python m4a2mp3.py <diretorio_entrada> <diretorio_saida>")
    sys.exit(1)

# Obtém os diretórios de entrada e saída dos parâmetros da linha de comando
input_directory = sys.argv[1]
output_directory = sys.argv[2]

# Iniciar conversão e cópia
convert_and_copy_music_in_directory(input_directory, output_directory)
