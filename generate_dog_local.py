#!/usr/bin/env python3
"""Generate a simple dog image using Pillow (fallback when ComfyUI is unavailable)."""

from PIL import Image, ImageDraw, ImageFilter
import math
import os

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "dog.png")


def draw_dog(draw: ImageDraw.ImageDraw, w: int, h: int):
    cx, cy = w // 2, h // 2

    # Sky background gradient drawn row by row
    img = draw._image
    for y in range(h):
        t = y / h
        r = int(135 + (200 - 135) * t)
        g = int(206 + (230 - 206) * t)
        b = int(235 + (240 - 235) * t)
        img.paste(Image.new("RGB", (w, 1), (r, g, b)), (0, y))

    # Ground
    draw.ellipse([0, cy + 80, w, h + 40], fill=(100, 160, 60))

    # Body
    body_color = (180, 120, 60)
    draw.ellipse([cx - 90, cy - 20, cx + 90, cy + 110], fill=body_color)

    # Head
    draw.ellipse([cx - 65, cy - 130, cx + 65, cy + 10], fill=body_color)

    # Ears (floppy)
    ear_color = (140, 85, 30)
    draw.ellipse([cx - 90, cy - 130, cx - 30, cy - 40], fill=ear_color)
    draw.ellipse([cx + 30, cy - 130, cx + 90, cy - 40], fill=ear_color)

    # Snout
    snout_color = (210, 160, 90)
    draw.ellipse([cx - 30, cy - 60, cx + 30, cy + 0], fill=snout_color)

    # Nose
    draw.ellipse([cx - 12, cy - 68, cx + 12, cy - 48], fill=(50, 30, 20))

    # Eyes
    draw.ellipse([cx - 35, cy - 100, cx - 15, cy - 80], fill=(240, 240, 240))
    draw.ellipse([cx + 15, cy - 100, cx + 35, cy - 80], fill=(240, 240, 240))
    draw.ellipse([cx - 30, cy - 96, cx - 18, cy - 84], fill=(50, 30, 10))
    draw.ellipse([cx + 18, cy - 96, cx + 30, cy - 84], fill=(50, 30, 10))
    # Pupils
    draw.ellipse([cx - 27, cy - 94, cx - 21, cy - 88], fill=(10, 10, 10))
    draw.ellipse([cx + 21, cy - 94, cx + 27, cy - 88], fill=(10, 10, 10))

    # Mouth
    draw.arc([cx - 20, cy - 50, cx, cy - 30], 0, 180, fill=(80, 40, 20), width=3)
    draw.arc([cx, cy - 50, cx + 20, cy - 30], 0, 180, fill=(80, 40, 20), width=3)

    # Legs
    for dx in [-60, -20, 20, 60]:
        draw.rounded_rectangle(
            [cx + dx - 15, cy + 70, cx + dx + 15, cy + 150],
            radius=10, fill=body_color
        )
        # Paws
        draw.ellipse([cx + dx - 18, cy + 138, cx + dx + 18, cy + 162], fill=ear_color)

    # Tail
    draw.arc([cx + 60, cy - 40, cx + 160, cy + 80], 220, 360, fill=ear_color, width=14)

    # Tongue
    draw.ellipse([cx - 10, cy - 30, cx + 10, cy - 5], fill=(230, 80, 80))

    # Collar
    draw.arc([cx - 50, cy - 20, cx + 50, cy + 40], 200, 340, fill=(220, 50, 50), width=10)
    draw.ellipse([cx - 8, cy + 18, cx + 8, cy + 34], fill=(230, 190, 50))


def main():
    w, h = 512, 512
    img = Image.new("RGB", (w, h), (135, 206, 235))
    draw = ImageDraw.Draw(img)
    draw_dog(draw, w, h)
    img = img.filter(ImageFilter.SMOOTH)
    img.save(OUTPUT_PATH)
    print(f"Saved dog image to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
