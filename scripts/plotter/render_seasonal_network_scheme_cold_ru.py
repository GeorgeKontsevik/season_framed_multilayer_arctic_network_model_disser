from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "itmo-phd-thesis-template-en" / "images" / "ch4" / "arctic" / "seasonal_network_scheme_cold.png"

W, H = 2048, 500
BG = (0, 0, 0)
INK = (46, 52, 64)
ORIGIN = (136, 206, 227)
DEST = (93, 139, 189)
AVIATION = (191, 97, 106)
ROAD = (235, 203, 139)
WINTER = (163, 190, 140)
WATER = (180, 142, 173)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

FONT = "/System/Library/Fonts/Supplemental/Arial.ttf"
BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


def f(size: int, bold: bool = False):
    return ImageFont.truetype(BOLD if bold else FONT, size)


def line(points, fill, width=4):
    d.line(points, fill=fill, width=width, joint="curve")


def node(x, y, color, label="", radius=24):
    d.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color, outline=INK, width=3)
    if label:
        box = d.textbbox((0, 0), label, font=f(20, True))
        d.text((x - (box[2] - box[0]) / 2, y - (box[3] - box[1]) / 2 - 2), label, font=f(20, True), fill=INK)


def legend(y, label, color=None, node_color=None):
    if node_color:
        node(62, y, node_color, radius=22)
    else:
        line((8, y, 98, y), color, 5)
    d.text((128, y - 17), label, font=f(24), fill=INK)


legend(55, "исходный узел", node_color=ORIGIN)
legend(120, "целевой узел", node_color=DEST)
legend(215, "авиация", AVIATION)
legend(270, "обычная дорога", ROAD)
legend(325, "зимник", WINTER)
legend(380, "водный транспорт", WATER)

# Network topology and modal edges.
coords = {1: (800, 48), 2: (700, 155), 3: (600, 305), 4: (810, 290), 5: (900, 155), 6: (990, 310), 7: (520, 415)}
line((coords[1], coords[5]), WATER, 4)
line((coords[1], coords[4]), ROAD, 4)
line((coords[2], coords[4]), AVIATION, 5)
line((coords[2], coords[3]), ROAD, 4)
line((coords[2], coords[4]), ROAD, 4)
line((coords[3], coords[4]), ROAD, 4)
line((coords[4], coords[5]), ROAD, 4)
line((coords[5], coords[6]), ROAD, 4)
line((coords[6], coords[4]), AVIATION, 5)
line((coords[5], coords[4]), WATER, 4)
line((coords[7], coords[4]), ROAD, 4)

for key, (x, y) in coords.items():
    if key == 1:
        node(x, y, ORIGIN, "1")
    elif key == 4:
        node(x, y, DEST, "4")
    else:
        node(x, y, ORIGIN, radius=22)

# Edge annotations.
annotations = [
    (775, 83, "P(T)=0,9\nt=3 ч"),
    (910, 43, "P(T)=0,9\nt=1 ч"),
    (965, 180, "P(T)=0,85\nt=2 ч"),
    (885, 255, "P(T)=0,7\nt=1 ч"),
    (895, 350, "P(T)=0,95\nt=1 ч"),
]
for x, y, text in annotations:
    d.multiline_text((x, y), text, font=f(14), fill=INK, spacing=1)

# Arrow and formula explanation.
line((1155, 205, 1240, 205), INK, 5)
d.polygon([(1240, 205), (1218, 193), (1218, 217)], fill=INK)

explanation = (
    "P — вероятность\n"
    "t — время\n"
    "T — температура\n\n"
    "Пусть Pпорог = 0,85\n"
    "Пусть tпорог = 4,5 ч\n\n"
    "P14(T) = среднее(P12(T), P23(T), P34(T)) = 0,9\n"
    "t14 = сумма(t12, t23, t34) = 4\n\n"
    "Тогда P14(T) удовлетворяет порогу P,\n"
    "а t14 удовлетворяет порогу t"
)
d.multiline_text((1340, 14), explanation, font=f(21), fill=INK, spacing=8)

OUT.parent.mkdir(parents=True, exist_ok=True)
img.save(OUT)
assert OUT.stat().st_size > 30_000
print(f"{OUT} | {img.size} | {OUT.stat().st_size:,} bytes")
