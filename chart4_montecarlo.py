"""Chart 4 - Monte Carlo fragility of Australia's overall well-being rank.

The meta-move / critical-assessment chart for "Is Australia doing well?".

There is no neutral "Australia is Nth on well-being" number. Any single composite
ranking is a choice about how much each indicator counts. We make that choice
explicit and then *randomise it*: draw 1,000 random weightings of the 9 core
indicators and watch where Australia lands each time.

Method (all sourced from the shared analysis_helpers contract):
  1. Percentile matrix @ 2023: for each of the 9 CORE_HANDLES take its own peer
     panel (value_flipped, ALREADY sign-flipped so higher = better - never negated
     again here) and percentile-rank every country WITHIN that indicator's panel
     (pandas rank(pct=True), 0-1). Missing country x indicator -> NaN. Panels vary
     n = 24..47 and not every country has every indicator, so we do NOT require
     complete cases (that would leave ~14 countries). A country's composite is the
     weighted mean of the indicator-percentiles it actually HAS.
  2. 1,000 Dirichlet weight vectors w ~ Dir(1,...,1) over the 9 indicators. For each
     country the weights are renormalised to the indicators it has present, so a
     country is scored only on the axes it is measured on.
  3. Rank countries best->worst each scheme (1 = best) and record Australia's rank.
     Equal weights (w = 1/9 each) give the reference "headline" rank.

The distribution of Australia's rank is wide: the same country, same data, same year,
ranks anywhere across a large band depending only on the weighting. The single
headline number is a political choice, not a neutral fact.

Contract notes honoured:
- value_flipped is used as-is (higher = better); never re-signed.
- Only the 9 CORE_HANDLES; uniform 2023 anchor via panel(df, handle, 2023).
- No complete-case requirement; rank is taken among the countries present per scheme.
- Deterministic: SEED = 42. The rank spread is COMPUTED, never hardcoded.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from analysis_helpers import load, panel, ANCHOR, CORE_HANDLES

SEED = 42
N_SCHEMES = 1000


def _ordinal(n: int) -> str:
    """1 -> '1st', 8 -> '8th', 21 -> '21st', 41 -> '41st'."""
    n = int(n)
    if 10 <= n % 100 <= 20:
        suf = "th"
    else:
        suf = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suf}"


def _percentile_matrix() -> pd.DataFrame:
    """countries x 9 core indicators at 2023; each cell = percentile rank (0-1)
    WITHIN that indicator's own peer panel. NaN where a country lacks the indicator."""
    df = load()
    cols = {}
    for h in CORE_HANDLES:
        s = panel(df, h, ANCHOR)          # value_flipped, higher = better (already signed)
        cols[h] = s.rank(pct=True)        # 0-1 percentile within this indicator's panel
    # keep any country with >= 1 of the 9 indicators (positive Dirichlet weights => a
    # defined weighted mean whenever at least one indicator is present).
    return pd.DataFrame(cols).dropna(how="all")


def _montecarlo() -> dict:
    """Run the 1,000 random weightings and record Australia's rank each time.

    Returns a dict of everything the title, caption self-check and plot need, so the
    heavy work happens exactly once and stays deterministic (SEED)."""
    P = _percentile_matrix()
    countries = P.index.to_numpy()
    assert "AUS" in P.index, "Australia missing from the 2023 percentile matrix"
    au_i = int(np.where(countries == "AUS")[0][0])

    M = P.to_numpy(dtype=float)           # n_countries x 9, NaN = indicator absent
    present = ~np.isnan(M)                # boolean mask of available indicators
    M_filled = np.where(present, M, 0.0)  # NaNs contribute 0 to the numerator...

    def au_rank(w: np.ndarray) -> int:
        # weighted mean over PRESENT indicators only: renormalise weights per country
        # by dividing the weighted sum by the weight mass actually present.
        num = M_filled @ w                # sum_j w_j * pct_ij  (absent -> 0)
        den = present @ w                 # sum_j w_j over present indicators (> 0)
        score = num / den
        au = score[au_i]
        return int((score > au).sum()) + 1  # 1 = best; ties resolve to the better rank

    rng = np.random.default_rng(SEED)
    ranks = np.fromiter(
        (au_rank(rng.dirichlet(np.ones(9))) for _ in range(N_SCHEMES)),
        dtype=int, count=N_SCHEMES,
    )
    eq_rank = au_rank(np.full(9, 1.0 / 9))       # equal-weight reference
    p5, p95 = (int(round(x)) for x in np.percentile(ranks, [5, 95]))

    return {
        "ranks": ranks,
        "n_countries": int(len(countries)),
        "n_schemes": N_SCHEMES,
        "eq_rank": int(eq_rank),
        "min": int(ranks.min()),
        "max": int(ranks.max()),
        "spread": int(ranks.max() - ranks.min()),
        "p5": p5,
        "p95": p95,
        "median": int(np.median(ranks)),
    }


