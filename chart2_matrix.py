"""Chart 2 - Level x Momentum 2x2 scatter for the Winter Datathon notebook.

Each of the 9 core indicators is one marker:
  X = Australia's percentile among OECD peers at the uniform 2023 anchor (level).
  Y = ~10-year momentum = slope of AU's sign-flipped value, standardised per indicator
      and expressed per decade (see CAPTION for the exact comparability transform).

Markers are coloured/shaped by role (objective vs lived) and sized by panel size n.
Quadrant lines at x=50 (peer median) and y=0 (flat trajectory) split the plane into
"High & rising", "High & falling", "Low & rising", "Low & falling".

Contract notes honoured:
- `value_flipped` from analysis_helpers is ALREADY sign-flipped (higher = better) - never negated again.
- negative_affect & lack_of_support are 3-year POOLED Gallup (6 real points) -> slope is taken
  over `pool_idx` (0..5), never annual year, then rescaled to per-decade.
- No complete-case requirement; each indicator ranked on its own panel; n shown per point.
- life_satisfaction & gdp_per_capita_wb are excluded callouts (only the 9 CORE_HANDLES are used).
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from analysis_helpers import (
    load, au_percentile, au_series, ANCHOR, CORE_HANDLES, LABELS, POOLED_HANDLES,
)

TITLE = ("Objective prosperity clusters high-and-rising; lived well-being clusters low - "
         "and Australia's felt-experience measures are still falling")

CAPTION = (
    "Source: OECD How's Life? Well-being Database (status-A observations only), values sign-flipped "
    "so higher = better; Australia benchmarked against up to 46 OECD peers. "
    "LEVEL (x-axis) = Australia's percentile within each indicator's peer panel at the uniform 2023 "
    "anchor; panels vary by indicator (n = 24-47, printed per point and encoded as marker size), and "
    "each point is ranked on its own panel (no complete-case requirement). "
    "MOMENTUM (y-axis) = slope of Australia's sign-flipped value over ~2010-latest, expressed per decade. "
    "Because indicators carry different native units, each series is first standardised to its own history "
    "(z-scored) before the slope is taken, so the shared axis reads in 'standard deviations of the "
    "indicator's own history per decade' (0 = flat, up = improving). Annual indicators: OLS slope over "
    "year x10. Negative affect and lack of social support are 3-year pooled Gallup samples with only 6 real "
    "observations (2010, 2011, 2014, 2017, 2020, 2023); their slope is taken over the pool index (0-5), never "
    "annual year, and rescaled to per-decade via x(10/2.6) since consecutive pools sit ~2.6 years apart. "
    "Life satisfaction (2 AU points) and GDP per capita (no peer panel) are excluded callouts. "
    "Caveats: disposable income rests on the thinnest panel (n=24) and housing affordability is "
    "panel-sensitive; the raw per-decade slope in each indicator's native units is available in the hover."
)

# --- role -> visual encoding ---
_ROLE_COLOR = {"objective": "#1f6feb", "lived": "#e8590c"}
_ROLE_SYMBOL = {"objective": "circle", "lived": "diamond"}
_ROLE_LABEL = {"objective": "Objective (macro prosperity)", "lived": "Lived (felt well-being)"}

# 6 real pooled points span 2010->2023 in 5 steps => ~2.6 years per pool step.
_POOL_STEP_YEARS = (2023 - 2010) / 5.0

# per-point text placement (kept out of build so it is easy to tune without touching logic)
_TEXTPOS = {
    "disposable_income": "bottom center",
    "life_expectancy": "top center",
    "employment_rate": "middle right",
    "housing_affordability": "bottom center",
    "gender_wage_gap": "top center",
    "long_hours": "top center",
    "deaths_despair": "bottom center",
    "negative_affect": "top center",
    "lack_of_support": "middle right",
}


def _slope_per_decade(handle: str, s: pd.DataFrame) -> tuple[float, float]:
    """Return (native_slope_per_decade, standardised_slope_per_decade) for one AU series.

    Native slope uses the exact required call numpy.polyfit(x, value_flipped, 1)[0].
    The standardised (plotted) slope z-scores the series to its own history first so the
    momentum axis is comparable across indicators that carry different native units.
    Pooled handles regress on pool_idx (never year); the per-decade factor differs accordingly.
    """
    y = s["value_flipped"].astype(float).to_numpy()
    if handle in POOLED_HANDLES:
        x = s["pool_idx"].astype(float).to_numpy()
        decade = 10.0 / _POOL_STEP_YEARS  # per pool step -> per decade
    else:
        x = s["TIME_PERIOD"].astype(float).to_numpy()
        decade = 10.0  # per year -> per decade

    native_slope = np.polyfit(x, y, 1)[0]  # required call
    sd = y.std(ddof=0)
    yz = (y - y.mean()) / sd if sd > 0 else np.zeros_like(y)
    std_slope = np.polyfit(x, yz, 1)[0]
    return native_slope * decade, std_slope * decade


def _prepare() -> pd.DataFrame:
    """One row per core indicator: level percentile, momentum, role/domain, panel n, series span."""
    df = load()
    meta = df.groupby("handle")[["role", "domain"]].first()
    rows = []
    for h in CORE_HANDLES:
        pct, n = au_percentile(df, h, ANCHOR)
        s = au_series(df, h)
        native_dec, std_dec = _slope_per_decade(h, s)
        rows.append({
            "handle": h,
            "label": LABELS[h],
            "role": meta.loc[h, "role"],
            "domain": meta.loc[h, "domain"],
            "n": int(n),
            "level": pct,
            "momentum": std_dec,
            "native_slope_dec": native_dec,
            "npts": int(len(s)),
            "span": f"{int(s['TIME_PERIOD'].min())}-{int(s['TIME_PERIOD'].max())}",
            "pooled": h in POOLED_HANDLES,
        })
    return pd.DataFrame(rows)


def _marker_sizes(n: pd.Series) -> np.ndarray:
    """Map panel size n (24..47) to marker diameter 12..26 px (bigger panel = more robust)."""
    lo, hi = 24.0, 47.0
    frac = (n.astype(float).clip(lo, hi) - lo) / (hi - lo)
    return 12.0 + frac * 14.0


def build() -> go.Figure:
    data = _prepare()
    data["size"] = _marker_sizes(data["n"])

    fig = go.Figure()

    # quadrant tints reinforce the diagonal story (top-right thriving vs bottom-left deteriorating)
    fig.add_shape(type="rect", x0=50, x1=100, y0=0, y1=3, layer="below",
                  fillcolor="rgba(16,150,80,0.05)", line=dict(width=0))
    fig.add_shape(type="rect", x0=0, x1=50, y0=-3, y1=0, layer="below",
                  fillcolor="rgba(220,40,40,0.05)", line=dict(width=0))

    # quadrant divider lines
    fig.add_vline(x=50, line=dict(color="#9aa0a6", width=1, dash="dash"))
    fig.add_hline(y=0, line=dict(color="#9aa0a6", width=1, dash="dash"))

    # one trace per role for a clean colour/shape legend
    for role in ("objective", "lived"):
        d = data[data["role"] == role]
        if d.empty:
            continue
        customdata = np.column_stack([
            d["n"].to_numpy(),
            np.round(d["native_slope_dec"].to_numpy(), 2),
            d["domain"].to_numpy(),
            d["npts"].to_numpy(),
            d["span"].to_numpy(),
            np.where(d["pooled"].to_numpy(), "pooled Gallup, slope over pool index", "annual, slope over year"),
        ])
        fig.add_trace(go.Scatter(
            x=d["level"], y=d["momentum"],
            mode="markers+text",
            name=_ROLE_LABEL[role],
            text=d["label"],
            textposition=[_TEXTPOS[h] for h in d["handle"]],
            textfont=dict(size=11, color="#3c4043"),
            marker=dict(
                size=d["size"], sizemode="diameter",
                color=_ROLE_COLOR[role], symbol=_ROLE_SYMBOL[role],
                line=dict(color="white", width=1.5), opacity=0.9,
            ),
            customdata=customdata,
            hovertemplate=(
                "<b>%{text}</b><br>"
                f"Role: {role}<br>"
                "Domain: %{customdata[2]}<br>"
                "Level: %{x:.1f}th percentile vs peers (n=%{customdata[0]})<br>"
                "Momentum: %{y:+.2f} SD/decade<br>"
                "Raw slope: %{customdata[1]} native units/decade<br>"
                "Series: %{customdata[3]} points, %{customdata[4]} (%{customdata[5]})"
                "<extra></extra>"
            ),
        ))

    # quadrant labels
    for x, y, txt in [
        (25, 2.7, "Low & rising"), (75, 2.7, "High & rising"),
        (25, -2.7, "Low & falling"), (75, -2.7, "High & falling"),
    ]:
        fig.add_annotation(x=x, y=y, text=txt, showarrow=False,
                           font=dict(size=13, color="#80868b"), opacity=0.9)

    # compact standalone source footnote (full detail lives in CAPTION)
    fig.add_annotation(
        xref="paper", yref="paper", x=0, y=-0.14, xanchor="left", showarrow=False,
        align="left", font=dict(size=10.5, color="#5f6368"),
        text=("Source: OECD How's Life?  |  Level = 2023 percentile vs OECD peers (n per point = marker size)  |  "
              "Momentum = per-decade slope, z-scored per indicator (SD of its own history), so a small absolute "
              "move in a low-variance series can read as 'rising'; subjective series are 3-year pooled Gallup (6 pts)."),
    )

    fig.update_layout(
        template="plotly_white",
        title=dict(
            text=(f"<b>{TITLE}</b><br>"
                  "<sup>Level (peer percentile, 2023) x Momentum (~decade trend) for Australia's 9 core well-being indicators</sup>"),
            x=0.01, xanchor="left", font=dict(size=17),
        ),
        xaxis=dict(
            title="Level  -  Australia's percentile among OECD peers, 2023  (higher = ranks better)",
            range=[0, 100], zeroline=False, ticksuffix="",
            tickvals=[0, 25, 50, 75, 100],
        ),
        yaxis=dict(
            title="Momentum  -  change per decade (SD of the indicator's own history; up = improving)",
            range=[-3, 3], zeroline=False,
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    title_text=""),
        margin=dict(l=80, r=40, t=95, b=95),
        width=980, height=680,
        hoverlabel=dict(bgcolor="white"),
    )
    return fig


if __name__ == "__main__":
    fig = build()
    assert fig.data, "chart2: figure has no data traces"

    data = _prepare()
    n_points = len(data)
    assert n_points == 9, f"chart2: expected 9 core points, got {n_points}"

    def _quad(r):
        hi = r["level"] >= 50
        rising = r["momentum"] >= 0
        return ("High & rising" if hi and rising else
                "High & falling" if hi and not rising else
                "Low & rising" if not hi and rising else
                "Low & falling")

    data["quad"] = data.apply(_quad, axis=1)
    counts = data["quad"].value_counts().to_dict()
    obj_side = data.loc[data.role == "objective", "quad"].tolist()
    summary = " | ".join(f"{q}: {counts.get(q, 0)}" for q in
                         ["High & rising", "High & falling", "Low & rising", "Low & falling"])
    print(f"chart2 OK | {n_points} points, {len(fig.data)} traces | {summary}")
    print(f"chart2 OK | objective indicators all in: {sorted(set(obj_side))} | "
          f"felt-experience trio (neg affect, deaths of despair, lack of support) -> "
          f"{data.loc[data.handle.isin(['negative_affect','deaths_despair','lack_of_support']),'quad'].unique().tolist()}")
