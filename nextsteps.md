# Next steps — "Mind the Gap: Australia's Lived Reality Paradox"

Where the analysis is heading. Read alongside `CLAUDE.md` (schema, gotchas) and `definitions.md` (indicator wording).

## Refined question

> "Has Australia truly progressed from 2010 to 2024, or is macro prosperity masking a widening gap between objective metrics and lived well-being?"

## Verified indicator pairing (available data only)

Objective (rising) vs subjective/lived (decoupling). **Only indicators with usable AU coverage** — the original plan's GDP, overcrowding, and time-use pairs were cut (not in the dataset for AU). See `CLAUDE.md` coverage table.

| Domain | Objective (↑, strong AU coverage) | Lived counterpart (usable) | Story |
| --- | --- | --- | --- |
| Material | Disposable income per capita | Housing affordability (↑, % left after housing) | Income rises; housing eats it |
| Work | Employment rate | Long hours (↓) + gender wage gap (↓) | More jobs, persistent strain |
| Health | Life expectancy | Deaths of despair (↓) | Longer lives vs mental-health strain |
| Subjective | Disposable income (proxy for macro) | Negative affect balance (↓, strong →2025) | Affluence up, felt well-being flat/worse |
| Social | Employment / income | Lack of social support (↓, strong →2025) | Connected economy, thinner support |

**Subjective axis = Negative affect + Lack of social support + Housing affordability + Deaths of despair** — all full time series. Life satisfaction (2 pts) is NOT the backbone; bring it in only via HILDA, framed as corroboration.

## Chart plan (feasibility-checked)

1. **Macro Illusion — domain scorecard heatmap.** Normalised, 2010→2024. Objective indicators glow green → sets up the "looks great" illusion.
2. **Level × Momentum 2×2.** X = current OECD percentile (needs all 47 countries per indicator), Y = ~10-yr slope. **Only plot indicators with ≥ several years** — sparse ones (life sat, not-having-a-say) are annotated, not sloped.
3. **Lived-Reality divergence.** Dual-axis/gap plot: income & employment climbing vs housing affordability & negative affect worsening since ~2019.
4. **Fragility / sensitivity (the meta-move).** Monte Carlo, ~1,000 random weighting schemes → AU composite rank distribution. **The rank spread is a RESULT — compute it, never pre-state a range.** Restrict the composite to broad-coverage indicators; **sign-flip all ↓ indicators first.** Punchline: "rankings are political choices, not neutral facts."

## External data — see `external/citations.md` (verified-only; no ✅ without a file)

- **Household debt (OECD)** ✅ PULLED → `external/household_debt_oecd.csv`. AU full series **2010–2024, % of household disposable income: 190 → 217 (2018 peak) → 210**. Near top of OECD; peers far lower (NZ ~122, Canada ~182 — *those are peer values, not AU's range*). Metric is **% of disposable income, NOT debt-to-GDP** — don't conflate. Backbone of the cost-of-living/housing wedge. Direction ↓ (sign-flip).
- **HILDA** ⚠️ published figures only (microdata gated). 3 quote-verified callouts: housing stress 11.3% (2018), loneliness 26.6% (2020), financial stress 1-in-8 with ≥2 indicators (2023, 2nd-highest in ~20yr). Corroborating callouts, NOT a trend chart, NOT microdata.
- **Measuring What Matters** (Treasury/ABS) ✅ MAPPED (structure). 5 themes (Healthy/Secure/Sustainable/Cohesive/Prosperous) · 12 dimensions · 50 indicators (ABS 2025). Qualitative wider-context benchmark — AU's own framework tracks the same domains. **No improving/deteriorating count** (not stated in source; don't invent one).
- **GDP per capita** ❌ NOT pulled — World Bank API was down (HTTP 502) at pull time; no file, no figures. Macro anchor = **OECD disposable income** (already in `OECD Data.csv`, AU 2010–2024), which also fits a thesis that critiques GDP. Optional later: ABS "per-capita recession" as a *published callout*, figure verified first.

## Video arc (3 min)

I Trap (0:00–0:30): economist vs everyday-Australian framing. II Paradox (0:30–1:30): Level×Momentum matrix, cost-of-living wedge. III Critical (1:30–2:20): averages hide two Australias + sparse OECD subjective coverage + Monte Carlo fragility. IV Context (2:20–3:00): MWM framework, policy conclusion.

## Open TODOs

Data (done — verified, files exist):

- [x] Household debt (OECD SDMX) → `external/household_debt_oecd.csv`.
- [x] HILDA published callouts (3, quote-verified) → `external/citations.md`.
- [x] MWM framework structure mapped → `external/citations.md`.
- [ ] (optional) GDP per capita — retry World Bank when API is up, OR pull from OECD SDMX; only then cite figures.

Build (not started — the actual deliverable, deadline tomorrow):

- [ ] Wide table + normalisation helper (sign-flip ↓ indicators) on top of `indicator_series()`; merge `external/` series in.
- [ ] Chart 3 divergence (income vs household debt — verified data, do FIRST) → Chart 1 heatmap → Chart 2 matrix → Chart 4 Monte Carlo.
- [ ] Compulsory-voting + provisional-year + mixed-housing-units caveats into captions.
- [ ] Render notebook → HTML; record 3-min video.
