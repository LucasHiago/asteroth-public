#!/usr/bin/env python3
"""
remove-bg.py: tira fundo de imagem por chroma key, baseado em distancia de
cor pros cantos da imagem. Salva como PNG com transparencia.

Uso:
    scripts/remove-bg.py <input1> [<input2> ...]
    scripts/remove-bg.py --threshold 35 --soft 25 concepts/bosses/cthulhu/cthulhu.jpg
    scripts/remove-bg.py --inplace concepts/bosses/*/*.jpg

Como funciona:
    1. Le os 4 cantos da imagem, calcula a cor media (estimativa de background).
    2. Pra cada pixel, calcula a distancia Euclidiana em RGB ate essa cor.
    3. Distancia < threshold => transparente (alpha = 0).
       Distancia >= threshold + soft => opaco (alpha = 255).
       No meio => alpha interpolado pra borda suave.
    4. Salva como <nome>.png no mesmo diretorio (ou outro com --out / --inplace).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image


def estimate_bg_color(arr: np.ndarray, corner: int = 8) -> np.ndarray:
    """Media das 4 caixas de canto, em RGB."""
    h, w = arr.shape[:2]
    c = min(corner, h // 4, w // 4)
    samples = np.concatenate([
        arr[:c, :c, :3].reshape(-1, 3),
        arr[:c, -c:, :3].reshape(-1, 3),
        arr[-c:, :c, :3].reshape(-1, 3),
        arr[-c:, -c:, :3].reshape(-1, 3),
    ])
    return samples.mean(axis=0)


def remove_bg(
    img: Image.Image,
    threshold: float = 30.0,
    soft: float = 20.0,
    bg_color: np.ndarray | None = None,
) -> Image.Image:
    """Retorna copia de img com fundo (proximo de bg_color) transparente."""
    rgba = img.convert("RGBA")
    arr = np.array(rgba, dtype=np.float32)

    if bg_color is None:
        bg_color = estimate_bg_color(arr)
    bg = np.asarray(bg_color, dtype=np.float32)[:3]

    diff = arr[:, :, :3] - bg
    dist = np.sqrt((diff * diff).sum(axis=2))

    if soft <= 0:
        alpha = np.where(dist < threshold, 0.0, 255.0)
    else:
        # Borda suave: rampa linear entre threshold e threshold+soft
        alpha = np.clip((dist - threshold) / soft, 0.0, 1.0) * 255.0

    # Preserva alpha original (caso a imagem ja tenha transparencia parcial)
    arr[:, :, 3] = np.minimum(arr[:, :, 3], alpha)

    return Image.fromarray(arr.astype(np.uint8))


def output_path(input_path: Path, outdir: Path | None, inplace: bool) -> Path:
    if outdir is not None:
        outdir.mkdir(parents=True, exist_ok=True)
        return outdir / (input_path.stem + ".png")
    return input_path.with_suffix(".png")


def main() -> int:
    p = argparse.ArgumentParser(description="Tira fundo de imagem por chroma key.")
    p.add_argument("inputs", nargs="+", type=Path, help="arquivo(s) de entrada")
    p.add_argument("--threshold", type=float, default=30.0,
                   help="distancia maxima pra considerar background (default 30)")
    p.add_argument("--soft", type=float, default=20.0,
                   help="largura da rampa de alpha pras bordas (default 20, use 0 pra corte duro)")
    p.add_argument("--out", type=Path, default=None,
                   help="diretorio de saida (default: mesmo dir do input, .jpg vira .png)")
    p.add_argument("--inplace", action="store_true",
                   help="sobrescrever o input com o png (apaga o original)")
    p.add_argument("--bg", type=str, default=None,
                   help="cor de fundo explicita em R,G,B (default: estimar dos cantos)")
    args = p.parse_args()

    bg_color = None
    if args.bg:
        bg_color = np.array([int(x) for x in args.bg.split(",")], dtype=np.float32)

    errors = 0
    for inp in args.inputs:
        if not inp.exists():
            print(f"[skip] {inp}: arquivo nao existe", file=sys.stderr)
            errors += 1
            continue
        try:
            img = Image.open(inp)
            result = remove_bg(img, threshold=args.threshold, soft=args.soft, bg_color=bg_color)
            out = output_path(inp, args.out, args.inplace)
            result.save(out, "PNG", optimize=True)
            print(f"[ok]   {inp} -> {out}")
            if args.inplace and inp.suffix.lower() != ".png":
                inp.unlink()
                print(f"       (removido original {inp})")
        except Exception as e:
            print(f"[fail] {inp}: {e}", file=sys.stderr)
            errors += 1

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
