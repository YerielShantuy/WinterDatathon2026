"""Chart 7 — Australia's OECD-percentile trajectory, 2010 -> 2023 (dumbbell / arrow plot).

Thesis: "Is Australia doing well?" -> it did NOT stand still. Ranked against OECD
peers, Australia's percentile *collapsed* on almost every lived indicator between
2010 and 2023, while objective prosperity (disposable income) held or rose.

One row per core indicator: an open dot at the 2010 percentile, a solid dot at the
2023 percentile, joined by an arrow pointing 2010 -> 2023. Connector colour encodes
direction (rose = teal, fell = amber, collapsed >=20 pctile = deep red). Rows are
sorted by the size of the move so the collapses read top-to-bottom.

Values are recomputed from analysis_helpers.au_percentile (not hardcoded). All
percentiles use status-A observations only; higher percentile = AU ranks better.
"""
from analysis_helpers import load, au_percentile, CORE_HANDLES, LABELS
import plotly.graph_objects as go

# --- the finding (title) and the source + caveat (caption) ---
TITLE = "Australia didn't stand still - it slid on almost everything lived, 2010->2023"

CAPTION = (
    "Source: OECD How's Life? Well-being Database (status-A observations only). Each value is "
    "Australia's percentile among available OECD peers that year - the share of countries AU "
    "ranks above on the direction-aligned indicator (sign-flipped so higher = better). "
    "Caveat: the peer panel differs between 2010 and 2023 (n changes per indicator), so part of "
    "each shift is panel composition, not pure movement. But the largest lived drops sit on full "
    "n=47 panels (lack of social support 85->47, negative affect 49->26) and n>=36 "
    "(deaths of despair 70->39), so those collapses are robust; small moves "
    "(e.g. gender wage gap) should not be over-read."
)

# --- palette (per brief) ---
TEAL = "#2F6F8F"   # rose (ranks better)
AMBER = "#C1652F"  # fell
RED = "#9E2B25"    # collapsed (big drop)
GREY = "#9AA5AD"   # 2010 open dot + median line
INK = "#3A4550"    # 2023 dot / text default
BIG_DROP = 20.0    # |delta pctile| at/above which a fall is a "collapse" (deep red)


def _dir_color(delta: float) -> str:
    if delta > 0:
        return TEAL
    if abs(delta) >= BIG_DROP:
        return RED
    return AMBER


def _rows():
    """Recompute every row from the helper. Returns list sorted for plotting (top = biggest fall)."""
    df = load()
    role = df.groupby("handle")["role"].first()
    rows = []
    for h in CORE_HANDLES:
        p10, n10 = au_percentile(df, h, 2010)
        p23, n23 = au_percentile(df, h, 2023)
        rows.append({
            "handle": h, "label": LABELS[h], "role": role.get(h),
            "p10": p10, "n10": n10, "p23": p23, "n23": n23,
            "delta": p23 - p10,
        })
    # sort by delta ASC -> most negative (biggest collapse) first; assign top-most y last
    rows.sort(key=lambda r: r["delta"])
    n = len(rows)
    for i, r in enumerate(rows):
        r["y"] = n - 1 - i          # biggest collapse gets the highest y (top of chart)
        r["color"] = _dir_color(r["delta"])
    return rows


