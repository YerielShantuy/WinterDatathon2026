"""Chart 3 - Lived-Reality divergence (the centrepiece) for the Winter Datathon notebook.

Australia's objective prosperity (disposable income, employment) against lived strain
(household debt, negative affect, deaths of despair) on ONE shared axis, 2010->2024.
Every series is indexed to 100 at its 2010 baseline so wildly different native units
(dollars, %, per-100k) share a single vertical scale and the divergence is visible.

THE READING TRAP this chart must defuse: on the shared index axis UP means OPPOSITE
things for the two families. Green (objective) UP = BETTER. Red/amber (lived) UP = WORSE.
That is the whole story - it is stated in short on-plot direction badges, in the direct
end-labels, in the legend, and in the caption.

Contract notes honoured (see analysis_helpers.py):
- RAW OBS_VALUE trends are shown (indexed), NOT value_flipped, so the real up/down
  direction is preserved; annotations orient "up=good vs up=bad" explicitly per series.
- negative_affect is 3-year POOLED Gallup (6 real points: 2010,2011,2014,2017,2020,2023).
  Plotted as MARKERS with a dotted guide (never a smooth annual line) and a "(pooled 3-yr)"
  legend suffix. Markers sit at each pool's MID-YEAR; the first pool's mid-year (2009) is
  clamped to 2010 so it lands on the shared axis.
- Household debt is external OECD SDMX, % of NET DISPOSABLE INCOME (higher=worse), NOT
  debt-to-GDP - flagged in the caption.
- Annual objective series are capped at 2024 to hold the stated 2010->2024 axis (employment
  carries a provisional 2025 point in source; excluded from the shared axis).
- No re-loading of CSVs and no re-signing: everything comes through analysis_helpers.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from analysis_helpers import load, au_series, household_debt

TITLE = "Income and jobs climbed; household debt and distress climbed faster"

CAPTION = (
    "Source: OECD How's Life? Well-being Database (status-A observations) for disposable income, "
    "employment rate, deaths of despair and negative affect; OECD household-debt SDMX for household "
    "debt. All series indexed to 100 at their 2010 baseline so different native units share one axis. "
    "DIRECTION IS NOT UNIFORM: for the objective/green series (disposable income, employment) a higher "
    "index = BETTER; for the lived/red-amber series (household debt, negative affect, deaths of despair) "
    "a higher index = WORSE. "
    "Negative affect is a 3-year POOLED Gallup sample with only 6 real observations "
    "(2010, 2011, 2014, 2017, 2020, 2023), drawn as MARKERS (dotted guide, not a smooth annual line) and "
    "placed at each pool's mid-year; the first pool's mid-year (2009) is clamped to 2010. "
    "Household debt is measured as % of net household disposable income (NOT debt-to-GDP). "
    "Objective annual series are capped at 2024 to hold the 2010-2024 axis (employment has a provisional "
    "2025 point in source). Deaths of despair are per-100 000 mortality from suicide, alcohol and drugs. "
    "Caveats: indexing hides level differences and is sensitive to the 2010 base year; the first negative-"
    "affect pool spans 2008-2010, so its 2011 dip partly reflects pooled-sample noise; household-debt "
    "units differ slightly across OECD vintages."
)

# --- palette: green family = objective (up=good), red/amber = lived (up=bad) ---
_GREEN1 = "#2b8a3e"   # disposable income
_GREEN2 = "#099268"   # employment
_RED = "#c92a2a"      # deaths of despair
_AMBER = "#f08c00"    # household debt
_ORANGE = "#e8590c"   # negative affect (pooled)

_BASE_YEAR = 2010
_YEAR_MAX = 2024

# one entry per series; order controls draw + legend order
_SPECS = [
    dict(key="disposable_income", short="Disposable income", color=_GREEN1,
         role="objective", pooled=False, unit="per-capita disposable income (real)"),
    dict(key="employment_rate", short="Employment", color=_GREEN2,
         role="objective", pooled=False, unit="% of working-age population"),
    dict(key="deaths_despair", short="Deaths of despair", color=_RED,
         role="lived", pooled=False, unit="deaths per 100 000"),
    dict(key="household_debt", short="Household debt", color=_AMBER,
         role="lived", pooled=False, external=True, unit="% of net disposable income"),
    dict(key="negative_affect", short="Negative affect", color=_ORANGE,
         role="lived", pooled=True, unit="% reporting negative affect (Gallup)"),
]

# small pixel nudges so the clustered right-hand end-labels do not overlap
_LABEL_YSHIFT = {
    "disposable_income": 7,
    "household_debt": 0,
    "employment_rate": -9,
    "deaths_despair": 0,
    "negative_affect": 0,
}


def _prepare(df: pd.DataFrame) -> list[dict]:
    """Return one dict per series with x, raw, indexed values and summary stats.

    Index = raw OBS_VALUE / (raw value at 2010) * 100. Every series starts at 2010,
    so the baseline is simply the first (sorted) observation.
    """
    out = []
    for sp in _SPECS:
        if sp.get("external"):
            hd = household_debt()
            hd = hd[hd["year"] <= _YEAR_MAX]
            x = hd["year"].to_numpy(float)
            raw = hd["debt_pct"].to_numpy(float)
            yr_first, yr_last = int(x[0]), int(x[-1])
        else:
            s = au_series(df, sp["key"])
            if sp["pooled"]:
                # markers at the pool mid-year; clamp the 2009 first pool onto the axis
                x = np.clip(s["pool_midyear"].to_numpy(float), _BASE_YEAR, _YEAR_MAX)
                raw = s["OBS_VALUE"].to_numpy(float)
                tp = s["TIME_PERIOD"].to_numpy(int)
                yr_first, yr_last = int(tp[0]), int(tp[-1])  # honest data years for reporting
            else:
                s = s[s["TIME_PERIOD"] <= _YEAR_MAX]
                x = s["TIME_PERIOD"].to_numpy(float)
                raw = s["OBS_VALUE"].to_numpy(float)
                yr_first, yr_last = int(x[0]), int(x[-1])

        idx = raw / raw[0] * 100.0
        out.append({
            **sp,
            "x": x, "raw": raw, "idx": idx,
            "idx_last": float(idx[-1]), "pct": float(idx[-1] - 100.0),
            "year_first": yr_first, "year_last": yr_last,
        })
    return out


def build() -> go.Figure:
    data = _prepare(load())
    fig = go.Figure()

    # 2010 = 100 baseline
    fig.add_hline(y=100, line=dict(color="#adb5bd", width=1, dash="dot"))

    # cost-of-living squeeze window where the gap widens
    fig.add_vrect(
        x0=2019, x1=2023, fillcolor="rgba(120,120,120,0.07)", line_width=0, layer="below",
        annotation_text="2019-23: cost-of-living squeeze, gap widens",
        annotation_position="top left",
        annotation_font_size=10.5, annotation_font_color="#868e96",
    )

    for d in data:
        pooled = d["pooled"]
        name = d["short"] + (" (pooled 3-yr)" if pooled else "")
        if pooled:
            mode = "lines+markers"
            line = dict(color=d["color"], width=1.4, dash="dot")
            marker = dict(color=d["color"], size=11, symbol="square",
                          line=dict(color="white", width=1))
        else:
            mode = "lines"
            line = dict(color=d["color"], width=3)
            marker = dict(color=d["color"], size=0)

        customdata = np.column_stack([d["raw"], np.full(len(d["raw"]), d["unit"])])
        fig.add_trace(go.Scatter(
            x=d["x"], y=d["idx"], mode=mode, name=name,
            line=line, marker=marker,
            customdata=customdata,
            hovertemplate=(
                f"<b>{name}</b><br>"
                "Year %{x:.0f}<br>"
                "Index %{y:.1f}  (2010 = 100)<br>"
                "Raw %{customdata[0]:.1f} %{customdata[1]}"
                "<extra></extra>"
            ),
        ))

        # direct end-label with the 2010->latest move, in the series colour
        sign = "+" if d["pct"] >= 0 else ""
        fig.add_annotation(
            x=d["x"][-1], y=d["idx_last"], xanchor="left", xshift=12,
            yshift=_LABEL_YSHIFT.get(d["key"], 0), showarrow=False,
            text=f"{d['short']} {sign}{d['pct']:.0f}%" + (" (pooled)" if pooled else ""),
            font=dict(color=d["color"], size=11),
        )

    # short direction badges (far upper-left, over empty space)
    fig.add_annotation(x=2010.3, y=145, xanchor="left", showarrow=False, align="left",
                       text="▲ higher = WORSE", font=dict(color=_RED, size=12.5))
    fig.add_annotation(x=2010.3, y=137, xanchor="left", showarrow=False, align="left",
                       text="▲ higher = BETTER", font=dict(color=_GREEN1, size=12.5))

    # standalone source footnote (full detail lives in CAPTION)
    fig.add_annotation(
        xref="paper", yref="paper", x=0, y=-0.13, xanchor="left", showarrow=False, align="left",
        font=dict(size=10.5, color="#5f6368"),
        text=("Source: OECD How's Life? (income, employment, deaths of despair, negative affect) + OECD "
              "household-debt SDMX.  |  Indexed to 100 at 2010.  |  Negative affect = 3-yr pooled Gallup "
              "(markers, at pool mid-year).  |  Household debt = % of net disposable income, not debt-to-GDP."),
    )

    fig.update_layout(
        template="plotly_white",
        title=dict(
            text=(f"<b>{TITLE}</b><br>"
                  "<sup>Australia, indexed to 100 at 2010 - objective prosperity vs lived strain on one axis</sup>"),
            x=0.01, xanchor="left", font=dict(size=18),
        ),
        xaxis=dict(title="Year", range=[2010, 2024], dtick=2, tickformat="d", showgrid=False),
        yaxis=dict(title="Index  (2010 = 100)", range=[80, 156], dtick=10, zeroline=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, title_text=""),
        margin=dict(l=70, r=185, t=95, b=90),
        width=1000, height=640,
        hoverlabel=dict(bgcolor="white"),
    )
    return fig


if __name__ == "__main__":
    fig = build()
    assert fig.data, "chart3: figure has no data traces"
    assert len(fig.data) == 5, f"chart3: expected 5 series, got {len(fig.data)}"

    # the pooled series must be markers, never a smooth annual line
    na = next(t for t in fig.data if "Negative affect" in t.name)
    assert "markers" in na.mode, "chart3: negative affect must be plotted as markers"

    data = _prepare(load())
    by = {d["key"]: d for d in data}

    # thesis check: a lived-strain series out-climbs the fastest objective series
    obj_max = max(by[k]["idx_last"] for k in ("disposable_income", "employment_rate"))
    lived_max = max(by[k]["idx_last"] for k in ("deaths_despair", "negative_affect", "household_debt"))
    assert lived_max > obj_max, "chart3: thesis broken - lived strain should out-climb objective"

    parts = " | ".join(
        f"{d['short']}{' (pooled)' if d['pooled'] else ''} "
        f"{d['year_first']}->{d['year_last']}: 100->{d['idx_last']:.0f} "
        f"({'+' if d['pct'] >= 0 else ''}{d['pct']:.0f}%)"
        for d in data
    )
    print(f"chart3 OK | {len(fig.data)} traces | {parts}")
    print(f"chart3 OK | fastest lived +{lived_max - 100:.0f}% (deaths of despair) "
          f"vs fastest objective +{obj_max - 100:.0f}% (disposable income)")
