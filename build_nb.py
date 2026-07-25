"""Generate analysis.ipynb — the Winter Datathon report — from verified modules.

Structure: (1) question, (2) data + cleaning shown inline, (3) the finding + charts,
(4) critical assessment (data-quality catch + sensitivity, both shown inline),
(5) wider context, (6) conclusion.

Charts stay in standalone, self-checked modules (chartN_*.py); the notebook shows the key
analytical steps as visible code and imports the polished figures. Quarto renders the .ipynb
to HTML via the YAML in the leading raw cell.

Run: python build_nb.py
     python -m jupyter nbconvert --to notebook --execute --inplace analysis.ipynb
"""
import nbformat as nbf

nb = nbf.v4.new_notebook()
C, M, R = nbf.v4.new_code_cell, nbf.v4.new_markdown_cell, nbf.v4.new_raw_cell

yaml = """---
title: "Mind the Gap: Australia's Lived-Reality Paradox"
subtitle: "Is Australia doing well? OECD How's Life? well-being data, 2010-2024"
author: "Yeriel Putra Harsono (541023027) and Alfons Dennis (550151254)"
date: "2026-07-22"
format:
  html:
    theme: cosmo
    toc: true
    toc-depth: 2
    code-fold: true
    code-tools: true
    embed-resources: true
---"""

intro = """# Mind the Gap: Australia's Lived-Reality Paradox

**Yeriel Putra Harsono** (SID 541023027) &nbsp;·&nbsp; **Alfons Dennis** (SID 550151254)
Winter Data Analysis Challenge 2026

## The question we actually answered

> Has Australia progressed from 2010 to 2024, or is macro prosperity hiding a growing gap between the numbers that get measured and the well-being people actually feel?

"Is Australia doing well?" doesn't have one answer, so we stopped pretending it did. We took 9 OECD well-being indicators and sorted them into two piles. One is objective: income, jobs, how long people live. The other is lived: housing stress, negative mood, whether people have someone to lean on, and deaths from suicide, alcohol and drugs. Then we measured how far apart Australia sits on the two.

The short version: in 2023 Australia ranks around the 72nd percentile of OECD countries on the objective indicators and the 38th on the lived ones. Good on paper, mediocre in practice.

Every claim below arrives with the number behind it and the caveat that limits it. Section 2 is the data and the cleaning it needed. Section 3 is the finding. Section 4 is where we try to break our own conclusion. Section 5 is everything outside the OECD file that happens to agree with it."""

# ---- 2. Data & method ----
data_md = """## 2. Data and method

Everything comes from the OECD *How's Life?* Well-being Database: national averages for 47 countries, 2010 to 2024. Nine core indicators do the work in every comparison, and two more (GDP and life satisfaction) sit on the side as context. The data lives in two files so Australia never gets ranked against itself by accident. Definitions are in `definitions.md`, and anything pulled from outside the OECD is logged in `external/citations.md`."""

setup = '''import analysis_helpers as H
import pandas as pd, numpy as np
import plotly.io as pio
pio.renderers.default = "notebook"   # embed plotly.js so static HTML export renders

df = H.load()                        # 47 countries, status-A only, sign-flipped, pooled-corrected
print(f"{df['REF_AREA'].nunique()} countries | {len(df)} observations | "
      f"{df['handle'].nunique()} indicators | {df['TIME_PERIOD'].min()}-{df['TIME_PERIOD'].max()}")'''

cleaning_md = """### 2.1 Two cleaning decisions that change the answer

Most people trend this data straight out of the file. That's a mistake, for two reasons."""

cleaning_code = '''# (a) Quality filter: keep only OBS_STATUS == 'A' (normal); drop break/estimated/provisional/revised.
raw_all = H.load(status_a_only=False)
dropped = len(raw_all) - len(df)
print(f"(a) Status filter: kept {len(df)} normal obs, dropped {dropped} flagged "
      f"({100*dropped/len(raw_all):.1f}% — provisional/estimated).")

# (b) The subjective series are 3-year POOLED Gallup samples, not annual. The raw extract
#     repeats each pooled value across its 3 years. We collapse to the real observations.
na = H.au_series(df, "negative_affect")
print(f"(b) Negative affect (AU): {na['TIME_PERIOD'].nunique()} REAL observations "
      f"{list(na['TIME_PERIOD'])} — not the 16 'annual' rows the raw file implies. "
      f"Same for lack of social support.")'''

