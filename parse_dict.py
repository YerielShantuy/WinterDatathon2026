"""Parse the OECD How's Life definitions PDF (pre-extracted to scratchpad) into a
clean definitions.md. 84 entries, 4 fields each: name+unit / type / definition / source.
Tags each entry present in OECD Data.csv (the 21-indicator subset) with [IN CSV]."""
import re

SCRATCH = r"C:/Users/YERIEL~1/AppData/Local/Temp/claude/c--Users-Yeriel-Putra-Harsono-Documents-Claude/54c14db8-e2f7-427e-b415-2f3afeff8a23/scratchpad"
RAW = SCRATCH + "/dict_raw.txt"
OUT = "definitions.md"
CSV = "OECD Data.csv"

FIELDS = ["Indicator and unit of measurement", "Type of indicator", "Definition", "Source"]


HEADER = re.compile(r"OECD HOW.?S LIFE\?? WELL-BEING DATABASE:?\s*DEFINITIONS AND METADATA\s*\d*",
                    re.I)


def clean(s: str) -> str:
    s = s.replace("===PAGE===", " ")
    s = HEADER.sub(" ", s)                         # strip running page header/footer + page no.
    s = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", s)   # de-hyphenate line breaks
    s = re.sub(r"\s*\n\s*", " ", s)                # newlines -> space
    s = re.sub(r"\s{2,}", " ", s)                  # collapse spaces
    return s.strip()


def parse(text: str):
    # split on the entry-start label; keep the label
    parts = re.split(r"(?m)^\s*(?=Indicator and unit of measurement:)", text)
    entries = []
    for blk in parts:
        if "Indicator and unit of measurement:" not in blk:
            continue
        rec = {}
        for i, f in enumerate(FIELDS):
            nxt = FIELDS[i + 1] if i + 1 < len(FIELDS) else None
            pat = re.escape(f) + r":\s*(.*?)" + (r"(?=" + re.escape(nxt) + r":)" if nxt else r"\Z")
            m = re.search(pat, blk, re.S)
            rec[f] = clean(m.group(1)) if m else ""
        if rec["Definition"]:
            entries.append(rec)
    return entries


# The 21 indicators present in OECD Data.csv, mapped to a distinctive substring of
# their (longer) dictionary name. CSV uses short names, the dict uses full ones, so
# token-overlap matching is unreliable — an explicit map is correct and auditable.
CSV_KEYWORDS = {
    "Household disposable income per capita": "net adjusted disposable income",
    "Median net wealth": "median net wealth",
    "Top income quintile (S80/S20)": "top 20%",
    "Housing affordability": "remaining, after deductions",
    "Overcrowding": "overcrowded",
    "Employment rate": "Employed people aged 25-64",
    "Long hours in paid work": "50+ hours",
    "Gender wage gap": "male and female median wages",
    "Life expectancy": "Life expectancy at birth",
    "Deaths of despair": "suicide",
    "Student maths skills": "students in maths",
    "Air pollution (PM2.5)": "PM2.5",
    "Extreme temperature": "hot days for at least two weeks",
    "Life satisfaction": "Mean values on an 11-point scale",
    "Negative affect balance": "more negative than positive feelings",
    "Time in social interactions": "Time spent interacting with friends and family",
    "Lack of social support": "count on",
    "Time off (leisure)": "leisure and personal care",
    "Gender gap in working hours": "women work, relative",
    "Voter turnout": "votes cast among the population registered",
    "Not having a say in government": "score equal to 6 or above",
}


def in_csv(name):
    return any(kw.lower() in name.lower() for kw in CSV_KEYWORDS.values())


def main():
    text = open(RAW, encoding="utf-8").read()
    entries = parse(text)
    assert len(entries) >= 80, f"expected ~84 entries, got {len(entries)}"
    assert all(e["Definition"] for e in entries), "an entry has empty definition"

    # validate the map: every CSV keyword must hit exactly one dictionary entry
    names = [e["Indicator and unit of measurement"] for e in entries]
    for label, kw in CSV_KEYWORDS.items():
        hits = sum(kw.lower() in n.lower() for n in names)
        assert hits == 1, f"keyword for '{label}' matched {hits} entries (want 1): {kw!r}"

    lines = [
        "# OECD How's Life? Well-being Database — Definitions & Metadata",
        "",
        "Full data dictionary extracted from `oecd-well-being-database-definitions.pdf` "
        "(June 2026, 43 pp, 84 indicators of the 80+ Well-being Dashboard).",
        "`[IN CSV]` = present in `OECD Data.csv` (the 21-indicator subset you have data for). "
        "Untagged = wider dashboard, reference/citation only (pull values from the OECD "
        "Well-being Data Monitor if needed).",
        "",
    ]
    n_csv = 0
    for e in entries:
        name = e["Indicator and unit of measurement"]
        tag = ""
        if in_csv(name):
            tag = " `[IN CSV]`"
            n_csv += 1
        lines += [
            f"## {name}{tag}",
            f"- **Type:** {e['Type of indicator']}",
            f"- **Source:** {e['Source']}",
            "",
            e["Definition"],
            "",
        ]
    open(OUT, "w", encoding="utf-8").write("\n".join(lines))
    print(f"wrote {OUT}: {len(entries)} indicators, {n_csv} tagged [IN CSV]")


if __name__ == "__main__":
    main()