def build() -> go.Figure:
    rows = _rows()
    fig = go.Figure()

    # --- direction arrows (2010 tail -> 2023 head), one per row ---
    for r in rows:
        fig.add_annotation(
            x=r["p23"], y=r["y"], ax=r["p10"], ay=r["y"],
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=3, arrowsize=1.1, arrowwidth=3,
            arrowcolor=r["color"], startstandoff=5, standoff=5, opacity=0.95,
        )

    # per-point outward text placement (label sits on the side away from the other dot)
    tp10 = ["middle left" if r["p10"] <= r["p23"] else "middle right" for r in rows]
    tp23 = ["middle left" if r["p23"] <= r["p10"] else "middle right" for r in rows]

    # --- 2010 dots (open, grey = the starting position) ---
    fig.add_trace(go.Scatter(
        x=[r["p10"] for r in rows], y=[r["y"] for r in rows],
        mode="markers+text", cliponaxis=False, showlegend=False,
        marker=dict(symbol="circle-open", size=12, color=GREY, line=dict(width=2.5, color=GREY)),
        text=[f"{r['p10']:.1f}" for r in rows], textposition=tp10,
        textfont=dict(size=11, color=GREY),
        customdata=[[r["label"], r["n10"]] for r in rows],
        hovertemplate="<b>%{customdata[0]}</b><br>2010: %{x:.1f} pctile  (n=%{customdata[1]})<extra></extra>",
    ))

    # --- 2023 dots (solid, coloured by direction = where AU ended up) ---
    fig.add_trace(go.Scatter(
        x=[r["p23"] for r in rows], y=[r["y"] for r in rows],
        mode="markers+text", cliponaxis=False, showlegend=False,
        marker=dict(symbol="circle", size=13, color=[r["color"] for r in rows],
                    line=dict(width=1.4, color="white")),
        text=[f"{r['p23']:.1f}" for r in rows], textposition=tp23,
        textfont=dict(size=11, color=INK),
        customdata=[[r["label"], r["n23"], r["p10"]] for r in rows],
        hovertemplate=("<b>%{customdata[0]}</b><br>2010: %{customdata[2]:.1f} -> "
                       "2023: %{x:.1f} pctile  (n=%{customdata[1]})<extra></extra>"),
    ))

    # --- manual legend (dummy traces, nothing plotted) ---
    def _legend_line(name, color):
        fig.add_trace(go.Scatter(x=[None], y=[None], mode="lines", name=name,
                                 line=dict(color=color, width=4), hoverinfo="skip"))
    _legend_line("Rose (ranks better)", TEAL)
    _legend_line("Fell", AMBER)
    _legend_line(f"Collapsed (>={int(BIG_DROP)} pctile drop)", RED)
    fig.add_trace(go.Scatter(x=[None], y=[None], mode="markers", name="2010",
                             marker=dict(symbol="circle-open", size=11, color=GREY,
                                         line=dict(width=2.5, color=GREY)), hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=[None], y=[None], mode="markers", name="2023",
                             marker=dict(symbol="circle", size=12, color=INK,
                                         line=dict(width=1.4, color="white")), hoverinfo="skip"))

    # --- median reference ---
    fig.add_vline(x=50, line_dash="dash", line_color=GREY, line_width=1.4,
                  annotation_text="50th pctile (OECD median)", annotation_position="top",
                  annotation_font=dict(size=11, color=GREY))

    # --- axes / layout ---
    ticktext = [f"{r['label']}<br><span style='font-size:10px;color:{GREY}'>{r['role']}</span>"
                for r in rows]
    n = len(rows)
    fig.update_layout(
        template="plotly_white", width=1000, height=640,
        title=dict(
            text=(f"{TITLE}<br><span style='font-size:13px;color:{GREY}'>"
                  "Percentile rank among OECD peers - arrows point 2010 -> 2023</span>"),
            x=0.01, xanchor="left", y=0.955, font=dict(size=19, color=INK),
        ),
        margin=dict(l=215, r=45, t=95, b=155),
        xaxis=dict(title="Percentile rank among OECD peers  (higher = better)",
                   range=[-1, 104], tickvals=[0, 25, 50, 75, 100],
                   zeroline=False, gridcolor="#EEF1F3"),
        yaxis=dict(tickvals=[r["y"] for r in rows], ticktext=ticktext,
                   range=[-0.6, n - 0.4], showgrid=False, tickfont=dict(size=12, color=INK)),
        legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.13, yanchor="top",
                    font=dict(size=11)),
        plot_bgcolor="white", paper_bgcolor="white",
    )

    # --- caption (source + caveat) below the plot ---
    fig.add_annotation(
        text=CAPTION, xref="paper", yref="paper", x=0, y=-0.24, xanchor="left", yanchor="top",
        showarrow=False, align="left", font=dict(size=10.5, color=GREY),
        width=940,
    )
    return fig


if __name__ == "__main__":
    fig = build()
    assert fig.data, "chart7: fig.data is empty"

    # name the 3 biggest LIVED drops, recomputed from the helper
    rows = _rows()
    lived_drops = sorted((r for r in rows if r["role"] == "lived" and r["delta"] < 0),
                         key=lambda r: r["delta"])[:3]
    parts = [f"{r['handle']} {r['p10']:.1f}->{r['p23']:.1f}" for r in lived_drops]
    print("chart7 OK | 3 biggest lived drops: " + "; ".join(parts))
