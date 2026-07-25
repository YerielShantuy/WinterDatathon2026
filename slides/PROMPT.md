# Claude Design — Deck-generation Prompt

Paste the block below into Claude (an Artifact-capable chat). **Attach the eight chart
PNGs** from `slides/assets/` (`01_split.png`, `08_heatmap.png`, `02_matrix.png`,
`03_divergence.png`, `05_trajectory.png`, `07_dataquality.png`, `04_fragility.png`,
`06_peers.png`) to the same message. `DESIGN.md` is the deeper reference — attach it too if
you want Claude to have the full spec, but the prompt below is self-contained.

---

> Build me a **16:9 presentation deck as a single self-contained HTML artifact** — a
> data-science / analyst readout for a university datathon. It must look **quiet,
> editorial, evidence-first** (think Financial Times or Our World in Data), **full but
> tidy** — every slide earns its whitespace, nothing floats or feels empty. No pitch-deck
> gloss, no gradients, no drop shadows, no icon clip-art.
>
> **Format**
> - 13 slides, each a 1920×1080 (16:9) section. Arrow-key / click navigation between
>   slides; also print-to-PDF friendly (each slide a page, `@media print { page-break }`).
> - Self-contained: inline all CSS. Embed the eight attached chart PNGs as base64 `data:`
>   URIs so nothing loads from the network. Load fonts from Google Fonts.
>
> **Type** — `Inter` (400/500/700/800) for everything; `IBM Plex Mono` (400/500) for
> eyebrows, stat labels, captions. Enable tabular numerals (`font-feature-settings:"tnum"`).
> Headlines Inter-700 ~52px, deck title Inter-800 ~76px, big stat numbers Inter-800
> 96–140px. Every headline states the *finding*, not the topic. Eyebrows are mono,
> uppercase, muted, and double as the slide number (`03 / THE SPLIT`).
>
> **Color** (exact — the charts already use these, so they sit seamlessly):
> - paper `#F7F6F2` (bg) · surface `#FFFFFF` · ink `#1C1E21` · body `#33373D` · muted `#6B7280` · hairline `#E3E0D8`
> - **objective (teal)** `#2F6F8F` and **lived (amber)** `#C1652F` are *semantic*: teal = what's measured, amber = what's felt. Never swap or add a third accent. Deep strain `#9E2B25` for emphasis only. Pale bands: `#EAF1F0` (good), `#F6ECE4` (strain).
> - No pure black/white. No gradients. Borders are 1px hairline; shadows at most `0 1px 2px rgba(0,0,0,.04)`.
>
> **Layout system** — 88px safe margin; 12-col grid, 8px spacing unit. Thin hairline footer
> (`Mind the Gap · Winter Datathon 2026` left, `NN / 12` right) on every slide except the
> title. Chart slides put the transparent PNG on a white/paper plate (24px pad, optional 1px
> hairline, 8px radius) — **do not** add a colored box behind a transparent chart, don't
> recolor or stretch it, and don't repeat the chart's baked-in title in the chrome. Keep
> slides full by pairing each chart with a 4-col **side rail** of 2–3 takeaways + one stat.
>
> **The 13 slides** (use this copy verbatim — numbers are verified):
>
> 1. **Title** — eyebrow `WINTER DATATHON 2026 · IS AUSTRALIA DOING WELL?`; title **Mind the Gap**; subtitle *Australia's Lived-Reality Paradox*; lead "Macro prosperity is rising. Lived well-being is not. We measured the distance between them."; hook stat row: **72** OBJECTIVE PERCENTILE · **38** LIVED PERCENTILE · **2010–2024** OECD HOW'S LIFE?. Footer/byline: "Yeriel Putra Harsono (541023027) · Alfons Dennis (550151254) — Winter Data Analysis Challenge 2026".
> 2. **The question** — eyebrow `01 / THE QUESTION`; headline **"Is Australia doing well?" depends on what you measure.**; two cards — **Objective** (teal): what gets measured — income, jobs, life expectancy; **Lived** (amber): what gets felt — housing stress, negative affect, social support, deaths of despair; lead "The same country can top one list and sit mid-table on the other."
> 3. **Data & method** — eyebrow `02 / DATA & METHOD`; headline **47 countries, 9 indicators, one honest cross-section.**; left facts: OECD How's Life? · 47 OECD countries · 2010–2024 · 9 core + 2 callout indicators; right method chips (mono pills): `STATUS-A ONLY`, `SIGN-FLIPPED (higher = better)`, `3-YR POOLED FIX`, `UNIFORM 2023 ANCHOR`, `NO COMPLETE-CASE (n = 24–47)`; caption "Every number carries its n and its caveat."
> 4. **Finding 1** — eyebrow `03 / THE SPLIT`; headline **High on what's measured, low on what's lived.**; chart = attached `01_split.png`; rail: Objective mean 72 vs lived mean 38 — a 34-point gap · every objective indicator outranks every lived one · worst rank: long working hours (17th pct).
> 5. **Finding 1 (grouped heatmap view)** — eyebrow `03 / THE SPLIT`; headline **The same split, as a scorecard.**; chart = `08_heatmap.png`; one-line read "The nine indicators colour-coded: the objective block glows green, the lived block sinks red — the divide in a single glance." (Same section as slide 4 — a second, colour-graded view of the finding.)
> 6. **Finding 2** — eyebrow `04 / LEVEL × MOMENTUM`; headline **Prosperity sits high-and-rising; felt experience sits low-and-falling.**; chart = `02_matrix.png`; rail: objective cluster top-right (high & improving) · felt-experience trio bottom-left · the gap is widening, not closing.
> 7. **Finding 3 (hero)** — eyebrow `05 / THE DIVERGENCE`; headline **Income and jobs climbed — debt and distress climbed faster.**; chart = `03_divergence.png` near-full-bleed; one-line read "Indexed to 2010: deaths of despair +49% and negative affect +21% outpace income +13% and employment +6%."
> 8. **Finding 4 — did Australia progress?** *(NEW)* — eyebrow `06 / DID AUSTRALIA PROGRESS?`; headline **Australia didn't stand still — it slid on almost everything lived.**; chart = `05_trajectory.png`; rail: percentile among peers 2010→2023 — lack of social support 85th→47th · deaths of despair 70th→39th · negative affect 49th→26th · only disposable income clearly rose. The brief asks whether Australia improved over time; on lived well-being it regressed.
> 9. **Critical assessment — the data-quality catch** *(NEW)* — eyebrow `07 / WE CHECKED THE DATA FIRST`; headline **The data isn't annual — 16 "yearly" points are really 6.**; chart = `07_dataquality.png`; one-line read "OECD's subjective series are 3-year pooled Gallup samples; ~67% of their apparent year-to-year change was forward-fill. We corrected it before trending anything." (Lead with this — it's the critical-assessment lens and it builds credibility.)
> 10. **Finding 5 — how fragile is the ranking?** — eyebrow `08 / THE RANKING IS A CHOICE`; headline **Australia's rank swings 33 places on weighting alone.**; chart = `04_fragility.png`; rail: 1,000 random weightings → 8th to 41st · equal weights give 21st (one choice among many) · the spread **survives dropping thin-panel countries** (still 6th–37th), so it's real, not an artifact · any single "Australia is Nth" headline is a weighting choice, not a neutral fact.
> 11. **Wider context — peers & national data** *(NEW peer chart)* — eyebrow `09 / IT'S NOT JUST THE OECD`; headline **Australians owe more than any Anglo peer — and it's not just debt.**; chart = `06_peers.png`; stat cards beside/under it: **~210%** HOUSEHOLD DEBT / DISPOSABLE INCOME (vs UK 131%, NZ 122%, US 99%) · **11.3%** HOUSING STRESS, PEAK 2018 (HILDA) · **26.6%** LONELINESS, 2020 (HILDA) · **1 in 8** FINANCIAL STRESS, 2023 (HILDA); note "Treasury's Measuring What Matters framework tracks the same domains."
> 12. **Conclusion** — eyebrow `10 / SO — IS AUSTRALIA DOING WELL?`; headline **Prosperity up. Lived experience down. The ranking too fragile to trust alone.**; lead "There is no single honest answer — the number you quote depends on the weights you pick. The defensible finding is the gap itself, and that it has widened since 2010."; closing mono line "Measure what people live, not just what's easy to count."
> 13. **Sources & reproducibility** — eyebrow `APPENDIX / SOURCES`; sources: OECD How's Life? · OECD household-debt SDMX · HILDA Statistical Report 2024 (published figures) · Treasury/ABS Measuring What Matters · World Bank GDP (AU callout); caveats: subjective series 3-yr pooled Gallup (6 real points) · panels 24–47 countries · disposable-income panel thinnest (n=24) · housing affordability panel-sensitive; repro `github.com/YerielShantuy/WinterDatathon2026 · analysis.ipynb reproduces every figure`.
>
> Ship one HTML file. Prioritize legibility from the back of a room: big headlines, high
> contrast, tabular numbers, generous line-height. Left-align headlines. One idea per slide.

---

## Notes

- **Editing charts later:** rerun `python slides/make_slide_charts.py` (from the project
  root) → new PNGs in `assets/`. Re-attach and ask Claude to swap them in. Every figure's
  numbers come from `analysis_helpers.py`, so they stay in lockstep with the notebook.
- **If Claude's artifact runtime blocks Google Fonts** (strict CSP): tell it to fall back
  to a system stack — `-apple-system, "Segoe UI", Helvetica, Arial, sans-serif` for Inter
  and `"SFMono-Regular", "Consolas", monospace` for the mono — the design still holds.
- **Want a native editable deck (PPTX / Adobe Express) instead of HTML?** Say so — the same
  `DESIGN.md` spec drives it; the four PNGs drop straight onto slides 4–7.