# Compute once at import so the finding drives the title (deterministic under SEED).
_R = _montecarlo()

TITLE = (
    f"Australia's well-being rank swings {_R['spread']} places "
    f"({_ordinal(_R['min'])} to {_ordinal(_R['max'])}) on weighting choices alone"
)

CAPTION = (
    f"Method: {N_SCHEMES:,} random weighting schemes (weights drawn from a "
    "Dirichlet(1,...,1) over the 9 sign-flipped core well-being indicators, seed = 42). "
    "For each scheme every country's composite is the WEIGHTED MEAN of the "
    "per-indicator percentile ranks it has, where each indicator is percentile-ranked "
    "within its own peer panel at the 2023 anchor (value_flipped, higher = better); "
    "weights are renormalised to the indicators a country actually has present, and "
    "countries are then ranked best-to-worst (1 = best) to read off Australia's rank. "
    f"The dashed line is Australia's rank under EQUAL weights ({_ordinal(_R['eq_rank'])}). "
    "Caveats: panels are unbalanced (n = 24-47 countries per indicator) and NOT every "
    "country has every indicator, so there is deliberately NO complete-case requirement "
    "(requiring all 9 would collapse the field to ~14 countries); each scheme's rank is "
    "taken among the countries present that scheme, and the whole exercise is a single "
    "2023 cross-section. Australia has all 9 indicators; most peers have most of them. "
    "The point is not the exact rank but its fragility: the same country, same data, "
    "same year moves across a wide band purely from how the indicators are weighted, so "
    "any single 'Australia is Nth' headline is a weighting choice, not a neutral fact."
)

# --- visual constants ---
_BAR = "#1f6feb"          # histogram fill (objective blue, matches sibling charts)
_BAND = "rgba(31,111,235,0.08)"  # 5-95 shaded band
_EQ = "#e8590c"           # equal-weight reference line (lived orange)
_EDGE = "#5f6368"


