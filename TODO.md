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
- [ ] **CES conference, 27–28 Nov 2026**: which paper will you present? It is in News as "Paper
      accepted"; after the conference change that line to the title and add the talk to `data/talks.yml`.
- [ ] **Czech Economic Society membership**: since when? With a date it can also go into News.
- [ ] **News** (`data/news.yml`): check the selection. Conferences: only WCERE 2026, IEW 2025 and CES
      2026 (FSR Climate, EAERE, Mannheim, Tbilisi and the others stay in the CV list only).
- [ ] **Chile, January 2027** is shown as an upcoming research stay (News and CV), host from the
      M4G pre-confirmation letter (group of Prof. Juan-Pablo Montero).
- [ ] **Under-review papers** show the target journal ("Under review · Journal of …"). Keep the
      names, or show only "Under review" (empty the `journal` field)? Have co-authors agreed to
      the listing?
- [ ] **"How Much Measured Irrationality Is One Mistake?"**: year 2026 assumed; abstract?
- [ ] Abstracts are missing for the ERAE, JOES (optimal inflation), Energy Policy and IJF manuscripts.
- [ ] "Measured but not moved" is now listed as under review at *Energy Policy* (your message, 27 Oct
      2026, said "sent to Energy Policy"; the Oct 2026 list said Economic Policy, in preparation).

## Please confirm (drafted by Claude)

- [ ] **Home page redesign** (28 Oct 2026): the lede "Using the right methods to find out what the data
      really show" (CS "Správnými metodami zjistit, co v datech opravdu je"), the reworded bio (positive
      economist, methods first; climate and energy as one application) and the four numbers: articles (computed),
      4 continents of research stays (Chile, California, New Zealand, Spain), 2 ministries, 20 ha.
- [ ] **Sciencecon**: "Founder" (you wrote "hlavní zakladatel"; say if you prefer "Lead founder" or
      "Co-founder"), "2026–present" in the CV, the card text and the News item on Sciencecon #1
      (19 March 2026, Falcon, Klatovy; dates and talk title from sciencecon.cz).

- [ ] Bio (index.qmd) and its Czech translation (cs/index.qmd), including the second paragraph
      about the family farm ("from the other side of the fence") and family.
- [ ] "On the farm" photo section and captions (index.qmd, cs/index.qmd).
- [ ] Award wording: "Young Economist of the Year 2016, honourable mention (Czech Economic
      Society)" (cse.cz list of award winners: "ČU – Honorable Mention"; "bachelor's thesis" is from
      the ČNB vlog page). Shown on the home page, the CV page and as a Video link on CJEF 2017.
- [ ] Research interests (index.qmd, cs/index.qmd); "Meta-analysis and research synthesis" was added.
- [ ] Featured papers: JOLE, JEI, Empirical Economics, Resource and Energy Economics, Empirica (Brexit), CJEF 2017 (ČNB exchange-rate commitment) (`featured: true`).
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
