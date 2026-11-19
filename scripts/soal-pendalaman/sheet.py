import sys, glob, os
from PIL import Image
files = sorted(glob.glob(sys.argv[1]))
out = sys.argv[2]; cols = int(sys.argv[3]) if len(sys.argv) > 3 else 3
W = 450
ims = []
for f in files:
    im = Image.open(f); im.thumbnail((W, 340)); ims.append((os.path.basename(f), im))
rows = (len(ims) + cols - 1) // cols
H = 360
sheet = Image.new("RGB", (cols * W, rows * H), "white")
from PIL import ImageDraw
d = ImageDraw.Draw(sheet)
for i, (n, im) in enumerate(ims):
    x, y = (i % cols) * W, (i // cols) * H
    sheet.paste(im, (x, y + 18)); d.text((x + 4, y + 2), n, fill="red")
sheet.save(out)
