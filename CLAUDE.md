# Maintenance notes for Claude Code

Personal academic website of Matej Opatrny (Quarto website → GitHub Pages, user site
`matej612.github.io`). The owner is the only author; he reviews every change.

## Ground rules

1. **Never invent content.** No made-up publications, DOIs, co-authors, journals, pages, dates,
   URLs, IDs or affiliations. If a value is unknown, leave it empty and add it to `TODO.md`.
2. **Metadata comes from APIs, not memory**: Crossref for DOIs (`add_paper.py`), ORCID for the
   missing-works report (`sync_orcid.py`). Auto-filled entries get `needs_review: true`.
3. **Unpublished or under-review work stays `visible: false`** unless the owner confirms it.
4. Ask the owner before changing his bio, titles, affiliations or anything marked `CONFIRM`.
5. Commit in small steps with clear messages. Don't push or publish without the owner's approval.
6. When unsure about Quarto (listings, EJS templates, publishing), check quarto.org; don't guess.

## Where things live

- `data/publications.yml`, `data/projects.yml`, `data/talks.yml`: **single source of truth**,
  rendered by `templates/*.ejs.md` through Quarto listings. Pages never hard-code entries.
- `_variables.yml`: name, email, IDs and URLs. The email is also hard-coded (split) in
  `assets/html/site-script.html`; change both together.
- English pages in the root, Czech twins in `cs/` with **identical file names** (except
  `notes/index.qmd` ↔ `cs/notes.qmd`). `site-script.html` relies on this to translate the navbar
  and to build the CS/EN switch. Every content change goes into both languages.
- Topic chips come from `categories` in `publications.yml`. Each new category also needs a Czech
  label in `cs/research.qmd` (`template-params.labels`).
- In `talks.yml` the date field is `month` (YYYY-MM). Don't call it `date`: Quarto listings
  reformat fields named `date`.
- `scripts/build_stamp.py` runs after every render and writes "Last updated" into the footers.
- Notes: `notes/YYYY-MM-DD-slug/index.qmd`, created with `new_note.py`, `draft: true` until
  published. Code chunks are frozen (`_freeze/`, committed) so CI needs no R or Python packages.

## Commands

```sh
python scripts/add_paper.py 10.xxxx/yyyy   # Crossref → new entry (asks [y/N]; --yes for scripts)
python scripts/sync_orcid.py               # report ORCID DOIs missing from publications.yml
python scripts/new_note.py "Title"         # scaffold a draft note (--lang cs for Czech)
python scripts/validate.py                 # schema check; must pass
quarto render                              # must finish with zero warnings
quarto preview                             # local preview on port 4321
```

**Before every commit:** `python scripts/validate.py` and `quarto render` must both pass.

## Style

- **British spelling** on English pages (modelling, behaviour, programme); published titles
  and abstracts stay verbatim.
- Entries follow the Robert E. Hall format: **Title** (linked to the DOI) / "with co-authors" /
  *Journal*, Vol(Issue), pages / pills for DOI · PDF · Data · Code · Slides, then the abstract.
- Status labels: Forthcoming, Under review (journal shown only if `journal` is filled), Work in
  progress. In `coauthors_display` the owner is left out.
- Names: English pages "Matej Opatrny, MSc, PhD"; Czech pages "Mgr. Matej Opatrny, Ph.D.".
- One accent colour (teal); colours only via the `--c-*` tokens in `light.scss` / `dark.scss`.
  No new JavaScript frameworks, CMS or trackers.
