#!/usr/bin/python3
"""Диаграмма «обнаружено / случайный успех» по уровням изоляции
(results/results.tsv -> article/fig/levels.png). Только Pillow."""
import collections
import pathlib

from PIL import Image, ImageDraw, ImageFont

top = pathlib.Path(__file__).resolve().parent.parent
rows = [l.split("\t") for l in (top / "results" / "results.tsv").read_text().splitlines()[1:]]
count = collections.Counter((r[1], r[4]) for r in rows)

LEVELS = [("level1", "Уровень 1", "хост-система"),
          ("level2", "Уровень 2", "hasher + полный набор"),
          ("level3", "Уровень 3", "минимальный hasher")]
DET, OK = "обнаружена", "случайный успех"
C_DET, C_OK = (44, 98, 160), (205, 120, 40)

W, H = 1600, 1000
img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)
fdir = "/usr/share/fonts/ttf/dejavu/"
f = ImageFont.truetype(fdir + "DejaVuSans.ttf", 30)
fb = ImageFont.truetype(fdir + "DejaVuSans-Bold.ttf", 32)
fs = ImageFont.truetype(fdir + "DejaVuSans.ttf", 26)

x0, y0, x1, y1 = 150, 70, W - 60, H - 270   # область построения
scale = (y1 - y0) / 10
for v in range(0, 11, 2):
    y = y1 - v * scale
    d.line([(x0, y), (x1, y)], fill=(225, 225, 225), width=2)
    d.text((x0 - 20, y), str(v), font=f, fill="black", anchor="rm")
d.line([(x0, y0), (x0, y1)], fill="black", width=3)
d.line([(x0, y1), (x1, y1)], fill="black", width=3)
lab = Image.new("RGB", (400, 50), "white")
ImageDraw.Draw(lab).text((200, 25), "пакетов из 10", font=f, fill="black", anchor="mm")
lab = lab.rotate(90, expand=True)
img.paste(lab, (25, int((y0 + y1) / 2 - 200)))

group = (x1 - x0) / len(LEVELS)
bw = 150
for i, (lvl, name, sub) in enumerate(LEVELS):
    cx = x0 + group * (i + 0.5)
    for j, (kind, col) in enumerate(((DET, C_DET), (OK, C_OK))):
        v = count[(lvl, kind)]
        bx = cx - bw - 10 + j * (bw + 20)
        if v:
            d.rectangle([bx, y1 - v * scale, bx + bw, y1], fill=col)
        d.text((bx + bw / 2, y1 - v * scale - 8), str(v), font=fb, fill="black", anchor="md")
    d.text((cx, y1 + 20), name, font=fb, fill="black", anchor="ma")
    d.text((cx, y1 + 62), sub, font=fs, fill="black", anchor="ma")

ly = H - 120
for kind, col, label in ((DET, C_DET, "необъявленная зависимость обнаружена (отказ сборки)"),
                         (OK, C_OK, "случайный успех (сборка прошла)")):
    d.rectangle([x0 + 30, ly, x0 + 66, ly + 36], fill=col)
    d.text((x0 + 80, ly + 18), label, font=f, fill="black", anchor="lm")
    ly += 52

out = top / "article" / "fig" / "levels.png"
out.parent.mkdir(parents=True, exist_ok=True)
img.save(out)
print(out)
