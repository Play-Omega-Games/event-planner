#!/usr/bin/env python3
"""Write data/*.json from the library modules. Run after editing library.py, drafts.py or links.py."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from library import TASKS, PHASES, EVENT_TYPES, BUDGET_CATEGORIES, VENUES, FOOD, ALCOHOL, ENTRY, SIZES, HELP, COUNTRIES
from drafts import DRAFTS
from links import LINKS
OUT = os.path.join(os.path.dirname(HERE), "data")
os.makedirs(OUT, exist_ok=True)
def w(name, obj):
    json.dump(obj, open(os.path.join(OUT, name), "w"), ensure_ascii=False, indent=1)
w("tasks.json", {"phases": PHASES, "tasks": TASKS})
w("event_types.json", {"types": EVENT_TYPES, "answers": {"venue": VENUES, "food": FOOD, "alcohol": ALCOHOL, "entry": ENTRY, "size": SIZES, "help": HELP, "country": COUNTRIES}})
w("budget.json", {"categories": BUDGET_CATEGORIES,
                  "note": "Every amount comes from your own quotes and costs. Categories start empty."})
w("drafts.json", {"drafts": DRAFTS})
w("links.json", {"links": {k: {c: ([{"label": a, "url": u, "expect": e} for a, u, e in v] if c != "generic" else v) for c, v in t.items()} for k, t in LINKS.items()}})
print(f"wrote data/: {len(TASKS)} tasks, {len(DRAFTS)} drafts, {len(LINKS)} link topics")
