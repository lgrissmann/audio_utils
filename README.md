# Audio Utils

Coleção de ferramentas úteis na organização de arquivos de áudio.

## Pré-requisitos

- Python 3.x
- FFmpeg (para obter o bitrate dos arquivos)

---
## m4a2mp3


- Converte arquivos `.m4a` para `.mp3` mantendo a qualidade de áudio.
- Preserva as tags de metadados do arquivo original.
- Copia arquivos `.mp3` existentes para o diretório de saída.
- Mantém a mesma estrutura de diretórios do diretório de entrada.

    #### Uso

    ```bash
    python m4a2mp3.py <diretorio_entrada> <diretorio_saida>
    ```

    Exemplo:

    ```bash
    python m4a2mp3.py /home/usuario/Music /tmp/Music_Converted
    ```

---
## change_bitrate

- Altera o bitrate do arquivo .mp3
- Preserva as tags de metadados do arquivo original.
- Sobrescreve o arquivo original com o novo arquivo.

    #### Uso

    ```bash
    python change_bitrate.py <diretorio_entrada> <bitrate_kbps>
    ```

    Exemplo:

    ```bash
    python change_bitrate.py /tmp/Music_Converted 160
    ```

---
## compare_dir

- Compara os arquivos presentes em duas arvores de diretórios.
- Ignora a extensão dos arquivos na comparação

    #### Uso

    ```bash
    python compare_dir.py <diretorio_1> <diretorio_2>
    ```

    Exemplo:

    ```bash
    python compare_dir.py /home/usuario/Music /tmp/Music_Converted
    ```
