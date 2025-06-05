import os
import sys
import logging
from pydub import AudioSegment
import subprocess
import shutil
from mutagen.easymp4 import EasyMP4  # Para ler tags do m4a
from mutagen.flac import FLAC       # Para ler tags do flac
from mutagen.oggvorbis import OggVorbis  # Para ler tags do ogg vorbis
from mutagen.oggopus import OggOpus  # Para ler tags do ogg opus
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TDRC, TCON, ID3NoHeaderError

# Configuração do sistema de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),  # Logs para console
        logging.FileHandler("conversion.log", mode="w")  # Logs para arquivo
    ]
)

logger = logging.getLogger(__name__)

# Constante para o bitrate padrão
DEFAULT_BITRATE = "160k"

# Função para copiar tags de .m4a, .flac, .ogg e .opus para .mp3
def copy_tags(source_file, mp3_file):
    try:
        if source_file.endswith('.m4a'):
            source_tags = EasyMP4(source_file)
        elif source_file.endswith('.flac'):
            source_tags = FLAC(source_file)
        elif source_file.endswith('.ogg'):
            source_tags = OggVorbis(source_file)
        elif source_file.endswith('.opus'):
            source_tags = OggOpus(source_file)
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
    except ID3NoHeaderError:
        logger.warning(f"{mp3_file}: Não foi possível adicionar tags ao arquivo")

# Função para converter arquivo de entrada para .mp3 mantendo o bitrate
def convert_to_mp3(source_file, output_file, bitrate):
    audio = AudioSegment.from_file(source_file)
    audio.export(output_file, format="mp3", bitrate=bitrate)
    

# Função para buscar arquivos em um diretório recursivamente e processá-los
def convert_and_copy_music_in_directory(root_dir, output_dir, target_bitrate):
    for subdir, _, files in os.walk(root_dir):
        for file in files:

            if file.endswith((".m4a", ".flac", ".ogg", ".opus", ".mp3")):
                source_file = os.path.join(subdir, file)
                
                # Caminho relativo para manter a estrutura de diretórios
                relative_path = os.path.relpath(subdir, root_dir)
                output_subdir = os.path.join(output_dir, relative_path)
                os.makedirs(output_subdir, exist_ok=True)
                
                output_mp3_file = os.path.join(output_subdir, os.path.splitext(file)[0] + ".mp3")

                if file.endswith((".m4a", ".flac", ".ogg", ".opus")):
                    convert_to_mp3(source_file, output_mp3_file, target_bitrate)
                    copy_tags(source_file, output_mp3_file)
                    logger.info(f"{source_file} - convertido -> {output_mp3_file}")

                # Se for arquivo .mp3, copia diretamente mantendo a estrutura de diretórios
                elif file.endswith(".mp3"):
                    shutil.copy2(source_file, output_mp3_file)
                    logger.info(f"{source_file} -> {output_mp3_file}")



# Verifica se os argumentos de linha de comando foram passados
if len(sys.argv) < 3 or len(sys.argv) > 4:
    logger.error("Uso: python m4a2mp3.py <diretorio_entrada> <diretorio_saida> [bitrate_alvo]")
    sys.exit(1)

# Obtém os diretórios de entrada e saída dos parâmetros da linha de comando
input_directory = sys.argv[1]
output_directory = sys.argv[2]

# Obtém o bitrate alvo, se fornecido
if len(sys.argv) == 4:
    target_bitrate = sys.argv[3]
else:
    target_bitrate = DEFAULT_BITRATE

# Iniciar conversão e cópia
convert_and_copy_music_in_directory(input_directory, output_directory, target_bitrate)
