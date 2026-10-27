#!/usr/bin/env python3
"""Create a new note (blog post) as a draft.

    python scripts/new_note.py "Title of the note"
    python scripts/new_note.py "Název poznámky" --lang cs

Creates notes/YYYY-MM-DD-slug/index.qmd. It stays out of the published site until
you change `draft: true` to `draft: false` (quarto preview shows drafts anyway).
"""

from __future__ import annotations

import argparse
import datetime as dt

from _common import ROOT, die, slugify

TEMPLATE = """---
title: "{title}"
date: {date}
description: ""          # one sentence, shown in listings and link previews
categories: []           # e.g. [Energy poverty, Policy]
lang: {lang}
draft: true              # set to false to publish
---

Write the note here. Markdown works, and so do R or Python code chunks; their
results are frozen (see `_freeze/`) so the site builds without R or Python packages.
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("title")
    parser.add_argument("--date", default=dt.date.today().isoformat(), help="YYYY-MM-DD (default: today)")
    parser.add_argument("--lang", default="en", choices=("en", "cs"), help="language of the note")
    args = parser.parse_args()

    try:
        dt.date.fromisoformat(args.date)
    except ValueError:
        die(f"--date must be YYYY-MM-DD, got '{args.date}'")
    slug = slugify(args.title, max_words=8)
    if not slug:
        die("the title must contain at least one letter or digit")

    folder = ROOT / "notes" / f"{args.date}-{slug}"
    if folder.exists():
        die(f"{folder.relative_to(ROOT)} already exists")
    folder.mkdir(parents=True)
    title = args.title.replace('"', '\\"')
    (folder / "index.qmd").write_text(
        TEMPLATE.format(title=title, date=args.date, lang=args.lang), encoding="utf-8", newline="\n")
    print(f"Created {(folder / 'index.qmd').relative_to(ROOT).as_posix()} (draft). "
          "Preview with: quarto preview")


if __name__ == "__main__":
    main()
