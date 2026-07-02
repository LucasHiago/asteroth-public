#!/usr/bin/env python3
"""Recorta o fundo chapado dos ícones de item (JPG do catálogo) e gera PNG
com alpha, 640px, pro site (Compêndio de Itens).

Uso: python3 scripts/cut_item_bg.py concepts/items/<categoria>/*.jpg

O fundo dos JPGs do pipeline Leonardo é um cinza uniforme; o recorte é por
flood-fill a partir das bordas (só remove a região conectada à borda, não
toca cinzas internos do item), com erosão de 1px pra matar a franja e um
feather suave. Requer: pillow, scipy, numpy.
"""
import os
import sys

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

TOLERANCIA = 42  # soma |dR|+|dG|+|dB| em relação à cor de fundo


def cut(src: str) -> None:
    im = Image.open(src).convert('RGB')
    a = np.array(im).astype(int)
    bg = np.median(np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]]), axis=0)
    close = np.abs(a - bg).sum(axis=2) <= TOLERANCIA
    lab, _ = ndimage.label(close)
    border_labels = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]])))
    border_labels.discard(0)
    bgmask = np.isin(lab, list(border_labels))
    alpha = np.where(bgmask, 0, 255).astype(np.uint8)
    alpha = ndimage.grey_erosion(alpha, size=(3, 3))
    alpha_im = Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(1.0))
    out = im.convert('RGBA')
    out.putalpha(alpha_im)
    out = out.resize((640, 640), Image.LANCZOS)
    dst = os.path.splitext(src)[0] + '.png'
    out.save(dst, optimize=True)
    pct = (np.array(alpha_im) > 128).mean() * 100
    print(f'{os.path.basename(dst)}  conteudo={pct:.0f}%  {os.path.getsize(dst) // 1024}KB')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for path in sys.argv[1:]:
        cut(path)
