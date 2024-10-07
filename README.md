# Conversor de Áudio M4A para MP3

**m4a2mp3** converte arquivos de áudio no formato `.m4a` para `.mp3` mantendo a mesma estrutura de diretórios. Ele também copia arquivos `.mp3` que já estão no formato correto para o diretório de saída e preserva as tags de metadados como Título, Artista, Álbum e Ano.

## Funcionalidades

- Converte arquivos `.m4a` para `.mp3` mantendo a qualidade de áudio.
- Preserva as tags de metadados do arquivo original.
- Copia arquivos `.mp3` existentes para o diretório de saída.
- Mantém a mesma estrutura de diretórios do diretório de entrada.

## Pré-requisitos

- Python 3.x
- FFmpeg (para obter o bitrate dos arquivos)

## Uso

Execute o script passando os diretórios de entrada e saída como parâmetros da linha de comando:

    python m4a2mp3.py <diretorio_entrada> <diretorio_saida>

Exemplo:

    python m4a2mp3.py /diretorio/de/musicas/mpa /diretorio/de/musicas/mp3
