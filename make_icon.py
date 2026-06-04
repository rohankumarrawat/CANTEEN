"""
Generate app_icon.ico for AWWA Lunch Project.
Run: python make_icon.py [output_path]
Requires: pillow (already in requirements.txt)

Fix: Save starting from the LARGEST frame so Pillow's ICO
     size-filter (which caps at the primary image's dimension)
     does not discard the smaller sizes.
"""
import os
import sys
import math
from PIL import Image, ImageDraw


def make_frame(sz):
    """Draw one square frame at sz x sz pixels."""
    img  = Image.new("RGBA", (sz, sz), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # ── Army-green circle ─────────────────────────────────────────────────────
    m = max(1, sz // 16)          # margin
    draw.ellipse([m, m, sz - m - 1, sz - m - 1], fill=(31, 51, 32, 255))

    # ── Tricolor band clipped to top of circle ────────────────────────────────
    band_h = max(2, sz // 9)
    r      = sz // 2 - m
    cx = cy = sz // 2

    # Draw the 3 colour strips
    for i, col in enumerate([(255, 153, 51), (255, 255, 255), (19, 136, 8)]):
        draw.rectangle([sz * i // 3, m, sz * (i + 1) // 3, m + band_h], fill=col + (255,))

    # Re-draw army green "below the band" so band is clipped to top arc
    # (simple trick: redraw the lower portion of the circle over the band edges)
    draw.chord([m, m + band_h, sz - m - 1, sz - m - 1 + band_h],
               start=180, end=360, fill=(31, 51, 32, 255))

    # ── Gold star ────────────────────────────────────────────────────────────
    if sz >= 24:
        star_r  = sz * 28 // 100
        star_ri = sz * 12 // 100
        scx     = sz // 2
        scy     = int(sz * 0.56)
        pts = []
        for k in range(10):
            angle = math.radians(-90 + k * 36)
            rv    = star_r if k % 2 == 0 else star_ri
            pts.append((scx + rv * math.cos(angle),
                        scy + rv * math.sin(angle)))
        draw.polygon(pts, fill=(201, 168, 76, 255))

    # ── Gold border ───────────────────────────────────────────────────────────
    bw = max(1, sz // 28)
    draw.ellipse([m, m, sz - m - 1, sz - m - 1],
                 outline=(201, 168, 76, 255), width=bw)

    return img


def make_icon(out_path="app_icon.ico"):
    SIZES = [16, 24, 32, 48, 64, 128, 256]

    # Build frames from LARGEST to SMALLEST so Pillow's ICO saver
    # uses the 256×256 as the primary image and includes all sizes.
    frames = [make_frame(sz) for sz in reversed(SIZES)]

    # frames[0] is 256×256 (largest) — all smaller ones go in append_images
    frames[0].save(
        out_path,
        format="ICO",
        sizes=[(sz, sz) for sz in SIZES],
        append_images=frames[1:]
    )
    print(f"Icon saved: {out_path}  ({os.path.getsize(out_path):,} bytes)")


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "app_icon.ico"
    make_icon(out)
