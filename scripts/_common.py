"""Shared helpers for the scripts in this folder (paths, config, DOI and slug handling)."""

from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
PUBLICATIONS = DATA / "publications.yml"
PROJECTS = DATA / "projects.yml"
TALKS = DATA / "talks.yml"
NEWS = DATA / "news.yml"
VARIABLES = ROOT / "_variables.yml"

TYPES = ("article", "working_paper", "report", "chapter", "book")
STATUSES = ("published", "forthcoming", "rr", "under_review", "wip")
LINK_KEYS = ("pdf", "ssrn", "repec", "data", "code", "slides", "video", "media")

# Crossref's own recommendation for matching modern DOIs.
DOI_RE = re.compile(r"^10\.\d{4,9}/[-._;()/:A-Za-z0-9<>]+$")

# Windows consoles default to a legacy code page; make Czech names print correctly.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")


def die(message: str, code: int = 1) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(code)


def load_yaml(path: Path):
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_vars() -> dict:
    return load_yaml(VARIABLES) or {}


def load_publications() -> list[dict]:
    if not PUBLICATIONS.exists():
        return []
    return load_yaml(PUBLICATIONS) or []


def normalize_doi(raw: str) -> str:
    """Accept '10.x/y', 'doi:10.x/y' or a doi.org URL; return the bare DOI."""
    doi = raw.strip()
    doi = re.sub(r"^(https?://)?(dx\.)?doi\.org/", "", doi, flags=re.I)
    doi = re.sub(r"^doi:\s*", "", doi, flags=re.I)
    return doi


def slugify(text: str, max_words: int | None = None) -> str:
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    words = re.findall(r"[a-z0-9]+", ascii_text.lower())
    if max_words:
        words = words[:max_words]
    return "-".join(words)


def is_owner(author: str, owner_name: str) -> bool:
    """Match on the full name, so a co-author who shares the surname is kept."""
    return slugify(author) == slugify(owner_name)


def coauthors_display(authors: list[str], owner_name: str) -> str:
    """'with A, B and C' (owner removed); long lists are shortened."""
    others = [a for a in authors if not is_owner(a, owner_name)]
    if not others:
        return ""
    if len(others) > 4:
        return f"with {others[0]}, {others[1]} and {len(others) - 2} others"
    if len(others) == 1:
        return f"with {others[0]}"
    return f"with {', '.join(others[:-1])} and {others[-1]}"