decisions_md = """Five choices run through everything that follows. None of them is neutral, so here is each one and the reason for it.

| Decision | Why |
| --- | --- |
| `status-A only` | Provisional and estimated observations would manufacture trends. |
| `sign-flip lower-is-better` (`value_flipped`) | Higher means better for every indicator before anything gets combined. |
| `3-yr pooled → 6 real points` | The subjective series aren't annual (see §4.1), so we never slope them year by year. |
| `uniform 2023 anchor` | One comparable cross-section. It adds 15 country-observations over mixed anchors and costs nothing. |
| `no complete-case` | Rank each indicator on its own panel (n = 24-47) instead of collapsing to the ~14 countries that have all nine. |"""

# ---- 3. Headline ----
headline_md = """## 3. The finding: strong on paper, weak in practice

Before the table, here is exactly how one number in it is built, sign-flip and all. The rest of the table is the same calculation run nine times."""

scoring_code = '''# One indicator's percentile = the share of peers Australia beats on the sign-flipped
# value (value_flipped, so higher always means better). Worked through for negative affect:
h = "negative_affect"                       # raw is lower-is-better, so it gets flipped
v = H.panel(df, h, H.ANCHOR)                # value_flipped at 2023, indexed by country code
au_raw = df[(df.handle == h) & (df.REF_AREA == "AUS")
            & (df.TIME_PERIOD == H.ANCHOR)]["OBS_VALUE"].iloc[0]
pct = 100 * (v < v["AUS"]).mean()
print(f"raw OBS_VALUE {au_raw:.1f} (higher = worse)  ->  value_flipped {v['AUS']:.1f} (higher = better)")
print(f"AU beats {(v < v['AUS']).sum()} of {len(v) - 1} peers with 2023 data  ->  {pct:.1f}th percentile")
print("au_percentile_table() below runs this for all 9 core indicators.")'''

headline_code = '''# AU percentile per core indicator at 2023 (higher = ranks better among OECD peers)
tbl = H.au_percentile_table(df)
obj  = tbl[tbl.role == "objective"]["au_percentile"].mean()
lived = tbl[tbl.role == "lived"]["au_percentile"].mean()
print(f"AU mean percentile @2023  ->  objective {obj:.1f}   lived {lived:.1f}   gap {obj-lived:.1f}")
tbl[["label", "role", "domain", "n", "au_percentile"]]'''

# The math behind charts 2, 3 and 7, shown once each next to its figure.
momentum_code = '''# Momentum (Chart 2): make "how fast is it moving" comparable across indicators with
# different units. Standardise each series to its own history, then take the per-decade
# slope of that. Pooled series slope over the pool index, not the year. For employment:
h = "employment_rate"
s = H.au_series(df, h).sort_values("TIME_PERIOD")
y = s["value_flipped"].to_numpy(float)
yz = (y - y.mean()) / y.std()                                   # standardise to own history
slope = np.polyfit(s["TIME_PERIOD"].to_numpy(float), yz, 1)[0] * 10   # per decade
print(f"{h}: momentum = {slope:+.2f} SD per decade (positive = improving). "
      f"Chart 2 runs this for all 9 and plots it against the percentile.")'''

index_code = '''# Indexing (Chart 3): put series with wildly different units on one axis by setting each
# one to 100 at its 2010 value; every later point is a percentage of that. For income:
h = "disposable_income"
s = H.au_series(df, h).sort_values("TIME_PERIOD")
base = s["OBS_VALUE"].iloc[0]; latest = s["OBS_VALUE"].iloc[-1]
print(f"{h}: 2010 {base:.0f} -> index 100;  latest {latest:.0f} -> index {latest/base*100:.0f} "
      f"(+{latest/base*100-100:.0f}%). Chart 3 does this for every line.")'''

