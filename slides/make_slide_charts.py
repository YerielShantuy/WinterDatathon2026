"""Render slide-ready static charts for the deck (matplotlib, transparent PNG @200dpi).

These are NOT the notebook's interactive plotly charts — they are redrawn clean and
large-type for projection, styled to the DESIGN.md palette. Single source of truth for
every number is analysis_helpers (+ chart4's verified Monte Carlo run). Nothing is
re-loaded or re-signed here.

Run from project root:  python slides/make_slide_charts.py
Outputs: slides/assets/01_split.png .. 04_fragility.png
"""
from pathlib import Path
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import analysis_helpers as H
from analysis_helpers import load, au_series, au_percentile, household_debt, ANCHOR, CORE_HANDLES, LABELS, POOLED_HANDLES

OUT = Path(__file__).resolve().parent / "assets"
OUT.mkdir(exist_ok=True)

# --- palette (matches DESIGN.md) ---
INK       = "#1C1E21"
MUTED     = "#6B7280"
HAIRLINE  = "#CFCBC0"
FAINT     = "#E7E4DC"
OBJECTIVE = "#2F6F8F"   # measured / prosperity  (teal-blue)
OBJ_LT    = "#6FA3BC"
LIVED     = "#C1652F"   # felt / strain          (burnt amber)
LIVED_DEEP= "#9E2B25"   # strongest strain       (deep red)
GOODBAND  = "#EAF1F0"
BADBAND   = "#F6ECE4"

FONT = "Arial"  # available on host; Inter-like neutral grotesque
plt.rcParams.update({
    "font.family": FONT,
    "font.size": 15,
    "text.color": INK,
    "axes.edgecolor": HAIRLINE,
    "axes.labelcolor": INK,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "axes.linewidth": 1.0,
    "figure.dpi": 200,
    "savefig.dpi": 200,
})

DPI = 200


def _save(fig, name):
    fig.savefig(OUT / name, transparent=True, bbox_inches="tight", pad_inches=0.18, dpi=DPI)
    plt.close(fig)
    return name


def _spine(ax, keep=("left", "bottom")):
    for s in ("top", "right", "left", "bottom"):
        ax.spines[s].set_visible(s in keep)
        if s in keep:
            ax.spines[s].set_color(HAIRLINE)


def _titleblock(fig, title, sub=None, x=0.02):
    """Title + subtitle drawn at the top of the FIGURE (subtitle below title, never over it)."""
    fig.text(x, 0.965, title, fontsize=20, fontweight="bold", color=INK, ha="left", va="top")
    if sub:
        fig.text(x, 0.908, sub, fontsize=13, color=MUTED, ha="left", va="top")


def _source(fig, text):
    fig.text(0.008, 0.008, text, fontsize=9.5, color=MUTED, ha="left", va="bottom")


