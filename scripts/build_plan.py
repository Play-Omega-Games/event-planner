#!/usr/bin/env python3
"""Build a dated event plan, working back from the event date.

Usage: python3 scripts/build_plan.py profile.json [-o plan.json] [--md checklist.md]

Reads data/tasks.json, data/budget.json, data/event_types.json, data/links.json.
Scheduling rules:
- Each task has an ideal offset (days before the event) and a latest offset.
- Full plan: runway (event date minus today) covers every task's ideal offset.
- Compressed plan: tasks inside the final 14 days keep their dates; earlier
  tasks are squeezed proportionally into the runway, never later than their
  latest offset when that still fits.
- Sprint plan (14 days or less): nice-to-have tasks are dropped; tasks whose
  latest offset has passed become "rush" (due today) with a warning.
- Steps that mean contacting a business never land on a weekend before event
  week: they move to the Friday before (or the Monday after if that's past).
Nothing here sends anything. Drafts are for the owner to send.
"""
import datetime as dt, json, os, sys, math

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load(name): return json.load(open(os.path.join(ROOT, "data", name)))
PIVOT = 14

def matches(task, p):
    for k, allowed in task["when"].items():
        if p.get(k) not in allowed:
            return False
    return True

def weekend_shift(d, today, event):
    if d.weekday() < 5 or (event - d).days <= 7:
        return d
    fri = d - dt.timedelta(days=d.weekday() - 4)
    if fri >= today:
        return fri
    mon = d + dt.timedelta(days=7 - d.weekday())
    return mon if mon < event else d

def budget_lines(p, B):
    """One empty slot per category. Amounts come only from the owner's quotes and costs."""
    return [{"category": cid, "label": label, "planned": None} for cid, label in B["categories"]]

