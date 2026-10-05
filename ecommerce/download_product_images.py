#!/usr/bin/env python3
"""
Download 150 real product images for the Nawab e-commerce project.

Usage:
    python download_product_images.py

The script creates:
    images/fashion/
    images/home/
    images/gaming/
    images/electronics/
    images/accessories/

and saves exactly the filenames used by the JavaScript products array.

Requirements:
    pip install requests beautifulsoup4 pillow
"""

from pathlib import Path
from io import BytesIO
import json
import re
import time
import random

import requests
from bs4 import BeautifulSoup
from PIL import Image

ROOT = Path(__file__).resolve().parent
IMAGE_ROOT = ROOT / "images"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/154.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

# Exact 150 products from the supplied products array.
PRODUCTS = [
    # Fashion
    ("fashion", "classic-cotton-tshirt", "Classic Cotton T-Shirt"),
    ("fashion", "slim-fit-jeans", "Slim Fit Jeans"),
    ("fashion", "casual-hoodie", "Casual Hoodie"),
    ("fashion", "denim-jacket", "Denim Jacket"),
    ("fashion", "casual-shirt", "Casual Shirt"),
    ("fashion", "formal-shirt", "Formal Shirt"),
    ("fashion", "cargo-pants", "Cargo Pants"),
    ("fashion", "track-pants", "Track Pants"),
    ("fashion", "oversized-tshirt", "Oversized T-Shirt"),
    ("fashion", "polo-tshirt", "Polo T-Shirt"),
    ("fashion", "bomber-jacket", "Bomber Jacket"),
    ("fashion", "leather-jacket", "Leather Jacket"),
    ("fashion", "chinos", "Chinos"),
    ("fashion", "linen-shirt", "Linen Shirt"),
    ("fashion", "printed-shirt", "Printed Shirt"),
    ("fashion", "sweatshirt", "Sweatshirt"),
    ("fashion", "winter-sweater", "Winter Sweater"),
    ("fashion", "sports-shorts", "Sports Shorts"),
    ("fashion", "running-shorts", "Running Shorts"),
    ("fashion", "kurta", "Kurta"),
    ("fashion", "casual-sneakers", "Casual Sneakers"),
    ("fashion", "running-shoes", "Running Shoes"),
    ("fashion", "canvas-shoes", "Canvas Shoes"),
    ("fashion", "baseball-cap", "Baseball Cap"),
    ("fashion", "leather-belt", "Leather Belt"),
    ("fashion", "classic-wallet", "Classic Wallet"),
    ("fashion", "sunglasses", "Sunglasses"),
    ("fashion", "backpack", "Backpack"),
    ("fashion", "analog-watch", "Analog Watch"),
    ("fashion", "fashion-scarf", "Fashion Scarf"),

    # Home
    ("home", "modern-table-lamp", "Modern Table Lamp"),
    ("home", "led-ceiling-light", "LED Ceiling Light"),
    ("home", "decorative-wall-clock", "Decorative Wall Clock"),
    ("home", "ceramic-vase", "Ceramic Vase"),
    ("home", "cushion-set", "Cushion Set"),
    ("home", "cotton-bedsheet", "Cotton Bedsheet"),
    ("home", "soft-blanket", "Soft Blanket"),
    ("home", "bath-towel-set", "Bath Towel Set"),
    ("home", "kitchen-storage-set", "Kitchen Storage Set"),
    ("home", "non-stick-frying-pan", "Non-Stick Frying Pan"),
    ("home", "stainless-steel-bottle", "Stainless Steel Bottle"),
    ("home", "electric-kettle", "Electric Kettle"),
    ("home", "coffee-maker", "Coffee Maker"),
    ("home", "dinner-set", "Dinner Set"),
    ("home", "glass-tumbler-set", "Glass Tumbler Set"),
    ("home", "kitchen-knife-set", "Kitchen Knife Set"),
    ("home", "wooden-cutting-board", "Wooden Cutting Board"),
    ("home", "storage-organizer", "Storage Organizer"),
    ("home", "laundry-basket", "Laundry Basket"),
    ("home", "floor-mat", "Floor Mat"),
    ("home", "artificial-plant", "Artificial Plant"),
    ("home", "scented-candle", "Scented Candle"),
    ("home", "photo-frame", "Photo Frame"),
    ("home", "wall-art", "Wall Art"),
    ("home", "table-runner", "Table Runner"),
    ("home", "curtain-set", "Curtain Set"),
    ("home", "pillow-set", "Pillow Set"),
    ("home", "bathroom-organizer", "Bathroom Organizer"),
    ("home", "laundry-bag", "Laundry Bag"),
    ("home", "decorative-mirror", "Decorative Mirror"),

    # Gaming
    ("gaming", "gaming-mouse", "Gaming Mouse"),
    ("gaming", "mechanical-keyboard", "Mechanical Gaming Keyboard"),
    ("gaming", "gaming-headset", "Gaming Headset"),
    ("gaming", "rgb-mouse-pad", "RGB Gaming Mouse Pad"),
    ("gaming", "gaming-controller", "Gaming Controller"),
    ("gaming", "gaming-chair", "Gaming Chair"),
    ("gaming", "gaming-desk", "Gaming Desk"),
    ("gaming", "usb-gaming-microphone", "USB Gaming Microphone"),
    ("gaming", "webcam", "Webcam"),
    ("gaming", "gaming-speakers", "Gaming Speakers"),
    ("gaming", "rgb-led-strip", "RGB LED Strip"),
    ("gaming", "console-stand", "Console Stand"),
    ("gaming", "controller-charging-dock", "Controller Charging Dock"),
    ("gaming", "gaming-laptop-stand", "Gaming Laptop Stand"),
    ("gaming", "vr-headset", "VR Headset"),
    ("gaming", "portable-gaming-console", "Portable Gaming Console"),
    ("gaming", "gaming-earbuds", "Gaming Earbuds"),
    ("gaming", "gaming-keypad", "Gaming Keypad"),
    ("gaming", "streaming-light", "Streaming Light"),
    ("gaming", "capture-card", "Gaming Capture Card"),
    ("gaming", "controller-grip", "Game Controller Grip"),
    ("gaming", "gaming-finger-sleeves", "Gaming Finger Sleeves"),
    ("gaming", "cooling-pad", "Gaming Cooling Pad"),
    ("gaming", "monitor-stand", "Gaming Monitor Stand"),
    ("gaming", "rgb-desk-mat", "RGB Desk Mat"),
    ("gaming", "game-storage-case", "Game Storage Case"),
    ("gaming", "gaming-backpack", "Gaming Backpack"),
    ("gaming", "headset-stand", "Headset Stand"),
    ("gaming", "cable-organizer", "Gaming Cable Organizer"),
    ("gaming", "rgb-gaming-controller", "RGB Gaming Controller"),

    # Electronics
    ("electronics", "smartphone", "Smartphone"),
    ("electronics", "tablet", "Tablet"),
    ("electronics", "laptop", "Laptop"),
    ("electronics", "smart-tv", "Smart TV"),
    ("electronics", "bluetooth-speaker", "Bluetooth Speaker"),
    ("electronics", "wireless-earbuds", "Wireless Earbuds"),
    ("electronics", "smartwatch", "Smartwatch"),
    ("electronics", "power-bank", "Power Bank"),
    ("electronics", "wireless-charger", "Wireless Charger"),
    ("electronics", "usb-c-charger", "USB-C Charger"),
    ("electronics", "bluetooth-headphones", "Bluetooth Headphones"),
    ("electronics", "digital-camera", "Digital Camera"),
    ("electronics", "action-camera", "Action Camera"),
    ("electronics", "portable-projector", "Portable Projector"),
    ("electronics", "smart-home-hub", "Smart Home Hub"),
    ("electronics", "wifi-router", "Wi-Fi Router"),
    ("electronics", "bluetooth-adapter", "Bluetooth Adapter"),
    ("electronics", "usb-hub", "USB Hub"),
    ("electronics", "external-ssd", "External SSD"),
    ("electronics", "external-hard-drive", "External Hard Drive"),
    ("electronics", "computer-monitor", "Computer Monitor"),
    ("electronics", "wireless-keyboard", "Wireless Keyboard"),
    ("electronics", "wireless-mouse", "Wireless Mouse"),
    ("electronics", "laser-printer", "Laser Printer"),
    ("electronics", "smart-doorbell", "Smart Doorbell"),
    ("electronics", "security-camera", "Security Camera"),
    ("electronics", "digital-alarm-clock", "Digital Alarm Clock"),
    ("electronics", "smart-plug", "Smart Plug"),
    ("electronics", "electric-shaver", "Electric Shaver"),
    ("electronics", "electric-trimmer", "Electric Trimmer"),

    # Accessories
    ("accessories", "leather-wallet", "Leather Wallet"),
    ("accessories", "travel-backpack", "Travel Backpack"),
    ("accessories", "laptop-backpack", "Laptop Backpack"),
    ("accessories", "phone-case", "Phone Case"),
    ("accessories", "screen-protector", "Screen Protector"),
    ("accessories", "usb-c-cable", "USB-C Cable"),
    ("accessories", "lightning-cable", "Lightning Cable"),
    ("accessories", "car-phone-holder", "Car Phone Holder"),
    ("accessories", "phone-stand", "Phone Stand"),
    ("accessories", "laptop-stand", "Laptop Stand"),
    ("accessories", "cable-organizer", "Cable Organizer"),
    ("accessories", "travel-adapter", "Travel Adapter"),
    ("accessories", "keychain", "Keychain"),
    ("accessories", "card-holder", "Card Holder"),
    ("accessories", "sunglasses-case", "Sunglasses Case"),
    ("accessories", "wristband", "Wristband"),
    ("accessories", "fitness-band-strap", "Fitness Band Strap"),
    ("accessories", "watch-strap", "Watch Strap"),
    ("accessories", "key-organizer", "Key Organizer"),
    ("accessories", "travel-pouch", "Travel Pouch"),
    ("accessories", "passport-holder", "Passport Holder"),
    ("accessories", "luggage-tag", "Luggage Tag"),
    ("accessories", "travel-neck-pillow", "Travel Neck Pillow"),
    ("accessories", "foldable-umbrella", "Foldable Umbrella"),
    ("accessories", "waterproof-pouch", "Waterproof Pouch"),
    ("accessories", "reusable-shopping-bag", "Reusable Shopping Bag"),
    ("accessories", "minimalist-key-ring", "Minimalist Key Ring"),
    ("accessories", "cable-clips", "Cable Clips"),
    ("accessories", "desk-organizer", "Desk Organizer"),
    ("accessories", "multi-purpose-pouch", "Multi-Purpose Pouch"),
]

