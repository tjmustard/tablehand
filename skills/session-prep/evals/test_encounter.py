"""Checks scripts/encounter.py against the worked examples in SRD 5.2.1. Run: python3 evals/test_encounter.py"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "scripts"))
from encounter import rate

# SRD example 1: four level 1 characters, Low budget 200; one CR 1 creature (200 XP) fits Low
assert rate([1] * 4, ["1"]) == {"total": 200, "budgets": {"Low": 200, "Moderate": 300, "High": 400}, "tier": "Low", "crs": ["1"]}
# SRD example 2: five level 3 characters, Moderate budget 1,125; 2 x CR 2 + 9 x CR 1/8 = 1,125 XP
r = rate([3] * 5, ["2x2", "9x1/8"])
assert (r["total"], r["budgets"]["Moderate"], r["tier"]) == (1125, 1125, "Moderate")
# SRD example 3: six level 15 characters, High budget 46,800
assert rate([15] * 6, ["20"])["budgets"]["High"] == 46800
# mixed levels sum per character; no group multiplier; over High is flagged
assert rate([3, 3, 4], ["4", "2x1/8"]) == {"total": 1150, "budgets": {"Low": 550, "Moderate": 825, "High": 1300}, "tier": "High", "crs": ["4", "1/8", "1/8"]}
assert rate([1], ["5"])["tier"] == "Above High"
for bad in (([0], ["1"]), ([21], ["1"]), ([4], ["1/3"]), ([4], ["ax2"]), ([4], ["31"]), ([4], ["0x5"]), ([4], ["x4"]), ([4], ["101x1"]), ([4], ["2x2x2"]), ([4], ["5.5"])):
    try:
        rate(*bad)
    except ValueError:
        continue
    raise AssertionError(f"accepted {bad}")
# repeated flags add up instead of replacing each other
import contextlib, io
from encounter import main
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    main(["--levels", "4", "4", "--levels", "4", "4", "--monsters", "5", "--monsters", "2x1/2"])
assert "= 2,000 XP" in buf.getvalue() and "Party: 4 characters" in buf.getvalue(), buf.getvalue()
print("ok")
