# TODO / CONFIRM

Open points from the initial build (27 Oct 2026). Pages mark them with `<!-- CONFIRM -->` comments.

## Questions for Matej

- [ ] **ORCID has a work that is not in your publication list**: "The role of conservative
      treatment in regional variations of 30-day acute myocardial infarction mortality: a case of
      the Czech Republic" (2025, DOI 10.21101/cejph.a8462). Add it? → `python scripts/add_paper.py 10.21101/cejph.a8462`
- [ ] **Brussels, February 2026**: the travel folder has only tickets and invoices. What was it,
      and should it appear on the site?
- [ ] **McKinsey & Company**: role and years (cv.qmd currently shows the name only).
- [ ] **MSc**: institution and year (cv.qmd, Education).
- [ ] **IES**: your position title and start year (cv.qmd shows "Current").
- [ ] **Role in MARCHES and in GAČR EXPRO FE3M** (`role_en` / `role_cs` in data/projects.yml).
- [ ] **Talks**: please check `data/talks.yml`. Open points:
  - Limassol 2023: the acceptance email says "…crop diversity" but the report says "…land use
    diversity". I used the accepted title.
  - Mannheim 2023: the preliminary programme lists Ščasný with a different title.
  - Bergen 2025 (EAERE): no presentation is documented. Did you present?
  - Brno, Nov 2026: will you present?
- [ ] **Chile, January 2027** is listed as a planned research stay. OK to show it before it happens?
- [ ] **Under-review papers** show the target journal ("Under review · Journal of …"). Keep the
      names, or show only "Under review" (empty the `journal` field)? Have co-authors agreed to
      the listing?
- [ ] **"How Much Measured Irrationality Is One Mistake?"**: year 2026 assumed; abstract?
- [ ] Abstracts are missing for the ERAE, JOES (optimal inflation), Energy Policy and IJF manuscripts.
- [ ] "Measured but not moved" is now listed as under review at *Energy Policy* (your message, 27 Oct
      2026, said "sent to Energy Policy"; the Oct 2026 list said Economic Policy, in preparation).

## Please confirm (drafted by Claude)

- [ ] Bio (index.qmd) and its Czech translation (cs/index.qmd), including the second paragraph
      about the family farm ("from the other side of the fence") and family.
- [ ] "On the farm" photo section and captions (index.qmd, cs/index.qmd).
- [ ] Award wording: "Mladý ekonom roku 2016 (Young Economist of the Year), award for the
      bachelor's thesis" (from the ČNB vlog page; organiser and placing are not stated there).
      Shown on the home page, the CV page and as a Video link on the CJEF 2017 article.
- [ ] Research interests (index.qmd, cs/index.qmd); "Meta-analysis and research synthesis" was added.
- [ ] Featured papers: JOLE, JEI, Empirical Economics, Resource and Energy Economics (`featured: true`).
- [ ] Topic categories and their Czech labels (data/publications.yml, cs/research.qmd).
- [ ] Project texts (data/projects.yml). The FE3M English text and the Czech SEEPIA work-package
      title are translations.
- [ ] Teaching text; Czech course name "Mikroekonomie I"; link to the course page, if public.
- [ ] CV page entries (cv.qmd, cs/cv.qmd), including "Invited expert" for the EC DG EMPL workshop.
- [ ] Czech page name "Mgr. Matej Opatrny, Ph.D." (English pages: "MSc, PhD").
- [ ] Abstracts were copied from Opatrny_2026_CV_OPJAK.pdf ("mju" written as μ, as in the
      published versions).
- [ ] The published CV (files/cv.pdf = Opatrny_2026_CV_OPJAK.pdf) shows date of birth, gender
      and nationality. Consider a web version without them.

## Data housekeeping

- [ ] Eight Crossref entries have `needs_review: true`. Check each one and set it to `false`.
      Years and status were already corrected against your publication list. JOLE is set
      `forthcoming`; Crossref's "article numbers" for JOLE and JOES 70116 were dropped.
- [ ] The CJEF 2017 article has no DOI; it links to the journal page.
- [ ] Add PDFs, data, code and slides links where you have them (`links:`).

## Going live

- [ ] Approve the local preview (`quarto preview`).
- [ ] Create the GitHub repository, push, run `quarto publish gh-pages` once, then set
      Pages → gh-pages, Enforce HTTPS, and workflow permissions to "Read and write" (see README).
- [ ] After the first deploy: check that the *Checks* workflow (link check) passes, and run Lighthouse.
