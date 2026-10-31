"""Offline checks for the event planner data, plan builder, budget math and skill drafts.
Run: python3 tests/test_planner.py (or python3 -m pytest tests -q)."""
import datetime as dt, itertools, json, os, re, string, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from build_plan import build
from budget import summary

try:
    import pytest; Skip = pytest.skip.Exception
except ImportError:
    class Skip(Exception): pass

def need(path, why):
    """Skip a check whose inputs are not in this checkout (the source texts or the bot's skill drafts)."""
    if not os.path.exists(path):
        raise Skip(why)

def load(n): return json.load(open(os.path.join(ROOT, "data", n)))
TASKS, DRAFTS, LINKS, BUD, TYPES = load("tasks.json"), load("drafts.json")["drafts"], load("links.json")["links"], load("budget.json"), load("event_types.json")
EM, EN = "\u2014", "\u2013"
D = dt.date
ANS = TYPES["answers"]

def profile(**kw):
    p = dict(business_name="Shop", owner_name="Sam", today="2026-11-09", type="launch", event_name="Test", date="2027-02-01",
             venue="own", size="medium", food="light", alcohol="none", entry="rsvp", budget_total=2000, help="team", country="US", time_window="6 to 9 PM")
    p.update(kw); return p

def all_profiles():
    for ty, ve, fo, al, en, sz in itertools.product(TYPES["types"], ANS["venue"], ANS["food"], ANS["alcohol"], ANS["entry"], ["small", "xl"]):
        yield profile(type=ty, venue=ve, food=fo, alcohol=al, entry=en, size=sz)

def test_library_shape():
    ids = [t["id"] for t in TASKS["tasks"]]
    assert len(ids) == len(set(ids)) and len(ids) >= 60
    phases = [p for p, _ in TASKS["phases"]]
    for t in TASKS["tasks"]:
        assert t["phase"] in phases and t["priority"] in (1, 2, 3)
        assert t["offset"] >= t["latest"], t["id"]
        assert set(t["when"]) <= {"type", "venue", "food", "alcohol", "entry", "size", "help"}, t["id"]
        for k, v in t["when"].items():
            pool = list(TYPES["types"]) if k == "type" else ANS[k]
            assert set(v) <= set(pool), (t["id"], k, v)
        assert t["draft"] is None or t["draft"] in {d["id"] for d in DRAFTS}, t["id"]
        assert t["link"] is None or t["link"] in LINKS, t["id"]
        assert set(t["after"]) <= set(ids), t["id"]
        assert t["title"] and t["why"] and t["why"].endswith((".", "?"))

def test_every_draft_used_or_on_demand():
    used = {t["draft"] for t in TASKS["tasks"] if t["draft"]}
    on_demand = {"vendor_decline", "weather_update"}
    assert {d["id"] for d in DRAFTS} <= used | on_demand

def test_budget_has_no_starting_split_or_cushion():
    assert set(BUD) == {"categories", "note"}, set(BUD)
    assert [c for c, _ in BUD["categories"]] == ["venue", "food", "people", "marketing", "decor", "supplies", "permits"]
    shipped = json.dumps([TASKS, BUD, TYPES], ensure_ascii=False).lower()
    for bad in ("split", "contingency", "10%", "percent of", "guideline is to keep"):
        assert bad not in shipped, bad

def test_all_combinations_build_cleanly():
    n = 0
    for p in all_profiles():
        plan = build(p); n += 1
        E = D.fromisoformat(plan["meta"]["event_date"]); today = D.fromisoformat(p["today"])
        for t in plan["tasks"]:
            d = D.fromisoformat(t["due"])
            assert today <= d <= E + dt.timedelta(days=14), (p, t["id"], t["due"])
            if t["phase"] not in ("day", "wrap"):
                assert d < E or t["phase"] == "day", (t["id"], t["due"])
        assert all(l["planned"] is None for l in plan["budget"]["lines"]) and plan["budget"]["total"] == p["budget_total"]
        assert plan["budget"]["cushion_pct"] is None
        assert plan["meta"]["mode"] in ("full", "compressed", "sprint")
    assert n > 1000

