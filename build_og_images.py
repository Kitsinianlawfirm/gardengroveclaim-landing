"""
Generate Open Graph (link preview) images for the landing page.
1200x630 — the dimension Facebook/LinkedIn/iMessage/etc. use for previews.
Headline + trust line are BURNED IN to the image (no HTML overlay) because
social media platforms render the image, not the page.

Output:
  - og-en.jpg  (English version, for root URL)
  - og-es.jpg  (Spanish version, for /es/ URL)
"""

from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
from pathlib import Path

OUT = Path(__file__).parent
PHOTO_PATH = OUT / "hero.jpg"
LOGO_PATH = OUT / "logo.png"

W, H = 1200, 630

# Brand palette
COLORS = {
    "bg_dark": (12, 14, 20),
    "yellow": (255, 209, 0),
    "red": (220, 38, 38),
    "white": (255, 255, 255),
    "gold": (198, 162, 92),
    "muted": (174, 180, 192),
}

# Fonts (firm standards)
FONT_BEBAS = "/Users/hkitsinian/Library/Fonts/BebasNeue-Regular.otf"
FONT_BARLOW_BLACK = "/Users/hkitsinian/Library/Fonts/Barlow-Black.otf"
FONT_BARLOW_XBOLD = "/Users/hkitsinian/Library/Fonts/Barlow-ExtraBold.otf"
FONT_BARLOW_COND_XB = "/Users/hkitsinian/Library/Fonts/BarlowCondensed-ExtraBold.otf"
FONT_INTER_XBOLD = "/Users/hkitsinian/Library/Fonts/Inter-ExtraBold.otf"
FONT_INTER_SEMI = "/Users/hkitsinian/Library/Fonts/Inter-SemiBold.otf"


def f(path, size):
    return ImageFont.truetype(path, size)


def cap_height(draw, font):
    b = draw.textbbox((0, 0), "H", font=font, anchor="lt")
    return b[3] - b[1]


def draw_cap_centered(draw, cx, cy, text, font, fill):
    ch = cap_height(draw, font)
    top_y = cy - ch // 2
    draw.text((cx, top_y), text, font=font, fill=fill, anchor="mt")


def cover_fit(src, w, h):
    sw, sh = src.size
    scale = max(w / sw, h / sh)
    new_w, new_h = int(sw * scale), int(sh * scale)
    img = src.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - w) // 2
    top = (new_h - h) // 2
    return img.crop((left, top, left + w, top + h))


