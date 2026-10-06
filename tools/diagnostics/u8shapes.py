"""Render U8 shape files (e.g. STATIC/U8GUMPS.FLX) to PNG for review.

Read-only; the PNGs are game artwork and must stay out of the repository
(write them to private_test/ or a scratch directory).

Usage:
  python u8shapes.py sheet <out.png> [--flex U8GUMPS.FLX] [--shapes 0-80]
      contact sheet: every frame of the shapes, labelled shape,frame
  python u8shapes.py frame <shape> <frame> <out.png> [--flex ...] [--scale 3]

Format as in ScummVM (gfx/shape.cpp, gfx/raw_shape_frame.cpp, gfx/shape_frame.cpp).
"""
import argparse
import os
import struct
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
import u8dis  # noqa: E402

STATIC = os.path.join(os.path.dirname(u8dis.USECODE), "..", "STATIC")


def palette():
    raw = open(os.path.join(STATIC, "U8PAL.PAL"), "rb").read()[4:4 + 768]
    pal = []
    for c in raw:
        pal.append((c << 2) | (c >> 4))
    return pal


def frames(shape_data):
    """Yield (width, height, xoff, yoff, pixels or None)."""
    if len(shape_data) < 6:
        return
    count = struct.unpack_from("<H", shape_data, 4)[0]
    for i in range(count):
        off = struct.unpack_from("<I", shape_data, 6 + 6 * i)[0] & 0xFFFFFF
        size = struct.unpack_from("<H", shape_data, 6 + 6 * i + 4)[0]
        d = shape_data[off:off + size + 8]
        if len(d) < 18:
            yield None
            continue
        compressed = d[8]
        w, h, xo, yo = struct.unpack_from("<hhhh", d, 10)
        if w <= 0 or h <= 0 or w > 2000 or h > 2000:
            yield None
            continue
        lines = [struct.unpack_from("<H", d, 18 + 2 * y)[0] - (h - y) * 2 for y in range(h)]
        rle = 18 + 2 * h
        px = bytearray([255]) * (w * h)
        for y in range(h):
            p = rle + lines[y]
            x = 0
            while True:
                x += d[p]; p += 1
                if x >= w:
                    break
                dlen = d[p]; p += 1
                typ = 0
                if compressed:
                    typ = dlen & 1
                    dlen >>= 1
                for k in range(dlen):
                    if x + k < w:
                        px[y * w + x + k] = d[p]
                    if not typ:
                        p += 1
                x += dlen
                if typ:
                    p += 1
                if x >= w:
                    break
        yield (w, h, xo, yo, bytes(px))


def to_image(fr, pal, scale=1):
    w, h, _, _, px = fr
    img = Image.frombytes("P", (w, h), px)
    img.putpalette(pal)
    img.info["transparency"] = 255
    img = img.convert("RGBA")
    if scale != 1:
        img = img.resize((w * scale, h * scale), Image.NEAREST)
    return img


def parse_range(s, n):
    out = []
    for part in s.split(","):
        if "-" in part:
            a, b = part.split("-")
            out += range(int(a), min(int(b), n - 1) + 1)
        else:
            out.append(int(part))
    return [x for x in out if x < n]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["sheet", "frame"])
    ap.add_argument("args", nargs="+")
    ap.add_argument("--flex", default="U8GUMPS.FLX")
    ap.add_argument("--shapes", default="0-999")
    ap.add_argument("--scale", type=int, default=2)
    a = ap.parse_args()

    data, ents = u8dis.load_flex(os.path.join(STATIC, a.flex))
    pal = palette()

    if a.cmd == "frame":
        shape, frame, out = int(a.args[0]), int(a.args[1]), a.args[2]
        fr = list(frames(u8dis.obj(data, ents, shape)))[frame]
        to_image(fr, pal, a.scale).save(out)
        print(out, fr[:4])
        return

    out = a.args[0]
    tiles = []
    for s in parse_range(a.shapes, len(ents)):
        if not ents[s][1]:
            continue
        for f, fr in enumerate(frames(u8dis.obj(data, ents, s))):
            if fr:
                tiles.append((f"{s},{f}", to_image(fr, pal)))
    # simple row packing
    width = 1600
    x = y = rowh = 0
    pos = []
    for label, img in tiles:
        w, h = img.size[0], img.size[1] + 12
        if x + w > width:
            x, y, rowh = 0, y + rowh + 6, 0
        pos.append((x, y))
        x += max(w, 40) + 6
        rowh = max(rowh, h)
    sheet = Image.new("RGBA", (width, y + rowh + 6), (40, 40, 60, 255))
    draw = ImageDraw.Draw(sheet)
    for (label, img), (px, py) in zip(tiles, pos):
        draw.text((px, py), label, fill=(255, 255, 0, 255))
        sheet.alpha_composite(img, (px, py + 12))
    sheet.save(out)
    print(out, len(tiles), "frames", sheet.size)


if __name__ == "__main__":
    main()
