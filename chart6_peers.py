"""Chart 6 — peer household debt (Winter Datathon).

The missing PEER comparison the brief asks for: Australia "among select peers".
Series = household debt as % of net household disposable income (higher = WORSE;
this is NOT debt-to-GDP). 5 Anglo peers, 2010-2024, one line each.

Emphasis is on Australia (thick amber line, direct end-label, 2018 peak marked);
the 4 peers are muted grey. Legend is off — every line carries a direct end-label.

Imports only pandas / numpy / plotly (+ analysis_helpers for the external/ path).
Reads external/household_debt_oecd.csv directly (cols: REF_AREA, TIME_PERIOD, OBS_VALUE).
No sign-flip needed: the raw ratio is already "higher = worse".
"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go

try:  # honour the project's external/ path contract when importable
    from analysis_helpers import EXTERNAL
except Exception:  # fallback: module lives at project root, external/ is a sibling
    EXTERNAL = Path(__file__).resolve().parent / "external"

# --- finding-first title + caveat-carrying caption (project chart contract) ---
TITLE = "Australians owe more than almost any peer — and never deleveraged"
CAPTION = (
    "Source: OECD household-debt SDMX pull. Household debt as "
    "% of net household disposable income, NOT debt-to-GDP; higher = worse. "
    "34-country pull, 5 Anglo peers shown. NZ has no 2015/2024 obs (line "
    "bridges 2015, ends 2023)."
)

# 5 Anglo peers: code -> readable name (Australia emphasised, rest muted)
PEERS = {
    "AUS": "Australia",
    "NZL": "New Zealand",
    "CAN": "Canada",
    "GBR": "United Kingdom",
    "USA": "United States",
}
YEAR_MIN, YEAR_MAX = 2010, 2024
AU_PEAK_YEAR = 2018

AU_COLOR = "#C1652F"       # amber — debt = strain
PEER_COLOR = "#9aa0a6"     # muted grey
AU_WIDTH = 3.6
PEER_WIDTH = 1.8


def _load() -> pd.DataFrame:
    """Wide frame indexed by year, one column per peer code, filtered 2010-2024."""
    hd = pd.read_csv(EXTERNAL / "household_debt_oecd.csv")
    hd = hd[hd["REF_AREA"].isin(PEERS)].copy()
    hd["TIME_PERIOD"] = hd["TIME_PERIOD"].astype(int)
    hd = hd[(hd["TIME_PERIOD"] >= YEAR_MIN) & (hd["TIME_PERIOD"] <= YEAR_MAX)]
    wide = hd.pivot_table(index="TIME_PERIOD", columns="REF_AREA", values="OBS_VALUE")
    return wide.sort_index()


def _last_valid(wide: pd.DataFrame, code: str):
    """(year, value) of the last non-NaN observation for one series."""
    s = wide[code].dropna()
    return int(s.index[-1]), float(s.iloc[-1])


def build() -> go.Figure:
    wide = _load()
    fig = go.Figure()

    # draw peers first (grey, underneath), Australia last (amber, on top)
    order = [c for c in PEERS if c != "AUS"] + ["AUS"]
    for code in order:
        is_au = code == "AUS"
        s = wide[code]
        fig.add_trace(
            go.Scatter(
                x=s.index,
                y=s.values,
                mode="lines",
                name=PEERS[code],
                line=dict(
                    color=AU_COLOR if is_au else PEER_COLOR,
                    width=AU_WIDTH if is_au else PEER_WIDTH,
                ),
                connectgaps=True,  # bridge NZ's single 2015 gap; trailing NaN still ends the line
                hovertemplate=f"{PEERS[code]} %{{x}}: %{{y:.0f}}%<extra></extra>",
                showlegend=False,
            )
        )

    # direct end-labels (replaces the legend)
    for code in order:
        is_au = code == "AUS"
        yr, val = _last_valid(wide, code)
        fig.add_annotation(
            x=yr,
            y=val,
            text=f"<b>{PEERS[code]}</b>" if is_au else PEERS[code],
            xanchor="left",
            xshift=8,
            yanchor="middle",
            showarrow=False,
            font=dict(
                color=AU_COLOR if is_au else PEER_COLOR,
                size=15 if is_au else 12,
            ),
        )

    # mark Australia's 2018 peak
    au_peak = float(wide.loc[AU_PEAK_YEAR, "AUS"])
    fig.add_trace(
        go.Scatter(
            x=[AU_PEAK_YEAR],
            y=[au_peak],
            mode="markers",
            marker=dict(color=AU_COLOR, size=10, line=dict(color="white", width=1.5)),
            hovertemplate=f"AU peak {AU_PEAK_YEAR}: {au_peak:.0f}%<extra></extra>",
            showlegend=False,
        )
    )
    fig.add_annotation(
        x=AU_PEAK_YEAR,
        y=au_peak,
        text=f"peak {AU_PEAK_YEAR} · {au_peak:.0f}%",
        yanchor="bottom",
        yshift=12,
        showarrow=False,
        font=dict(color=AU_COLOR, size=12),
    )

    fig.update_layout(
        template="plotly_white",
        width=980,
        height=600,
        title=dict(text=f"<b>{TITLE}</b>", x=0.02, xanchor="left", font=dict(size=20)),
        margin=dict(l=70, r=140, t=90, b=90),
        showlegend=False,
        hovermode="closest",
    )
    fig.update_xaxes(
        range=[YEAR_MIN - 0.4, YEAR_MAX + 2.6],  # headroom for the end-labels
        tickmode="array",
        tickvals=list(range(YEAR_MIN, YEAR_MAX + 1, 2)),
        title_text=None,
    )
    fig.update_yaxes(
        title_text="Household debt (% of net disposable income)",
        rangemode="tozero",
    )
    # caption as a page footnote
    fig.add_annotation(
        text=CAPTION,
        xref="paper", yref="paper",
        x=0, y=-0.14,
        xanchor="left", yanchor="top",
        showarrow=False,
        align="left",
        font=dict(size=10.5, color="#666"),
    )
    return fig


if __name__ == "__main__":
    fig = build()
    lines = [t for t in fig.data if t.mode and "lines" in t.mode]
    assert len(fig.data) >= 5, f"expected >=5 traces, got {len(fig.data)}"
    assert len(lines) >= 5, f"expected >=5 line series, got {len(lines)}"

    wide = _load()
    au = wide["AUS"]
    n_peers = sum(1 for c in PEERS if c != "AUS")
    print(
        f"chart6 OK | AU debt %net-disp-income: "
        f"2010={au.loc[2010]:.0f}  2018={au.loc[2018]:.0f}(peak)  2024={au.loc[2024]:.0f}"
        f" | {len(lines)} lines = AU + {n_peers} peers"
    )
