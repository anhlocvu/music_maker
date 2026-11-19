"""Browse the presets in a soundfont.

    python list_presets.py                  list the font keys you can use
    python list_presets.py main             every preset in the "main" font
    python list_presets.py main violin      presets with "violin" in the name
"""
import sys
from engine import instruments

if len(sys.argv) < 2:
    for k, f in instruments.FONTS.items():
        print(f"{k:<12} {f}")
    sys.exit()

sf = instruments.font(sys.argv[1])
needle = sys.argv[2] if len(sys.argv) > 2 else ""
for b, p, n in sf.find(needle):
    print(f'  ("{sys.argv[1]}", {b}, {p}),   # {n}')
