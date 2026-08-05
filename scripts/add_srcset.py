#!/usr/bin/env python3
"""
Aponta as <img> do concepts/ pras derivadas leves do backend, em vez do PNG de 1024.
Veja a rota /assets/site/<path>?w=N em asteroth-back/src/assets/assets.controller.ts.

Duas coisas acontecem aqui:

  1. toda <img src="concepts/..."> ganha um ?w=N no src, dimensionado pro tamanho em
     que ela de fato aparece na tela (medido no styles.css);
  2. as que são visíveis ganham srcset/sizes, pra que celular em 4G baixe a candidata
     pequena e desktop retina baixe a maior.

As entradas de detalhe (.item-list / .boss-list / .world-list) são display:none e só
existem pra alimentar o modal, que copia getAttribute('src') do <img> escondido. Nelas
o srcset seria peso morto no HTML sem nunca ser consultado — então levam só o ?w=.

Por que query param e não pasta: o deploy.yml reescreve só o PREFIXO das refs
("concepts/ -> $ASSET_HOST/assets/site/concepts/). Com a largura no ?w= o mesmo
prefixo serve pras três candidatas do srcset, e no dev local o browser ignora a
query e carrega o PNG pelo symlink site/concepts — nada quebra sem backend.

    python3 scripts/add_srcset.py              # aplica
    python3 scripts/add_srcset.py --check      # só relata, não grava

Idempotente: <img> que já tem ?w= no src é pulada. Rode de novo depois de somar arte.
"""
from __future__ import annotations
import argparse
import pathlib
import re
import sys
from collections import Counter

SITE = pathlib.Path(__file__).resolve().parent.parent / 'site'

# Larguras que o backend aceita (WIDTHS em image-derive.service.ts). Pedir uma fora da
# lista funciona — ele arredonda pra cima — mas aí src e srcset apontariam pra URLs
# diferentes da MESMA variante, cada uma ocupando sua entrada de cache no browser.
BACKEND_WIDTHS = {128, 160, 192, 256, 320, 384, 512, 640, 768, 1024, 1280, 1536}

# bucket -> (sizes, larguras do srcset, largura do src)
# srcset vazio = só reescreve o src (elemento oculto que serve de fonte pro modal).
#
# O `sizes` é o tamanho RENDERIZADO em CSS. Os números saíram do styles.css, não de chute.
BUCKETS: dict[str, tuple[str, list[int], int]] = {
    # .itens-grid .item-card img -> card de 96px menos 36px de moldura = 60px CSS.
    # É o grosso da página: compêndio, bestiário e skills.
    'grid-item':    ('60px',                            [128, 192, 256, 384], 256),
    # .boss-card img -> .boss-grid é minmax(170px, 1fr)
    'boss':         ('(max-width: 700px) 45vw, 200px',  [256, 384, 512],      384),
    # .world-card img -> .worlds-grid é minmax(280px, 1fr), aspect 4/3
    'world':        ('(max-width: 900px) 92vw, 340px',  [384, 512, 768],      512),
    # .lore-block-art img -> metade da dobra, arte grande
    'lore':         ('(max-width: 900px) 92vw, 46vw',   [512, 768, 1024],     768),
    'prog':         ('(max-width: 700px) 92vw, 300px',  [384, 512, 768],      512),
    'wordmark':     ('min(560px, 90vw)',                [512, 768, 1024],     768),
    'icon-64':      ('64px',                            [128, 192],           192),
    'icon-48':      ('48px',                            [128, 192],           128),
    'medallion':    ('90px',                            [128, 192, 256],      192),
    'default':      ('(max-width: 700px) 45vw, 220px',  [256, 384, 512],      384),
    # Ocultos: o modal mostra a arte em .scroll-solo-art = min(300px, 74%) — 512 cobre 2x.
    'entry':        ('',                                [],                   512),
    'entry-boss':   ('',                                [],                   640),
    # No modal de mundo a arte vai a 100% de min(760px, 100%).
    'entry-world':  ('',                                [],                   1024),
}

# Seções cujo grid usa o card de 96px.
GRID_SECTIONS = {'itens', 'bestiario', 'skills'}
# Contêineres display:none que só alimentam o modal.
HIDDEN_LISTS = ('item-list', 'boss-list', 'world-list')

IMG_RE = re.compile(r'<img\b[^>]*?>', re.S)
SRC_RE = re.compile(r'\ssrc="(concepts/[^"]+)"')
CLASS_RE = re.compile(r'\sclass="([^"]*)"')
SECTION_RE = re.compile(r'<section\b[^>]*\bid="([^"]+)"', re.S)
# Quase nenhuma <img> do compêndio tem class: quem carrega a semântica é o contêiner
# (.item-card, .lore-block-art, .boss-card...). Então o bucket olha pro pai também.
PARENT_RE = re.compile(r'<(?:div|figure|article|a|span|li)\b[^>]*\sclass="([^"]*)"[^>]*>\s*$', re.S)
PARENT_WINDOW = 300
DIV_RE = re.compile(r'</?div\b[^>]*>')


