#!/usr/bin/env python
"""Embed app screenshots into the case-study galleries of v2/index.html.

Drop screenshots into a folder per project:

    assets/shots/escore/01-matches.png
    assets/shots/escore/02-tournament.png
    assets/shots/str/01-home.png
    ...

then run:

    python tools/embed-shots.py

Every image is resized, converted to WebP and written into the `SHOTS`
registry inside v2/index.html as a data: URI, in filename order — so
number the files in the order you want them to appear. A project with no
folder keeps its fallback (a screenshot already on the page, or nothing).

Options:  --width 460   --quality 72   --dry
"""
import base64, io, re, sys, pathlib
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC  = ROOT / "assets" / "shots"
PAGE = ROOT / "v2" / "index.html"

ORDER = ["escore", "str", "tark", "host", "curai", "azk"]
# what a project falls back to when it has no folder of its own
FALLBACK = {"escore": ["'#sh-escore'"], "str": ["'#sh-str'"], "tark": ["'#sh-tark'"]}
EXT = {".png", ".jpg", ".jpeg", ".webp"}

width   = 460
quality = 72
dry     = "--dry" in sys.argv
for flag, cast in (("--width", int), ("--quality", int)):
    if flag in sys.argv:
        globals()[flag[2:]] = cast(sys.argv[sys.argv.index(flag) + 1])


def encode(path):
    im = Image.open(path)
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGB")
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.convert("RGB").save(buf, "WEBP", quality=quality, method=6)
    return base64.b64encode(buf.getvalue()).decode(), buf.tell()


def main():
    blocks, total = [], 0
    for key in ORDER:
        folder = SRC / key
        files = sorted(p for p in folder.glob("*") if p.suffix.lower() in EXT) if folder.is_dir() else []
        if not files:
            entries = FALLBACK.get(key, [])
            print("%-7s -> %s" % (key, "fallback" if entries else "no screens"))
        else:
            entries = []
            for p in files:
                b64, size = encode(p)
                total += size
                entries.append("'data:image/webp;base64,%s'" % b64)
                print("%-7s <- %-34s %6.1f KB" % (key, p.name, size / 1024))
        body = ("\n    " + ",\n    ".join(entries) + "\n  ") if len(entries) > 1 else "".join(entries)
        blocks.append("  %s:[%s]" % (key, body))

    shots = "const SHOTS={\n" + ",\n".join(blocks) + "\n};"
    page  = PAGE.read_text(encoding="utf-8")
    new, n = re.subn(r"const SHOTS=\{.*?\n\};", lambda m: shots, page, count=1, flags=re.S)
    if n != 1:
        sys.exit("could not find the SHOTS registry in %s" % PAGE)

    print("\nembedded %.0f KB of screenshots | page %.0f KB -> %.0f KB"
          % (total / 1024, len(page.encode()) / 1024, len(new.encode()) / 1024))
    if dry:
        print("--dry: nothing written")
    else:
        PAGE.write_text(new, encoding="utf-8")
        print("wrote %s" % PAGE)


main()
