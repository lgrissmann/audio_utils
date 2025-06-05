#!/bin/bash
###############################################################################
#
# USO
#     ./baixar.sh "https://www.youtube.com/@canal" PastaDeDestino
#
###############################################################################

# Verifica se a URL do canal foi fornecida
if [ -z "$1" ]; then
  echo "Uso: $0 <url-do-canal>"
  exit 1
fi

URL_CANAL="$1"
NOME_CANAL="$2"
SAFE_NOME_CANAL="$(echo "$NOME_CANAL" | tr '/:*?"<>|' '_')"
COOKIES="--cookies cookies.txt"

PASTA_VIDEOS="videos_completos/$SAFE_NOME_CANAL"
PASTA_AUDIOS="audios/$SAFE_NOME_CANAL"
ARQUIVO="$SAFE_NOME_CANAL.lst"

mkdir -p "$PASTA_VIDEOS"
mkdir -p "$PASTA_AUDIOS"

# Obter todas as URLs dos vídeos
echo "Obtendo lista de vídeos do canal ($SAFE_NOME_CANAL)"
yt-dlp $COOKIES --flat-playlist --print "%(url)s" "$URL_CANAL" | grep -v '/shorts/' > "$ARQUIVO"

# Processar cada URL
while IFS= read -r URL_VIDEO; do
  [ -z "$URL_VIDEO" ] && continue

  echo "---------------------------------------"
  echo "Analisando $URL_VIDEO"

  # Obter título
  TITULO="$(yt-dlp $COOKIES --get-title "$URL_VIDEO" 2>/dev/null)"
  SAFE_TITULO="$(echo "$TITULO" | tr '/:*?"<>|' '_')"

  ARQ_VIDEO="$PASTA_VIDEOS/$SAFE_TITULO.mp4"
  ARQ_AUDIO="$PASTA_AUDIOS/$SAFE_TITULO.mp3"

  # Baixar vídeo completo (caso não exista)
  if [ -f "$ARQ_VIDEO" ]; then
    echo ".... Vídeo já existe: $ARQ_VIDEO"
  else
    echo ".... Baixando vídeo completo: $URL_VIDEO"
    yt-dlp $COOKIES -f bestvideo+bestaudio --merge-output-format mp4 -o "$PASTA_VIDEOS/$SAFE_TITULO.%(ext)s" "$URL_VIDEO"
  fi

  # Baixar áudio em MP3 (caso não exista)
  if [ -f "$ARQ_AUDIO" ]; then
    echo ".... Áudio já existe: $ARQ_AUDIO"
  else
    echo ".... Extraindo áudio em MP3: $URL_VIDEO"
    yt-dlp $COOKIES -x --audio-format mp3 -o "$PASTA_AUDIOS/$SAFE_TITULO.%(ext)s" "$URL_VIDEO"
  fi

done < "$ARQUIVO"