# ---------------------------------------------------------------- Chart 1: the split
def fig_split():
    df = load()
    t = H.au_percentile_table(df).sort_values("au_percentile").reset_index(drop=True)
    y = np.arange(len(t))
    colors = [OBJECTIVE if r == "objective" else LIVED for r in t["role"]]

    obj_m = t[t.role == "objective"]["au_percentile"].mean()
    liv_m = t[t.role == "lived"]["au_percentile"].mean()

    fig, ax = plt.subplots(figsize=(12.2, 6.9))
    # median reference
    ax.axvline(50, color=HAIRLINE, lw=1.2, ls=(0, (4, 3)), zorder=1)
    ax.annotate("OECD median", xy=(50, len(t) - 0.15), fontsize=10.5, color=MUTED, ha="center", va="bottom")
    # lollipop stems + dots + value·n label
    for yi, val, c, n in zip(y, t["au_percentile"], colors, t["n"]):
        ax.plot([0, val], [yi, yi], color=c, lw=2.4, alpha=0.35, zorder=2, solid_capstyle="round")
        ax.scatter(val, yi, s=190, color=c, zorder=3, edgecolor="white", linewidth=1.6)
        ax.annotate(f"{val:.0f}", xy=(val, yi), xytext=(11, 0), textcoords="offset points",
                    va="center", fontsize=13.5, fontweight="bold", color=c)
        ax.annotate(f"n={n}", xy=(val, yi), xytext=(34, 0), textcoords="offset points",
                    va="center", fontsize=9.5, color=MUTED)
    ax.set_yticks(y)
    ax.set_yticklabels(list(t["label"]), fontsize=14, color=INK)
    ax.set_xlim(0, 108)
    ax.set_ylim(-0.6, len(t) - 0.25)
    ax.set_xlabel("Australia's percentile among OECD peers, 2023  (higher = ranks better)", fontsize=13)
    _spine(ax, keep=("bottom",))
    ax.tick_params(axis="y", length=0)
    ax.set_xticks([0, 25, 50, 75, 100])

    _titleblock(fig, "High on what's measured, low on what's lived",
                f"AU percentile per indicator, 2023 · objective mean {obj_m:.0f} vs lived mean {liv_m:.0f} — "
                f"a {obj_m - liv_m:.0f}-point gap")
    # small colour key, in the empty upper-left of the plot
    ax.annotate("● objective", xy=(2, len(t) - 1.15), color=OBJECTIVE, fontsize=12, fontweight="bold", va="center")
    ax.annotate("● lived", xy=(20, len(t) - 1.15), color=LIVED, fontsize=12, fontweight="bold", va="center")
    _source(fig, "Source: OECD How's Life? Well-being Database (status-A). Panels n=24–47; sign-flipped so higher = better.")
    fig.subplots_adjust(left=0.185, right=0.97, top=0.82, bottom=0.12)
    return _save(fig, "01_split.png")


# ---------------------------------------------------------------- Chart 2: level x momentum
def _slope_per_decade(handle, s):
    y = s["value_flipped"].astype(float).to_numpy()
    if handle in POOLED_HANDLES:
        x = s["pool_idx"].astype(float).to_numpy(); dec = 10.0 / ((2023 - 2010) / 5.0)
    else:
        x = s["TIME_PERIOD"].astype(float).to_numpy(); dec = 10.0
    sd = y.std(ddof=0)
    yz = (y - y.mean()) / sd if sd > 0 else np.zeros_like(y)
    return np.polyfit(x, yz, 1)[0] * dec


def fig_matrix():
    df = load()
    meta = df.groupby("handle")[["role"]].first()
    rows = []
    for h in CORE_HANDLES:
        pct, n = au_percentile(df, h, ANCHOR)
        mom = _slope_per_decade(h, au_series(df, h))
        rows.append((h, LABELS[h], meta.loc[h, "role"], pct, mom, n))
    import pandas as pd
    d = pd.DataFrame(rows, columns=["handle", "label", "role", "level", "mom", "n"])

    fig, ax = plt.subplots(figsize=(12.2, 7.0))
    # quadrant tints
    ax.add_patch(plt.Rectangle((50, 0), 50, 3, color=GOODBAND, zorder=0))
    ax.add_patch(plt.Rectangle((0, -3), 50, 3, color=BADBAND, zorder=0))
    ax.axvline(50, color=HAIRLINE, lw=1.1, ls=(0, (4, 3)))
    ax.axhline(0, color=HAIRLINE, lw=1.1, ls=(0, (4, 3)))
    for x, yy, txt, ha in [(97, 2.85, "HIGH & RISING", "right"), (3, 2.85, "LOW & RISING", "left"),
                           (97, -2.85, "HIGH & FALLING", "right"), (3, -2.85, "LOW & FALLING", "left")]:
        ax.annotate(txt, (x, yy), ha=ha, va="top", fontsize=10.5, color="#9aa0a6", fontweight="bold")

    for _, r in d.iterrows():
        c = OBJECTIVE if r.role == "objective" else LIVED
        mk = "o" if r.role == "objective" else "D"
        sz = 150 + (r.n - 24) / (47 - 24) * 240
        ax.scatter(r.level, r.mom, s=sz, marker=mk, color=c, edgecolor="white", linewidth=1.6, zorder=4, alpha=0.92)
    # labels (offset to reduce overlap)
    off = {"disposable_income": (-8, -20), "life_expectancy": (-12, 15), "employment_rate": (2, 14),
           "housing_affordability": (0, -20), "gender_wage_gap": (-14, 12), "long_hours": (0, 15),
           "deaths_despair": (0, -20), "negative_affect": (0, 16), "lack_of_support": (14, 12)}
    for _, r in d.iterrows():
        c = OBJECTIVE if r.role == "objective" else LIVED
        dx, dy = off.get(r.handle, (0, 14))
        ax.annotate(r.label, (r.level, r.mom), xytext=(dx, dy), textcoords="offset points",
                    ha="center", fontsize=11.5, color=INK)
    ax.set_xlim(0, 100); ax.set_ylim(-3, 3)
    ax.set_xlabel("LEVEL — percentile among OECD peers, 2023  (higher = ranks better)", fontsize=13)
    ax.set_ylabel("MOMENTUM — change per decade  (SD of own history; up = improving)", fontsize=12.5)
    ax.set_xticks([0, 25, 50, 75, 100])
    _spine(ax, keep=("left", "bottom"))
    _titleblock(fig, "Prosperity sits high-and-rising; felt experience sits low-and-falling",
                "Australia's 9 core indicators · marker size = panel n · circle = objective, diamond = lived", x=0.045)
    _source(fig, "Source: OECD How's Life? (status-A). Momentum z-scored per indicator; pooled series sloped over pool index.")
    fig.subplots_adjust(left=0.09, right=0.97, top=0.80, bottom=0.11)
    return _save(fig, "02_matrix.png")


