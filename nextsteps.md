# Next steps — "Mind the Gap: Australia's Lived Reality Paradox"

Where the analysis is heading. Read alongside `CLAUDE.md` (schema, gotchas) and `definitions.md` (indicator wording).

**Status 22 Jul 2026:** data is build-ready and verified. Remaining work is charts + notebook + video.

## Refined question

> "Has Australia truly progressed from 2010 to 2024, or is macro prosperity masking a widening gap between objective metrics and lived well-being?"

## Data files (use these — not the root CSVs)

| File | Rows | Contents |
| --- | --- | --- |
| `data/oecd_wellbeing_clean_AUS.csv` | 135 | Australia only, 11 handles |
| `data/oecd_wellbeing_clean_ROW.csv` | 4,954 | 46 peers, 10 handles (no GDP) |
| `data/country_coverage.csv` | 11 | Per-handle panel sizes + anchor-year guidance |

> Downloaded copies may carry `(1)`/`(2)` suffixes — rename to the clean names above before the notebook imports them.

Root `oecd_wellbeing_clean.csv` is **superseded** — it contains forward-filled subjective series (see below). Do not import it.

**Schema beyond the OECD columns:** `handle` (short indicator key) · `domain` · `role` (`objective`/`lived`) · `direction` (+1/−1) · `use` (`core`/`callout`) · `unit_type` (readable unit) · `value_flipped` (pre-signed — use this for any composite) · `pooled` + `pool_label` + `pool_midyear` + `pool_idx` (see below).

Verified clean: 0 duplicate (handle, country, year) rows · 0 nulls · `value_flipped` consistent on every row · AUS absent from ROW (46 + 1 = 47) · pool columns null on all unpooled rows.

## The pooled-series correction (biggest data finding)

**Negative affect** and **lack of social support** are Gallup World Poll, released by OECD as **3-year pooled samples** — not annual. The raw OECD extract repeated each pooled value across its 3 years, which made 6 real observations look like 16 annual ones (67% of "year-to-year change" was fake).

Both series are now collapsed to their **6 real points: 2010, 2011, 2014, 2017, 2020, 2023**, flagged `pooled=True`, with `pool_label` (`2008-10` … `2023-25`), `pool_midyear`, and `pool_idx` (0–5).

Consequences that bind the whole analysis:

- **The subjective axis is NOT a full time series.** Six points. Say so in the report — this is a critical-assessment win, not a weakness to hide.
- **No annual slope on these two.** Plot against `pool_idx` (even spacing) or `pool_midyear`, never raw year — raw year puts a 1-year gap between point 0 and 1 and 3-year gaps after.
- **`pool_midyear=2009` for the first pool sits outside the 2010–2025 window.** Honest (the pool really is 2008–10) but it renders left of every other series — clamp or caption.
- **Any anchor year after 2023 silently drops both indicators.** This drives the anchor decision below.

## Verified indicator set (11 handles)

`use=core` (9) — the composite and the Level×Momentum matrix:

| Domain | Objective (↑) | Lived counterpart | Story |
| --- | --- | --- | --- |
| Material | Disposable income per capita | Housing affordability (% left after housing) | Income rises; housing eats it |
| Work | Employment rate | Long hours (↓) + gender wage gap (↓) | More jobs, persistent strain |
| Health | Life expectancy | Deaths of despair (↓) | Longer lives vs mental-health strain |
| Subjective | — | Negative affect balance (↓, **pooled, 6 pts**) | Affluence up, felt well-being worse |
| Social | — | Lack of social support (↓, **pooled, 6 pts**) | Connected economy, thinner support |

`use=callout` (2) — context only, never in the composite or the matrix:

