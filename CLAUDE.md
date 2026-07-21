# Winter Datathon 2026 — project instructions

## 1. Context & goals

USyd Winter Data Analysis Challenge (undergrad, teams ≤3). Open question: **"Is Australia doing well?"**

Working thesis — *"Mind the Gap: Australia's Lived Reality Paradox"*: macro prosperity (income, employment, life expectancy) is rising while lived/subjective well-being (housing stress, negative affect, social support) decouples. Refined question and full plan → `nextsteps.md`.

- **Deadline:** 11:59PM Wed 22 Jul 2026. Deliverables: (1) 3-min video + (2) reproducible report.
- **Judged on** (NOT single-metric accuracy): analytical innovation · clarity of communication · critical assessment & evaluation · demonstration of wider context. Optimise for a defensible, well-caveated story.
- **Prizes:** $1000 / $500 / $200. Sponsors: Westpac Institutional Bank, Canva.

## 2. Data — schema & base tables

**Base table:** `OECD Data.csv` — OECD *How's Life?* well-being DB. 8,806 rows × 30 cols. **Grain: one row per indicator × country × year** (long/tidy). 21 indicators · 10 domains · 47 countries · 2010–2026.

**Key columns** (each has a CODE + a LABEL twin; the LABEL twins `Time period`, `Observation value`, `Observation status` are BLANK in data rows — always read the CODE):

| Purpose | Use column | Note |
| --- | --- | --- |
| Country (join key) | `REF_AREA` (`AUS`) | label `Reference area` (`Australia`) |
| Indicator (join key) | `MEASURE` (`1_1`) | readable `Measure` (long name) |
| Year (join key) | `TIME_PERIOD` (int) | label twin is blank |
| Value | `OBS_VALUE` | numeric; coerce |
| Quality flag | `OBS_STATUS` | `A`=normal; `B/D/E/P`=break/estimated/provisional/revised |
| Domain / Unit | `Domain`, `Unit of measure` | populated (readable) |

`AGE`/`SEX`/`EDUCATION_LEV` are all `_T` (Total) — **no demographic breakdowns in this file.**

**Reshape:** pivot to wide with `index=[REF_AREA, TIME_PERIOD]`, `columns=MEASURE`, `values=OBS_VALUE`. **Join external data** on `Reference area` (or ISO) + `TIME_PERIOD`.

**Data dictionary:** `definitions.md` — all 84 dashboard indicators (Type · Source · Definition), 21 tagged `[IN CSV]`. Quote its wording for the critical-assessment criterion.

**External tables (allowed, cite real sources — no fabrication):** HILDA (AU life-satisfaction & financial-stress time series — use *published Statistical Report figures*, not microdata, before deadline); Treasury/ABS `Measuring What Matters` (national benchmark); World Bank/ABS for GDP (NOT in OECD data).

### 21 indicators — direction & Australia coverage (drives every modelling call)

`↑`=higher better, `↓`=lower better (sign-flip `↓` before any composite).

| Indicator | Domain | Dir | AU coverage |
| --- | --- | --- | --- |
| Disposable income per capita | Income | ↑ | strong →2024 |
| Median net wealth | Income | ↑ | **sparse (4 pts)** |
| Top quintile S80/S20 | Income | ↓ | **sparse (5 pts)** |
| Housing affordability (% left after housing) | Housing | ↑ | strong →2024 |
| Overcrowding | Housing | ↓ | **missing for AU** |
| Employment rate | Work | ↑ | strong →2025 |
| Long hours (≥50h/wk) | Work | ↓ | strong →2025 |
| Gender wage gap | Work | ↓ | strong →2024 |
| Life expectancy | Health | ↑ | strong →2023 |
| Deaths of despair (suicide/alcohol/drugs) | Health | ↓ | strong →2024 |
| Student maths (PISA) | Knowledge | ↑ | 4 pts, triennial |
| Air pollution (PM2.5) | Environment | ↓ | **ends 2020** |
| Extreme temperature | Environment | ↓ | →2024 |
| Life satisfaction | Subjective | ↑ | **ONLY 2019–20 (2 pts)** |
| Negative affect balance | Subjective | ↓ | strong →2025 |
| Time in social interactions | Social | ↑ | **missing for AU** |
| Lack of social support | Social | ↓ | strong →2025 |
| Time off (leisure) | Work-life | ↑ | **missing for AU** |
| Gender gap in working hours | Work-life | ↓ | **missing for AU** |
| Voter turnout | Civic | ↑ | election yrs (6 pts), compulsory |
| Not having a say in govt | Civic | ↓ | **2 pts (2021–23)** |