# ---------------------------------------------------------------- Chart 3: divergence
def fig_divergence():
    df = load()
    YR = 2024
    specs = [
        ("disposable_income", "Disposable income", OBJECTIVE, False, False, "objective"),
        ("employment_rate", "Employment", OBJ_LT, False, False, "objective"),
        ("household_debt", "Household debt", LIVED, False, True, "lived"),
        ("negative_affect", "Negative affect", "#E8863C", True, False, "lived"),
        ("deaths_despair", "Deaths of despair", LIVED_DEEP, False, False, "lived"),
    ]
    fig, ax = plt.subplots(figsize=(12.8, 6.9))
    ax.axhline(100, color=HAIRLINE, lw=1.0, ls=(0, (2, 3)))
    ax.axvspan(2019, 2023, color="#F1EFEA", zorder=0)
    ax.annotate("2019–23 cost-of-living squeeze", xy=(2019.1, 152), fontsize=10.5, color=MUTED, ha="left")

    ends = []
    for key, short, color, pooled, external, role in specs:
        if external:
            hd = household_debt(); hd = hd[hd.year <= YR]
            x = hd.year.to_numpy(float); raw = hd.debt_pct.to_numpy(float)
        else:
            s = au_series(df, key)
            if pooled:
                x = np.clip(s.pool_midyear.to_numpy(float), 2010, YR); raw = s.OBS_VALUE.to_numpy(float)
            else:
                s = s[s.TIME_PERIOD <= YR]; x = s.TIME_PERIOD.to_numpy(float); raw = s.OBS_VALUE.to_numpy(float)
        idx = raw / raw[0] * 100.0
        if pooled:
            ax.plot(x, idx, color=color, lw=1.6, ls=(0, (1, 2)), zorder=2)
            ax.scatter(x, idx, color=color, s=54, marker="s", zorder=3, edgecolor="white", linewidth=1.0)
        else:
            ax.plot(x, idx, color=color, lw=3.2 if role == "objective" else 2.6, zorder=3, solid_capstyle="round")
        ends.append((x[-1], idx[-1], short, color, idx[-1] - 100, pooled))

    # direct end-labels, de-overlapped
    ends_sorted = sorted(ends, key=lambda e: e[1])
    last_y = -1e9
    for x1, y1, short, color, pct, pooled in ends_sorted:
        yy = max(y1, last_y + 4.0); last_y = yy
        sign = "+" if pct >= 0 else ""
        ax.annotate(f"{short}  {sign}{pct:.0f}%" + (" (pooled)" if pooled else ""),
                    xy=(x1, y1), xytext=(8, yy - y1 if abs(yy - y1) > 0.1 else 0),
                    textcoords="offset points", va="center", ha="left",
                    fontsize=12, fontweight="bold", color=color)
    # direction badges
    ax.annotate("▲ higher = WORSE", xy=(2010.2, 149), fontsize=12, color=LIVED_DEEP, fontweight="bold")
    ax.annotate("▲ higher = BETTER", xy=(2010.2, 141), fontsize=12, color=OBJECTIVE, fontweight="bold")

    ax.set_xlim(2010, 2025.4); ax.set_ylim(84, 156)
    ax.set_xticks(range(2010, 2025, 2))
    ax.set_xlabel("Year", fontsize=13)
    ax.set_ylabel("Index  (2010 = 100)", fontsize=13)
    _spine(ax, keep=("left", "bottom"))
    _titleblock(fig, "Income and jobs climbed — debt and distress climbed faster",
                "Australia, every series indexed to 100 at 2010", x=0.045)
    _source(fig, "Source: OECD How's Life? + OECD household-debt SDMX. Negative affect = 3-yr pooled Gallup (markers). Debt = % of disposable income.")
    fig.subplots_adjust(left=0.08, right=0.80, top=0.80, bottom=0.12)
    return _save(fig, "03_divergence.png")


