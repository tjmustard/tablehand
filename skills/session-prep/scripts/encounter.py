#!/usr/bin/env python3
"""Rate a D&D 5e combat encounter with the SRD 5.2.1 XP budgets.

Usage: python3 encounter.py --levels 4 4 4 4 --monsters 4 2x1/8
  --levels    one level (1-20) per character, so four level-4 characters is 4 4 4 4
  --monsters  one CR per monster (0, 1/8, 1/4, 1/2, 1-30); NxCR repeats it N times (N from 1 to 100); flags may repeat

This work includes material from the System Reference Document 5.2.1 ("SRD 5.2.1")
by Wizards of the Coast LLC, available at https://www.dndbeyond.com/srd. The SRD 5.2.1
is licensed under the Creative Commons Attribution 4.0 International License, available
at https://creativecommons.org/licenses/by/4.0/legalcode.
"""
import argparse, sys

# SRD 5.2.1, "XP Budget per Character": level -> (Low, Moderate, High)
BUDGET = {1: (50, 75, 100), 2: (100, 150, 200), 3: (150, 225, 400), 4: (250, 375, 500),
          5: (500, 750, 1100), 6: (600, 1000, 1400), 7: (750, 1300, 1700), 8: (1000, 1700, 2100),
          9: (1300, 2000, 2600), 10: (1600, 2300, 3100), 11: (1900, 2900, 4100), 12: (2200, 3700, 4700),
          13: (2600, 4200, 5400), 14: (2900, 4900, 6200), 15: (3300, 5400, 7800), 16: (3800, 6100, 9800),
          17: (4500, 7200, 11700), 18: (5000, 8700, 14200), 19: (5500, 10700, 17200), 20: (6400, 13200, 22000)}
# SRD 5.2.1, "Experience Points by Challenge Rating". CR 0 is "0 or 10"; counted as 10 here.
XP = {"0": 10, "1/8": 25, "1/4": 50, "1/2": 100, "1": 200, "2": 450, "3": 700, "4": 1100, "5": 1800,
      "6": 2300, "7": 2900, "8": 3900, "9": 5000, "10": 5900, "11": 7200, "12": 8400, "13": 10000,
      "14": 11500, "15": 13000, "16": 15000, "17": 18000, "18": 20000, "19": 22000, "20": 25000,
      "21": 33000, "22": 41000, "23": 50000, "24": 62000, "25": 75000, "26": 90000, "27": 105000,
      "28": 120000, "29": 135000, "30": 155000}
TIERS = ("Low", "Moderate", "High")


def expand(items):
    """['4', '2x1/8'] -> ['4', '1/8', '1/8']"""
    out = []
    for it in items:
        n, x, cr = it.lower().rpartition("x")
        if cr not in XP or (x and not (n.isdigit() and 1 <= int(n) <= 100)):
            raise ValueError(f"not a CR: {it!r} (use 0, 1/8, 1/4, 1/2, 1-30, or NxCR with N from 1 to 100)")
        out += [cr] * (int(n) if x else 1)
    return out


def rate(levels, monsters):
    if not levels or any(lv not in BUDGET for lv in levels):
        raise ValueError("party levels must be whole numbers from 1 to 20")
    crs = expand(monsters)
    if not crs:
        raise ValueError("no monsters given")
    total = sum(XP[cr] for cr in crs)
    budgets = [sum(BUDGET[lv][i] for lv in levels) for i in range(3)]
    tier = next((TIERS[i] for i in range(3) if total <= budgets[i]), "Above High")
    return {"total": total, "budgets": dict(zip(TIERS, budgets)), "tier": tier, "crs": crs}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--levels", nargs="+", type=int, action="extend", required=True)
    ap.add_argument("--monsters", nargs="+", action="extend", required=True)
    a = ap.parse_args(argv)
    try:
        r = rate(a.levels, a.monsters)
    except ValueError as e:
        sys.exit(f"error: {e}")
    counts = {cr: r["crs"].count(cr) for cr in dict.fromkeys(r["crs"])}
    b = r["budgets"]
    print(f"Party: {len(a.levels)} character{'s' if len(a.levels) != 1 else ''}, levels {', '.join(map(str, a.levels))}")
    print("Monsters: " + ", ".join(f"{n} x CR {cr} ({XP[cr]:,} XP each)" for cr, n in counts.items())
          + f" = {r['total']:,} XP")
    print(f"XP budgets: Low {b['Low']:,} | Moderate {b['Moderate']:,} | High {b['High']:,}")
    if r["tier"] == "Above High":
        print(f"Difficulty: Above High ({r['total'] - b['High']:,} XP over the High budget; SRD 5.2.1 has no higher tier)")
    else:
        print(f"Difficulty: {r['tier']} ({r['total']:,} XP is within the {r['tier']} budget)")
    if "0" in counts:
        print("Note: CR 0 creatures are worth 0 or 10 XP; each was counted as 10.")


if __name__ == "__main__":
    main()
