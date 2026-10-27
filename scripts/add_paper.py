#!/usr/bin/env python3
"""Add a publication to data/publications.yml from its DOI, via the Crossref REST API.

    python scripts/add_paper.py 10.1007/s10663-020-09481-7

The new entry is shown as a diff and written only after you answer "y".
It gets needs_review: true and visible: false. Topics (categories), links and
the abstract are left for you. Fields Crossref does not return stay empty,
and an unknown DOI stops the script; nothing is guessed.
"""

from __future__ import annotations

import argparse
import difflib
import html
import re
from urllib.parse import quote

import requests
import yaml

from _common import (
    DOI_RE, PUBLICATIONS, TYPES, STATUSES, coauthors_display, die,
    load_publications, load_vars, normalize_doi, slugify,
)

CROSSREF_TYPES = {
    "journal-article": "article",
    "book-chapter": "chapter",
    "book": "book",
    "monograph": "book",
    "edited-book": "book",
    "report": "report",
    "posted-content": "working_paper",
}

STOPWORDS = {"a", "an", "the", "of", "and", "in", "on", "for", "to", "with", "from", "by", "at", "as", "is"}


def fetch_crossref(doi: str, mailto: str) -> dict:
    url = f"https://api.crossref.org/works/{quote(doi, safe='/')}"
    try:
        r = requests.get(
            url,
            params={"mailto": mailto},
            headers={"User-Agent": f"add_paper.py (personal website; mailto:{mailto})"},
            timeout=30,
        )
    except requests.RequestException as exc:
        die(f"could not reach Crossref: {exc}")
    if r.status_code == 404:
        die(f"DOI not found in Crossref: {doi}")
    if r.status_code != 200:
        die(f"Crossref returned HTTP {r.status_code} for {doi}")
    return r.json()["message"]


def clean(text: str) -> str:
    """Strip JATS/HTML tags and entities that Crossref sometimes includes in titles."""
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def first(msg: dict, key: str) -> str:
    value = msg.get(key) or []
    return clean(value[0]) if value else ""


def year_of(msg: dict):
    for key in ("issued", "published", "published-online", "published-print"):
        parts = (msg.get(key) or {}).get("date-parts") or [[None]]
        if parts[0] and parts[0][0]:
            return int(parts[0][0])
    return None


def build_entry(msg: dict, doi: str, existing_ids: set[str], owner_name: str,
                type_override: str | None, status_override: str | None) -> dict:
    ctype = msg.get("type", "")
    entry_type = type_override or CROSSREF_TYPES.get(ctype)
    if not entry_type:
        die(f"Crossref type '{ctype}' has no mapping; rerun with --type {{{','.join(TYPES)}}}")

    authors = []
    for a in msg.get("author", []):
        if a.get("family"):
            authors.append(f"{a.get('given', '')} {a['family']}".strip())
        elif a.get("name"):
            authors.append(a["name"])
    if not authors:
        die("Crossref returned no authors for this DOI; add the entry by hand instead")

    title = first(msg, "title")
    if not title:
        die("Crossref returned no title for this DOI; add the entry by hand instead")
    year = year_of(msg)

    keywords = [w for w in slugify(title).split("-") if w not in STOPWORDS][:3]
    base = "-".join(p for p in (slugify(authors[0].split()[-1]), str(year or ""), *keywords) if p)
    entry_id, n = base, 2
    while entry_id in existing_ids:
        entry_id, n = f"{base}-{n}", n + 1

    return {
        "id": entry_id,
        "type": entry_type,
        "status": status_override or ("wip" if entry_type == "working_paper" else "published"),
        "visible": False,
        "needs_review": True,
        "featured": False,
        "title": title,
        "authors": authors,
        "coauthors_display": coauthors_display(authors, owner_name),
        "journal": first(msg, "container-title"),
        "year": year,
        "volume": msg.get("volume", ""),
        "issue": msg.get("issue", ""),
        "pages": msg.get("page", ""),
        "article_number": msg.get("article-number", ""),
        "doi": msg.get("DOI", doi).lower(),
        "abstract": "",
        "categories": [],
        "links": {},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("doi", help="DOI, doi: prefix or https://doi.org/ URL")
    parser.add_argument("--type", choices=TYPES, help="override the type inferred from Crossref")
    parser.add_argument("--status", choices=STATUSES, help="override the default status")
    parser.add_argument("--yes", action="store_true", help="write without asking (for scripted use)")
    args = parser.parse_args()

    doi = normalize_doi(args.doi)
    if not DOI_RE.match(doi):
        die(f"'{doi}' does not look like a DOI (expected 10.xxxx/...)")

    pubs = load_publications()
    if doi.lower() in {str(p.get("doi", "")).lower() for p in pubs}:
        die(f"{doi} is already in {PUBLICATIONS.name}")

    config = load_vars()
    mailto = config.get("crossref_mailto")
    if not mailto:
        die("set crossref_mailto in _variables.yml (Crossref asks for a contact address)")

    msg = fetch_crossref(doi, mailto)
    entry = build_entry(msg, doi, {p.get("id") for p in pubs}, config.get("name", ""),
                        args.type, args.status)

    block = yaml.safe_dump([entry], allow_unicode=True, sort_keys=False,
                           default_flow_style=None, width=100)
    old = PUBLICATIONS.read_text(encoding="utf-8") if PUBLICATIONS.exists() else ""
    new = old.rstrip("\n") + "\n\n" + block if old.strip() else block

    print("".join(difflib.unified_diff(old.splitlines(True), new.splitlines(True),
                                       "data/publications.yml", "data/publications.yml (new)")))
    if not args.yes:
        if input("Write this entry? [y/N] ").strip().lower() != "y":
            print("Nothing written.")
            return
    PUBLICATIONS.write_text(new, encoding="utf-8", newline="\n")
    print(f"Added '{entry['id']}' (visible: false, needs_review: true). "
          "Check it, add categories/links, then set visible: true and needs_review: false.")


if __name__ == "__main__":
    main()