- **GDP per capita (World Bank, constant 2010 USD)** — AU 2010–2024, 15 pts, all status A. **Australia-only; no peer panel exists in this dataset**, so it has no percentile. Kept as callout because (a) no peers and (b) it correlates r = 0.84 with disposable income for AU — as `core` it would hand the macro axis two votes for one signal, inflating exactly the effect the thesis exposes. Unit is constant-2010-USD, *not* PPP — never compare its level against disposable income (`ppp_usd`); index both first.
- **Life satisfaction** — AU has only 2019–2020 (2 pts). Chart 2 must **skip it explicitly**, not let AU fall to NaN. Corroborate via HILDA instead.

**Cut:** `no_say` (not having a say in government) — 2 ragged years, no objective Civic pair survived, so the Civic domain was dropped entirely. Also absent for AU throughout: overcrowding, time-use indicators. GDP is not in the OECD *How's Life?* file at all (the framework critiques GDP by design).

## Anchor-year decision: use 2023 uniformly

`data/country_coverage.csv` recommends per-indicator anchors that mix 2023/2024/2025. **Override that — anchor everything at 2023.** It costs nothing and gains panel size:

| handle | coverage-file anchor | n | → 2023 n | gain |
| --- | --- | --- | --- | --- |
| housing_affordability | 2024 | 20 | **28** | +8 |
| employment_rate | 2025 | 42 | **46** | +4 |
| gender_wage_gap | 2024 | 31 | **33** | +2 |
| long_hours | 2025 | 40 | **41** | +1 |
| other 5 core | 2023 | — | unchanged | 0 |

4 of 9 improve, +15 country-observations, **zero regress**, and percentiles barely move. 2023 is also the only recent year in which the pooled subjective backbone exists at all.

Two rules that follow:

- **Do not require complete cases.** All 9 core handles present simultaneously gives only 14 countries at 2023 (and 0 at 2024, 0 at 2025). Rank each indicator on its own panel and **print n on every point**.
- `raw_latest_year` in the coverage file is a trap: housing_affordability 2025 has **1** country, disposable_income 2025 has 3, life_expectancy 2024 has 4. Never rank cross-sectionally on it.

## Headline result (computed, uniform 2023 anchor, sign-flipped so higher = better)

| handle | role | n | AU percentile |
| --- | --- | --- | --- |
| long_hours | lived | 41 | **17.1** |
| negative_affect | lived | 47 | **25.5** |
| deaths_despair | lived | 36 | **38.9** |
| lack_of_support | lived | 47 | **46.8** |
| gender_wage_gap | lived | 33 | **48.5** |
| housing_affordability | lived | 28 | **53.6** |
| employment_rate | objective | 46 | **58.7** |
| life_expectancy | objective | 43 | **79.1** |
| disposable_income | objective | 24 | **79.2** |

**Mean AU percentile: objective 72.3 · lived 38.4.** Near-total separation — every objective indicator outranks every lived one except the employment/housing overlap. This *is* the thesis, and it comes straight out of the data. It feeds Chart 1 and the headline number.

Caveats to carry with it: `disposable_income` n = 24 is the thinnest core panel; `housing_affordability` is panel-sensitive (AU percentile 62.2 on the 2018 n=37 panel vs 55.0 on the 2024 n=20 panel — the 2024 panel drops Germany, France, Netherlands, Norway, Switzerland, NZ and 11 others).

## Chart plan (feasibility-checked)

1. **Macro Illusion — domain scorecard heatmap.** Normalised, 2010→2024, from the percentile table above. Objective indicators glow green → sets up the "looks great" illusion.
2. **Level × Momentum 2×2.** X = AU percentile at the **uniform 2023 anchor** (annotate n per point), Y = ~10-yr slope on `value_flipped`. Pooled indicators get their slope from `pool_idx`, not year. Life satisfaction is skipped, not plotted.
3. **Lived-Reality divergence.** Income & employment climbing vs housing affordability, household debt, and negative affect worsening. Note the subjective line is 6 pooled points — step/marker style, not a smooth annual line.
4. **Fragility / sensitivity (the meta-move).** Monte Carlo, ~1,000 random weighting schemes over the 9 `core` handles → AU composite rank distribution. Use `value_flipped` (already signed). **The rank spread is a RESULT — compute it, never pre-state a range.** Punchline: "rankings are political choices, not neutral facts."

