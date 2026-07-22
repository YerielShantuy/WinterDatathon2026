"""Shared data-prep contract for the Winter Datathon notebook.

Every chart module imports from here. Do NOT re-implement loading or sign-flipping
in a chart — call these. `value_flipped` is ALREADY signed (higher = better for
every indicator); never flip it again.

Data: data/oecd_wellbeing_clean_{AUS,ROW}.csv (handle schema) + country_coverage.csv.
Root oecd_wellbeing_clean.csv is SUPERSEDED (forward-filled subjective series) — unused.
"""
from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parent / "data"
EXTERNAL = Path(__file__).resolve().parent / "external"

# --- constants (see nextsteps.md) ---
ANCHOR = 2023  # uniform cross-section year for Level x Momentum / percentile charts
POOLED_HANDLES = ["negative_affect", "lack_of_support"]  # 3-yr Gallup pools, 6 real pts
CALLOUT_HANDLES = ["gdp_per_capita_wb", "life_satisfaction"]  # never in composite/matrix

# 9 core handles that make up the composite + matrix
CORE_HANDLES = [
    "disposable_income", "housing_affordability", "employment_rate", "long_hours",
    "gender_wage_gap", "life_expectancy", "deaths_despair", "negative_affect",
    "lack_of_support",
]

# readable labels for charts
LABELS = {
    "disposable_income": "Disposable income",
    "housing_affordability": "Housing affordability",
    "employment_rate": "Employment rate",
    "long_hours": "Long working hours",
    "gender_wage_gap": "Gender wage gap",
    "life_expectancy": "Life expectancy",
    "deaths_despair": "Deaths of despair",
    "negative_affect": "Negative affect",
    "lack_of_support": "Lack of social support",
    "gdp_per_capita_wb": "GDP per capita",
    "life_satisfaction": "Life satisfaction",
}


def load(status_a_only: bool = True) -> pd.DataFrame:
    """Full 47-country long table. status_a_only drops B/D/E/P (provisional/estimated)."""
    aus = pd.read_csv(DATA / "oecd_wellbeing_clean_AUS.csv")
    row = pd.read_csv(DATA / "oecd_wellbeing_clean_ROW.csv")
    df = pd.concat([row, aus], ignore_index=True)
    df["TIME_PERIOD"] = df["TIME_PERIOD"].astype(int)
    if status_a_only:
        df = df[df["OBS_STATUS"] == "A"].copy()
    return df


def coverage() -> pd.DataFrame:
    return pd.read_csv(DATA / "country_coverage.csv")


def panel(df: pd.DataFrame, handle: str, year: int) -> pd.Series:
    """value_flipped for one handle at one year, indexed by REF_AREA (higher = better)."""
    s = df[(df["handle"] == handle) & (df["TIME_PERIOD"] == year)]
    return s.set_index("REF_AREA")["value_flipped"]


def au_percentile(df: pd.DataFrame, handle: str, year: int = ANCHOR):
    """AU percentile within the peer panel at `year`. Returns (pctile, n) or (None, n).

    Percentile = share of countries AU beats on value_flipped (higher = better).
    """
    v = panel(df, handle, year)
    n = len(v)
    if "AUS" not in v.index or n == 0:
        return None, n
    return round(100 * (v < v["AUS"]).mean(), 1), n


def au_series(df: pd.DataFrame, handle: str) -> pd.DataFrame:
    """AU time series for one handle: TIME_PERIOD, OBS_VALUE, value_flipped, pool cols."""
    s = df[(df["handle"] == handle) & (df["REF_AREA"] == "AUS")].copy()
    cols = ["TIME_PERIOD", "OBS_VALUE", "value_flipped", "pooled", "pool_idx", "pool_midyear"]
    cols = [c for c in cols if c in s.columns]
    return s[cols].sort_values("TIME_PERIOD").reset_index(drop=True)


def household_debt() -> pd.DataFrame:
    """AU household debt, % of net disposable income (higher = worse). Cols: year, debt_pct."""
    hd = pd.read_csv(EXTERNAL / "household_debt_oecd.csv")
    # find the AU rows + the year/value cols robustly (SDMX csv column names vary)
    area_col = next((c for c in hd.columns if c.upper() in ("REF_AREA", "REFERENCE AREA")), None)
    year_col = next((c for c in hd.columns if c.upper() in ("TIME_PERIOD", "TIME")), None)
    val_col = next((c for c in hd.columns if c.upper() in ("OBS_VALUE", "VALUE")), None)
    au = hd[hd[area_col].astype(str).str.upper().isin(["AUS", "AUSTRALIA"])].copy()
    out = au[[year_col, val_col]].rename(columns={year_col: "year", val_col: "debt_pct"})
    out["year"] = out["year"].astype(int)
    return out.sort_values("year").reset_index(drop=True)


def au_percentile_table(df: pd.DataFrame, year: int = ANCHOR) -> pd.DataFrame:
    """Headline table: AU percentile per core handle at `year`, with role/domain/n."""
    meta = df.groupby("handle")[["role", "domain"]].first()
    rows = []
    for h in CORE_HANDLES:
        pct, n = au_percentile(df, h, year)
        rows.append({"handle": h, "label": LABELS[h], "role": meta.loc[h, "role"],
                     "domain": meta.loc[h, "domain"], "n": n, "au_percentile": pct})
    return pd.DataFrame(rows).sort_values("au_percentile").reset_index(drop=True)


if __name__ == "__main__":
    df = load()
    assert df["REF_AREA"].nunique() == 47, "expected 47 countries"
    assert (df["OBS_STATUS"] == "A").all(), "status filter failed"
    t = au_percentile_table(df)
    assert len(t) == 9, "expected 9 core handles"
    obj = t[t.role == "objective"]["au_percentile"].mean()
    lived = t[t.role == "lived"]["au_percentile"].mean()
    assert obj > lived, "thesis broken: objective should outrank lived"
    hd = household_debt()
    assert hd["year"].is_monotonic_increasing and len(hd) >= 14, "household debt series bad"
    print(f"OK | countries={df['REF_AREA'].nunique()} | core handles={len(t)}")
    print(f"AU percentile @ {ANCHOR}: objective={obj:.1f}  lived={lived:.1f}")
    print(f"household debt AU: {hd['year'].min()}-{hd['year'].max()}, {len(hd)} pts")