assert len(PRODUCTS) == 150, f"Expected 150 products, found {len(PRODUCTS)}"


def bing_image_urls(query, count=8):
    """Get candidate image URLs from Bing Images without an API key."""
    url = "https://www.bing.com/images/search"
    params = {
        "q": query,
        "form": "HDRSC2",
        "first": 1,
        "count": count,
        "safeSearch": "Strict",
    }

    r = requests.get(url, params=params, headers=HEADERS, timeout=25)
    r.raise_for_status()

    # Bing embeds image metadata in m=... JSON-ish attributes.
    soup = BeautifulSoup(r.text, "html.parser")
    results = []

    for a in soup.select("a.iusc"):
        raw = a.get("m")
        if not raw:
            continue
        try:
            data = json.loads(raw)
            image_url = data.get("murl")
            if image_url and image_url.startswith(("http://", "https://")):
                results.append(image_url)
        except Exception:
            continue

    return results


def download_and_convert(url, destination):
    """Download an image, validate it, convert it to JPEG."""
    try:
        r = requests.get(
            url,
            headers=HEADERS,
            timeout=25,
            allow_redirects=True,
        )
        r.raise_for_status()

        content_type = r.headers.get("Content-Type", "").lower()
        if "image" not in content_type and len(r.content) < 5000:
            return False

        image = Image.open(BytesIO(r.content))
        image = image.convert("RGB")

        # Avoid tiny icons/thumbnails.
        width, height = image.size
        if width < 250 or height < 250:
            return False

        # Store a reasonably sized local product image.
        image.thumbnail((1400, 1400), Image.Resampling.LANCZOS)
        image.save(destination, "JPEG", quality=88, optimize=True)
        return True

    except Exception:
        return False