# ---------------------------------------------------------------- Chart 4: fragility
def fig_fragility():
    from chart4_montecarlo import _R as MC, _ordinal  # verified 1000-scheme run, deterministic (seed 42)
    ranks = np.asarray(MC["ranks"])
    lo, hi, eq, p5, p95, med, ncnt = MC["min"], MC["max"], MC["eq_rank"], MC["p5"], MC["p95"], MC["median"], MC["n_countries"]

    fig, ax = plt.subplots(figsize=(12.4, 6.6))
    bins = np.arange(0.5, ncnt + 1.5, 1)
    ax.axvspan(p5 - 0.5, p95 + 0.5, color="#EAF1F0", zorder=0)
    ax.annotate(f"90% of schemes: {_ordinal(p5)}–{_ordinal(p95)}", xy=(p5 - 0.4, ax.get_ylim()[1]),
                xytext=(p5 - 0.4, 0.94), textcoords=("data", "axes fraction"),
                fontsize=11, color=MUTED, ha="left")
    n_arr, _, patches = ax.hist(ranks, bins=bins, color=OBJECTIVE, edgecolor="white", linewidth=0.6, alpha=0.9, zorder=2)
    ymax = n_arr.max()
    ax.axvline(eq, color=LIVED, lw=2.4, ls=(0, (5, 3)), zorder=4)
    ax.annotate(f"Equal weights: {_ordinal(eq)}", xy=(eq, ymax * 0.98), xytext=(6, 0),
                textcoords="offset points", color=LIVED, fontsize=12.5, fontweight="bold", va="top")
    # min/max endpoints
    for x, lbl, ha in [(lo, f"best {_ordinal(lo)}", "left"), (hi, f"worst {_ordinal(hi)}", "right")]:
        ax.annotate(lbl, xy=(x, ymax * 0.5), fontsize=11.5, color=INK, ha=ha, fontweight="bold")
    # spread box
    ax.annotate(f"Rank swings {hi-lo} places\n{_ordinal(lo)} → {_ordinal(hi)} across 1,000 weightings",
                xy=(0.985, 0.98), xycoords="axes fraction", ha="right", va="top",
                fontsize=12.5, color=INK,
                bbox=dict(boxstyle="round,pad=0.5", fc="white", ec=HAIRLINE, lw=1.1))
    ax.set_xlim(0.5, ncnt + 0.5)
    ax.set_xlabel("Australia's rank among OECD countries  (1 = best)", fontsize=13)
    ax.set_ylabel("Number of weighting schemes  (of 1,000)", fontsize=12.5)
    _spine(ax, keep=("left", "bottom"))
    _titleblock(fig, f"Australia's rank swings {hi-lo} places on weighting alone",
                "1,000 random Dirichlet weightings of the 9 core indicators, 2023", x=0.045)
    _source(fig, "Source: OECD How's Life? (status-A, 2023). Composite = weighted mean of available per-indicator percentiles; no complete-case requirement.")
    fig.subplots_adjust(left=0.09, right=0.97, top=0.80, bottom=0.12)
    return _save(fig, "04_fragility.png")


