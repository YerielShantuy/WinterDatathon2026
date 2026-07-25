"""Chart 5 - Data-quality catch: the subjective series are NOT annual.

The single strongest critical-assessment finding, made visible. OECD delivers negative
affect & lack of social support as 3-year POOLED Gallup samples, but the raw extract
repeats each pooled value across its 3 years — dressing 6 real observations up as 16
"annual" points. Naively trended, that manufactures ~67% fake year-to-year movement.

This chart shows AU negative affect two ways on the same axis:
  - grey step line: the series "as delivered" (forward-filled, looks annual)
  - coloured markers: the 6 real Gallup observations (2010, 2011, 2014, 2017, 2020, 2023)

The forward-filled version is reconstructed from the 6 real points (each value fills its
pool's years) — faithful to the raw artifact, from the cleaned data alone.

value_flipped is not used here (we show raw OBS_VALUE, higher = worse). Nothing re-signed.
"""
from __future__ import annotations
import numpy as np
import plotly.graph_objects as go
from analysis_helpers import load, au_series

TITLE = "The data isn't annual: 16 'yearly' points are really 6"

CAPTION = (
    "Source: OECD How's Life? (Gallup World Poll). Australia's negative-affect series is a "
    "3-year POOLED sample: only 6 real observations exist (2010, 2011, 2014, 2017, 2020, 2023). "
    "The raw extract repeated each pooled value across its three years, so a naive annual trend "
    "would read ~67% of its year-to-year change as an artifact of forward-filling, not real "
    "change. We collapse both pooled series to their real observations and never slope them "
    "annually. The same correction applies to lack of social support. Higher = worse "
    "(share reporting more negative than positive feelings)."
)

_GREY = "#9aa0a6"
_ORANGE = "#C1652F"
_YEAR_MAX = 2025  # the 2023-25 pool legitimately covers through 2025 (matches the 16-row raw extract)


def _forward_filled(years, vals, year_max=_YEAR_MAX):
    """Reconstruct the 'as delivered' annual series: each real value fills its pool's years,
    i.e. from its own year up to (but not including) the next real observation's year."""
    ff_years, ff_vals = [], []
    for i, (yr, v) in enumerate(zip(years, vals)):
        end = years[i + 1] if i + 1 < len(years) else year_max + 1
        for y in range(int(yr), int(end)):
            if y <= year_max:
                ff_years.append(y); ff_vals.append(v)
    return ff_years, ff_vals


def build() -> go.Figure:
    s = au_series(load(), "negative_affect")
    years = s["TIME_PERIOD"].astype(int).tolist()
    vals = s["OBS_VALUE"].astype(float).tolist()
    ff_years, ff_vals = _forward_filled(years, vals)

    fig = go.Figure()
    # "as delivered" forward-filled step line (the misleading version)
    fig.add_trace(go.Scatter(
        x=ff_years, y=ff_vals, mode="lines", name="As delivered — forward-filled (looks annual)",
        line=dict(color=_GREY, width=2.4, shape="hv"),
        hovertemplate="%{x}: %{y:.1f}  (carried forward)<extra></extra>",
    ))
    # the 6 real observations
    fig.add_trace(go.Scatter(
        x=years, y=vals, mode="markers+text", name="Real Gallup observations (6)",
        marker=dict(color=_ORANGE, size=14, symbol="circle", line=dict(color="white", width=1.5)),
        text=[str(y) for y in years], textposition="top center", textfont=dict(size=11, color=_ORANGE),
        hovertemplate="<b>%{x}</b>: %{y:.1f}  (real 3-yr pooled sample)<extra></extra>",
    ))
    n_real, n_apparent = len(years), len(ff_years)
    fake = 1 - (n_real - 1) / (n_apparent - 1)
    fig.add_annotation(
        xref="paper", yref="paper", x=0.02, y=0.06, xanchor="left", showarrow=False,
        align="left", bgcolor="rgba(255,255,255,0.85)", bordercolor="#E3E0D8", borderwidth=1, borderpad=6,
        font=dict(size=12.5, color="#1C1E21"),
        text=(f"<b>{n_apparent} apparent annual points → {n_real} real observations.</b><br>"
              f"~{fake*100:.0f}% of year-to-year 'change' was forward-fill, not signal."),
    )
    fig.update_layout(
        template="plotly_white",
        title=dict(text=f"<b>{TITLE}</b><br><sup>Australia, negative affect — why we don't trend these series annually</sup>",
                   x=0.01, xanchor="left", font=dict(size=17)),
        xaxis=dict(title="Year", dtick=2, tickformat="d"),
        yaxis=dict(title="% reporting negative affect  (higher = worse)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, title_text=""),
        width=980, height=560, margin=dict(l=70, r=40, t=95, b=70),
        hoverlabel=dict(bgcolor="white"),
    )
    return fig


if __name__ == "__main__":
    s = au_series(load(), "negative_affect")
    years = s["TIME_PERIOD"].astype(int).tolist()
    assert len(years) == 6, f"expected 6 real points, got {len(years)}"
    ffy, ffv = _forward_filled(years, s["OBS_VALUE"].astype(float).tolist())
    fig = build()
    assert fig.data and len(fig.data) == 2, "chart5: expected 2 traces"
    fake = 1 - (len(years) - 1) / (len(ffy) - 1)
    print(f"chart5 OK | {len(ffy)} apparent -> {len(years)} real | ~{fake*100:.0f}% of transitions were forward-fill | "
          f"real years {years}")
