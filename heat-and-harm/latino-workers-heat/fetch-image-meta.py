#!/usr/bin/env python3
"""
Fetch image captions and credits from WordPress for Heat & Harm images.

Usage: python3 fetch-image-meta.py

Queries the Planet Detroit WordPress REST API for each image used in the
story and displays caption, alt text, and credit fields. Run this after
captions/credits have been added in WordPress to see what needs updating
in index.html.
"""

import json
import urllib.request
import html

WP_API = "https://planetdetroit.org/wp-json/wp/v2/media"

# Map: local filename -> WordPress search term
IMAGES = {
    "hero.png": "WEBSITE-",
    "aus6.jpg": "Heat-Harm-Photo-by-AUS-6",
    "aus7.jpg": "Heat-Harm-Photo-by-AUS-7",
    "luis2.jpg": "Heat-Harm-Don-Luis-Photo-by-Maricela-Hernandez-2",
    "storyreach-logo.webp": "storyreach-midwest-PC-logo",
}


def fetch_media(search_term):
    url = f"{WP_API}?search={search_term}&per_page=1"
    req = urllib.request.Request(url, headers={"User-Agent": "PlanetDetroit-DeepDives/1.0"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def clean_html(text):
    """Strip HTML tags and decode entities."""
    import re
    text = re.sub(r"<[^>]+>", "", text)
    return html.unescape(text).strip()


def main():
    print("=" * 60)
    print("Heat & Harm — WordPress Image Metadata")
    print("=" * 60)

    for filename, search in IMAGES.items():
        print(f"\n--- {filename} ---")
        try:
            results = fetch_media(search)
            if not results:
                print("  Not found in WordPress")
                continue

            media = results[0]
            title = html.unescape(media.get("title", {}).get("rendered", ""))
            alt = media.get("alt_text", "")
            caption = clean_html(media.get("caption", {}).get("rendered", ""))
            credit = media.get("meta", {}).get("_media_credit", "")
            credit_url = media.get("meta", {}).get("_media_credit_url", "")

            print(f"  Title:      {title or '(empty)'}")
            print(f"  Alt text:   {alt or '(empty)'}")
            print(f"  Caption:    {caption or '(empty)'}")
            print(f"  Credit:     {credit or '(empty)'}")
            if credit_url:
                print(f"  Credit URL: {credit_url}")

        except Exception as e:
            print(f"  Error: {e}")

    print("\n" + "=" * 60)
    print("Run again after updating captions/credits in WordPress.")
    print("=" * 60)


if __name__ == "__main__":
    main()
