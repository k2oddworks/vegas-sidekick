from pathlib import Path
from PIL import Image, ImageOps

root = Path(__file__).resolve().parents[1]
brand = root / "images" / "brand"
source = Image.open(brand / "spike-icon.png").convert("RGBA")
# Identify the existing green/gold mascot rather than the surrounding dark badge.
probe = source.copy()
probe.thumbnail((512, 512))
mask = Image.new("L", probe.size)
mask.putdata([255 if a > 100 and g > 55 and g > b * 1.22 and (g > r * .85 or r > b * 1.5) else 0 for r,g,b,a in probe.getdata()])
bounds = mask.getbbox()
if bounds:
    sx, sy = source.width / probe.width, source.height / probe.height
    x0,y0,x1,y1 = bounds
    w,h = (x1-x0)*sx,(y1-y0)*sy
    # Retain a margin around the sunglasses, cactus and spines.
    pad = max(w,h)*.12
    crop = (max(0,int(x0*sx-pad)),max(0,int(y0*sy-pad)),min(source.width,int(x1*sx+pad+1)),min(source.height,int(y1*sy+pad+1)))
    source = source.crop(crop)
for size, name, inset in [(192, "hub-icon-192.png", 1.0), (512, "hub-icon-512.png", 1.0), (512, "hub-icon-maskable.png", .80)]:
    canvas = Image.new("RGBA", (size, size), "#111111")
    art = ImageOps.contain(source, (round(size * inset), round(size * inset)), Image.Resampling.LANCZOS)
    canvas.alpha_composite(art, ((size-art.width)//2, (size-art.height)//2))
    canvas.convert("RGB").save(brand / name, optimize=True)
