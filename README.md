# matej612.github.io

Personal academic website of Matej Opatrny, built with [Quarto](https://quarto.org) and
published on GitHub Pages at <https://matej612.github.io>. English pages sit in the root and
Czech pages in `cs/`; the **CS / EN** button in the menu switches between the two.

## Everyday updates

| I want to… | Do this |
|---|---|
| add a paper that has a DOI | `python scripts/add_paper.py 10.xxxx/yyyy`, then in `data/publications.yml` check the new entry, add `categories` and `links`, and set `visible: true`, `needs_review: false` |
| add a paper without a DOI | copy the template block at the top of `data/publications.yml` and fill it in |
| see what is missing | `python scripts/sync_orcid.py` lists ORCID works not on the site (it changes nothing) |
| write a note | `python scripts/new_note.py "Title"`, write in the new `notes/…/index.qmd`, set `draft: false` |
| add a talk | add a block to `data/talks.yml` (template at the top) |
| change a project | edit `data/projects.yml` (English and Czech text side by side) |
| update the CV | replace `files/cv.pdf` (keep the name) |
| link a PDF, data or slides | put the file in `files/papers/`, then e.g. `links: {pdf: files/papers/x.pdf, code: "https://github.com/…"}` |
| change text on a page | edit the `.qmd` file and its Czech twin in `cs/` |
| change name, email or IDs | `_variables.yml` (the email also sits in `assets/html/site-script.html`) |

Then check, preview and publish:

```sh
python scripts/validate.py    # checks the data files
quarto preview                # local preview at http://localhost:4321, refreshes as you edit
git add -A
git commit -m "Add …"
git push                      # GitHub renders and publishes in about two minutes
```

## Setup on a new computer

Install Quarto 1.10.19, Python 3 and git, then in this folder:

```sh
python -m venv .venv
.venv\Scripts\activate        # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

On Windows with Python 3.15, run `$env:PYYAML_FORCE_LIBYAML = "0"` before `pip install`.

## How it fits together

- `data/*.yml` is the single source of truth for publications, projects and talks.
  Pages turn it into HTML with the templates in `templates/`.
- Look and feel: `assets/styles/` (`base.scss` layout, `light.scss` / `dark.scss` colours).
- Every push to `main` runs two GitHub Actions. *Publish* renders the site to the `gh-pages`
  branch. *Checks* validates the data and tests every link, also once a week.

## Going live (one time)

1. On GitHub, create an empty public repository named `matej612.github.io`.
2. `git remote add origin https://github.com/matej612/matej612.github.io.git` and `git push -u origin main`.
3. `quarto publish gh-pages` (once, from this folder).
4. In the repository settings: **Pages → Source: branch `gh-pages`**, tick **Enforce HTTPS**;
   **Actions → General → Workflow permissions: Read and write**.
