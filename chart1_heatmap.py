"""Chart 1 — "Macro Illusion" domain scorecard heatmap.

Makes the objective-vs-lived split visible at a glance: Australia's percentile
rank among OECD peers at 2023 (higher = better) for the 9 core indicators,
grouped into an OBJECTIVE block (top) and a LIVED block (bottom). Objective rows
glow green, lived rows sink red/amber — that IS the finding.

All data comes from the shared contract in analysis_helpers (value_flipped is
ALREADY signed higher=better; percentiles/n come from au_percentile_table).
Nothing is re-loaded or re-signed here.
"""
from analysis_helpers import load, au_percentile_table
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Title states the FINDING, not the variable.
TITLE = "Australia scores high on what's measured, low on what's lived"

CAPTION = (
    "Source: OECD How's Life? Well-being Database (status-A observations). "
    "Each cell is Australia's percentile rank among OECD peers at 2023 — the "
    "share of countries AU beats on the higher-is-better (sign-flipped) value; "
    "50 = peer median. Per-cell n is the number of countries with 2023 data, "
    "shown on every cell (panels range 24-47 countries, so cross-country ranks "
    "are not equally deep). Subjective indicators (negative affect, lack of "
    "social support) are 3-year pooled Gallup World Poll estimates. "
    "Life satisfaction & GDP per capita are excluded (handled as callouts)."
)


def build() -> go.Figure:
    df = load()                         # 47-country, status-A only (shared helper)
    tbl = au_percentile_table(df)       # 9 core handles, percentile + role/domain/n

    # Group by role; sort ASCENDING within each block so that, on a default
    # (bottom-up) plotly y-axis, the best cell sits at the top of its block.
    obj = tbl[tbl["role"] == "objective"].sort_values("au_percentile")
    liv = tbl[tbl["role"] == "lived"].sort_values("au_percentile")

    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        row_heights=[len(obj), len(liv)],          # 3 vs 6 rows -> honest proportions
        vertical_spacing=0.07,
        subplot_titles=(
            "OBJECTIVE - macro prosperity (what gets measured)",
            "LIVED - subjective & lived experience (what gets felt)",
        ),
    )

    XCOL = "Australia @ 2023"

    for r, sub in enumerate((obj, liv), start=1):
        vals = sub["au_percentile"].tolist()
        labels = sub["label"].tolist()
        ns = sub["n"].tolist()
        roles = sub["role"].tolist()
        doms = sub["domain"].tolist()
        customdata = [[[n, role, dom]] for n, role, dom in zip(ns, roles, doms)]

        fig.add_trace(
            go.Heatmap(
                z=[[v] for v in vals],
                x=[XCOL],
                y=labels,
                coloraxis="coloraxis",     # shared scale across both blocks
                customdata=customdata,
                hovertemplate=(
                    "<b>%{y}</b><br>AU percentile: %{z:.1f}"
                    "<br>panel n=%{customdata[0]} countries"
                    "<br>%{customdata[1]} · %{customdata[2]} domain<extra></extra>"
                ),
                xgap=4, ygap=4,            # separate cells -> scorecard look
            ),
            row=r, col=1,
        )

        # Per-cell annotation: percentile (big) + its n (small). White text on the
        # deep-red low cells for contrast, near-black elsewhere.
        for v, label, n in zip(vals, labels, ns):
            fig.add_annotation(
                row=r, col=1, x=XCOL, y=label, showarrow=False,
                text=f"<b>{v:.1f}</b>  <span style='font-size:11px'>(n={n})</span>",
                font=dict(size=15, color="#ffffff" if v <= 30 else "#1b1b1b"),
            )

    obj_mean = obj["au_percentile"].mean()
    liv_mean = liv["au_percentile"].mean()

    fig.update_layout(
        template="plotly_white",
        title=dict(
            text=(
                f"{TITLE}<br>"
                f"<span style='font-size:13px;color:#555'>Objective mean percentile "
                f"{obj_mean:.0f} vs lived mean {liv_mean:.0f} — a "
                f"{obj_mean - liv_mean:.0f}-point prosperity-vs-experience gap</span>"
            ),
            x=0.5, xanchor="center", y=0.965,
        ),
        coloraxis=dict(
            colorscale="RdYlGn",           # diverging red->yellow->green
            cmin=0, cmax=100, cmid=50,     # centred on the peer median
            colorbar=dict(
                title=dict(text="AU percentile<br>vs OECD peers", side="right"),
                tickvals=[0, 25, 50, 75, 100],
                ticktext=["0<br>worst", "25", "50<br>median", "75", "100<br>best"],
                thickness=16, len=0.62, y=0.45,
            ),
        ),
        width=780, height=660,
        margin=dict(l=190, r=140, t=115, b=70),
    )

    # X label lives on the shared bottom axis only.
    fig.update_xaxes(tickfont=dict(size=12), showgrid=False)
    fig.update_yaxes(showgrid=False, ticksuffix="  ")

    # Recolour the two subplot-block titles (annotations[0], [1]) to reinforce split.
    fig.layout.annotations[0].update(font=dict(size=13, color="#1e8449"))
    fig.layout.annotations[1].update(font=dict(size=13, color="#c0392b"))

    return fig


if __name__ == "__main__":
    fig = build()
    assert fig.data, "chart1: no traces on figure"
    assert len(fig.data) == 2, "chart1: expected objective + lived heatmap traces"

    tbl = au_percentile_table(load())
    obj_mean = tbl[tbl["role"] == "objective"]["au_percentile"].mean()
    liv_mean = tbl[tbl["role"] == "lived"]["au_percentile"].mean()
    nmin, nmax = int(tbl["n"].min()), int(tbl["n"].max())
    print(
        "chart1 OK | traces=%d | 9 core indicators (3 objective / 6 lived) | "
        "obj mean pctile %.1f vs lived mean %.1f (gap %.1f) | "
        "panels n=%d-%d | RdYlGn 0-100 centred at 50"
        % (len(fig.data), obj_mean, liv_mean, obj_mean - liv_mean, nmin, nmax)
    )
