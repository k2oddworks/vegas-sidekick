from pathlib import Path
from PIL import Image, ImageOps

root = Path(__file__).resolve().parents[1]
brand = root / "images" / "brand"
source = Image.open(brand / "spike-icon.png").convert("RGBA")
for size, name, inset in [(192, "hub-icon-192.png", .90), (512, "hub-icon-512.png", .90), (512, "hub-icon-maskable.png", .68)]:
    canvas = Image.new("RGBA", (size, size), "#111111")
    art = ImageOps.contain(source, (round(size * inset), round(size * inset)), Image.Resampling.LANCZOS)
    canvas.alpha_composite(art, ((size-art.width)//2, (size-art.height)//2))
    canvas.convert("RGB").save(brand / name, optimize=True)