def build_queries(category, product):
    """Queries are intentionally product-specific to reduce wrong images."""
    category_names = {
        "fashion": "fashion product",
        "home": "home product",
        "gaming": "gaming product",
        "electronics": "electronics product",
        "accessories": "accessory product",
    }

    base = category_names[category]

    return [
        f"{product} {base} product photo",
        f"{product} isolated product",
        f"{product} white background product",
        f"{product} ecommerce product photo",
    ]


def download_product(category, slug, name):
    folder = IMAGE_ROOT / category
    folder.mkdir(parents=True, exist_ok=True)

    destination = folder / f"{slug}.jpg"

    if destination.exists() and destination.stat().st_size > 10_000:
        print(f"[SKIP] {category}/{slug}.jpg already exists")
        return True

    print(f"\n[{category.upper()}] {name}")

    candidates = []
    seen = set()

    for query in build_queries(category, name):
        try:
            urls = bing_image_urls(query)
            for u in urls:
                if u not in seen:
                    seen.add(u)
                    candidates.append(u)
            if len(candidates) >= 15:
                break
        except Exception as exc:
            print(f"  Search failed: {exc}")

        time.sleep(0.5)

    random.shuffle(candidates)

    for index, url in enumerate(candidates[:20], 1):
        print(f"  Trying image {index}/{min(len(candidates), 20)}...", end=" ")

        if download_and_convert(url, destination):
            print("OK")
            return True

        print("rejected")

    print("  FAILED - no suitable image found")
    return False


