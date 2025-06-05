import os
import shutil
import argparse
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

def generate_markdown(directory, output_file):
    """
    Gera um arquivo Markdown com uma tabela contendo título, ano de gravação e duração das músicas.
    """
    rows = []
    for file in os.listdir(directory):
        if file.lower().endswith(".mp3"):  # Trata .mp3 e .MP3 de forma igual
            try:
                filepath = os.path.join(directory, file)
                tags = EasyID3(filepath)
                title = tags.get("title", ["Desconhecido"])[0]
                year = tags.get("date", ["Desconhecido"])[0]
                
                # Obtém a duração da música
                audio = MP3(filepath)
                duration = audio.info.length
                duration_minutes = int(duration // 60)
                duration_seconds = int(duration % 60)
                duration_str = f"{duration_minutes:02}:{duration_seconds:02}"  # Formato MM:SS

                rows.append((title, year, duration_str, file))
            except Exception as e:
                print(f"Erro ao processar {file}: {e}")
    
    rows.sort(key=lambda x: (x[1], x[0]))  # Ordena por ano e depois por título

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Tabela de Músicas\n\n")
        f.write("| Título | Ano | Duração | Arquivo |\n")
        f.write("|--------|-----|---------|---------|\n")
        for title, year, duration, file in rows:
            f.write(f"| {title} | {year} | {duration} | {file} |\n")
    print(f"Arquivo Markdown salvo em {output_file}")

def organize_by_album(directory):
    """
    Organiza músicas em subpastas baseadas no título e ano (simulando o álbum).
    """
    for file in os.listdir(directory):
        if file.lower().endswith(".mp3"):  # Trata .mp3 e .MP3 de forma igual
            try:
                filepath = os.path.join(directory, file)
                tags = EasyID3(filepath)
                title = tags.get("title", ["Desconhecido"])[0]
                year = tags.get("date", ["Desconhecido"])[0]
                album_folder = f"{year} - Album Desconhecido"

                # Cria a pasta do álbum
                album_path = os.path.join(directory, album_folder)
                if not os.path.exists(album_path):
                    os.makedirs(album_path)
                
                # Move o arquivo para a pasta
                shutil.move(filepath, os.path.join(album_path, file))
                print(f"Movido: {file} -> {album_folder}")
            except Exception as e:
                print(f"Erro ao processar {file}: {e}")

def main():
    # Configuração do parser de argumentos
    parser = argparse.ArgumentParser(description="Organize MP3 files by album and generate a Markdown report.")
    parser.add_argument("music_directory", help="Caminho da pasta contendo as músicas MP3.")
    parser.add_argument("markdown_file", help="Caminho do arquivo Markdown a ser gerado.")
    
    args = parser.parse_args()

    # Executa as funções com os argumentos fornecidos
    generate_markdown(args.music_directory, args.markdown_file)
    # organize_by_album(args.music_directory)

if __name__ == "__main__":
    main()
