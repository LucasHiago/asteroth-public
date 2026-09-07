#!/usr/bin/env python3
"""Gera site/img/**.webp a partir de site/concepts/** (symlink -> asteroth-assets).

Os PNG de concept art sao 1024px+ com alpha e pesam ~1MB cada; o site desenha
card de ~200-350px. Converte pra WebP no maior lado MAX_SIDE, mantendo a subarvore.

As paginas ja apontam pra img/**.webp; rodar depois de trocar arte em concepts/.

Uso:
  python3 scripts/build-webp.py            # converte o que falta
  python3 scripts/build-webp.py --force    # reconverte tudo
"""
import os
import re
import sys
from concurrent.futures import ProcessPoolExecutor

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
SRC = os.path.join(SITE, "concepts")
OUT = os.path.join(SITE, "img")

MAX_SIDE = 512
QUALITY = 78

# Paths montados em JS (prefixo + variavel + '.png'): converte o diretorio inteiro.
DYNAMIC_DIRS = ["classes/treated", "forja/ui/roman"]

SCAN_FILES = ["index.html", "afinidades-grafo.html", "changelog.html", "404.html", "styles.css"]

# As paginas apontam pro resultado (img/**.webp); a fonte e' descoberta por extensao.
REF = re.compile(r"""(["'(])img/([^"')]+?)\.webp""")
SRC_EXT = (".png", ".jpg", ".jpeg", ".webp")


def source_of(stem):
    for ext in SRC_EXT:
        path = os.path.join(SRC, stem + ext)
        if os.path.exists(path):
            return path
    return None


def stems_from_sources():
    found = set()
    for name in SCAN_FILES:
        path = os.path.join(SITE, name)
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as fh:
            for _, stem in REF.findall(fh.read()):
                found.add(stem)
    for d in DYNAMIC_DIRS:
        base = os.path.join(SRC, d)
        for f in sorted(os.listdir(base)):
            if f.lower().endswith(SRC_EXT):
                found.add(f"{d}/{os.path.splitext(f)[0]}")
    return sorted(found)


def convert(job):
    stem, force = job
    src = source_of(stem)
    dst = os.path.join(OUT, stem + ".webp")
    if not force and os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
        return ("skip", os.path.getsize(src), os.path.getsize(dst))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    im = Image.open(src)
    im = im.convert("RGBA" if "A" in im.getbands() else "RGB")
    w, h = im.size
    if max(w, h) > MAX_SIDE:
        scale = MAX_SIDE / max(w, h)
        im = im.resize((max(1, round(w * scale)), max(1, round(h * scale))), Image.LANCZOS)
    im.save(dst, "WEBP", quality=QUALITY, method=6)
    return ("done", os.path.getsize(src), os.path.getsize(dst))


def main():
    force = "--force" in sys.argv
    stems = stems_from_sources()
    missing = [s for s in stems if source_of(s) is None]
    if missing:
        sys.exit("ref sem original em concepts/:\n  " + "\n  ".join(missing[:20]))

    with ProcessPoolExecutor() as pool:
        results = list(pool.map(convert, [(s, force) for s in stems], chunksize=8))

    done = sum(1 for s, _, _ in results if s == "done")
    src_bytes = sum(s for _, s, _ in results)
    out_bytes = sum(d for _, _, d in results)
    print(f"{len(stems)} refs · {done} convertidos · {len(stems) - done} ja em dia")
    print(f"{src_bytes / 2**20:.0f} MB -> {out_bytes / 2**20:.0f} MB ({src_bytes / out_bytes:.0f}x)")


if __name__ == "__main__":
    main()
