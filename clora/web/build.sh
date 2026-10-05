#!/usr/bin/env sh
# Envuelve la landing en un documento HTML completo para subirla a cualquier hosting estático
# (Netlify, Vercel, GitHub Pages, Cloudflare Pages). Salida: web/dist/index.html
set -e
cd "$(dirname "$0")"
mkdir -p dist
{
  printf '<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
  printf '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
  grep -E '^<(title|meta|link)' index.html
  printf '<style>body{margin:0}img{max-width:100%%}[hidden]{display:none!important}</style>\n</head>\n<body>\n'
  grep -vE '^<(title|meta|link)' index.html
  printf '\n</body>\n</html>\n'
} > dist/index.html
cp legal.html gracias.html dist/
echo "Generado web/dist/ (index, legal y gracias)"
