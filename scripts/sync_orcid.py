#!/usr/bin/env python3
"""Report works on your public ORCID record whose DOI is missing from data/publications.yml.

    python scripts/sync_orcid.py

Report only: nothing is written. Add the ones you want with add_paper.py.
Uses the ORCID public API anonymously; if you register free public-API
credentials, put the access token in the ORCID_TOKEN environment variable
(never in the repository) and it will be sent as a bearer token.
"""

from __future__ import annotations

import os

import requests

from _common import die, load_publications, load_vars, normalize_doi


def orcid_works(orcid: str) -> list[dict]:
    headers = {"Accept": "application/json"}
    if os.environ.get("ORCID_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['ORCID_TOKEN']}"
    try:
        r = requests.get(f"https://pub.orcid.org/v3.0/{orcid}/works", headers=headers, timeout=30)
    except requests.RequestException as exc:
        die(f"could not reach ORCID: {exc}")
    if r.status_code != 200:
        die(f"ORCID returned HTTP {r.status_code} for {orcid}")

    works = []
    for group in r.json().get("group", []):
        summary = (group.get("work-summary") or [{}])[0]
        title = ((summary.get("title") or {}).get("title") or {}).get("value", "")
        year = ((summary.get("publication-date") or {}).get("year") or {}).get("value", "")
        dois = {normalize_doi(x["external-id-value"]).lower()
                for x in (group.get("external-ids") or {}).get("external-id", [])
                if x.get("external-id-type") == "doi" and x.get("external-id-value")}
        works.append({"title": title, "year": year, "dois": dois})
    return works


def main() -> None:
    orcid = load_vars().get("orcid")
    if not orcid:
        die("set 'orcid' in _variables.yml")

    known = {str(p.get("doi") or "").lower() for p in load_publications()} - {""}
    works = orcid_works(orcid)

    missing = [w for w in works if w["dois"] and not (w["dois"] & known)]
    no_doi = [w for w in works if not w["dois"]]

    print(f"ORCID {orcid}: {len(works)} works, {len(missing)} with a DOI not in publications.yml.\n")
    for w in missing:
        doi = sorted(w["dois"])[0]
        print(f"  {w['year'] or '----'}  {w['title']}\n        python scripts/add_paper.py {doi}")
    if no_doi:
        print(f"\n{len(no_doi)} ORCID work(s) have no DOI; check by hand whether they belong on the site:")
        for w in no_doi:
            print(f"  {w['year'] or '----'}  {w['title']}")


if __name__ == "__main__":
    main()