## 3. Common mistakes to avoid

- **Read CODE columns, not label twins** — `Time period`/`Observation value`/`Observation status` are blank in data rows.
- **Filter `OBS_STATUS=='A'`** before any trend claim; annotate `B/D/E/P`. Late years (2025/26) are provisional/partial.
- **Sign-flip `↓` indicators** (negative affect, long hours, gender gaps, lack of support, overcrowding, not-having-a-say, top-quintile) before normalising into any composite. Mixing directions = silently wrong index.
- **Don't build an AU headline on sparse series** — life satisfaction (2 pts), not-having-a-say (2 pts), wealth (4–5 pts). Patch with HILDA/MWM.
- **Don't assume an indicator exists for AU** — overcrowding, time-use (social interactions, time off, gender gap in hours) are missing. **GDP is not in the dataset at all** (How's Life critiques GDP; only appears as a denominator).
- **Housing affordability = % income LEFT AFTER housing** (higher=better), not the cost. Units mixed cross-country (gross vs disposable, COICOP 1999 vs 2018) → caveat.
- **Voter turnout:** AU has compulsory voting → structurally high, not peer-comparable without a note.
- **No slope from 2 points** — the 2×2 momentum axis needs ≥ several years; sparse indicators can't have a trajectory.

## 4. Structured output format

**Report = `analysis.ipynb`** (Jupyter-first). Section order: (1) refined question → (2) data + cleaning + caveats → (3) the divergence story, chart by chart → (4) critical assessment (dataset flaws + sensitivity) → (5) wider context + policy conclusion.

**Every finding** = *claim → evidence (chart/number) → caveat*. Never a number without its limitation.

**Every chart:**

- Title states the *finding*, not the variable ("Housing swallows income gains", not "Housing affordability over time").
- Caption carries source + the relevant caveat (provisional years, compulsory voting, sparse coverage).
- Note any sign-flip / normalisation in a code comment and the caption.
- Interactive = `plotly`; static/print = `matplotlib`/`seaborn`.

**Reproducibility:** generators (`build_nb.py`, `parse_dict.py`) stay in-repo; anyone can rebuild notebook + dictionary from source. Pin deps in `requirements.txt`.

## 5. Stack & file map

Python analysis + Jupyter report. NOT a webapp — the deliverable is a document. No Cloudflare/Supabase/DB/dashboard framework.

| Layer | Tool |
| --- | --- |
| Env / repro | `uv` (or `venv`) + `requirements.txt` |
| Wrangle | `pandas` |
| Charts | `plotly` (interactive) + `matplotlib`/`seaborn` (static) |
| Report | **Jupyter notebook** (`analysis.ipynb`), primary. Quarto optional → renders the same `.ipynb` to self-contained HTML (YAML in leading raw cell). |
| Video | OBS Studio, narrate over notebook / rendered HTML |

**Run:** `pip install -r requirements.txt` → `python -m jupyter lab` (the `jupyter` CLI may not be on PATH; `python -m jupyter …` always works). Headless execute: `python -m jupyter nbconvert --to notebook --execute --inplace analysis.ipynb`. Optional HTML: `quarto render analysis.ipynb`.

**Files:**

- `analysis.ipynb` — the report (primary deliverable). `build_nb.py` regenerates its skeleton.
- `definitions.md` — full data dictionary. `parse_dict.py` regenerates it.
- `nextsteps.md` — chosen concept, verified indicator pairing, chart plan, open TODOs. **Read for where the project is heading.**
- `external/` — pulled supplementary data + provenance. `household_debt_oecd.csv` (OECD SDMX, AU 2010–2024), `citations.md` (every external figure, quote-verified; no fabrication).
- `brief.md`, `OECD Data.csv`, `oecd-well-being-database-definitions.pdf` — source material (never edit).
- Full dataset background (indicator definitions, coverage, vetted sources) → `wiki/projects/winter-datathon.md`.
