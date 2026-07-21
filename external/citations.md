# External data — pulls & citations

Real sources only. Every figure below is quote-verified against its source; unverified
extractor output was discarded (brief forbids fabrication).

## 1. Household debt (OECD) — `household_debt_oecd.csv` ✅ full series

- **Indicator:** Household debt as % of net disposable income (OECD Financial dashboard, Households & NPISH).
- **Source:** OECD SDMX API — dataflow `OECD.SDD.NAD,DSD_FIN_DASH@DF_FIN_DASH_S1M`, key `A..LES1M_FD4.PT_B6N_S1M`, `startPeriod=2010`. Endpoint: `https://sdmx.oecd.org/public/rest/data/...` (Accept: `application/vnd.sdmx.data+csv`).
- **Coverage:** 34 countries; **Australia 2010–2024, 15 annual points** (no gaps).
- **AUS series (% of disposable income):** 2010≈191 → 2018≈217 (peak) → **2024≈210**. Peers far lower: NZ ≈122, Canada ≈182.
- **Use:** cost-of-living / housing wedge with a hard number — AU household debt near the top of the OECD while macro income rises. Direction ↓ (higher = worse) — sign-flip in any composite.

## 2. HILDA (Melbourne Institute) — published figures only ⚠️ point stats, not a time series

Microdata is gated (ADA Dataverse registration) — cannot pull the raw series before deadline. These are **published summary figures**, quote-verified; use as corroborating callouts, not a HILDA trend chart.

- **Housing stress:** highest in **2018 at 11.3%** of the population. (2024 HILDA Statistical Report)
- **Loneliness:** rose to **26.6% in 2020** (pandemic acceleration of an existing upward trend). (2024 HILDA Statistical Report)
- **Financial stress:** **1 in 8 people** reported ≥2 indicators of financial stress in **2023 — second-highest in ~20 years**. (Guardian, 19 Sep 2025, citing HILDA)

Sources:

- 2024 HILDA Statistical Report (PDF): `melbourneinstitute.unimelb.edu.au/__data/assets/pdf_file/0003/5229912/2024-HILDA-Statistical-Report.pdf`
- Guardian summary: `theguardian.com/australia-news/2025/sep/19/the-unique-hilda-survey-reveals-key-insights-into-australians-lives-here-are-five-things-we-learned`

## 3. Measuring What Matters (Treasury/ABS) — framework benchmark ✅ structure only

- **Framework:** 5 wellbeing themes — Healthy · Secure · Sustainable · Cohesive · Prosperous — with 12 dimensions and 50 key indicators. Dashboard maintained by ABS (2025 update).
- **Use:** wider-context benchmark — show AU's own national framework tracks the same domains as OECD, corroborating the decoupling story at a policy level. **No indicator-count trend claim** (source states no clean improving/deteriorating tally — do not invent one).
- **Sources:** `treasury.gov.au/policy-topics/measuring-what-matters`, `abs.gov.au/statistics/measuring-what-matters`.

## 4. GDP per capita — NOT pulled ❌

World Bank API (`NY.GDP.PCAP.KD`) was returning HTTP 502 (outage) at pull time — no series obtained. **No `gdp_per_capita_wb.csv` exists.** Do NOT cite specific GDP-per-capita figures until pulled and verified. The macro anchor is OECD **disposable income** (in `OECD Data.csv`, AU 2010–2024) — sufficient, and better aligned with a thesis that critiques GDP. AU's 2023–24 "per-capita recession" (ABS National Accounts) may be added later as a *published callout*, with the ABS figure verified first.

**Discarded (extractor mismatched value↔quote, unverified):** life satisfaction "7.9", financial stress "30%", mental health "38%", plus any GDP-per-capita $ figure. Do not cite unless re-verified against the primary source.