def build(p):
    T, B, E_T, L = load("tasks.json"), load("budget.json"), load("event_types.json"), load("links.json")["links"]
    today = dt.date.fromisoformat(p["today"])
    etype = E_T["types"][p["type"]]
    warnings = []
    if p.get("date"):
        event = dt.date.fromisoformat(p["date"]); locked = True
    else:
        event = today + dt.timedelta(days=etype["lead_days"]); locked = False
        warnings.append(f"No date yet, so this plan uses a working date of {event.isoformat()} ({etype['lead_days'] // 7} weeks out, Omega's suggested lead time for this kind of event). Lock a real date as soon as you can.")
    R = (event - today).days
    if R < 0:
        raise SystemExit("event date is in the past")
    tasks = [t for t in T["tasks"] if matches(t, p) and R >= t.get("min_runway", 0)]
    M = max([t["offset"] for t in tasks if t["offset"] > 0] or [0])
    mode = "full" if R >= M else ("compressed" if R > PIVOT else "sprint")
    if mode == "sprint":
        tasks = [t for t in tasks if t["priority"] < 3]
    if R == 0:
        tasks = [t for t in tasks if t["offset"] <= 0]
    out, rushed = [], []
    f_offsets = [t["offset"] for t in tasks if t["phase"] == "foundations"]
    f_lo = min(f_offsets or [0])
    for t in tasks:
        o, latest, rush = t["offset"], t["latest"], False
        if R > M and t["phase"] == "foundations" and M > f_lo:
            # long runway: make the foundation decisions in the first two weeks, in order
            o2 = max(o, R - round((M - o) * 14 / (M - f_lo)))
        elif o <= 0 or R >= M or o <= min(PIVOT, R):
            o2 = o
        elif latest > R:
            o2, rush = R, True
        elif mode == "compressed":
            o2 = PIVOT + round((o - PIVOT) * (R - PIVOT) / (M - PIVOT))
            o2 = max(min(o2, R), latest)
        else:   # sprint, latest still fits
            o2 = latest
        due = event - dt.timedelta(days=o2)
        if t["vendor_contact"] and o2 > 7:
            due = weekend_shift(due, today, event)
        item = {k: t[k] for k in ("id", "title", "why", "phase", "priority", "category", "draft", "link", "vendor_contact")}
        item.update(due=due.isoformat(), status="open", rush=rush, owner_sends=bool(t["draft"]))
        if t["link"]:
            topic = L[t["link"]]
            item["guidance"] = topic["generic"]
            item["official_links"] = topic.get(p.get("country", "other"), [])
        out.append(item)
        if rush:
            rushed.append(item)
    phase_order = [ph for ph, _ in T["phases"]]
    # spread rush items over the first few days, most foundational first
    rushed.sort(key=lambda x: (phase_order.index(x["phase"]), x["priority"]))
    span = max(1, min(3, R - 7))
    for i, item in enumerate(rushed):
        d = today + dt.timedelta(days=i * span // max(1, len(rushed)))
        if item["vendor_contact"] and d.weekday() >= 5:
            d += dt.timedelta(days=7 - d.weekday())
            if d >= event: d = today
        item["due"] = d.isoformat()
    # dependency pass: never due before what it depends on (stays before the event)
    by_id = {x["id"]: x for x in out}
    deps = {t["id"]: t.get("after", []) for t in tasks}
    for _ in range(3):
        for x in sorted(out, key=lambda y: y["due"]):
            prev = [by_id[d]["due"] for d in deps.get(x["id"], []) if d in by_id]
            if prev and max(prev) >= x["due"] and x["phase"] not in ("day", "wrap"):
                nd = dt.date.fromisoformat(max(prev)) + dt.timedelta(days=1)
                if x["vendor_contact"] and nd.weekday() >= 5 and (event - nd).days > 7:
                    nd += dt.timedelta(days=7 - nd.weekday())
                if nd < event:
                    x["due"] = nd.isoformat()
    out.sort(key=lambda x: (x["due"], phase_order.index(x["phase"]), x["priority"]))
    tight = [x["title"] for x in rushed if x["vendor_contact"] and x["priority"] == 1]
    if tight:
        warnings.append("These usually need more notice than you have, so check today whether they're still possible: " + "; ".join(tight) + ".")
    if mode == "compressed":
        warnings.append(f"The event is {R} days away, so the early steps are squeezed together." + (" Do the rush items first." if rushed else ""))
    if mode == "sprint":
        warnings.append(f"The event is {R} days away, so this is a sprint plan: must-dos first, nice-to-haves dropped.")
    return {
        "meta": {"event_name": p.get("event_name") or etype["label"], "type": p["type"], "type_label": etype["label"],
                 "event_date": event.isoformat(), "date_locked": locked, "today": today.isoformat(), "runway_days": R,
                 "mode": mode, "task_count": len(out), "country": p.get("country", "other")},
        "warnings": warnings,
        "tasks": out,
        "budget": {"total": p.get("budget_total"), "cushion_pct": p.get("cushion_pct"), "lines": budget_lines(p, B), "note": B["note"],
                   "income": [{"source": s, "expected": None, "received": None} for s in
                              (["Donations", "Sponsorships", "Tickets"] if p["type"] == "fundraiser" else
                               (["Tickets"] if p.get("entry") == "tickets" else []))]},
    }

def markdown(plan):
    m = plan["meta"]; L = [f"# {m['event_name']}: {m['type_label']} on {m['event_date']}", f"Plan: {m['mode']}, {m['runway_days']} days to go, {m['task_count']} steps", ""]
    for w in plan["warnings"]:
        L.append(f"> {w}")
    for t in plan["tasks"]:
        flag = " (rush)" if t["rush"] else ""
        L.append(f"- [ ] {t['due']}  {t['title']}{flag}" + ("  [draft ready, you send]" if t["owner_sends"] else ""))
    return "\n".join(L) + "\n"

if __name__ == "__main__":
    a = sys.argv[1:]
    p = json.load(open(a[0]))
    plan = build(p)
    out = a[a.index("-o") + 1] if "-o" in a else None
    s = json.dumps(plan, ensure_ascii=False, indent=1)
    if out: open(out, "w").write(s)
    else: print(s)
    if "--md" in a: open(a[a.index("--md") + 1], "w").write(markdown(plan))
