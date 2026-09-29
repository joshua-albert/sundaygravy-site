"""Photo list for the site, plus a helper that makes the WebP sizes.

Run `python3 tools/photos.py` after adding a photo here (and dropping its
1800px JPG in photos/ as <slug>.jpg). Needs Pillow: pip3 install --user pillow
"""
from pathlib import Path

# slug, alt text. Order = order on the Work page.
PHOTOS = [
    ("bacon-cheeseburger-fries-restaurant-photography-philadelphia", "Bacon cheeseburger and fries in a checkered basket"),
    ("birria-tacos-food-photography-philadelphia", "Birria tacos on a pink plate with a hard shadow"),
    ("cucumber-margarita-cocktail-photography-philadelphia", "Cucumber margarita held over sliced cucumbers"),
    ("drink-poured-over-ice-strawberries-drink-photography-philadelphia", "Drink poured over ice on a checkerboard tray with strawberries"),
    ("shrimp-tacos-menu-photography-philadelphia", "Shrimp tacos on a blue plate against orange and green"),
    ("full-breakfast-overhead-cafe-photography-philadelphia", "Full breakfast with eggs, tomato and coffee, shot from above"),
    ("flan-dessert-food-photography-philadelphia", "Flan being sliced on a green set"),
    ("chips-and-crema-restaurant-photography-philly", "Hand dipping a chip into crema on an orange grid"),
    ("chips-and-salsa-food-photographer-philadelphia", "Chips and salsa on lilac with a hand reaching in"),
    ("fish-and-chips-overhead-restaurant-photography-philadelphia", "Fish and chips from overhead on dark wood"),
    ("tostada-sunlight-food-photography-philadelphia", "Tostada with tomato and sprouts on a sunlit wood table"),
    ("fresh-limes-bar-photography-philadelphia", "A pile of fresh limes"),
    ("salt-rim-pink-margarita-cocktail-photography-philadelphia", "Salt-rimmed pink margarita with a lime wedge"),
    ("shrimp-tacos-orange-wall-restaurant-photographer-philly", "Shrimp tacos on a blue plate, orange wall, green table"),
    ("tortilla-chips-crema-overhead-food-photography-philly", "Tortilla chips and crema from overhead on an orange grid"),
    ("bangers-and-mash-pub-food-photography-philadelphia", "Bangers, mash and peas on a wood table"),
    ("soda-poured-over-ice-drink-photography-philadelphia", "Soda poured over ice with a knife and lime on the board"),
    ("avocado-half-food-photography-philadelphia", "Half an avocado on white"),
    ("chips-and-salsa-lilac-menu-photography-philly", "Chips and salsa on lilac, second angle"),
    ("cleaned-squid-ingredient-photography-philadelphia", "Cleaned squid, tentacles and rings"),
    ("layer-cakes-bakery-photography-philadelphia", "Three layer cakes on a mosaic patio table"),
]

WIDTHS = (600, 900, 1200, 1800)
ROOT = Path(__file__).resolve().parent.parent / "photos"


def build():
    from PIL import Image
    for slug, _ in PHOTOS:
        src = ROOT / f"{slug}.jpg"
        im = Image.open(src).convert("RGB")
        for w in WIDTHS:
            out = ROOT / f"{slug}-{w}.webp"
            if out.exists() and out.stat().st_mtime > src.stat().st_mtime:
                continue
            h = round(im.height * w / im.width)
            (im if w >= im.width else im.resize((w, h), Image.LANCZOS)).save(out, "WEBP", quality=78, method=6)
        small = ROOT / f"{slug}-900.jpg"
        if not small.exists():
            im.resize((900, round(im.height * 900 / im.width)), Image.LANCZOS).save(small, "JPEG", quality=82, optimize=True, progressive=True)


if __name__ == "__main__":
    build()
