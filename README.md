# Audio Utils

Coleção de ferramentas úteis na organização de arquivos de áudio.

## Pré-requisitos

- Python 3.x
- FFmpeg (para obter o bitrate dos arquivos)

## m4a2mp3

    python m4a2mp3.py <diretorio_entrada> <diretorio_saida>

- Converte arquivos `.m4a` para `.mp3` mantendo a qualidade de áudio.
- Preserva as tags de metadados do arquivo original.
- Copia arquivos `.mp3` existentes para o diretório de saída.
- Mantém a mesma estrutura de diretórios do diretório de entrada.


## change_bitrate

    python change_bitrate.py <diretorio_entrada> <bitrate>

- Altera o bitrate do arquivo .mp3
- Preserva as tags de metadados do arquivo original.
- Sobrescreve o arquivo original com o novo arquivo.

## compare_dir

    python compare_dir.py <diretorio_1> <diretorio_2>

- Compara os arquivos presentes em duas arvores de diretórios.
- Ignora a extensão dos arquivos na comparação
