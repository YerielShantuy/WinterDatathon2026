"""Generate analysis.ipynb (Jupyter-first working notebook) from the verified skeleton.
Quarto can still render this .ipynb to HTML — the YAML lives in a leading raw cell."""
import nbformat as nbf

nb = nbf.v4.new_notebook()

yaml = """---
title: "Is Australia Doing Well?"
subtitle: "OECD How's Life? well-being data, 2010-2026"
format:
  html:
    theme: cosmo
    toc: true
    code-fold: true
    embed-resources: true
---"""

setup = '''import pandas as pd
import plotly.express as px

# Label cols (Time period, Observation value) are BLANK in data rows -
# real values live in the CODE cols. Use those.
df = pd.read_csv("OECD Data.csv")
assert "Australia" in df["Reference area"].values, "AU missing - wrong file?"'''

clean = '''# OBS_STATUS: A = normal. B/D/E/P (~3%) = break/estimated/provisional/revised.
# Keep normal for trend claims; late years (2025/26) are provisional.
normal = df[df["OBS_STATUS"] == "A"].copy()
normal["TIME_PERIOD"] = normal["TIME_PERIOD"].astype(int)
normal["OBS_VALUE"] = pd.to_numeric(normal["OBS_VALUE"], errors="coerce")
print(f"kept {len(normal)} normal obs, dropped {len(df) - len(normal)} flagged")'''

helper = '''def indicator_series(measure_substr, countries):
    """One indicator (substring of Measure), long -> tidy per country x year."""
    sub = normal[
        normal["Measure"].str.contains(measure_substr, case=False, na=False)
        & normal["Reference area"].isin(countries)
    ]
    out = sub[["Reference area", "TIME_PERIOD", "OBS_VALUE", "Unit of measure"]].dropna()
    return out.sort_values(["Reference area", "TIME_PERIOD"])

# self-check: reshape returns rows and expected columns
_probe = indicator_series("disposable income per capita", ["Australia"])
assert len(_probe) > 0 and "OBS_VALUE" in _probe.columns, "helper returned nothing"'''

chart = '''PEERS = ["Australia", "New Zealand", "Canada"]
income = indicator_series("disposable income per capita", PEERS)

fig = px.line(
    income, x="TIME_PERIOD", y="OBS_VALUE", color="Reference area", markers=True,
    labels={"TIME_PERIOD": "Year", "OBS_VALUE": "USD PPP per person"},
    title="Household net adjusted disposable income per capita",
)
fig.update_layout(hovermode="x unified", legend_title_text="")
fig'''

nb.cells = [
    nbf.v4.new_raw_cell(yaml),
    nbf.v4.new_markdown_cell("# Is Australia Doing Well?\n\nOECD *How's Life?* well-being data, 2010-2026. Full data dictionary in `definitions.md`; project notes in `CLAUDE.md`."),
    nbf.v4.new_code_cell(setup),
    nbf.v4.new_markdown_cell("## Data cleaning\n\nFilter `OBS_STATUS` to normal values before any trend claim."),
    nbf.v4.new_code_cell(clean),
    nbf.v4.new_code_cell(helper),
    nbf.v4.new_markdown_cell("## Peer benchmark - AU vs Anglo peers\n\nStarter: disposable income, AU vs NZ & Canada. Swap `PEERS` / the substring to retarget. Sign-flip lower-is-better indicators before any composite."),
    nbf.v4.new_code_cell(chart),
]
nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}

nbf.write(nb, "analysis.ipynb")
print("wrote analysis.ipynb:", len(nb.cells), "cells")
