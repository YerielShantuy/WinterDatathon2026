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

**Discarded (extractor mismatched value↔quote, unverified):** life satisfaction "7.9", financial stress "30%", mental health "38%". Do not cite unless re-verified against the primary PDF.