def test_dependencies_respected():
    after = {t["id"]: t["after"] for t in TASKS["tasks"]}
    for runway_date in ("2027-03-01", "2026-12-20", "2026-11-25", "2026-11-16"):
        for p in all_profiles():
            p["date"] = runway_date
            plan = build(p); due = {t["id"]: t["due"] for t in plan["tasks"]}
            for tid, deps in after.items():
                for dep in deps:
                    if tid in due and dep in due and plan["tasks"][[t["id"] for t in plan["tasks"]].index(tid)]["phase"] not in ("day", "wrap"):
                        assert due[dep] <= due[tid], (runway_date, p["type"], p["venue"], dep, tid, due[dep], due[tid])

def test_conditions_drive_tasks():
    ids = lambda **kw: {t["id"] for t in build(profile(**kw))["tasks"]}
    assert {"charity_permission", "raffle_check", "donor_receipts", "donation_count"} <= ids(type="fundraiser")
    assert not {"charity_permission", "raffle_check"} & ids(type="launch")
    assert {"weather_plan", "weather_call", "venue_book", "site_visit"} <= ids(venue="outdoor")
    assert "own_layout" in ids(venue="own") and "venue_book" not in ids(venue="own")
    assert {"alcohol_plan", "alcohol_license"} <= ids(alcohol="sold")
    assert "alcohol_license" not in ids(alcohol="served") and "alcohol_plan" in ids(alcohol="served")
    assert not {"caterer_quotes", "final_count"} & ids(food="none")
    assert {"popup_inventory", "sales_tax"} <= ids(type="popup")
    assert "signup_setup" not in ids(entry="free") and "rsvp_reminder" in ids(entry="tickets")
    assert "staff_brief" not in ids(help="solo")

def test_full_compressed_sprint():
    full = build(profile(date="2027-06-01"))
    assert full["meta"]["mode"] == "full" and not any(t["rush"] for t in full["tasks"])
    found = [t for t in full["tasks"] if t["phase"] == "foundations"]
    assert all(D.fromisoformat(t["due"]) <= D(2026, 11, 9) + dt.timedelta(days=14) for t in found)
    comp = build(profile(date="2026-12-20", venue="rented"))
    assert comp["meta"]["mode"] == "compressed"
    for t in comp["tasks"]:
        lib = next(x for x in TASKS["tasks"] if x["id"] == t["id"])
        if not t["rush"] and lib["latest"] <= comp["meta"]["runway_days"] and lib["offset"] > 0:
            assert (D(2026, 12, 20) - D.fromisoformat(t["due"])).days >= min(lib["latest"], 1) or t["id"] in lib["after"], t["id"]
    sprint = build(profile(date="2026-11-18", venue="rented"))
    assert sprint["meta"]["mode"] == "sprint"
    assert all(t["priority"] < 3 for t in sprint["tasks"])
    assert any(t["rush"] for t in sprint["tasks"]) and sprint["warnings"]
    rush_days = {t["due"] for t in sprint["tasks"] if t["rush"]}
    assert len(rush_days) >= 2, "rush items should be spread over a few days"
    same_day = build(profile(date="2026-11-09"))
    assert all(t["phase"] in ("day", "wrap") for t in same_day["tasks"])

def test_vendor_contact_not_on_weekends_before_event_week():
    for date in ("2027-03-06", "2027-01-17", "2026-12-12"):
        for p in all_profiles():
            p["date"] = date
            plan = build(p); E = D.fromisoformat(date)
            for t in plan["tasks"]:
                d = D.fromisoformat(t["due"])
                if t["vendor_contact"] and (E - d).days > 7 and not t["rush"]:
                    assert d.weekday() < 5, (date, t["id"], t["due"])

def test_no_date_uses_working_date():
    plan = build(profile(date=None, type="fundraiser"))
    assert not plan["meta"]["date_locked"] and plan["meta"]["event_date"] == (D(2026, 11, 9) + dt.timedelta(days=84)).isoformat()
    assert "working date" in plan["warnings"][0]

