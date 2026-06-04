"""
Generate app_icon.ico for AWWA Lunch Project.
Run: python make_icon.py
Requires: pillow  (already in requirements.txt)
"""
from PIL import Image, ImageDraw
import os, sys

def make_icon(out_path="app_icon.ico"):
    SIZES = [256, 128, 64, 48, 32, 16]
    frames = []

    for sz in SIZES:
        img  = Image.new("RGBA", (sz, sz), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # ── Army-green circle background ──────────────────────────────────────
        margin = max(1, sz // 16)
        draw.ellipse(
            [margin, margin, sz - margin - 1, sz - margin - 1],
            fill=(31, 51, 32, 255)
        )

        # ── Tricolor arc band (top of circle) ─────────────────────────────────
        band_h = max(2, sz // 10)
        cx, cy = sz // 2, sz // 2
        r = sz // 2 - margin

        # Just draw 3 horizontal colour blocks clipped to the circle top-half
        for i, color in enumerate([(255, 153, 51), (255, 255, 255), (19, 136, 8)]):
            x0 = sz * i // 3
            x1 = sz * (i + 1) // 3
            draw.rectangle([x0, 0, x1, band_h + margin + 2], fill=color)

        # Re-draw the circle outline to clip the tricolor
        draw.ellipse(
            [margin, margin, sz - margin - 1, sz - margin - 1],
            outline=(201, 168, 76, 255),
            width=max(1, sz // 32)
        )
        # Fill outside circle with transparent (cheap clip trick via overlay)
        # Mask: keep only inside circle
        mask = Image.new("L", (sz, sz), 0)
        mdraw = ImageDraw.Draw(mask)
        mdraw.ellipse([margin, margin, sz - margin - 1, sz - margin - 1], fill=255)
        # Composite over army green base to clip the band
        base = Image.new("RGBA", (sz, sz), (0, 0, 0, 0))
        bdraw = ImageDraw.Draw(base)
        bdraw.ellipse([margin, margin, sz - margin - 1, sz - margin - 1],
                      fill=(31, 51, 32, 255))
        # Tricolor band on top
        band_img = Image.new("RGBA", (sz, sz), (0, 0, 0, 0))
        bnd = ImageDraw.Draw(band_img)
        colors3 = [(255, 153, 51), (255, 255, 255), (19, 136, 8)]
        for i, c in enumerate(colors3):
            bnd.rectangle([sz * i // 3, margin, sz * (i + 1) // 3,
                            margin + band_h + 2], fill=c + (255,))
        band_img.putalpha(mask)
        base.paste(band_img, mask=band_img)

        # ── Gold star in centre ───────────────────────────────────────────────
        star_r  = sz * 28 // 100
        star_ri = sz * 12 // 100
        import math
        cx2 = cy2 = sz // 2
        # Shift star down a bit to clear the band
        cy2 = int(sz * 0.54)
        pts = []
        for k in range(10):
            angle = math.radians(-90 + k * 36)
            r_use = star_r if k % 2 == 0 else star_ri
            pts.append((cx2 + r_use * math.cos(angle),
                        cy2 + r_use * math.sin(angle)))
        if sz >= 32:
            bdraw2 = ImageDraw.Draw(base)
            bdraw2.polygon(pts, fill=(201, 168, 76, 255))

        # ── Gold circle border ─────────────────────────────────────────────────
        bdraw3 = ImageDraw.Draw(base)
        bdraw3.ellipse([margin, margin, sz - margin - 1, sz - margin - 1],
                       outline=(201, 168, 76, 255), width=max(1, sz // 28))

        frames.append(base)

    # Save as multi-resolution .ico
    frames[0].save(
        out_path,
        format="ICO",
        sizes=[(sz, sz) for sz in SIZES],
        append_images=frames[1:]
    )
    print(f"✅  Icon saved: {out_path}  ({os.path.getsize(out_path):,} bytes)")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "app_icon.ico"
    make_icon(out)
