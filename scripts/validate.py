#!/usr/bin/env python3
"""Check the YAML data in data/ before rendering or committing.

    python scripts/validate.py

Fails (exit 1) on schema errors; only warns about entries that are visible
but still flagged needs_review.
"""

from __future__ import annotations

import datetime
import re
import sys

from _common import (
    DOI_RE, LINK_KEYS, NEWS, PROJECTS, PUBLICATIONS, ROOT, STATUSES, TALKS, TYPES, load_yaml,
)

errors: list[str] = []
warnings: list[str] = []

URL_RE = re.compile(r"^https?://\S+$")
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
MONTH_RE = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")
NEWS_DATE_RE = re.compile(r"^\d{4}-(0[1-9]|1[0-2])(-(0[1-9]|[12]\d|3[01]))?$")
NEWS_KINDS = ("conference", "talk", "publication", "stay", "award", "policy", "other")


def err(where: str, msg: str) -> None:
    errors.append(f"{where}: {msg}")


def check_link(where: str, value: str) -> None:
    if value.startswith(("files/", "/files/")):
        if not (ROOT / value.lstrip("/")).is_file():
            err(where, f"local file '{value}' does not exist")
    elif not URL_RE.match(value):
        err(where, f"'{value}' is neither a files/… path nor an http(s) URL")


def load_list(path) -> list:
    if not path.exists():
        err(path.name, "file is missing")
        return []
    data = load_yaml(path)
    if data is None:
        return []
    if not isinstance(data, list):
        err(path.name, "top level must be a list of entries")
        return []
    return data


def check_ids(entries: list, fname: str) -> None:
    seen = set()
    for i, e in enumerate(entries):
        eid = e.get("id") if isinstance(e, dict) else None
        if not eid or not ID_RE.match(str(eid)):
            err(f"{fname}[{i}]", f"missing or malformed id {eid!r} (lowercase, digits, hyphens)")
        elif eid in seen:
            err(f"{fname}:{eid}", "duplicate id")
        seen.add(eid)


def check_publications() -> None:
    pubs = load_list(PUBLICATIONS)
    check_ids(pubs, PUBLICATIONS.name)
    for i, p in enumerate(pubs):
        where = f"publications.yml:{p.get('id', i) if isinstance(p, dict) else i}"
        if not isinstance(p, dict):
            err(where, "entry must be a mapping")
            continue

        for key in ("visible", "needs_review", "featured"):
            if not isinstance(p.get(key), bool):
                err(where, f"'{key}' must be true or false")
        if p.get("type") not in TYPES:
            err(where, f"type {p.get('type')!r} not in {TYPES}")
        if p.get("status") not in STATUSES:
            err(where, f"status {p.get('status')!r} not in {STATUSES}")
        if not str(p.get("title") or "").strip():
            err(where, "title is required")
        authors = p.get("authors")
        if not isinstance(authors, list) or not authors or not all(isinstance(a, str) for a in authors):
            err(where, "authors must be a non-empty list of names")
        if not isinstance(p.get("year"), int):
            err(where, "year must be a number, e.g. 2026")

        # Type-specific requirements
        if p.get("type") in ("article", "chapter") and p.get("status") in ("published", "forthcoming"):
            if not p.get("journal"):
                err(where, "published/forthcoming articles and chapters need 'journal'")
        if p.get("type") == "report" and not p.get("journal"):
            err(where, "reports need 'journal' (the institution or series)")
        if p.get("type") == "working_paper" and p.get("status") == "published":
            warnings.append(f"{where}: working_paper with status 'published' is not shown "
                            "(change type to article, or status to wip)")

        doi = str(p.get("doi") or "")
        if doi and not DOI_RE.match(doi):
            err(where, f"DOI '{doi}' is malformed (use the bare DOI, without https://doi.org/)")
        if p.get("url"):
            check_link(f"{where}.url", str(p["url"]))

        links = p.get("links") or {}
        if not isinstance(links, dict):
            err(where, "links must be a mapping, e.g. {pdf: files/x.pdf}")
            links = {}
        for key, value in links.items():
            if key not in LINK_KEYS:
                err(where, f"unknown link '{key}' (allowed: {', '.join(LINK_KEYS)})")
            elif value:
                check_link(f"{where}.links.{key}", str(value))

        cats = p.get("categories", [])
        if not isinstance(cats, list) or not all(isinstance(c, str) for c in cats):
            err(where, "categories must be a list of topic names")

        if p.get("visible") is True and p.get("needs_review") is True:
            warnings.append(f"{where}: visible but needs_review is still true")
        if p.get("featured") is True and p.get("visible") is not True:
            warnings.append(f"{where}: featured but not visible, so it will not appear")