def test_budget_from_owner_numbers_only():
    for kw in ({}, {"venue": "own"}, {"food": "none", "alcohol": "none"}, {"budget_total": None}, {"type": "fundraiser"}):
        bud = build(profile(**kw))["budget"]
        assert all(l["planned"] is None for l in bud["lines"]) and "starting_pct" not in json.dumps(bud)
        assert bud["cushion_pct"] is None and set(bud) == {"total", "cushion_pct", "lines", "note", "income"}
        assert all(i["expected"] is None and i["received"] is None for i in bud["income"])
    assert build(profile(cushion_pct=8))["budget"]["cushion_pct"] == 8   # only when the owner typed it
    # an empty tracker reports zeros and empty slots, never a suggested amount
    empty = {"total": 2000, "cushion_pct": None, "plan": {c: None for c, _ in BUD["categories"]}, "lines": [], "income": []}
    s = summary(empty, today=D(2026, 11, 9), headcount=40, ticket_price=15)
    assert s["committed"] == 0 and s["remaining"] == 2000 and s["cushion"] is None and s["cushion_left"] is None
    assert s["over_categories"] == [] and len(s["empty_categories"]) == 7
    assert s["cost_per_guest"] == 0 and s["break_even_tickets"] == 0
    assert all(c["planned"] is None for c in s["categories"].values())

def test_budget_math():
    b = {"total": 2000, "cushion_pct": None, "plan": {"venue": None, "food": 600, "decor": None},
         "lines": [{"category": "food", "item": "Catering", "estimate": 500, "quote": 700, "actual": None, "deposit": 200,
                    "deposit_due": "2026-11-10", "deposit_paid": True, "balance_due": "2026-11-20", "paid": False},
                   {"category": "venue", "item": "Hall", "estimate": 400, "quote": None, "actual": 380, "paid": True},
                   {"category": "decor", "item": "Balloons", "estimate": 50, "deposit": 20, "deposit_due": "2026-11-05", "deposit_paid": False}],
         "income": [{"source": "Tickets", "expected": 900, "received": 300}, {"source": "Sponsorships", "expected": 500, "received": 500}]}
    s = summary(b, today=D(2026, 11, 9), headcount=50, ticket_price=20)
    assert s["committed"] == 700 + 380 + 50 and s["paid"] == 200 + 380
    assert s["remaining"] == 2000 - 1130 and not s["over_total"]
    assert s["over_categories"] == ["food"]   # only against the owner's own target
    assert s["cushion"] is None and s["cushion_left"] is None and s["remaining_before_cushion"] is None
    assert s["empty_categories"] == []
    assert [p["item"] for p in s["overdue_payments"]] == ["Balloons"]
    assert {p["item"] for p in s["upcoming_payments"]} == {"Balloons", "Catering"}
    assert next(p for p in s["upcoming_payments"] if p["item"] == "Catering")["amount"] == 500
    assert s["cost_per_guest"] == round(1130 / 50, 2)
    assert s["break_even_tickets"] == 32   # (1130 - 500 sponsorship) / 20, rounded up
    assert s["net_so_far"] == 800 - 580 and s["net_projected"] == 1400 - 1130
    # owner-typed cushion: 8% of 2000 = 160
    b["cushion_pct"] = 8
    s = summary(b, today=D(2026, 11, 9))
    assert s["cushion"] == 160 and s["remaining_before_cushion"] == 2000 - 1130 - 160 and s["cushion_left"] == 160
    b["lines"].append({"category": "people", "item": "DJ", "quote": 800})
    s = summary(b, today=D(2026, 11, 9))
    assert s["remaining"] == 70 and s["cushion_left"] == 70 and s["remaining_before_cushion"] == -90
    b["lines"].append({"category": "supplies", "item": "Extras", "actual": 100})
    s = summary(b, today=D(2026, 11, 9))
    assert s["over_total"] and s["cushion_left"] == 0
    b["total"] = None
    s = summary(b, today=D(2026, 11, 9))
    assert s["cushion"] is None and s["remaining"] is None

def test_drafts_placeholders_known():
    known = {"event_name", "business_name", "owner_name", "event_type_lower", "headcount", "date_short", "date_long", "date_weekday",
             "time_window", "start_time", "venue_name", "venue_address", "food_style", "goal", "days_to_go", "sponsor_name"}
    for d in DRAFTS:
        names = {f for _, f, _, _ in string.Formatter().parse(d["skeleton"]) if f}
        assert names <= known, (d["id"], names - known)
        assert d["must_include"] and d["purpose"]

