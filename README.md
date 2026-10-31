# 📋 Event Planner for Small Business

Planning data and scripts for the Event Planner for Small Business bot.

- `data/tasks.json`: the step library (phases, ideal and latest timing, conditions, order rules).
- `data/event_types.json`, `data/budget.json`, `data/drafts.json`, `data/links.json`: event types, budget categories (empty slots filled from your own quotes), draft templates, official links.
- `scripts/build_plan.py profile.json -o plan.json`: a dated plan working back from the event date (full, compressed or sprint).
- `scripts/budget.py summary budget.json`: budget tracker totals from your own numbers: committed, paid, payments due, your optional cushion, cost per guest, break-even, net.
- `scripts/draft.py DRAFT_ID profile.json`: fills a draft with known details, leaving the rest as [blanks].
- `scripts/check_links.py`: live check of every official link.
- `scripts/library.py`, `scripts/drafts.py`, `scripts/links.py` + `scripts/export_data.py`: the editable source of `data/`.
- `tests/test_planner.py`: offline checks.

Everything the bot writes is a draft for the business owner to send. The planner never contacts anyone. Permit, insurance and tax pointers are general; your local office has the final word.

Questions or ideas? Contact Omega Games at john@playomega.games.
