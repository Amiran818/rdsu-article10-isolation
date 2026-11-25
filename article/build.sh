#!/bin/sh
# build.sh - собрать статью: article.md -> article.docx (pandoc) -> article.pdf
set -eu
cd "$(dirname "$0")"
tmp=$(mktemp -d)
trap 'rm -rf -- "$tmp"' EXIT

pandoc -o "$tmp/default.docx" --print-default-data-file reference.docx
python3 -B make-reference.py "$tmp/default.docx" "$tmp/reference.docx"
pandoc article.md -f markdown -t docx --reference-doc="$tmp/reference.docx" \
    --resource-path=. -o article.docx
soffice --headless --convert-to pdf --outdir . article.docx > /dev/null 2>&1
ls -l article.docx article.pdf
