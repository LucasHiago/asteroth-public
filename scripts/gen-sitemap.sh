#!/usr/bin/env bash
# Regenera as datas <lastmod> de site/sitemap.xml a partir da data do último
# commit de cada página. Rode antes de publicar quando alguma página mudou:
#
#     npm run sitemap
#
# Adicionar uma página nova: crie a entrada <url> no sitemap e some o arquivo
# na lista PAGES abaixo (a chave é o <loc> correspondente).
set -euo pipefail

cd "$(dirname "$0")/.."

SITEMAP="site/sitemap.xml"

# <arquivo em site/>|<loc no sitemap>
PAGES=(
  "index.html|https://asteroth.com.br/"
  "changelog.html|https://asteroth.com.br/changelog.html"
  "afinidades-grafo.html|https://asteroth.com.br/afinidades-grafo.html"
)

for entry in "${PAGES[@]}"; do
  file="${entry%%|*}"
  loc="${entry##*|}"

  # Data do último commit que tocou o arquivo; se o arquivo tem mudança não
  # commitada, usa hoje — é a data que vai ao ar de qualquer jeito.
  date=$(git log -1 --format=%cs -- "site/$file" 2>/dev/null || true)
  if [ -z "$date" ] || ! git diff --quiet -- "site/$file" 2>/dev/null; then
    date=$(date +%F)
  fi

  # Substitui o <lastmod> do bloco <url> cujo <loc> é esta página.
  python3 - "$SITEMAP" "$loc" "$date" <<'PY'
import re, sys
path, loc, date = sys.argv[1], sys.argv[2], sys.argv[3]
xml = open(path, encoding='utf-8').read()
pattern = re.compile(
    r'(<loc>' + re.escape(loc) + r'</loc>\s*<lastmod>)[^<]*(</lastmod>)')
xml, n = pattern.subn(r'\g<1>' + date + r'\g<2>', xml)
if n == 0:
    sys.exit(f'sitemap: <loc>{loc}</loc> não encontrado em {path}')
open(path, 'w', encoding='utf-8').write(xml)
print(f'  {loc} -> {date}')
PY
done

echo "sitemap.xml atualizado."
