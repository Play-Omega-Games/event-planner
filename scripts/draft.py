#!/usr/bin/env python3
"""Fill a draft skeleton from the profile. Unknown details stay as visible [blanks].

Usage: python3 scripts/draft.py DRAFT_ID profile.json [--today YYYY-MM-DD]
The result is a starting point for the drafting desk to rewrite in natural words.
It never invents a value: anything missing from the profile prints as [field name].
"""
import datetime as dt, json, os, string, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TYPES = json.load(open(os.path.join(ROOT, "data", "event_types.json")))["types"]
FOOD = {"light": "snacks or light bites", "meal": "a catered meal", "sellers": "food trucks or sellers"}

class Blank(dict):
    def __missing__(self, k):
        return "[" + k.replace("_", " ") + "]"

def fields(p, today):
    f = Blank()
    for k in ("event_name", "business_name", "owner_name", "time_window", "venue_name", "venue_address", "goal", "start_time", "sponsor_name"):
        if p.get(k): f[k] = p[k]
    if p.get("type"): f["event_type_lower"] = TYPES[p["type"]]["label"].lower()
    if p.get("headcount"): f["headcount"] = str(p["headcount"])
    if p.get("food") in FOOD: f["food_style"] = FOOD[p["food"]]
    if p.get("date"):
        d = dt.date.fromisoformat(p["date"])
        f["date_long"] = f"{d:%A, %B} {d.day}"
        f["date_short"] = f"{d:%b} {d.day}"
        f["date_weekday"] = f"{d:%A}"
        f["days_to_go"] = str((d - today).days)
    return f

def fill(draft_id, p, today=None):
    drafts = {d["id"]: d for d in json.load(open(os.path.join(ROOT, "data", "drafts.json")))["drafts"]}
    d = drafts[draft_id]
    return string.Formatter().vformat(d["skeleton"], (), fields(p, today or dt.date.today()))

if __name__ == "__main__":
    a = sys.argv[1:]
    today = dt.date.fromisoformat(a[a.index("--today") + 1]) if "--today" in a else None
    print(fill(a[0], json.load(open(a[1])), today))
