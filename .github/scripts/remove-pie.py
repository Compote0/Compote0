#!/usr/bin/env python3
"""Retire le camembert de langages des SVG generes par github-profile-3d-contrib.

Le camembert est le groupe <g transform="translate(40, 520)"> (position fixe
x=40, y=height-pieHeight-70 dans create-svg.ts). On supprime le bloc <g>...</g>
correspondant en comptant les balises imbriquees.
"""
import re
import sys
from pathlib import Path

MARKER = re.compile(r'<g transform="translate\(40, 5\d\d(?:\.\d+)?\)">')


def strip_pie(svg: str) -> str | None:
    m = MARKER.search(svg)
    if not m:
        return None
    start = m.start()
    depth = 0
    for tag in re.finditer(r'<g\b|</g>', svg[start:]):
        depth += 1 if tag.group() != '</g>' else -1
        if depth == 0:
            end = start + tag.end()
            return svg[:start] + svg[end:]
    return None


def main() -> None:
    changed = 0
    for path in Path('profile-3d-contrib').glob('profile-*.svg'):
        svg = path.read_text()
        out = strip_pie(svg)
        if out:
            path.write_text(out)
            changed += 1
            print(f'pie retire: {path.name}')
    print(f'{changed} fichier(s) modifie(s)')


if __name__ == '__main__':
    main()
