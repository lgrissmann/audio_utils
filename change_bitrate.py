import os
import sys
from pydub import AudioSegment
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError

# Função para alterar o bitrate de um arquivo MP3 e preservar os metadados
def change_bitrate_with_metadata(mp3_file, output_file, target_bitrate):
    try:
        # Carrega o arquivo MP3
        audio = AudioSegment.from_mp3(mp3_file)
        
        # Exporta o arquivo com o novo bitrate
        audio.export(output_file, format="mp3", bitrate=target_bitrate)
        print(f"Alterado: {mp3_file} -> {output_file} (bitrate: {target_bitrate})")
        
        # Copia os metadados
        try:
            tags = EasyID3(mp3_file)
            tags.save(output_file)  # Copia as tags do arquivo original para o novo
            # print(f"Metadados copiados de {mp3_file} para {output_file}")
        except ID3NoHeaderError:
            print(f"Arquivo {mp3_file} não contém metadados ID3.")
    
    except Exception as e:
        print(f"Erro ao processar {mp3_file}: {e}")

# Função para processar todos os arquivos MP3 no diretório e alterar o bitrate
def process_mp3_files(root_dir, target_bitrate):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".mp3"):
                mp3_file = os.path.join(subdir, file)
                
                # Cria o diretório de saída com a mesma estrutura do diretório de entrada
                output_dir = subdir
                os.makedirs(output_dir, exist_ok=True)
                
                # Define o arquivo de saída no mesmo local
                output_file = os.path.join(output_dir, file)
                
                # Altera o bitrate do arquivo MP3 e preserva os metadados
                change_bitrate_with_metadata(mp3_file, output_file, target_bitrate)

# Verifica se os argumentos de linha de comando foram passados
if len(sys.argv) != 3:
    print("Uso: python change_bitrate.py <diretorio_entrada> <bitrate>")
    sys.exit(1)

# Obtém o diretório de entrada e o bitrate alvo dos parâmetros da linha de comando
input_directory = sys.argv[1]
target_bitrate = sys.argv[2]

# Iniciar a alteração do bitrate
process_mp3_files(input_directory, target_bitrate)