## External data — see `external/citations.md` (verified-only; no ✅ without a file)

- **Household debt (OECD)** ✅ PULLED → `external/household_debt_oecd.csv`. AU **2010–2024, % of household disposable income: 190 → 217 (2018 peak) → 210**. Near top of OECD; peers far lower (NZ ~122, Canada ~182 — *those are peer values, not AU's range*). Metric is **% of disposable income, NOT debt-to-GDP** — don't conflate. Backbone of the cost-of-living/housing wedge. Direction ↓ (sign-flip).
- **GDP per capita (World Bank)** ✅ PULLED → in `data/oecd_wellbeing_clean_AUS.csv` as `gdp_per_capita_wb`. AU 2010–2024, constant 2010 USD, 53,768 → 61,481, COVID dip 2020. **AU only — no peer panel.** Callout, not core (see above).
- **HILDA** ⚠️ published figures only (microdata gated). 3 quote-verified callouts: housing stress 11.3% (2018), loneliness 26.6% (2020), financial stress 1-in-8 with ≥2 indicators (2023, 2nd-highest in ~20yr). Corroborating callouts, NOT a trend chart, NOT microdata.
- **Measuring What Matters** (Treasury/ABS) ✅ MAPPED (structure). 5 themes (Healthy/Secure/Sustainable/Cohesive/Prosperous) · 12 dimensions · 50 indicators (ABS 2025). Qualitative wider-context benchmark — AU's own framework tracks the same domains. **No improving/deteriorating count** (not stated in source; don't invent one).

## Video arc (3 min)

I Trap (0:00–0:30): economist vs everyday-Australian framing. II Paradox (0:30–1:30): objective 72nd percentile vs lived 38th, Level×Momentum matrix, cost-of-living wedge. III Critical (1:30–2:20): averages hide two Australias + the pooled-series discovery (6 real points, not 16) + Monte Carlo fragility. IV Context (2:20–3:00): MWM framework, policy conclusion.

## Open TODOs

Data — **done, verified**:

- [x] Household debt (OECD SDMX) → `external/household_debt_oecd.csv`.
- [x] GDP per capita (World Bank) → `data/oecd_wellbeing_clean_AUS.csv`, AU-only, callout.
- [x] HILDA published callouts (3, quote-verified) → `external/citations.md`.
- [x] MWM framework structure mapped → `external/citations.md`.
- [x] Pooled-series correction + `use`/`unit_type`/`pool_*` columns + coverage table.

Build — **the actual deliverable, due 11:59PM tonight**:

- [ ] Rename the `(1)`/`(2)` data files; load AUS + ROW, concat, filter `OBS_STATUS=='A'`.
- [ ] Wide table + normalisation helper on `value_flipped` (already signed — do **not** flip twice); merge `external/household_debt_oecd.csv`.
- [ ] Chart 3 divergence (income vs household debt — verified data, do FIRST) → Chart 1 heatmap → Chart 2 matrix → Chart 4 Monte Carlo.
- [ ] Captions: per-point n, uniform-2023 anchor, pooled-series 6-point note, GDP unit mismatch, housing panel sensitivity, provisional-year flags.
- [ ] Render notebook → HTML; record 3-min video.

## Caveats that must appear in captions

- Subjective indicators are **3-year pooled Gallup samples, 6 real observations** — not annual.
- Percentile panels vary by indicator (n = 24 to 47); n is printed on every point.
- `disposable_income` (PPP USD) and `gdp_per_capita_wb` (constant 2010 USD) are **different bases** — indexed comparison only.
- Housing affordability = **% of income left after housing** (higher = better), and cross-country units are mixed (gross vs disposable, COICOP 1999 vs 2018).
- `country_coverage.csv` counts are **status-A only** — 3 handles have more countries if provisional/estimated rows are included (life_expectancy 45→47, housing 38→40, income 34→37).
