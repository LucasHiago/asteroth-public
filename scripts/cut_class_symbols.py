#!/usr/bin/env python3
"""
cut_class_symbols.py — recorta silhuetas pretas de fundo branco (saída de GPT Image 2 / Leonardo.ai).

Produz dois PNGs por imagem de entrada:
  <nome>_black.png  — silhueta preta, fundo transparente
  <nome>_white.png  — silhueta branca, fundo transparente

Uso:
  python3 scripts/cut_class_symbols.py imagem.png [imagem2.jpg ...]
  python3 scripts/cut_class_symbols.py pasta_de_entrada/
  python3 scripts/cut_class_symbols.py pasta_de_entrada/ -o site/concepts/classes/

Opções:
  -o <dir>   pasta de saída (padrão: mesma pasta do arquivo de entrada)
  -t <0-255> limiar de luminância para considerar preto (padrão: 160)
"""

import sys
from pathlib import Path
from PIL import Image
import numpy as np

EXTS = {".jpg", ".jpeg", ".png", ".webp"}
DEFAULT_THRESHOLD = 160


def luminance(arr: np.ndarray) -> np.ndarray:
    """Rec.601 grayscale a partir de array RGB float32."""
    return 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]


def process(src: Path, out_dir: Path, threshold: int) -> None:
    img = Image.open(src).convert("RGB")
    arr = np.array(img, dtype=np.float32)
    mask = luminance(arr) < threshold  # True = pixel da silhueta

    n_px = int(mask.sum())
    if n_px == 0:
        print(f"  aviso: nenhum pixel escuro encontrado em {src.name} (threshold={threshold})")
        return

    h, w = arr.shape[:2]

    black = np.zeros((h, w, 4), dtype=np.uint8)
    black[mask] = [0, 0, 0, 255]
    out_black = out_dir / f"{src.stem}_black.png"
    Image.fromarray(black, "RGBA").save(out_black, optimize=True)

    white = np.zeros((h, w, 4), dtype=np.uint8)
    white[mask] = [255, 255, 255, 255]
    out_white = out_dir / f"{src.stem}_white.png"
    Image.fromarray(white, "RGBA").save(out_white, optimize=True)

    print(f"  {src.name:40s}  →  {out_black.name}  +  {out_white.name}  ({n_px} px, {w}×{h})")


def main() -> None:
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    # parse flags
    out_dir_arg: Path | None = None
    threshold = DEFAULT_THRESHOLD
    inputs = []
    i = 0
    while i < len(args):
        a = args[i]
        if a == "-o" and i + 1 < len(args):
            out_dir_arg = Path(args[i + 1])
            i += 2
        elif a == "-t" and i + 1 < len(args):
            threshold = int(args[i + 1])
            i += 2
        else:
            inputs.append(Path(a))
            i += 1

    # expand directories
    sources: list[Path] = []
    for p in inputs:
        if p.is_dir():
            sources.extend(sorted(f for f in p.iterdir() if f.suffix.lower() in EXTS))
        elif p.is_file():
            sources.append(p)
        else:
            print(f"aviso: {p} não encontrado, ignorando")

    if not sources:
        print("nenhuma imagem encontrada. Passe arquivos ou uma pasta.")
        sys.exit(1)

    print(f"threshold: {threshold}  |  {len(sources)} imagem(ns)")

    for src in sources:
        dest = out_dir_arg if out_dir_arg else src.parent
        dest.mkdir(parents=True, exist_ok=True)
        process(src, dest, threshold)

    print("pronto.")


if __name__ == "__main__":
    main()