def main():
    print("=" * 70)
    print("NAWAB - 150 PRODUCT IMAGE DOWNLOADER")
    print("=" * 70)
    print(f"Output: {IMAGE_ROOT}")
    print(f"Products: {len(PRODUCTS)}")
    print()

    IMAGE_ROOT.mkdir(parents=True, exist_ok=True)

    success = []
    failed = []

    for number, (category, slug, name) in enumerate(PRODUCTS, 1):
        print(f"\n--- {number}/150 ---")

        if download_product(category, slug, name):
            success.append((number, category, slug, name))
        else:
            failed.append((number, category, slug, name))

        # Be polite to the search service.
        time.sleep(random.uniform(0.8, 1.5))

    print("\n" + "=" * 70)
    print(f"FINISHED: {len(success)}/150 images downloaded")
    print("=" * 70)

    if failed:
        print("\nFAILED PRODUCTS:")
        for number, category, slug, name in failed:
            print(f"  {number:3}  {category}/{slug}.jpg  <- {name}")

        # Save failed list for an easy second run/debug.
        failed_file = ROOT / "failed_images.txt"
        failed_file.write_text(
            "\n".join(
                f"{number}|{category}|{slug}|{name}"
                for number, category, slug, name in failed
            ),
            encoding="utf-8",
        )
        print(f"\nFailed list saved to: {failed_file}")

    # Final filesystem verification.
    missing = []
    for number, (category, slug, name) in enumerate(PRODUCTS, 1):
        path = IMAGE_ROOT / category / f"{slug}.jpg"
        if not path.exists() or path.stat().st_size < 10_000:
            missing.append((number, category, slug, name))

    print(f"\nFilesystem verification: {150 - len(missing)}/150 present.")

    if missing:
        print("Missing:")
        for number, category, slug, name in missing:
            print(f"  {number:3} {category}/{slug}.jpg")

    print("\nYour JavaScript image paths can remain unchanged.")


if __name__ == "__main__":
    main()