# ---------------------------------------------------------------- Chart 5 (slide): trajectory
def fig_trajectory():
    df = load()
    meta = df.groupby("handle")[["role"]].first()
    rows = []
    for h in CORE_HANDLES:
        p10, _ = au_percentile(df, h, 2010)
        p23, _ = au_percentile(df, h, ANCHOR)
        if p10 is None or p23 is None:
            continue
        rows.append((h, LABELS[h], meta.loc[h, "role"], p10, p23, p23 - p10))
    import pandas as pd
    d = pd.DataFrame(rows, columns=["handle", "label", "role", "p10", "p23", "delta"]).sort_values("p23").reset_index(drop=True)
    y = np.arange(len(d))

    fig, ax = plt.subplots(figsize=(12.2, 7.0))
    ax.axvline(50, color=HAIRLINE, lw=1.1, ls=(0, (4, 3)), zorder=1)
    ax.annotate("OECD median", xy=(50, len(d) - 0.1), fontsize=10.5, color=MUTED, ha="center", va="bottom")
    for yi, r in zip(y, d.itertuples()):
        fell = r.delta < 0
        col = LIVED_DEEP if r.delta <= -20 else (LIVED if fell else OBJECTIVE)
        # connector
        ax.annotate("", xy=(r.p23, yi), xytext=(r.p10, yi),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=2.6, alpha=0.85))
        ax.scatter(r.p10, yi, s=90, facecolor="white", edgecolor=MUTED, linewidth=1.6, zorder=3)  # 2010 (open)
        ax.scatter(r.p23, yi, s=150, color=col, edgecolor="white", linewidth=1.4, zorder=4)        # 2023 (solid)
        # value labels at the ends
        ax.annotate(f"{r.p10:.0f}", xy=(r.p10, yi), xytext=(0, 11), textcoords="offset points",
                    ha="center", fontsize=10, color=MUTED)
        lx = 12 if r.p23 >= r.p10 else -12
        ax.annotate(f"{r.p23:.0f}", xy=(r.p23, yi), xytext=(lx, 0), textcoords="offset points",
                    va="center", ha="left" if lx > 0 else "right", fontsize=12, fontweight="bold", color=col)
    ax.set_yticks(y); ax.set_yticklabels(list(d["label"]), fontsize=13.5, color=INK)
    ax.set_xlim(0, 100); ax.set_ylim(-0.6, len(d) - 0.3)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xlabel("Australia's percentile among OECD peers  (higher = ranks better)", fontsize=13)
    _spine(ax, keep=("bottom",)); ax.tick_params(axis="y", length=0)
    # key
    ax.annotate("○ 2010", xy=(2, len(d) - 1.05), color=MUTED, fontsize=11.5, va="center")
    ax.annotate("● 2023", xy=(14, len(d) - 1.05), color=INK, fontsize=11.5, fontweight="bold", va="center")
    _titleblock(fig, "Australia didn't stand still — it slid on almost everything lived",
                "Percentile among OECD peers, 2010 → 2023 · red = collapse (≥20 pts), amber = fell, teal = rose")
    _source(fig, "Source: OECD How's Life? (status-A). Peer panels differ by year (n varies); the biggest lived drops sit on full n=47 / n≥36 panels, so they are robust.")
    fig.subplots_adjust(left=0.185, right=0.95, top=0.82, bottom=0.11)
    return _save(fig, "05_trajectory.png")


