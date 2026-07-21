# Next steps — "Mind the Gap: Australia's Lived Reality Paradox"

Where the analysis is heading. Read alongside `CLAUDE.md` (schema, gotchas) and `definitions.md` (indicator wording).

## Refined question

> "Has Australia truly progressed from 2010 to 2024, or is macro prosperity masking a widening gap between objective metrics and lived well-being?"

## Verified indicator pairing (available data only)

Objective (rising) vs subjective/lived (decoupling). **Only indicators with usable AU coverage** — the original plan's GDP, overcrowding, and time-use pairs were cut (not in the dataset for AU). See `CLAUDE.md` coverage table.

| Domain | Objective (↑, strong AU coverage) | Lived counterpart (usable) | Story |
|---|---|---|---|
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
4. **Fragility / sensitivity (the meta-move).** Monte Carlo, ~1,000 random weighting schemes → AU composite rank distribution (e.g. 6th↔19th). Restrict the composite to broad-coverage indicators; **sign-flip all ↓ indicators first.** Punchline: "rankings are political choices, not neutral facts."

## External data — see `external/citations.md`

- **Household debt (OECD)** ✅ PULLED → `external/household_debt_oecd.csv`. AU full series 2010–2024, ~191%→210% of disposable income, near top of OECD (NZ ~122, Canada ~182). Hard-number backbone for the cost-of-living/housing wedge. Direction ↓ (sign-flip). Same SDMX route can pull the other survey extras (financial insecurity, trust) — verify AU coverage first.
- **HILDA** ⚠️ published figures only (microdata gated). 3 quote-verified callouts: housing stress 11.3% (2018), loneliness 26.6% (2020), financial stress 1-in-8 with ≥2 indicators (2023, 2nd-highest in ~20yr). Corroborating callouts, NOT a trend chart.
- **Measuring What Matters** (Treasury/ABS) — benchmark OECD findings against AU's own framework (wider-context criterion). Still to pull.
- **World Bank / ABS** — GDP per capita if the macro anchor needs it (GDP is not in the OECD dataset). Still to pull.

## Video arc (3 min)

I Trap (0:00–0:30): economist vs everyday-Australian framing. II Paradox (0:30–1:30): Level×Momentum matrix, cost-of-living wedge. III Critical (1:30–2:20): averages hide two Australias + sparse OECD subjective coverage + Monte Carlo fragility. IV Context (2:20–3:00): MWM framework, policy conclusion.

## Open TODOs

- [ ] Build wide table + normalisation helper (sign-flip ↓ indicators) on top of `indicator_series()`.
- [ ] Chart 1 heatmap → Chart 3 divergence → Chart 2 matrix → Chart 4 Monte Carlo.
- [ ] Pull HILDA + MWM published figures; cite.
- [ ] Compulsory-voting + provisional-year + mixed-housing-units caveats into captions.
- [ ] Render notebook → HTML; record 3-min video.