def build() -> go.Figure:
    R = _R
    ranks = R["ranks"]
    lo, hi = R["min"], R["max"]
    p5, p95 = R["p5"], R["p95"]

    fig = go.Figure()

    # 5th-95th percentile band (drawn under the bars). +/-0.5 so it hugs the integer bars.
    fig.add_vrect(
        x0=p5 - 0.5, x1=p95 + 0.5, layer="below", line_width=0, fillcolor=_BAND,
        annotation_text=f"90% of schemes: {_ordinal(p5)}-{_ordinal(p95)}",
        annotation_position="top left",
        annotation_font=dict(size=11, color=_EDGE),
    )

    # one bar per integer rank
    fig.add_trace(go.Histogram(
        x=ranks,
        xbins=dict(start=0.5, end=R["n_countries"] + 0.5, size=1),
        marker=dict(color=_BAR, line=dict(color="white", width=0.5)),
        opacity=0.9,
        name="Weighting schemes",
        hovertemplate="Australia ranks %{x}<br>%{y} of "
                      f"{R['n_schemes']:,} schemes<extra></extra>",
    ))

    # equal-weight reference line + label
    fig.add_vline(
        x=R["eq_rank"], line=dict(color=_EQ, width=2.5, dash="dash"),
        annotation_text=f"Equal weights: {_ordinal(R['eq_rank'])}",
        annotation_position="top right",
        annotation_font=dict(size=12, color=_EQ),
    )

    # min / max spread markers - the punchline endpoints
    ymax = np.histogram(ranks, bins=np.arange(0.5, R["n_countries"] + 1.5))[0].max()
    for x, lbl in ((lo, f"Best case: {_ordinal(lo)}"), (hi, f"Worst case: {_ordinal(hi)}")):
        fig.add_annotation(
            x=x, y=ymax * 0.5, ax=x, ay=ymax * 0.92, xref="x", yref="y",
            axref="x", ayref="y", showarrow=True, arrowhead=2, arrowwidth=1.4,
            arrowcolor=_EDGE, text="", opacity=0.8,
        )
        fig.add_annotation(
            x=x, y=ymax * 0.95, text=lbl, showarrow=False,
            font=dict(size=11, color=_EDGE),
            xanchor="right" if x == hi else "left",
        )

    # spread call-out box
    fig.add_annotation(
        xref="paper", yref="paper", x=0.99, y=0.99, xanchor="right", yanchor="top",
        showarrow=False, align="right",
        bordercolor=_EDGE, borderwidth=1, borderpad=6, bgcolor="rgba(255,255,255,0.85)",
        font=dict(size=12, color="#202124"),
        text=(f"<b>Rank spread: {R['spread']} places</b><br>"
              f"{_ordinal(lo)} to {_ordinal(hi)} across {R['n_schemes']:,} weightings"),
    )

    # standalone source footnote (full detail in CAPTION)
    fig.add_annotation(
        xref="paper", yref="paper", x=0, y=-0.16, xanchor="left", showarrow=False,
        align="left", font=dict(size=10.5, color=_EDGE),
        text=("Source: OECD How's Life? (status-A, 2023 anchor)  |  "
              f"{R['n_schemes']:,} Dirichlet weightings x 9 sign-flipped core indicators  |  "
              f"per-indicator percentile ranks, composite = weighted mean of available "
              f"indicators (n = 24-47 per indicator, no complete-case requirement)."),
    )

    fig.update_layout(
        template="plotly_white",
        title=dict(
            text=(f"<b>{TITLE}</b><br>"
                  "<sup>Distribution of Australia's overall well-being rank across "
                  f"{N_SCHEMES:,} random weightings of the 9 core indicators (1 = best)</sup>"),
            x=0.01, xanchor="left", font=dict(size=17),
        ),
        xaxis=dict(
            title="Australia's rank among OECD countries  (1 = best)",
            range=[0.5, R["n_countries"] + 0.5], dtick=5, zeroline=False,
        ),
        yaxis=dict(
            title=f"Number of weighting schemes  (of {N_SCHEMES:,})",
            zeroline=False,
        ),
        bargap=0.02,
        showlegend=False,
        margin=dict(l=80, r=40, t=95, b=100),
        width=980, height=620,
        hoverlabel=dict(bgcolor="white"),
    )
    return fig


if __name__ == "__main__":
    fig = build()
    assert fig.data, "chart4: figure has no data traces"
    R = _R
    assert 1 <= R["min"] <= R["max"] <= R["n_countries"], "chart4: rank bounds invalid"
    assert R["spread"] > 0, "chart4: expected a non-trivial rank spread"
    print(
        f"chart4 OK | {R['n_schemes']:,} Dirichlet schemes over {R['n_countries']} countries | "
        f"AU equal-weight rank = {_ordinal(R['eq_rank'])} | "
        f"min = {_ordinal(R['min'])}, max = {_ordinal(R['max'])} "
        f"(spread = {R['spread']} places) | "
        f"5-95 band = {_ordinal(R['p5'])}-{_ordinal(R['p95'])} | median = {_ordinal(R['median'])}"
    )
