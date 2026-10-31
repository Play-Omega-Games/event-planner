#!/usr/bin/env python3
"""Budget tracker math. Every number comes from the owner; nothing is estimated,
suggested or split here. Categories start empty and fill from real quotes and costs.

Usage: python3 scripts/budget.py summary budget.json [--today YYYY-MM-DD] [--headcount N] [--ticket-price X] [--days 14]

budget.json:
{"total": 3000,                       # the owner's cap, or null
 "cushion_pct": null,                 # optional, only if the owner types one (for example 8); no default
 "plan": {"venue": null, "food": 900, ...},   # optional per-category target the owner sets; null = no target
 "lines": [{"category": "food", "item": "Catering", "vendor": "...", "estimate": 900, "quote": 950,
            "actual": null, "deposit": 300, "deposit_due": "2026-11-20", "deposit_paid": true,
            "balance_due": "2026-12-01", "paid": false}],
 "income": [{"source": "Tickets", "expected": 1200, "received": 400}]}
"Committed" for a line is its actual if set, else its quote, else the owner's own estimate.
"""
import datetime as dt, json, math, sys

def committed(l):
    for k in ("actual", "quote", "estimate"):
        if l.get(k) is not None:
            return l[k]
    return 0

def paid_so_far(l):
    if l.get("paid"):
        return committed(l)
    return (l.get("deposit") or 0) if l.get("deposit_paid") else 0

def summary(b, today=None, headcount=None, ticket_price=None, days=14):
    today = today or dt.date.today()
    total = b.get("total")
    pct = b.get("cushion_pct")
    if pct is not None and not (0 <= pct < 100):
        raise SystemExit("cushion_pct must be from 0 to under 100")
    cats = {}
    for c, target in (b.get("plan") or {}).items():
        cats[c] = {"planned": target, "committed": 0, "paid": 0, "lines": 0}
    for l in b.get("lines", []):
        c = cats.setdefault(l["category"], {"planned": None, "committed": 0, "paid": 0, "lines": 0})
        c["committed"] += committed(l); c["paid"] += paid_so_far(l); c["lines"] += 1
    spent_committed = sum(c["committed"] for c in cats.values())
    paid = sum(c["paid"] for c in cats.values())
    over = [k for k, c in cats.items() if c["planned"] is not None and c["committed"] > c["planned"]]
    cushion = None if (pct is None or total is None) else round(total * pct / 100, 2)
    room = None if total is None else total - spent_committed
    due = []
    for l in b.get("lines", []):
        if l.get("deposit") and not l.get("deposit_paid") and l.get("deposit_due"):
            due.append((l["deposit_due"], l["item"], "deposit", l["deposit"]))
        if not l.get("paid") and l.get("balance_due"):
            due.append((l["balance_due"], l["item"], "balance", committed(l) - (l.get("deposit") or 0)))
    horizon = today + dt.timedelta(days=days)
    upcoming = sorted(d for d in due if dt.date.fromisoformat(d[0]) <= horizon)
    overdue = [d for d in upcoming if dt.date.fromisoformat(d[0]) < today]
    income = b.get("income", [])
    income_exp = sum((i.get("expected") or 0) for i in income)
    income_rec = sum((i.get("received") or 0) for i in income)
    non_ticket_exp = sum((i.get("expected") or 0) for i in income if i["source"] != "Tickets")
    return {
        "total": total, "committed": spent_committed, "paid": paid,
        "remaining": room,
        "over_total": total is not None and spent_committed > total,
        "categories": cats, "over_categories": over,
        "empty_categories": [k for k, c in cats.items() if c["lines"] == 0],
        "cushion_pct": pct, "cushion": cushion,
        "remaining_before_cushion": None if cushion is None else room - cushion,
        "cushion_left": None if cushion is None else max(0, min(cushion, room)),
        "upcoming_payments": [{"date": d, "item": i, "kind": k, "amount": a} for d, i, k, a in upcoming],
        "overdue_payments": [{"date": d, "item": i, "kind": k, "amount": a} for d, i, k, a in overdue],
        "income_expected": income_exp, "income_received": income_rec,
        "net_so_far": income_rec - paid, "net_projected": income_exp - spent_committed,
        "cost_per_guest": None if not headcount else round(spent_committed / headcount, 2),
        "break_even_tickets": None if not ticket_price else math.ceil(max(0, spent_committed - non_ticket_exp) / ticket_price),
    }

if __name__ == "__main__":
    a = sys.argv[1:]
    b = json.load(open(a[1]))
    opt = lambda k, f: f(a[a.index(k) + 1]) if k in a else None
    print(json.dumps(summary(b, opt("--today", dt.date.fromisoformat), opt("--headcount", int), opt("--ticket-price", float), opt("--days", int) or 14), indent=1))
