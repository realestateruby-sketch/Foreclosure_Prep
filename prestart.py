"""Patches Streamlit's static index.html with Open Graph + Twitter Card meta tags.

Runs BEFORE `streamlit run` so the patched index.html is served on the very
first request. Idempotent — safe to run on every container start.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

OG_IMAGE_URL = "https://raw.githubusercontent.com/realestateruby-sketch/Foreclosure_Prep/main/logo.png"
OG_SITE_URL = "https://foreclosureprep-production.up.railway.app/"
OG_TITLE = "Foreclosure Prep"
OG_DESCRIPTION = (
    "Better data, faster decisions. Built for agents, investors, and "
    "negotiators who work foreclosures."
)


def main() -> int:
    try:
        import streamlit as st_mod
    except ImportError:
        print("[prestart] streamlit not importable; skipping OG patch", file=sys.stderr)
        return 0

    index_path = Path(st_mod.__file__).parent / "static" / "index.html"
    if not index_path.exists():
        print(f"[prestart] index.html not found at {index_path}; skipping", file=sys.stderr)
        return 0

    html = index_path.read_text(encoding="utf-8")
    if 'property="og:title"' in html:
        print("[prestart] OG tags already present; nothing to do", file=sys.stderr)
        return 0

    og_block = (
        f'    <meta property="og:title" content="{OG_TITLE}" />\n'
        f'    <meta property="og:description" content="{OG_DESCRIPTION}" />\n'
        f'    <meta property="og:image" content="{OG_IMAGE_URL}" />\n'
        f'    <meta property="og:url" content="{OG_SITE_URL}" />\n'
        f'    <meta property="og:type" content="website" />\n'
        f'    <meta name="twitter:card" content="summary_large_image" />\n'
        f'    <meta name="twitter:title" content="{OG_TITLE}" />\n'
        f'    <meta name="twitter:description" content="{OG_DESCRIPTION}" />\n'
        f'    <meta name="twitter:image" content="{OG_IMAGE_URL}" />\n'
    )
    html = html.replace("<head>", "<head>\n" + og_block, 1)
    html = re.sub(r"<title>.*?</title>", f"<title>{OG_TITLE}</title>", html, count=1)
    index_path.write_text(html, encoding="utf-8")
    print(f"[prestart] patched {index_path} with OG tags", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