def check_projects() -> None:
    projects = load_list(PROJECTS)
    check_ids(projects, PROJECTS.name)
    for p in projects:
        if not isinstance(p, dict):
            continue
        where = f"projects.yml:{p.get('id')}"
        for key in ("name", "summary_en"):
            if not p.get(key):
                err(where, f"'{key}' is required")
        if not isinstance(p.get("visible"), bool):
            err(where, "'visible' must be true or false")
        if not isinstance(p.get("start"), int):
            err(where, "'start' must be a year, e.g. 2021")
        if p.get("url"):
            check_link(f"{where}.url", str(p["url"]))


def check_talks() -> None:
    talks = load_list(TALKS)
    check_ids(talks, TALKS.name)
    for t in talks:
        if not isinstance(t, dict):
            continue
        where = f"talks.yml:{t.get('id')}"
        for key in ("event", "place", "title"):
            if not t.get(key):
                err(where, f"'{key}' is required")
        if not MONTH_RE.match(str(t.get("month", ""))):
            err(where, "'month' must look like 2026-06")
        if t.get("role") not in ("presenter", "discussant", "invited"):
            err(where, "'role' must be presenter, discussant or invited")
        if not isinstance(t.get("visible"), bool):
            err(where, "'visible' must be true or false")
        if not isinstance(t.get("coauthors", []), list):
            err(where, "'coauthors' must be a list of surnames")


def news_date(value) -> str:
    """YAML reads 2026-11-27 as a date and 2026-11 as text; accept both."""
    return value.isoformat() if isinstance(value, datetime.date) else str(value or "")


def check_news() -> None:
    news = load_list(NEWS)
    check_ids(news, NEWS.name)
    for n in news:
        if not isinstance(n, dict):
            continue
        where = f"news.yml:{n.get('id')}"
        start, end = news_date(n.get("start")), news_date(n.get("end"))
        if not NEWS_DATE_RE.match(start):
            err(where, "'start' must look like 2026-11-27 or 2026-11")
        if end and not NEWS_DATE_RE.match(end):
            err(where, "'end' must look like 2026-11-28 or 2026-11")
        elif end and end[:len(start)] < start[:len(end)]:
            err(where, "'end' is before 'start'")
        if n.get("kind") not in NEWS_KINDS:
            err(where, f"'kind' must be one of {', '.join(NEWS_KINDS)}")
        if not str(n.get("title_en") or "").strip():
            err(where, "'title_en' is required")
        if not isinstance(n.get("visible"), bool):
            err(where, "'visible' must be true or false")
        if n.get("url"):
            check_link(f"{where}.url", str(n["url"]))


def main() -> None:
    check_publications()
    check_projects()
    check_talks()
    check_news()
    for w in warnings:
        print(f"WARNING  {w}")
    for e in errors:
        print(f"ERROR    {e}")
    if errors:
        print(f"\n{len(errors)} error(s). Fix them before rendering.")
        sys.exit(1)
    print(f"OK: data is valid ({len(warnings)} warning(s)).")


if __name__ == "__main__":
    main()