def section_ranges(html: str) -> list[tuple[int, str]]:
    """Offsets de abertura de cada <section id=...>, pra saber em que seção a <img> caiu."""
    return [(m.start(), m.group(1)) for m in SECTION_RE.finditer(html)]


def section_at(ranges: list[tuple[int, str]], pos: int) -> str:
    found = ''
    for start, name in ranges:
        if start > pos:
            break
        found = name
    return found


def hidden_ranges(html: str) -> list[tuple[int, int]]:
    """
    Faixas [ini, fim) das listas display:none, achadas por contagem de <div>.
    Precisa ser contagem de profundidade e não janela fixa: as gemas do #mundo, por
    exemplo, são <a class="item-card"> lá no fundo de uma .world-list, e olhar só o
    pai imediato as classificaria como card visível.
    """
    out = []
    for name in HIDDEN_LISTS:
        for m in re.finditer(r'<div\b[^>]*\sclass="' + name + r'"[^>]*>', html):
            depth, end = 1, len(html)
            for d in DIV_RE.finditer(html, m.end()):
                depth += -1 if d.group(0).startswith('</') else 1
                if depth == 0:
                    end = d.start()
                    break
            out.append((m.start(), end))
    return sorted(out)


def in_hidden(ranges: list[tuple[int, int]], pos: int) -> bool:
    return any(a <= pos < b for a, b in ranges)


def parent_classes(html: str, pos: int) -> str:
    """Classes do elemento que abre imediatamente antes da <img>, se houver."""
    m = PARENT_RE.search(html[max(0, pos - PARENT_WINDOW):pos])
    return m.group(1) if m else ''


def pick_bucket(own: str, parent: str, section: str, path: str, hidden: bool) -> str:
    near = f'{own} {parent}'
    if hidden:
        if path.startswith('concepts/worlds/'):
            return 'entry-world'
        if path.startswith('concepts/bosses/'):
            return 'entry-boss'
        return 'entry'
    if 'wordmark' in own:
        return 'wordmark'
    if 'lore-block-art' in near:
        return 'lore'
    if 'conto-medallion' in own:
        return 'medallion'
    if any(c in own for c in ('ex-icon', 'prog-ff-icon', 'aff-empty-icon')):
        return 'icon-48'
    if 'prog-art' in own:
        return 'prog'
    if 'prog-race-head' in near or 'chr-card' in near or path.startswith('concepts/classes/'):
        return 'icon-64'
    if 'item-card' in near and section in GRID_SECTIONS:
        return 'grid-item'
    if 'world' in near or path.startswith('concepts/worlds/'):
        return 'world'
    if 'boss' in near or path.startswith('concepts/bosses/'):
        return 'boss'
    return 'default'


def rewrite(html: str, stats: Counter) -> str:
    secs = section_ranges(html)
    hidden = hidden_ranges(html)

    def sub(m: re.Match) -> str:
        tag = m.group(0)
        src = SRC_RE.search(tag)
        if not src:
            # src montado em JS ("'+url(...)+'") ou imagem fora do concepts/ — não mexer.
            stats['ignorada'] += 1
            return tag
        path = src.group(1)
        if '?w=' in path:
            stats['ja-tinha'] += 1
            return tag

        own = CLASS_RE.search(tag)
        bucket = pick_bucket(
            own.group(1) if own else '',
            parent_classes(html, m.start()),
            section_at(secs, m.start()),
            path,
            in_hidden(hidden, m.start()),
        )
        sizes, widths, fallback = BUCKETS[bucket]
        stats[bucket] += 1

        out = tag.replace(f' src="{path}"', f' src="{path}?w={fallback}"', 1)
        if not widths:
            return out
        srcset = ', '.join(f'{path}?w={w} {w}w' for w in widths)
        close = '/>' if out.rstrip().endswith('/>') else '>'
        out = out.rstrip()[: -len(close)].rstrip()
        return f'{out} srcset="{srcset}" sizes="{sizes}"{close}'

    return IMG_RE.sub(sub, html)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true', help='relata sem gravar')
    ap.add_argument('files', nargs='*')
    args = ap.parse_args()

    bad = [w for _, ws, f in BUCKETS.values() for w in [*ws, f] if w not in BACKEND_WIDTHS]
    if bad:
        print(f'ERRO: larguras fora da lista do backend: {sorted(set(bad))}', file=sys.stderr)
        return 2

    targets = [pathlib.Path(f) for f in args.files] or sorted(SITE.glob('*.html'))
    for path in targets:
        html = path.read_text(encoding='utf-8')
        stats: Counter = Counter()
        out = rewrite(html, stats)
        touched = sum(v for k, v in stats.items() if k not in ('ignorada', 'ja-tinha'))
        if not touched:
            continue
        print(f'{path.name}: {touched} <img> reescritas  '
              f'({", ".join(f"{k}={v}" for k, v in sorted(stats.items()))})')
        if not args.check:
            path.write_text(out, encoding='utf-8')

    if args.check:
        print('\n--check: nada gravado.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