def build_og(headline_lines, subhead, trust_line, domain, output_filename, chip_text="URGENT LEGAL NOTICE"):
    """headline_lines = list of strings rendered in Bebas Neue."""
    # Background photo with brighten + 50% dark overlay
    photo = Image.open(PHOTO_PATH).convert("RGB")
    bg = cover_fit(photo, W, H)
    bg = ImageEnhance.Brightness(bg).enhance(1.10)
    bg = ImageEnhance.Contrast(bg).enhance(1.15)
    overlay = Image.new("RGB", (W, H), COLORS["bg_dark"])
    bg = Image.blend(bg, overlay, 0.55)
    img = bg.convert("RGBA")

    # Gradient at bottom for trust line legibility
    grad = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grad)
    for y in range(int(H * 0.55), H):
        t = (y - int(H * 0.55)) / (H - int(H * 0.55))
        a = int(t * 200)
        gd.line([(0, y), (W, y)], fill=(8, 10, 16, a))
    img.alpha_composite(grad)

    draw = ImageDraw.Draw(img)

    # Top-left URGENT chip
    chip_font = f(FONT_INTER_XBOLD, 22)
    chip_pad_x, chip_pad_y = 22, 11
    chip_w = draw.textbbox((0, 0), chip_text, font=chip_font, anchor="lt")[2] + chip_pad_x * 2
    chip_h = chip_font.size + chip_pad_y * 2
    chip_x, chip_y = 50, 50
    draw.rounded_rectangle(
        [chip_x, chip_y, chip_x + chip_w, chip_y + chip_h],
        radius=chip_h // 2, fill=COLORS["red"],
    )
    draw_cap_centered(draw, chip_x + chip_w // 2, chip_y + chip_h // 2, chip_text, chip_font, COLORS["white"])

    # Headline (centered vertically in upper-middle)
    head_font = f(FONT_BEBAS, 120)
    n_lines = len(headline_lines)
    line_h = 110
    total_h = line_h * n_lines
    head_start_y = int(H * 0.30) - total_h // 2 + line_h // 2
    for i, line in enumerate(headline_lines):
        draw_cap_centered(
            draw, W // 2, head_start_y + i * line_h,
            line, head_font, COLORS["white"],
        )

    # Subhead (yellow, below headline)
    sub_font = f(FONT_BARLOW_COND_XB, 44)
    sub_y = head_start_y + n_lines * line_h + 30
    # support 2-line subhead via list or 1-line via string
    if isinstance(subhead, str):
        subhead = [subhead]
    sub_line_h = 50
    for i, line in enumerate(subhead):
        draw_cap_centered(
            draw, W // 2, sub_y + i * sub_line_h,
            line, sub_font, COLORS["yellow"],
        )

    # Trust line (gold, bottom)
    trust_font = f(FONT_BARLOW_XBOLD, 28)
    draw_cap_centered(draw, W // 2, H - 95, trust_line, trust_font, COLORS["gold"])

    # Logo + domain bottom
    try:
        logo = Image.open(LOGO_PATH).convert("RGBA")
        logo_h = 44
        logo_w = int(logo.width * (logo_h / logo.height))
        logo = logo.resize((logo_w, logo_h), Image.LANCZOS)
        # Bottom-center: logo on left, domain on right of logo
        domain_font = f(FONT_INTER_SEMI, 22)
        gap = 24
        domain_bbox = draw.textbbox((0, 0), domain, font=domain_font, anchor="lm")
        domain_w = domain_bbox[2] - domain_bbox[0]
        # Vertical divider
        block_w = logo_w + gap + 2 + gap + domain_w
        start_x = (W - block_w) // 2
        y_mid = H - 40
        img.paste(logo, (start_x, y_mid - logo_h // 2), logo)
        # divider
        div_x = start_x + logo_w + gap
        draw.line(
            [(div_x, y_mid - logo_h // 2 + 6), (div_x, y_mid + logo_h // 2 - 6)],
            fill=COLORS["gold"], width=2,
        )
        # domain
        draw.text(
            (div_x + gap, y_mid), domain,
            font=domain_font, fill=COLORS["muted"], anchor="lm",
        )
    except Exception as e:
        print(f"  logo render skipped: {e}")

    # Save as JPEG (smaller than PNG, OG-standard)
    out_path = OUT / output_filename
    img.convert("RGB").save(out_path, "JPEG", quality=88, optimize=True)
    print(f"  Wrote {out_path} ({W}x{H})")


def main():
    print("Building OG images...")

    # English
    build_og(
        headline_lines=["EVACUATED?"],
        subhead=["GARDEN GROVE CHEMICAL LEAK", "YOU MAY BE OWED COMPENSATION"],
        trust_line="FREE CASE REVIEW · NO FEE UNLESS WE WIN",
        domain="gardengrovetankleak.com",
        output_filename="og-en.jpg",
    )

    # Spanish
    build_og(
        headline_lines=["¿FUE EVACUADO?"],
        subhead=["DERRAME QUÍMICO EN GARDEN GROVE", "PUEDE TENER DERECHO A COMPENSACIÓN"],
        trust_line="CONSULTA GRATIS · SIN COSTO SI NO GANAMOS",
        domain="gardengrovetankleak.com/es",
        output_filename="og-es.jpg",
        chip_text="AVISO LEGAL URGENTE",
    )


if __name__ == "__main__":
    main()