# ---------------------------------------------------------------- Chart 6 (slide): peer debt
def fig_peers():
    import pandas as pd
    hd = pd.read_csv(H.EXTERNAL / "household_debt_oecd.csv")
    peers = [("AUS", "Australia"), ("GBR", "United Kingdom"), ("USA", "United States"),
             ("CAN", "Canada"), ("NZL", "New Zealand")]
    fig, ax = plt.subplots(figsize=(12.4, 6.9))
    end = []
    for code, name in peers:
        s = hd[(hd.REF_AREA == code) & (hd.TIME_PERIOD <= 2024)].sort_values("TIME_PERIOD")
        if s.empty:
            continue
        x = s.TIME_PERIOD.to_numpy(); yv = s.OBS_VALUE.to_numpy()
        if code == "AUS":
            ax.plot(x, yv, color=LIVED, lw=3.4, zorder=5, solid_capstyle="round")
            pk = int(x[np.argmax(yv)]); pv = yv.max()
            ax.scatter([pk], [pv], color=LIVED, s=60, zorder=6, edgecolor="white", linewidth=1.2)
            ax.annotate(f"2018 peak {pv:.0f}%", xy=(pk, pv), xytext=(0, 12), textcoords="offset points",
                        ha="center", fontsize=10.5, color=LIVED)
        else:
            ax.plot(x, yv, color="#B9B5AC", lw=1.8, zorder=3)
        end.append((x[-1], yv[-1], name, code))
    # de-overlapped end labels
    for x1, y1, name, code in sorted(end, key=lambda e: e[1]):
        c = LIVED if code == "AUS" else MUTED
        w = "bold" if code == "AUS" else "normal"
        ax.annotate(f"{name}  {y1:.0f}%", xy=(x1, y1), xytext=(8, 0), textcoords="offset points",
                    va="center", ha="left", fontsize=11.5 if code == "AUS" else 10.5, color=c, fontweight=w)
    ax.set_xlim(2010, 2025.6)
    ax.set_xticks(range(2010, 2025, 2))
    ax.set_xlabel("Year", fontsize=13)
    ax.set_ylabel("Household debt  (% of net disposable income)", fontsize=12.5)
    _spine(ax, keep=("left", "bottom"))
    _titleblock(fig, "Australians owe more than their peers — and never deleveraged",
                "Household debt as a share of disposable income, 2010 → 2024", x=0.045)
    _source(fig, "Source: OECD household-debt SDMX. % of net household disposable income (NOT debt-to-GDP). Anglo peers shown; NZ series ends 2023.")
    fig.subplots_adjust(left=0.09, right=0.82, top=0.82, bottom=0.12)
    return _save(fig, "06_peers.png")


# ---------------------------------------------------------------- Chart 7 (slide): pooling catch
def fig_dataquality():
    df = load()
    s = au_series(df, "negative_affect")
    years = s["TIME_PERIOD"].astype(int).tolist()
    vals = s["OBS_VALUE"].astype(float).tolist()
    # reconstruct the "as delivered" forward-filled annual series
    ffx, ffy = [], []
    for i, (yr, v) in enumerate(zip(years, vals)):
        end = years[i + 1] if i + 1 < len(years) else 2026  # 2023-25 pool covers through 2025
        for yy in range(int(yr), int(end)):
            if yy <= 2025:
                ffx.append(yy); ffy.append(v)

    fig, ax = plt.subplots(figsize=(12.0, 6.4))
    ax.step(ffx, ffy, where="post", color="#B9B5AC", lw=2.4, zorder=2,
            label="As delivered — forward-filled (looks annual)")
    ax.scatter(years, vals, color=LIVED, s=150, zorder=4, edgecolor="white", linewidth=1.6,
               label="Real Gallup observations (6)")
    for yr, v in zip(years, vals):
        ax.annotate(str(yr), xy=(yr, v), xytext=(0, 12), textcoords="offset points",
                    ha="center", fontsize=10.5, color=LIVED)
    n_app = len(ffx); fake = 1 - (len(years) - 1) / (n_app - 1)
    ax.annotate(f"{n_app} apparent annual points → {len(years)} real observations.\n"
                f"~{fake*100:.0f}% of year-to-year 'change' was forward-fill, not signal.",
                xy=(0.02, 0.05), xycoords="axes fraction", ha="left", va="bottom", fontsize=12, color=INK,
                bbox=dict(boxstyle="round,pad=0.5", fc="white", ec=HAIRLINE, lw=1.1))
    ax.set_xlim(2009.5, 2025.5); ax.set_xticks(range(2010, 2026, 2))
    ax.set_xlabel("Year", fontsize=13)
    ax.set_ylabel("% reporting negative affect  (higher = worse)", fontsize=12.5)
    ax.legend(loc="upper left", frameon=False, fontsize=11.5, bbox_to_anchor=(0.0, 1.02))
    _spine(ax, keep=("left", "bottom"))
    _titleblock(fig, "The data isn't annual: 16 'yearly' points are really 6",
                "Australia, negative affect — why we never trend these series annually")
    _source(fig, "Source: OECD How's Life? (Gallup World Poll). Subjective series are 3-year pooled samples; same correction applies to lack of social support.")
    fig.subplots_adjust(left=0.09, right=0.97, top=0.82, bottom=0.12)
    return _save(fig, "07_dataquality.png")