def test_draft_filler_never_invents():
    from draft import fill
    full = profile(headcount=40, venue_name="The Loft", venue_address="1 Main St", goal="40 sign-ups", start_time="6 PM")
    empty = {"type": "other"}
    for d in DRAFTS:
        a = fill(d["id"], full, D(2026, 11, 9)); b = fill(d["id"], empty, D(2026, 11, 9))
        assert "{" not in a and "}" not in a and "{" not in b, d["id"]
        for k in ("event name", "headcount", "date long", "venue name"):
            if "{" + k.replace(" ", "_") + "}" in d["skeleton"]:
                assert "[" + k + "]" in b, (d["id"], k)
    assert "Monday, February 1" in fill("invitation", full, D(2026, 11, 9))

BANNED_NAMES = re.compile(r"eventbrite|\bcanva\b|mailchimp|squareup|square pos|shopify|instagram|facebook|tiktok|\bx\.com|twitter|venmo|paypal|zelle|gmail|outlook|google|microsoft|zoom|peerspace|thumbtack|yelp", re.I)

def test_own_words_rules():
    blobs = [json.dumps(x, ensure_ascii=False) for x in (TASKS, DRAFTS, BUD, TYPES)]
    blobs += [json.dumps({k: v["generic"] for k, v in LINKS.items()})]
    for b in blobs:
        assert EM not in b and EN not in b
        assert not BANNED_NAMES.search(b), BANNED_NAMES.search(b).group(0)

def test_links_official_only():
    for topic, v in LINKS.items():
        assert v["generic"]
        for c, items in v.items():
            if c == "generic": continue
            assert c in ANS["country"]
            for it in items:
                assert re.match(r"^https://([a-z0-9.-]+\.)?(gov|gov\.uk|gov\.au|bizpal\.ca|ada\.gov|irs\.gov|sba\.gov|ready\.gov)(/|$)", it["url"]) or "bizpal.ca" in it["url"], it["url"]

def test_skills_rules():
    need(os.path.join(ROOT, "skills"), "skill drafts live with the bot, not in this repo")
    for f in os.listdir(os.path.join(ROOT, "skills")):
        s = open(os.path.join(ROOT, "skills", f), encoding="utf-8").read()
        assert EM not in s and EN not in s, f
        assert "Questions or ideas? Contact Omega Games at john@playomega.games." in s, f
        assert "allowCustom" in s, f
        for u in re.findall(r"https?://[^\s)\"'`]+", s):
            assert u.startswith("https://raw.githubusercontent.com/Play-Omega-Games/event-planner/main/"), (f, u)
        assert not BANNED_NAMES.search(s.replace("Google Calendar", "")), (f, BANNED_NAMES.search(s).group(0))
        low = s.lower()
        assert "never send" in low or "never sends" in low, f
        assert "drafts live in this chat only" in low, f
        assert "never save them into an email drafts folder" in low, f
        for m in re.finditer(r"drafts? folder", low):   # only ever mentioned as a prohibition
            ctx = low[max(0, m.start() - 60):m.start()]
            assert "never save" in ctx, (f, ctx)
        for bad in ("starting split", "omega's starting", "10%", "contingency", "guideline is to keep"):
            assert bad not in low, (f, bad)
        assert "Small Business Event Planner" not in s and "Event Planner for Small Business" in s, f

def test_names_and_ids():
    need(os.path.join(ROOT, "skills"), "skill drafts live with the bot, not in this repo")
    files = sorted(os.listdir(os.path.join(ROOT, "skills")))
    assert files == ["event-planner-drafting-desk.md", "event-planner-getting-started.md", "event-planner-weekly.md"], files
    for f in files:
        s = open(os.path.join(ROOT, "skills", f), encoding="utf-8").read()
        assert re.search(r"^name: " + re.escape(f[:-3]) + r"$", s, re.M), f

if __name__ == "__main__":
    fails = skips = 0
    for n, fn in list(globals().items()):
        if n.startswith("test_"):
            try: fn(); print("ok  ", n)
            except Skip as e: skips += 1; print("skip", n, e)
            except AssertionError as e: fails += 1; print("FAIL", n, str(e)[:300])
    print(f"{sum(1 for n in globals() if n.startswith('test_')) - fails - skips} passed, {fails} failed, {skips} skipped")
    sys.exit(1 if fails else 0)
