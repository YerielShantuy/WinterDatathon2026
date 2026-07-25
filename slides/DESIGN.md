# Slide Deck — Design Specification
### "Mind the Gap: Australia's Lived-Reality Paradox" · Winter Datathon 2026

A complete design system + per-slide blueprint for a **data-science / analyst** deck.
Aesthetic: **quiet, editorial, evidence-first.** Full but tidy — every slide earns its
whitespace, nothing floats. Think *Financial Times* / *Our World in Data* / a good
research-lab readout, not a startup pitch.

The four data charts are already rendered as transparent PNGs in `assets/`. This spec
covers the deck *chrome* (typography, color, layout, components) that frames them.

---

## 1. Canvas & grid

| Property | Value |
| --- | --- |
| Aspect ratio | **16:9** |
| Base resolution | **1920 × 1080** px |
| Outer margin (safe area) | 88 px all sides → 1744 × 904 content box |
| Column grid | **12 columns**, 24 px gutter |
| Baseline unit | **8 px** — all spacing is a multiple (8/16/24/32/48/64) |
| Slide count | **13** |

Never let content touch the outer 88 px margin except deliberate full-bleed chart slides.

---

## 2. Color palette

One neutral paper, one ink family, **two semantic accents** (`objective` vs `lived`)
that carry the entire thesis. The chart PNGs already use these exact hexes — the deck
must match so images sit seamlessly.

| Token | Hex | Use |
| --- | --- | --- |
| `paper` | `#F7F6F2` | Slide background (warm off-white) |
| `surface` | `#FFFFFF` | Cards, chart plates |
| `ink` | `#1C1E21` | Headlines, key numbers |
| `body` | `#33373D` | Body copy |
| `muted` | `#6B7280` | Eyebrows, captions, axis labels, footers |
| `hairline` | `#E3E0D8` | Borders, dividers, card edges |
| `objective` | `#2F6F8F` | Teal-blue — "measured / prosperity" (the good-on-paper axis) |
| `objective-lt`| `#6FA3BC` | Secondary objective series |
| `lived` | `#C1652F` | Burnt amber — "felt / lived strain" |
| `strain-deep`| `#9E2B25` | Deep red — strongest strain (deaths of despair, emphasis) |
| `tint-good` | `#EAF1F0` | Pale teal fill (positive band / good quadrant) |
| `tint-bad` | `#F6ECE4` | Pale amber fill (strain band / bad quadrant) |

**Rules**
- Accents are *semantic*, never decorative: teal = objective/measured, amber = lived/felt. Never swap.
- Max **one** accent dominant per slide's chrome; let the chart carry the rest.
- No gradients, no drop shadows heavier than `0 1px 2px rgba(0,0,0,0.04)`, no glassmorphism.
- Diverging red→green appears **only inside charts** where semantically required — never in deck chrome.

---

## 3. Typography

Two families. A neutral grotesque for everything, a mono for numerals/labels/eyebrows —
the mono is what signals "data" without shouting.

| Role | Font | Weight | Size (px @1080) | Tracking |
| --- | --- | --- | --- | --- |
| Eyebrow / kicker | **IBM Plex Mono** | 500 | 15 | +0.12em, UPPERCASE |
| Slide headline | **Inter** | 700 | 46–56 | −0.01em |
| Deck title (S1) | **Inter** | 800 | 76 | −0.02em |
| Subhead / lead | **Inter** | 500 | 24–28 | 0 |
| Body | **Inter** | 400 | 19–21 | 0, line-height 1.5 |
| Big stat number | **Inter** | 800 | 96–140 | −0.03em, tabular-nums |
| Stat label | **IBM Plex Mono** | 500 | 14 | +0.08em, UPPERCASE |
| Caption / source | **IBM Plex Mono** | 400 | 13 | 0 |

Fonts load from Google Fonts: `Inter` (400/500/700/800), `IBM Plex Mono` (400/500).
Always enable `font-feature-settings: "tnum" 1;` on numbers so figures align.

**Headline voice:** every slide headline states the *finding*, not the topic.
"High on what's measured, low on what's lived" — not "Percentile comparison".

---

## 4. Components

**Eyebrow** — mono, muted, uppercase, sits above every headline (`01 / THE SPLIT`).
Doubles as the slide number (`NN / SECTION`).

**Stat block** — big Inter-800 number in `ink` or an accent + mono uppercase label
beneath in `muted`. Used for the 72 vs 38 hook, HILDA figures, the 33-place swing.
Group related stats on a hairline-separated row.

**Chart plate** — the transparent chart PNG placed on `surface` (white) or straight on
`paper`. 24 px inner padding, optional 1px `hairline` border, radius 8px. Do **not**
add a title bar — the chart image already carries its finding-title and source line.

**Side rail** — a 3–4 col column beside a chart holding 2–3 takeaway bullets + one stat.
This is how slides stay *full but tidy*: chart on 8 cols, rail on 4.

