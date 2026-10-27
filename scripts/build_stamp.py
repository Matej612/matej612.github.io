#!/usr/bin/env python3
"""Quarto post-render step: write the build date and copyright year into the page footers.

Runs automatically after `quarto render` (see post-render in _quarto.yml). Standard
library only, so it works in CI without installing anything.
"""

import datetime as dt
import os
import re
from pathlib import Path

PLACEHOLDER = '<span class="build-stamp"></span>'
EN_MONTHS = ("January February March April May June July August September October November December").split()
CS_MONTHS = ("ledna února března dubna května června července srpna září října listopadu prosince").split()


def stamp(lang: str, today: dt.date) -> str:
    iso = today.isoformat()
    if lang.startswith("cs"):
        label = f"Aktualizováno {today.day}. {CS_MONTHS[today.month - 1]} {today.year}"
    else:
        label = f"Last updated {today.day} {EN_MONTHS[today.month - 1]} {today.year}"
    return f'<span class="build-stamp">© {today.year} · <time datetime="{iso}">{label}</time></span>'


def main() -> None:
    out_dir = Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "_site"))
    listed = os.environ.get("QUARTO_PROJECT_OUTPUT_FILES", "").splitlines()
    files = [Path(f) for f in listed if f.endswith(".html")] or list(out_dir.rglob("*.html"))
    today = dt.date.today()
    for f in files:
        if not f.is_file():
            continue
        html = f.read_text(encoding="utf-8")
        if PLACEHOLDER not in html:
            continue
        m = re.search(r'<html[^>]*\blang="([^"]+)"', html)
        f.write_text(html.replace(PLACEHOLDER, stamp(m.group(1) if m else "en", today)),
                     encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
