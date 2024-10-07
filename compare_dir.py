import os
import sys

# Função para listar os arquivos em um diretório, ignorando a extensão
def list_files_without_extension(directory):
    file_list = []
    for subdir, _, files in os.walk(directory):
        for file in files:
            # Ignora a extensão e armazena o nome do arquivo e o caminho relativo
            file_name_without_ext = os.path.splitext(file)[0]
            relative_path = os.path.relpath(subdir, directory)
            full_path = os.path.join(relative_path, file_name_without_ext)
            file_list.append(full_path)
    return file_list

# Função para listar arquivos que estão na origem mas não no destino
def compare_directories(input_dir, output_dir):
    source_files = list_files_without_extension(input_dir)
    destination_files = list_files_without_extension(output_dir)

    # Converte as listas em conjuntos para comparação
    missing_files = set(source_files) - set(destination_files)

    return missing_files

# Verifica se os argumentos de linha de comando foram passados
if len(sys.argv) != 3:
    print("Uso: python compare_dir.py <diretorio_1> <diretorio_2>")
    sys.exit(1)

# Obtém os diretórios de entrada e saída dos parâmetros da linha de comando
input_directory = sys.argv[1]
output_directory = sys.argv[2]

# Compara os diretórios
missing_files = compare_directories(input_directory, output_directory)

# Exibe os arquivos que estão na origem, mas não no destino
if missing_files:
    print("Arquivos que estão na origem mas não no destino:")
    for file in sorted(missing_files):
        print(file)
else:
    print("Todos os arquivos da origem estão presentes no destino.")