**Caption/source** — mono 13px `muted`, bottom-left of any chart plate. The PNGs include
their own source line, so the deck caption is for *interpretation* ("Read: the two blocks
barely overlap"), not attribution.

**Footer** — thin hairline rule 40px from bottom; left: `Mind the Gap · Winter Datathon 2026`;
right: slide `NN / 13`. Mono 12px `muted`. Omit on the title slide.

**Divider / section tint** — section-opener or emphasis panels may fill a column band with
`tint-good` or `tint-bad` at ~6% — the same wash the charts use.

---

## 5. Layout patterns (pick per slide)

- **A — Statement**: centered or left, one headline + one lead + one stat. Title, question, conclusion.
- **B — Chart + rail**: chart plate 7–8 cols left, takeaway rail 4–5 cols right. Findings 1, 2, 4.
- **C — Chart hero**: chart near-full-bleed (10–11 cols), headline top-left overlaid on paper, one-line read beneath. Finding 3 (the divergence money-shot).
- **D — Grid of cards**: 2×2 or 1×3 stat/definition cards on a 12-col split. Method, corroboration.

Whitespace is intentional, not empty: fill with a rail, a stat, or a tint band — never stretch type to fill.

---

## 6. Per-slide blueprint

> Copy below is final — real numbers, verified. Headlines are the finding.
> Assets are the transparent PNGs in `assets/`.

### S1 · Title — *layout A*
- Eyebrow: `WINTER DATATHON 2026 · IS AUSTRALIA DOING WELL?`
- Title: **Mind the Gap**
- Subtitle: *Australia's Lived-Reality Paradox*
- Lead: "Macro prosperity is rising. Lived well-being is not. We measured the distance between them."
- Hook stat row (hairline-separated): **72** `OBJECTIVE PERCENTILE` · **38** `LIVED PERCENTILE` · **2010–2024` OECD HOW'S LIFE?`
- Footer/byline: **Yeriel Putra Harsono** (541023027) · **Alfons Dennis** (550151254) — Winter Data Analysis Challenge 2026.

### S2 · The question — *layout A / D*
- Eyebrow: `01 / THE QUESTION`
- Headline: **"Is Australia doing well?" depends on what you measure.**
- Two definition cards side by side:
  - **Objective** (teal): what gets *measured* — income, jobs, life expectancy.
  - **Lived** (amber): what gets *felt* — housing stress, negative affect, social support, deaths of despair.
- Lead under: "The same country can top one list and sit mid-table on the other. This deck is about that gap."

### S3 · Data & method — *layout D* (credibility slide — judges score this)
- Eyebrow: `02 / DATA & METHOD`
- Headline: **47 countries, 9 indicators, one honest cross-section.**
- Left: source facts — `OECD How's Life? Well-being Database` · `47 OECD countries` · `2010–2024` · `9 core + 2 callout indicators`.
- Right: method chips (small mono pills), each a defensible choice:
  - `STATUS-A ONLY` — drop provisional/estimated obs
  - `SIGN-FLIPPED` — higher = better for every indicator
  - `3-YR POOLED FIX` — subjective series are 6 real Gallup points, not 16 annual
  - `UNIFORM 2023 ANCHOR` — one comparable cross-section
  - `NO COMPLETE-CASE` — rank each indicator on its own panel (n = 24–47)
- Caption: "Every number below carries its n and its caveat."

### S4 · Finding 1 — the split — *layout B* — asset `assets/01_split.png`
- Eyebrow: `03 / THE SPLIT`
- Headline: **High on what's measured, low on what's lived.**
- Rail: • Objective mean **72** vs lived mean **38** — a 34-point gap. • Every objective indicator outranks every lived one. • Australia's worst rank: long working hours (17th pct).

### S5 · Finding 1 — grouped heatmap view — *layout C* — asset `assets/08_heatmap.png`
- Eyebrow: `03 / THE SPLIT` (same section as S4 — a second view, no new section number)
- Headline: **The same split, as a scorecard.**
- One-line read: "The nine indicators colour-graded by AU percentile — the objective block glows green, the lived block sinks red. The divide in a single glance." *(This is the classic heatmap; S4's lollipop is the ranked view of the identical finding — pair them or use whichever your narration prefers.)*

### S6 · Finding 2 — *layout B* — asset `assets/02_matrix.png`
- Eyebrow: `04 / LEVEL × MOMENTUM`
- Headline: **Prosperity sits high-and-rising; felt experience sits low-and-falling.**
- Rail: • Objective indicators cluster top-right (high & improving). • The felt-experience trio — negative affect, deaths of despair, lack of support — sits bottom-left. • The gap isn't closing; it's widening.

### S7 · Finding 3 — *layout C (hero)* — asset `assets/03_divergence.png`
- Eyebrow: `05 / THE DIVERGENCE`
- Headline: **Income and jobs climbed — debt and distress climbed faster.**
- One-line read: "Indexed to 2010: deaths of despair +49% and negative affect +21% outpace income +13% and employment +6%."

### S8 · Finding 4 — *layout B* — asset `assets/05_trajectory.png`  *(NEW — the temporal answer)*
- Eyebrow: `06 / DID AUSTRALIA PROGRESS?`
- Headline: **Australia didn't stand still — it slid on almost everything lived.**
- Rail: • Percentile among peers, 2010→2023: lack of social support **85th→47th**, deaths of despair **70th→39th**, negative affect **49th→26th**. • Only disposable income clearly rose. • The brief asks whether Australia *improved over time*. On lived well-being, it regressed.

### S9 · Critical assessment — the data-quality catch — *layout B/C* — asset `assets/07_dataquality.png`  *(NEW)*
- Eyebrow: `07 / WE CHECKED THE DATA FIRST`
- Headline: **The data isn't annual — 16 "yearly" points are really 6.**
- One-line read: "OECD's subjective series are 3-year pooled Gallup samples. ~64% of their apparent year-to-year 'change' was forward-fill. We corrected it before trending anything." (This is the critical-assessment lens — lead with it, it builds credibility.)

### S10 · Finding 5 — how fragile is the ranking? — *layout B* — asset `assets/04_fragility.png`
- Eyebrow: `08 / THE RANKING IS A CHOICE`
- Headline: **Australia's rank swings 33 places on weighting alone.**
- Rail: • 1,000 random weightings → rank ranges **8th to 41st**. • Equal weights give 21st — one choice among many. • The spread **survives dropping thin-panel countries** (still 6th–37th), so it's real, not an artifact. • Any single "Australia is Nth" headline is a weighting choice, not a neutral fact.

### S11 · Wider context — peers & national data — *layout B* — asset `assets/06_peers.png`  *(NEW peer chart)*
- Eyebrow: `09 / IT'S NOT JUST THE OECD`
- Headline: **Australians owe more than any Anglo peer — and it's not just debt.**
- Rail (stat cards under/beside the peer-debt chart): **~210%** `HOUSEHOLD DEBT / DISPOSABLE INCOME (vs UK 131%, NZ 122%, US 99%)` · **11.3%** `HOUSING STRESS, PEAK 2018 (HILDA)` · **26.6%** `LONELINESS, 2020 (HILDA)` · **1 in 8** `FINANCIAL STRESS, 2023 (HILDA)`.
- Note: "Treasury's *Measuring What Matters* framework tracks the same domains — the decoupling shows up in Australia's national accounts too."

### S12 · Conclusion — *layout A*
- Eyebrow: `10 / SO — IS AUSTRALIA DOING WELL?`
- Headline: **Prosperity up. Lived experience down. The ranking too fragile to trust alone.**
- Lead: "There is no single honest answer — and the number you quote depends on the weights you pick. The defensible finding is the gap itself, and that it has widened since 2010."
- Closing line (mono, muted): "Measure what people live, not just what's easy to count."

### S13 · Sources & reproducibility — *layout D*
- Eyebrow: `APPENDIX / SOURCES`
- Sources: OECD *How's Life?* Well-being Database · OECD household-debt SDMX · HILDA Statistical Report 2024 (published figures) · Treasury/ABS *Measuring What Matters* · World Bank GDP (constant 2010 USD, AU callout).
- Caveats: subjective series are 3-yr pooled Gallup (6 real points) · panels 24–47 countries · disposable-income panel thinnest (n=24) · housing affordability panel-sensitive.
- Repro line: `github.com/YerielShantuy/WinterDatathon2026 · analysis.ipynb reproduces every figure`.

---

## 7. Chart-asset rules

| File | Slide | Shows |
| --- | --- | --- |
| `assets/01_split.png` | S4 | Objective vs lived, ranked lollipop (the 72/38 split) |
| `assets/08_heatmap.png` | S5 | Same split as a colour-graded scorecard heatmap |
| `assets/02_matrix.png` | S6 | Level × momentum quadrants |
| `assets/03_divergence.png` | S7 | Indexed 2010→2024 divergence (hero) |
| `assets/05_trajectory.png` | S8 | Percentile slide 2010→2023 (the temporal answer) |
| `assets/07_dataquality.png` | S9 | The pooling catch (16 → 6 real points) |
| `assets/04_fragility.png` | S10 | Monte-Carlo rank spread |
| `assets/06_peers.png` | S11 | Household debt vs Anglo peers |

- **Transparent background** — they inherit `paper`/`surface`; do not add a colored box behind.
- **Never recolor, stretch, or crop** the type. Scale proportionally to fit the content column.
- They are self-contained (finding-title + source baked in) — don't duplicate the title in deck chrome; use the deck headline as the *section* framing and let the chart's own title read as the detailed finding.
- Regenerate with `python slides/make_slide_charts.py` (single source of truth = `analysis_helpers.py`).

---

## 8. Do / Don't

**Do** — left-align headlines · tabular numerals · generous line-height · one idea per slide ·
finding-first headlines · mono for anything data-flavored · consistent 88px margins.

**Don't** — center long text · use more than 2 type families · add icon clip-art · use pure
`#000`/`#FFF` (use `ink`/`paper`) · put a bright fill behind a transparent chart · stretch
type to fill space (add a rail or stat instead) · introduce a 3rd accent color.
