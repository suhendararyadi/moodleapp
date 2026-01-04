from PIL import Image, ImageDraw, ImageFont
import os

def create_splash_with_text():
    # Settings
    CANVAS_SIZE = (2732, 2732)
    BG_COLOR = "white"
    LOGO_PATH = "logo app sagar.png"
    OUTPUT_PATH = "resources/splash.png"
    TEXT = "Dikembangkan Oleh\nTeknik Elektronika Industri"
    FONT_PATH = "/System/Library/Fonts/Geneva.ttf"
    FONT_SIZE = 90
    TEXT_COLOR = (51, 51, 51) # Dark gray #333333
    LOGO_SIZE = (1024, 1024) # Resize logo to this max dimension

    print(f"Generating splash screen with text...")

    # Create canvas
    img = Image.new("RGBA", CANVAS_SIZE, BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Load and Resize Logo
    if os.path.exists(LOGO_PATH):
        logo = Image.open(LOGO_PATH).convert("RGBA")
        logo.thumbnail(LOGO_SIZE, Image.Resampling.LANCZOS)

        # Center Logo (slightly higher to make room for text)
        logo_x = (CANVAS_SIZE[0] - logo.width) // 2
        logo_y = (CANVAS_SIZE[1] - logo.height) // 2 - 200 # Shift up 200px
        img.paste(logo, (logo_x, logo_y), logo)
    else:
        print(f"Error: {LOGO_PATH} not found!")
        return

    # Load Font
    try:
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    except IOError:
        print("Font not found, using default.")
        font = ImageFont.load_default()

    # Draw Text (Centered per line)
    lines = TEXT.split('\n')
    line_spacing = 20

    # Calculate total text height to position it
    total_text_height = 0
    line_heights = []
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        height = bbox[3] - bbox[1]
        line_heights.append(height)
        total_text_height += height + line_spacing

    # Start drawing text at bottom area
    current_y = logo_y + logo.height + 300 # 300px below logo

    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        text_x = (CANVAS_SIZE[0] - text_width) // 2

        draw.text((text_x, current_y), line, font=font, fill=TEXT_COLOR)
        current_y += line_heights[i] + line_spacing

    # Save
    img.save(OUTPUT_PATH)
    print(f"Splash screen saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    create_splash_with_text()
