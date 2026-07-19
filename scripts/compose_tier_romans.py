#!/usr/bin/env python3
"""Compõe os 11 algarismos romanos dos tiers (I…XI) como 1 PNG por romano, a
partir dos glifos entalhados gerados no ComfyUI (roman_I/V/X.png).

Espelha a composição do lab (game_rules/map/src/tiers.js → romanGlyphs): os
glifos entram lado-a-lado, normalizados à mesma altura, separados por um gap de
0.04×altura. Fundo transparente. Saída consumida pelo selo `.forja-roman` da
Forja no site (site/index.html).

Uso: python3 scripts/compose_tier_romans.py   (roda da raiz do repo público)
"""
from PIL import Image
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GLYPH_DIR = ROOT / "concepts" / "forja" / "ui" / "glyphs"
OUT_DIR = ROOT / "concepts" / "forja" / "ui" / "roman"

GAP_RATIO = 0.04  # mesmo gap do lab (fração da altura)

# tier → romano (só I, V, X cobrem 1..11; XI = X+I)
TIER_ROMAN = {
    1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI",
    7: "VII", 8: "VIII", 9: "IX", 10: "X", 11: "XI",
}


def load_glyphs():
    g = {}
    for c in "IVX":
        im = Image.open(GLYPH_DIR / f"roman_{c}.png").convert("RGBA")
        g[c] = im
    return g


def compose(roman, glyphs):
    parts = [glyphs[c] for c in roman]
    h = max(im.height for im in parts)  # todos 240; robusto se mudar
    gap = round(GAP_RATIO * h)
    widths = [round(im.width * h / im.height) for im in parts]
    total_w = sum(widths) + gap * (len(parts) - 1)
    canvas = Image.new("RGBA", (total_w, h), (0, 0, 0, 0))
    x = 0
    for im, w in zip(parts, widths):
        scaled = im if im.height == h else im.resize((w, h), Image.LANCZOS)
        canvas.alpha_composite(scaled, (x, 0))
        x += w + gap
    return canvas


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    glyphs = load_glyphs()
    for tier, roman in TIER_ROMAN.items():
        out = OUT_DIR / f"{roman}.png"
        compose(roman, glyphs).save(out)
        print(f"tier {tier:>2} · {roman:<4} → {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
