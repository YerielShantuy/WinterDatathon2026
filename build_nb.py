"""Generate analysis.ipynb — the Winter Datathon report — from verified modules.

Assembles: intro -> data + cleaning + caveats -> headline table -> 4 charts
(each imported from its chartN_*.py module) -> critical assessment -> wider context.

Charts live in standalone modules (chart1_heatmap.py ... chart4_montecarlo.py) so they
stay independently testable; this file only stitches them into narrative cells.
Quarto renders the .ipynb to HTML via the YAML in the leading raw cell.

Run: python build_nb.py  ->  python -m jupyter nbconvert --to notebook --execute --inplace analysis.ipynb
"""
import nbformat as nbf

nb = nbf.v4.new_notebook()

yaml = """---
title: "Mind the Gap: Australia's Lived-Reality Paradox"
subtitle: "Is Australia doing well? OECD How's Life? well-being data, 2010-2024"
format:
  html:
    theme: cosmo
    toc: true
    toc-depth: 2
    code-fold: true
    embed-resources: true
---"""

intro = """# Mind the Gap: Australia's Lived-Reality Paradox

**Question:** *Has Australia truly progressed from 2010 to 2024, or is macro prosperity masking a widening gap between objective metrics and lived well-being?*

**Answer, in one number:** at 2023, Australia's mean percentile among OECD peers is **72.3 on objective indicators** (income, jobs, life expectancy) but only **38.4 on lived indicators** (housing stress, negative affect, social support, deaths of despair). The country looks excellent on what's *measured* and poor on what's *felt*.

Every finding below follows one rule: **claim -> evidence -> caveat.** No number appears without its limitation. Full schema and cleaning decisions are in `CLAUDE.md`; the analysis plan is in `nextsteps.md`; external-source provenance is in `external/citations.md`."""

setup = '''import analysis_helpers as H
import pandas as pd
import plotly.io as pio
pio.renderers.default = "notebook"  # embed plotly.js in outputs so static HTML export renders

df = H.load()                       # 47 countries, status-A only (B/D/E/P dropped)
assert "AUS" in df["REF_AREA"].values, "AU missing - wrong file?"
print(f"{df['REF_AREA'].nunique()} countries, {len(df)} status-A observations, "
      f"{df['handle'].nunique()} indicators, {df['TIME_PERIOD'].min()}-{df['TIME_PERIOD'].max()}")'''

cleaning_md = """## Data, cleaning, and the caveats that shape everything

The OECD *How's Life?* extract is one row per indicator x country x year. Cleaning decisions baked into `analysis_helpers.load()`:

- **Only `OBS_STATUS == 'A'`** (normal) rows are kept; break/estimated/provisional/revised are dropped before any trend claim.
- **`value_flipped`** is pre-signed so higher = better for every indicator (lower-is-better ones — long hours, negative affect, gender wage gap, lack of support, deaths of despair — are already negated). Never flip twice.
- **Negative affect and lack of social support are 3-year *pooled* Gallup samples**, not annual: only 6 real observations exist (2010, 2011, 2014, 2017, 2020, 2023). The raw OECD file repeated each value across its 3 years, faking 16 annual points. We collapsed them — this is a deliberate correction, and a limitation the charts state openly.
- **Cross-country comparisons use a uniform 2023 anchor.** Panels vary from 24 to 47 countries per indicator; n is printed on every comparison.
- **GDP per capita** (World Bank) and **life satisfaction** (AU has only 2019-20) are callouts, excluded from the composite."""

headline = '''# Headline: the objective/lived split, quantified
tbl = H.au_percentile_table(df)      # 9 core indicators, AU percentile @ 2023
obj  = tbl[tbl.role == "objective"]["au_percentile"].mean()
lived = tbl[tbl.role == "lived"]["au_percentile"].mean()
print(f"AU mean percentile @2023  ->  objective {obj:.1f}   lived {lived:.1f}   gap {obj-lived:.1f}")
tbl[["label", "role", "domain", "n", "au_percentile"]]'''

# per-chart: narrative markdown + a cell that imports the module and renders build()
charts = [
    ("chart1_heatmap", "1", "The macro illusion",
     "Grouped as objective vs lived, Australia's OECD percentile makes the split unmissable — the top block glows, the bottom block sinks."),
    ("chart2_matrix", "2", "Level x momentum",
     "Where each indicator stands now (percentile) against where it's heading (decade momentum). Objective indicators cluster high-and-rising; the felt-experience trio sits low-and-falling."),
    ("chart3_divergence", "3", "The divergence",
     "Indexed to 100 at 2010: income and jobs rise, but household debt and distress rise faster. This is the paradox in one picture."),
    ("chart4_montecarlo", "4", "How fragile is 'Australia is Nth'?",
     "The critical move: re-weight the nine indicators 1,000 ways and Australia's overall rank swings across a wide band. Any single ranking is a weighting choice, not a neutral fact."),
]

# each chart: heading -> import+render module -> render its CAPTION as markdown
chart_cells = []
for mod, num, heading, blurb in charts:
    chart_cells.append(nbf.v4.new_markdown_cell(f"# Chart {num} — {heading}\n\n{blurb}"))
    chart_cells.append(nbf.v4.new_code_cell(
        f"import {mod} as c{num}\n"
        f"print(c{num}.TITLE)\n"
        f"c{num}.build().show()"))
    chart_cells.append(nbf.v4.new_code_cell(
        f"from IPython.display import Markdown\n"
        f"Markdown(c{num}.CAPTION)"))

critical = """# Critical assessment

- **Sparse and pooled series.** The subjective backbone is 6 real observations, not a smooth trend; life satisfaction (2 AU points) and civic voice were cut rather than over-read. Chart 4 shows the ranking itself is weighting-dependent.
- **Uneven panels.** Cross-country percentiles rest on 24-47 countries depending on the indicator; emerging economies drop out of the income and housing panels, biasing the peer baseline richer. n is shown everywhere.
- **Unit and framework mixing.** Housing affordability = % of income left after housing (higher = better), with mixed cross-country conventions; GDP (constant 2010 USD) and disposable income (PPP USD) are different bases and never compared at level.
- **Corroboration, not proof.** HILDA published figures (housing stress 11.3% in 2018; loneliness 26.6% in 2020; financial stress 1-in-8 in 2023) and household debt near the top of the OECD point the same way, but each is caveated in `external/citations.md`."""

context = """# Wider context and conclusion

Australia's own national framework — Treasury/ABS **Measuring What Matters** (5 themes, 12 dimensions, 50 indicators) — tracks the same domains as OECD *How's Life?*, and the decoupling shown here is visible at the policy level too.

**Conclusion.** By the metrics that make headlines, Australia is doing well. By the metrics people live, it is middling and, on several, sliding. "Is Australia doing well?" has no single honest answer — and Chart 4 proves the number you quote depends on the weights you pick. The defensible statement is the gap itself: **prosperity up, lived experience flat-to-worse, and a ranking too fragile to trust on its own.**"""

nb.cells = [
    nbf.v4.new_raw_cell(yaml),
    nbf.v4.new_markdown_cell(intro),
    nbf.v4.new_markdown_cell(cleaning_md),
    nbf.v4.new_code_cell(setup),
    nbf.v4.new_markdown_cell("## The nine core indicators, ranked"),
    nbf.v4.new_code_cell(headline),
    *chart_cells,
    nbf.v4.new_markdown_cell(critical),
    nbf.v4.new_markdown_cell(context),
]
nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}

nbf.write(nb, "analysis.ipynb")
print("wrote analysis.ipynb:", len(nb.cells), "cells")
