# matej612.github.io

Personal academic website of Matej Opatrny, built with [Quarto](https://quarto.org) and
published on GitHub Pages at <https://matejopatrny.cz> (repository `matej612.github.io`; the old
address redirects). English pages sit in the root and
Czech pages in `cs/`; the **CS / EN** button in the menu switches between the two.

## Everyday updates

| I want to… | Do this |
|---|---|
| add a paper that has a DOI | `python scripts/add_paper.py 10.xxxx/yyyy`, then in `data/publications.yml` check the new entry, add `categories` and `links`, and set `visible: true`, `needs_review: false` |
| add a paper without a DOI | copy the template block at the top of `data/publications.yml` and fill it in |
| see what is missing | `python scripts/sync_orcid.py` lists ORCID works not on the site (it changes nothing) |
| write a note | `python scripts/new_note.py "Title"`, write in the new `notes/…/index.qmd`, set `draft: false` |
| add a talk | add a block to `data/talks.yml` (template at the top) |
| add news (conference, new paper, research stay) | add a block to `data/news.yml`; the home page shows what is coming up and the six latest past items, `news.qmd` shows all |
| change a project | edit `data/projects.yml` (English and Czech text side by side) |
| update the CV | replace `files/cv.pdf` (keep the name) |
| link a PDF, data or slides | put the file in `files/papers/`, then e.g. `links: {pdf: files/papers/x.pdf, code: "https://github.com/…"}` |
| change text on a page | edit the `.qmd` file and its Czech twin in `cs/` |
| change the four numbers on the home page | `tiles` under the `stats` listing at the top of `index.qmd` and `cs/index.qmd` (the article count is computed) |
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

- `data/*.yml` is the single source of truth for publications, projects, talks and news.
  Pages turn it into HTML with the templates in `templates/`.
- Look and feel: `assets/styles/` (`base.scss` layout, `light.scss` / `dark.scss` colours).
- Every push to `main` runs two GitHub Actions. *Publish* renders the site to the `gh-pages`
  branch. *Checks* validates the data and tests every link, also once a week.

## Going live (one time)

1. On GitHub, create an empty public repository named `matej612.github.io`.
2. `git remote add origin https://github.com/matej612/matej612.github.io.git` and `git push -u origin main`.
3. `quarto publish gh-pages` (once, from this folder). With `--no-prompt` it needs an existing
   `gh-pages` branch: create an empty orphan branch and push it first.
4. In the repository settings: **Pages → Source: branch `gh-pages`**, tick **Enforce HTTPS**;
   **Actions → General → Workflow permissions: Read and write**.

## Custom domain

`matejopatrny.cz` is registered at WEDOS. The `CNAME` file in the root (copied into the site by
`resources` in `_quarto.yml`) tells GitHub Pages the domain. DNS at WEDOS: four `A` records for the
bare domain (185.199.108.153, .109.153, .110.153, .111.153), four `AAAA` records
(2606:50c0:8000::153 … 8003::153) and `www` CNAME `matej612.github.io`. In the repository settings:
Pages → Custom domain `matejopatrny.cz`, Enforce HTTPS. If the domain ever changes, update `CNAME`,
`site-url` in `_quarto.yml` and `site_url` in `_variables.yml` together.