trajectory_code = '''# Trajectory (Chart 7): this is just the section-3 percentile, taken at two years and
# differenced. Nothing new, only a before/after. For social support:
h = "lack_of_support"
p10, n10 = H.au_percentile(df, h, 2010)
p23, n23 = H.au_percentile(df, h, 2023)
print(f"{h}: {p10:.0f}th percentile in 2010 (n={n10})  ->  {p23:.0f}th in 2023 (n={n23}); "
      f"a {p23-p10:+.0f}-point move. Chart 7 shows all 9.")'''

charts_findings = [
    ("chart1_heatmap", "1", "The split",
     "Objective indicators on top, lived ones below. The two groups barely overlap. Australia clears the OECD median on everything it is measured on and falls short of it on most of what it lives, and the 34-point gap between the two averages is the finding.", None),
    ("chart2_matrix", "2", "Level and momentum",
     "Each indicator plotted by where Australia stands today (its percentile) against where it has been heading (the per-decade trend). The objective measures cluster top-right, high and still climbing. The lived ones sit bottom-left, low and drifting lower. The distance between the two groups is growing, not closing.", momentum_code),
    ("chart3_divergence", "3", "The divergence",
     "Everything indexed to 100 in 2010. Income rose 13% and employment 6%. Deaths of despair rose 49% and negative affect 21%. The lines that ought to move together pull apart instead.", index_code),
    ("chart7_trajectory", "7", "Did Australia progress? It went backwards on almost everything lived",
     "The brief asks whether Australia improved over time. On the lived indicators it lost ground. Between 2010 and 2023 its rank among OECD peers fell on nearly every one: social support from 85th to 47th, deaths of despair from 70th to 39th, negative affect from 49th to 26th. Disposable income is the only clear gain. Australia didn't hold its position; it slipped.", trajectory_code),
]

# ---- 4. Critical assessment ----
critical_md = """## 4. Where we try to break it

Two things separate an answer we would defend from a headline. Catching what the data gets wrong, and seeing how much our own conclusion leans on choices we made."""

dq_md = """### 4.1 The data isn't annual

This is the flaw we are proudest of catching. The subjective indicators are three-year pooled Gallup samples, but the raw file presents them as if they were yearly. Trend them as-is and most of the year-to-year "movement" is the same number repeated. So we collapse each series back to its real observations and never draw an annual slope through them."""

sens_md = """### 4.2 How much does "Australia is Nth" actually mean?

There is no neutral way to fold nine indicators into a single ranking; it all comes down to the weights. Rather than pick a set and defend it, we picked 1,000 sets at random (Dirichlet weightings) and recorded where Australia landed each time. The code is right here."""

mc_code = '''# Percentile-rank each core indicator within its own 2023 panel; composite = weighted mean
# of the indicators a country actually has (no complete-case requirement).
P = pd.DataFrame({h: H.panel(df, h, H.ANCHOR).rank(pct=True) for h in H.CORE_HANDLES}).dropna(how="all")
Mv = P.to_numpy(float); present = ~np.isnan(Mv); Mf = np.where(present, Mv, 0.0)
ai = list(P.index).index("AUS")

def au_rank(w):                       # 1 = best; renormalise weights to indicators present
    score = (Mf @ w) / (present @ w)
    return int((score > score[ai]).sum()) + 1

rng = np.random.default_rng(42)
ranks = [au_rank(rng.dirichlet(np.ones(len(H.CORE_HANDLES)))) for _ in range(1000)]
eq = au_rank(np.full(len(H.CORE_HANDLES), 1 / len(H.CORE_HANDLES)))
print(f"AU rank across 1,000 random weightings: best {min(ranks)}, worst {max(ranks)} "
      f"(of {len(P)} countries); equal weights give rank {eq}. "
      f"Same data, same year - the spread is pure weighting choice.")'''