# ---------------------------------------------------------------- Chart 1b (slide): heatmap
def fig_heatmap():
    import matplotlib as mpl
    from matplotlib.colors import Normalize
    from matplotlib.patches import Rectangle
    import pandas as pd
    df = load()
    t = H.au_percentile_table(df)
    obj = t[t["role"] == "objective"].sort_values("au_percentile")   # ascending
    liv = t[t["role"] == "lived"].sort_values("au_percentile")
    rows = list(liv.itertuples()) + list(obj.itertuples())           # lived bottom, objective top
    n = len(rows); ncut = len(liv)
    cmap = mpl.colormaps["RdYlGn"]; norm = Normalize(0, 100)

    fig, ax = plt.subplots(figsize=(9.8, 7.3))
    for i, r in enumerate(rows):
        ax.add_patch(Rectangle((0, i + 0.05), 1, 0.9, facecolor=cmap(norm(r.au_percentile)),
                               edgecolor="white", linewidth=2.5))
        tc = "white" if r.au_percentile <= 32 else "#1b1b1b"
        ax.annotate(f"{r.au_percentile:.0f}", (0.5, i + 0.58), ha="center", va="center",
                    fontsize=18, fontweight="bold", color=tc)
        ax.annotate(f"n={r.n}", (0.5, i + 0.3), ha="center", va="center", fontsize=9.5, color=tc)
    ax.set_yticks([i + 0.5 for i in range(n)]); ax.set_yticklabels([r.label for r in rows], fontsize=13.5)
    ax.set_xlim(0, 1); ax.set_ylim(0, n); ax.set_xticks([])
    ax.axhline(ncut, color=INK, lw=1.6, zorder=5)               # divider between blocks
    for s in ("top", "right", "left", "bottom"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    # block labels on the right
    ax.annotate("OBJECTIVE", (1.06, ncut + len(obj) / 2), rotation=90, va="center", ha="center",
                fontsize=12.5, fontweight="bold", color="#1e8449", annotation_clip=False)
    ax.annotate("LIVED", (1.06, ncut / 2), rotation=90, va="center", ha="center",
                fontsize=12.5, fontweight="bold", color="#c0392b", annotation_clip=False)
    # colorbar
    sm = mpl.cm.ScalarMappable(cmap=cmap, norm=norm); sm.set_array([])
    cb = fig.colorbar(sm, ax=ax, fraction=0.045, pad=0.11)
    cb.set_ticks([0, 25, 50, 75, 100]); cb.set_ticklabels(["0", "25", "50\nmedian", "75", "100"])
    cb.ax.tick_params(labelsize=10, color=HAIRLINE); cb.outline.set_edgecolor(HAIRLINE)
    cb.set_label("AU percentile vs OECD peers", fontsize=11, color=MUTED)

    _titleblock(fig, "Australia scores high on what's measured, low on what's lived",
                "AU percentile @2023 · objective block glows green, lived block sinks red", x=0.02)
    _source(fig, "Source: OECD How's Life? (status-A). Sign-flipped so higher = better; per-cell n = countries with 2023 data (panels 24–47).")
    fig.subplots_adjust(left=0.24, right=0.86, top=0.82, bottom=0.06)
    return _save(fig, "08_heatmap.png")


if __name__ == "__main__":
    made = [fig_split(), fig_heatmap(), fig_matrix(), fig_divergence(), fig_trajectory(),
            fig_dataquality(), fig_fragility(), fig_peers()]
    for m in made:
        p = OUT / m
        assert p.exists() and p.stat().st_size > 5000, f"{m} missing/too small"
        print(f"wrote {m}  ({p.stat().st_size//1024} KB)")
    print("all slide charts OK ->", OUT)