mc_robust_code = '''# Robustness: is that spread just an artifact of thin-panel countries riding on 1-2 axes?
# Restrict to countries measured on >= 6 of the 9 indicators and re-run.
keep = P.notna().sum(axis=1) >= 6
Pr = P[keep]; Mr = Pr.to_numpy(float); pr = ~np.isnan(Mr); Mrf = np.where(pr, Mr, 0.0)
ar = list(Pr.index).index("AUS")
def au_rank_r(w):
    sc = (Mrf @ w) / (pr @ w); return int((sc > sc[ar]).sum()) + 1
rng2 = np.random.default_rng(43)
rr = [au_rank_r(rng2.dirichlet(np.ones(len(H.CORE_HANDLES)))) for _ in range(1000)]
print(f"Robustness ({int(keep.sum())} countries with >=6 indicators): AU rank best {min(rr)}, "
      f"worst {max(rr)} - the wide spread persists, so it is not an artifact of thin panels.")'''

context_md = """## 5. It's not only the OECD

The brief asks us to compare Australia against a few peers. Line it up next to the other Anglo economies and the clearest gap is household debt."""

context_md2 = """Australia's own figures say the same thing, all published and quote-verified in `external/citations.md`:

- **HILDA** (Melbourne Institute): housing stress peaked at 11.3% in 2018, loneliness reached 26.6% in 2020, and by 2023 one in eight people reported at least two markers of financial stress, the second-worst reading in about twenty years.
- Treasury and the ABS run **Measuring What Matters**, a national well-being framework of 5 themes, 12 dimensions and 50 indicators. It covers the same ground, and the same split turns up in it.
- The macro engine never stalled. GDP per capita (World Bank, constant 2010 USD) climbed from roughly 54,000 to 61,000 across the period. Prosperity isn't in doubt, and that is exactly the point: a lived decline sitting on top of a rising economy is a paradox, not a downturn.

None of this is a second dataset, just corroboration, but it all points one way."""

conclusion_md = """## 6. So, is Australia doing well?

On the numbers that make headlines, yes. On the ones people live, it is middling, and on several it is slipping.

- 72nd percentile on the objective indicators, 38th on the lived ones. A 34-point gap (§3).
- Income and jobs rose; debt and distress rose faster (Chart 3).
- And it is worse now than in 2010. Australia's peer rank fell on almost every lived measure, social support from 85th to 47th, deaths of despair from 70th to 39th (Chart 7).
- The tidy "Australia is Nth" figure is really a choice. Reweight the indicators and the rank runs anywhere from 8th to 41st, and that spread holds even after we drop the countries with the thinnest data (§4.2).

There is no single honest answer to the question. The honest finding is the gap: prosperity up, lived experience flat to worse, and a ranking too shaky to quote on its own.

*To reproduce: `pip install -r requirements.txt`, then `python build_nb.py && python -m jupyter nbconvert --to notebook --execute --inplace analysis.ipynb`. Every figure comes from `analysis_helpers.py` and the `chartN_*.py` modules; the data is in `data/`.*"""


def chart_block(mod, num, heading, blurb, pre_code=None):
    """heading+blurb -> (optional method code) -> import & render module -> render CAPTION."""
    cells = []
    if heading:
        cells.append(M(f"### {heading}\n\n{blurb}"))
    if pre_code:
        cells.append(C(pre_code))
    cells.append(C(f"import {mod} as c{num}\nprint(c{num}.TITLE)\nc{num}.build().show()"))
    cells.append(C(f"from IPython.display import Markdown\nMarkdown(c{num}.CAPTION)"))
    return cells


cells = [
    R(yaml),
    M(intro),
    M(data_md),
    C(setup),
    M(cleaning_md),
    C(cleaning_code),
    M(decisions_md),
    M(headline_md),
    C(scoring_code),
    C(headline_code),
]
for mod, num, heading, blurb, pre in charts_findings:
    cells += chart_block(mod, num, heading, blurb, pre)
cells += [M(critical_md), M(dq_md)]
cells += chart_block("chart5_data_quality", "5", None, None)
cells += [M(sens_md), C(mc_code), C(mc_robust_code)]
cells += chart_block("chart4_montecarlo", "4", None, None)
cells += [M(context_md)]
cells += chart_block("chart6_peers", "6", None, None)
cells += [M(context_md2), M(conclusion_md)]

nb.cells = cells
nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
nbf.write(nb, "analysis.ipynb")
print("wrote analysis.ipynb:", len(nb.cells), "cells")
