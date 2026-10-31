"""Omega Games event planning library: the source for data/*.json.

All guidance is Omega Games' own writing. Rules:
- No invented facts or figures. Lead times are labeled Omega guidelines.
  The budget has no starting split and no default cushion: every amount comes
  from the owner's own quotes and costs. Legal and permit points are written generically ("ask your
  city or county") and link only to official government pages in links.py.
- Draft-only: every draft is for the owner to send. The bot never contacts
  vendors, guests, sponsors, press or officials.
- No em dashes. No third-party brand or product names.

Task fields:
  id, title, why, phase, offset (ideal days before the event; negative = after),
  latest (last sensible days before; tasks whose latest is already past are
  "rush"), priority (1 must, 2 should, 3 nice), when (conditions; every key
  must match the profile, values are allowed lists), category, draft (a draft
  id in DRAFTS or None), link (an id in links.py or None), vendor_contact
  (True if the step means the owner contacting a business during office hours).
"""

PHASES = [
    ("foundations", "Foundations"),
    ("book", "Book the big pieces"),
    ("promote", "Spread the word"),
    ("details", "Lock the details"),
    ("week", "Event week"),
    ("day", "Event day"),
    ("wrap", "Wrap up"),
]

EVENT_TYPES = {
    "launch": {"label": "Launch party", "lead_days": 56,
               "goal_examples": ["first-week sales", "sign-ups or pre-orders", "people who try the product"]},
    "workshop": {"label": "Workshop or class", "lead_days": 42,
                 "goal_examples": ["seats filled", "attendees who book a next session", "feedback score you set"]},
    "open_house": {"label": "Open house", "lead_days": 28,
                   "goal_examples": ["new faces through the door", "email sign-ups", "appointments booked"]},
    "popup": {"label": "Pop-up shop", "lead_days": 42,
              "goal_examples": ["sales", "new customers", "email or social follows"]},
    "fundraiser": {"label": "Fundraiser", "lead_days": 84,
                   "goal_examples": ["amount raised for the cause", "number of donors", "sponsors signed"]},
    "other": {"label": "Something else", "lead_days": 56,
              "goal_examples": ["turnout", "sales", "sign-ups"]},
}

# Profile answer values (getting-started questions)
VENUES = ["own", "rented", "outdoor", "host", "tbd"]            # my business, rented venue, outdoors/public space, someone else's shop or market, not sure yet
FOOD = ["none", "light", "meal", "sellers"]
ALCOHOL = ["none", "served", "sold"]
ENTRY = ["free", "rsvp", "tickets", "donations"]
SIZES = ["small", "medium", "large", "xl"]                      # under 25, 25 to 75, 75 to 200, over 200
HELP = ["solo", "team", "planner"]
COUNTRIES = ["US", "UK", "CA", "AU", "other"]

ANY_VENUE_OFFSITE = ["rented", "outdoor", "host", "tbd"]
BIGGER = ["medium", "large", "xl"]
SIGNUP = ["rsvp", "tickets", "donations"]

T = []
def task(id, title, why, phase, offset, latest, priority, when=None, category="plan", draft=None, link=None, vendor_contact=False):
    T.append(dict(id=id, title=title, why=why, phase=phase, offset=offset, latest=latest, priority=priority,
                  when=when or {}, category=category, draft=draft, link=link, vendor_contact=vendor_contact))

# 1. Foundations
task("goal", "Write the goal in one sentence and pick how you'll measure it",
     "Every later choice gets easier once you know what a win looks like. Pick one or two numbers you can actually count afterward.",
     "foundations", 84, 42, 1)
task("budget_cap", "Set your total budget cap",
     "Decide the number you won't go over before any quotes arrive. Every budget line then comes from your real quotes and costs. If you want a cushion for surprises, pick your own percentage and the tracker holds it back.",
     "foundations", 84, 42, 1, category="budget")
task("date_check", "Check the date against holidays, local events and your own busy days, and pick a backup date",
     "A clash with a big local event or a holiday weekend can empty the room. A backup date makes venue and vendor talks easier.",
     "foundations", 84, 49, 1)
task("guest_list", "Build the guest list and a headcount estimate",
     "Regulars, neighbors, partners, local groups, press. Headcount drives the space, the food and most of the budget.",
     "foundations", 80, 35, 1, category="guests")
task("roles", "Give each area one owner: guests, vendors, setup, social, money",
     "Even a team of two runs smoother when every area has exactly one person who decides.",
     "foundations", 77, 28, 2, when={"help": ["team", "planner"]})
task("permits_ask", "Ask your city or county what this event needs and how much notice they want",
     "Rules depend on where you are. Ask about event or temporary use permits, tents, amplified sound, signs, street or sidewalk use, food, alcohol and occupancy limits.",
     "foundations", 84, 28, 1, category="safety", link="permits", vendor_contact=True)
task("insurance_ask", "Call your insurance agent about this event",
     "Ask whether your policy covers this event, your guests and any off-site location, and whether you need a one-day event policy or liquor liability cover.",
     "foundations", 77, 28, 1, category="safety", link="insurance", vendor_contact=True)
task("charity_permission", "Confirm the cause and get written permission to use the charity's name and logo",
     "Charities usually approve how their name is used. Only a qualified charity can give donors a tax receipt, so agree up front who handles donations and receipts.",
     "foundations", 84, 42, 1, when={"type": ["fundraiser"]}, link="charity_receipts", vendor_contact=True)
task("fundraising_goal", "Set the fundraising goal and how you'll show progress",
     "A clear goal and a visible progress count give people a reason to give now. Use only real totals.",
     "foundations", 63, 21, 2, when={"type": ["fundraiser"]}, category="budget")
task("workshop_outline", "Outline the workshop: the outcome, the agenda and the materials",
     "People sign up for what they'll walk away with. Write the outcome in one line, then time the agenda in 15-minute blocks with a buffer at the end.",
     "foundations", 70, 28, 1, when={"type": ["workshop"]})
task("launch_ready", "Set a go or no-go date for the product or service being launched",
     "A launch with nothing to buy wastes the buzz. Decide now what has to be true by that date, and what happens if it slips.",
     "foundations", 70, 21, 1, when={"type": ["launch"]})
task("popup_host", "Shortlist host spaces or markets and ask about their terms",
     "Ask about fees or revenue share, hours, setup and pack-down times, what's provided (tables, power, Wi-Fi), insurance and how sales tax is handled.",
     "foundations", 70, 35, 1, when={"venue": ["host"]}, category="venue", draft="venue_inquiry", vendor_contact=True)

# 2. Book the big pieces
task("venue_inquiries", "Send venue inquiries to your top two or three spaces",
     "Same questions to each so quotes compare cleanly: dates, hours including setup and teardown, headcount, what's included, deposit and cancellation, insurance, end time and noise rules.",
     "book", 70, 35, 1, when={"venue": ["rented", "outdoor", "tbd"]}, category="venue", draft="venue_inquiry", vendor_contact=True)
task("site_visit", "Visit the space at the same time of day as the event",
     "Check light, noise, parking, power outlets, restrooms, step-free entry, the load-in path and phone signal. Take photos and measurements.",
     "book", 63, 28, 1, when={"venue": ANY_VENUE_OFFSITE}, category="venue")
task("venue_book", "Book the space and read the agreement before you sign",
     "Look for the deposit, the cancellation and weather terms, the hard end time, cleanup rules, insurance requirements and anything billed as extra. Get it in writing.",
     "book", 56, 21, 1, when={"venue": ANY_VENUE_OFFSITE}, category="venue", draft="booking_confirmation", vendor_contact=True)
task("own_layout", "Plan the layout of your own space",
     "Walk it as a guest: entry, check-in, where people gather, eat, buy and exit. Keep exits and aisles clear and know your space's occupancy limit.",
     "book", 49, 14, 1, when={"venue": ["own"]}, category="venue")
task("caterer_quotes", "Get two or three food quotes",
     "Share the headcount, service style, dietary needs and timing. Ask what's included (staff, rentals, cleanup), their deadline for the final headcount and their insurance.",
     "book", 56, 21, 1, when={"food": ["light", "meal"]}, category="vendors", draft="caterer_inquiry", vendor_contact=True)
task("caterer_book", "Book food and note the final headcount deadline on your plan",
     "Confirm the menu, service times, staffing, deposit and the date they need your final count. Put that date on the checklist.",
     "book", 49, 14, 1, when={"food": ["light", "meal"]}, category="vendors", draft="booking_confirmation", vendor_contact=True)
task("food_sellers", "Invite food trucks or sellers and collect their permits and insurance",
     "Sellers usually need their own food permits for temporary events. Ask for copies, their power and space needs, and arrival times.",
     "book", 56, 21, 1, when={"food": ["sellers"]}, category="vendors", draft="vendor_inquiry", link="permits", vendor_contact=True)
task("alcohol_plan", "Decide how drinks will be served and check the rules",
     "Serving free drinks and selling them often fall under different rules. Use a licensed bartender or caterer where required, check IDs, and ask your insurer about liquor liability.",
     "book", 56, 21, 1, when={"alcohol": ["served", "sold"]}, category="safety", link="permits")
task("alcohol_license", "If you're selling drinks, confirm the license or permit you need",
     "Selling alcohol without the right license is a serious risk. Your city, county or state licensing office can tell you what applies and how long it takes.",
     "book", 56, 28, 1, when={"alcohol": ["sold"]}, category="safety", link="alcohol", vendor_contact=True)
task("rentals", "Reserve rentals: tables, chairs, tent, linens, sound",
     "Busy dates book up. Confirm delivery and pickup windows, who sets up, and what happens if it rains.",
     "book", 49, 14, 2, when={"venue": ["rented", "outdoor", "tbd"], "size": BIGGER}, category="vendors", draft="rentals_inquiry", vendor_contact=True)
task("weather_plan", "Make a rain, heat and wind plan",
     "Decide your backup space or tent, your call time for moving or postponing, and who tells guests. Tents need proper weights or stakes; ask the rental company.",
     "book", 49, 14, 1, when={"venue": ["outdoor"]}, category="safety")
task("extras_book", "Book a photographer, entertainment or speaker if you want one",
     "Ask what they need from you (power, space, a meal, parking) and when they arrive. Agree on how photos can be used.",
     "book", 49, 21, 3, category="vendors", draft="vendor_inquiry", vendor_contact=True)
task("workshop_materials", "Order workshop materials and confirm any co-host",
     "Order a few extra sets. Confirm the co-host's timing, what they bring and how they're paid.",
     "book", 35, 10, 1, when={"type": ["workshop"]}, category="vendors")
task("signup_setup", "Set up RSVPs or tickets with a clear capacity",
     "Use one sign-up tool, cap it at what the space can hold, and ask only what you need: name, email, dietary and access needs, and permission for follow-up emails.",
     "book", 49, 21, 1, when={"entry": SIGNUP}, category="guests")
task("popup_inventory", "Plan inventory, pricing and payments",
     "Count what you'll bring, price everything clearly, test your card reader including what happens without internet, and plan a cash float.",
     "book", 42, 10, 1, when={"type": ["popup"]}, category="budget")
task("sales_tax", "Check sales tax for selling at this location",
     "Selling at a temporary location can mean collecting tax there. Ask your tax office or accountant, or the market organizer.",
     "book", 42, 14, 1, when={"type": ["popup"]}, category="budget", link="taxes")
task("sponsors", "Ask local businesses for sponsorship or in-kind donations",
     "Offer something concrete in return: a thank-you on signs and posts, a table, a mention from the stage. Ask early; budgets get set ahead.",
     "book", 63, 28, 2, when={"type": ["fundraiser"]}, category="budget", draft="sponsor_ask", vendor_contact=True)
task("raffle_check", "Check the rules before any raffle, auction or game of chance",
     "Many places restrict raffles to registered charities and require a permit. Check before you sell a single ticket.",
     "book", 63, 35, 1, when={"type": ["fundraiser"]}, category="safety", link="gaming")
task("accessibility", "Plan for accessibility",
     "Step-free entry, a route without obstacles, seating, an accessible restroom, clear signs, a microphone or captions for talks. Ask guests about access needs when they sign up.",
     "book", 42, 14, 1, category="safety", link="accessibility")
task("vendor_coi", "Collect certificates of insurance from vendors",
     "Many venues require them, and they protect you if a vendor's equipment or staff cause damage or injury. Ask whether the venue needs to be named on them.",
     "book", 28, 10, 2, when={"venue": ANY_VENUE_OFFSITE}, category="vendors", draft="coi_request", vendor_contact=True)

# 3. Spread the word
task("save_the_date", "Send a save-the-date to your key guests",
     "Busy people fill their calendars early. A short note now beats a perfect invite later.",
     "promote", 49, 28, 2, when={"size": BIGGER}, category="guests", draft="save_the_date")
task("invitation", "Send the invitation",
     "What, when, where, why it's worth coming, and one clear way to respond. Personal invites to your top guests work best.",
     "promote", 35, 14, 1, category="guests", draft="invitation")
task("announce_post", "Post the announcement",
     "Lead with why it's worth coming, then the date, time, place and how to sign up.",
     "promote", 35, 10, 1, category="promo", draft="social_announce")
task("listings", "List the event on local event calendars and your business profiles",
     "Many local calendars are free. Use the same short description everywhere.",
     "promote", 35, 7, 2, category="promo", draft="listing_blurb")
task("in_store", "Tell regulars in person, on signs and with your receipts",
     "Your best guests are already walking through the door.",
     "promote", 28, 7, 2, when={"venue": ["own"]}, category="promo")
task("partner_share", "Ask partners and vendors to share the event",
     "Give them ready-to-post text and an image so it takes them a minute.",
     "promote", 28, 7, 3, category="promo", draft="partner_share")
task("press_note", "Send a short note to local press or newsletters",
     "Keep it to what's new, who it helps and the key details, with a contact for questions.",
     "promote", 28, 10, 3, when={"type": ["launch", "fundraiser"]}, category="promo", draft="press_note")
task("bts_post", "Post a behind-the-scenes look",
     "Prep photos, a sneak peek or the people involved keep the event in people's feeds.",
     "promote", 21, 5, 3, category="promo", draft="social_bts")
task("launch_moment", "Plan the launch moment",
     "Decide what happens at the peak of the event: the reveal, a short welcome, a first sale or demo. Keep any talk under five minutes.",
     "promote", 21, 7, 2, when={"type": ["launch"]})
task("open_house_demo", "Set up a reason to walk in and something to try",
     "A demo station, a tour time, a small offer for visitors, or a chance to meet the team.",
     "promote", 21, 7, 2, when={"type": ["open_house"]})
task("rsvp_reminder", "Send an RSVP or ticket reminder",
     "A friendly nudge with the key details and the sign-up link.",
     "promote", 10, 5, 1, when={"entry": SIGNUP}, category="guests", draft="rsvp_reminder")
task("go_no_go", "Check sign-ups against your minimum and decide go or no-go",
     "If you set a minimum, decide now while guests and vendors can still be told kindly.",
     "promote", 10, 5, 1, when={"type": ["workshop"]}, category="guests")
task("countdown_post", "Post a one-week countdown",
     "Short, upbeat and specific: one thing guests will see, try or get.",
     "promote", 7, 5, 2, category="promo", draft="social_countdown")

# 4. Lock the details
task("run_of_show", "Write the run of show, from setup to teardown",
     "Who does what, when and where, with every vendor's arrival time and contact. Share it with your team and vendors.",
     "details", 14, 5, 1, draft="run_of_show")
task("vendor_confirm", "Confirm every vendor in writing",
     "Arrival time, setup location, contact on the day, what they bring, final amount and when it's due.",
     "details", 10, 4, 1, category="vendors", draft="vendor_final_details", vendor_contact=True)
task("final_count", "Give the caterer your final headcount by their deadline",
     "Use RSVPs plus what you know about your own past turnout. Check the date they gave you.",
     "details", 7, 3, 1, when={"food": ["light", "meal"]}, category="vendors", vendor_contact=True)
task("signs_print", "Order signs, name tags, menus and handouts",
     "Wayfinding from the street, a welcome sign, prices for pop-ups, the sign-up or social handle at check-in.",
     "details", 14, 5, 2, category="promo")
task("staff_brief", "Brief staff and volunteers",
     "One page: the goal, the schedule, each person's job, where things are, who to ask, and what to do if something goes wrong.",
     "details", 7, 2, 1, when={"help": ["team", "planner"]}, draft="staff_brief")
task("checkin_flow", "Plan check-in and how you'll capture contacts",
     "A short line, a printed list as a backup, and a simple way for walk-ins to leave an email with permission.",
     "details", 10, 3, 2, when={"entry": SIGNUP}, category="guests")
task("safety_plan", "Write a one-page safety plan",
     "Exits, first aid kit, who calls emergency services and from where, a plan for a lost child or a medical issue, and the venue contact's number.",
     "details", 10, 3, 1, when={"size": BIGGER}, category="safety", link="emergency")
task("payments_due", "Pay deposits and balances on time",
     "Check the payment dates on the budget tracker. Late balances can cost you the booking.",
     "details", 14, 3, 1, category="budget")
task("photo_consent", "Plan photos and consent",
     "Tell guests photos will be taken, offer a no-photo option, and ask before posting close-ups, especially of children.",
     "details", 10, 2, 2, category="safety")
task("music_rights", "Check music rights",
     "Playing recorded music at a public or business event may need a public performance license. Ask your venue whether it already holds one.",
     "details", 14, 5, 3, category="safety")
task("event_kit", "Pack the event kit",
     "Tape, scissors, zip ties, extension cords, chargers, pens, a first aid kit, trash bags, cleaning supplies, spare batteries and printed copies of the run of show.",
     "details", 5, 1, 2)
task("know_before", "Send the know-before-you-go note",
     "Parking, entrance, accessibility, what to bring, the start time and a phone number for the day.",
     "details", 3, 1, 1, when={"entry": SIGNUP}, category="guests", draft="know_before_you_go")
task("weather_call", "Check the forecast and make the weather call",
     "Decide at the call time you set and tell guests and vendors the same day.",
     "details", 3, 1, 1, when={"venue": ["outdoor"]}, category="safety", draft="weather_update")
task("popup_display", "Set up your table or display once at home and photograph it",
     "A practice setup shows what's missing and makes the real one twice as fast.",
     "details", 7, 2, 2, when={"type": ["popup"]})

# 5. Event week, 6. Event day
task("walkthrough", "Walk through the space with your run of show",
     "Stand where guests enter and go step by step. Fix anything confusing now.",
     "week", 2, 1, 1)
task("day_before_post", "Post a day-before reminder",
     "Tomorrow, the time, the place and one reason not to miss it.",
     "week", 1, 1, 2, category="promo", draft="social_day_before")
task("setup_test", "Set up and test sound, lights, Wi-Fi and payments before doors open",
     "Leave enough time that you're greeting guests, not fixing cables.",
     "day", 0, 0, 1)
task("run_event", "Run the event: greet people, capture contacts, take photos, enjoy it",
     "Name one person to watch the clock and one to watch the door.",
     "day", 0, 0, 1)
task("live_post", "Share a live photo or story",
     "One good photo during the peak moment is plenty.",
     "day", 0, 0, 3, category="promo", draft="social_live")
task("donation_count", "Count and record donations with two people present",
     "Two people, a written tally and a photo of the total protect everyone.",
     "day", 0, 0, 1, when={"type": ["fundraiser"]}, category="budget")
task("teardown", "Tear down, count cash and leave the space as you found it",
     "Check the agreement's cleanup terms and take photos of the space when you leave.",
     "day", 0, 0, 1)

# 7. Wrap up
task("thank_guests", "Thank your guests",
     "Within a day or two, while it's fresh. Include photos, a next step or an offer.",
     "wrap", -1, -3, 1, category="guests", draft="thank_you_guests")
task("thank_vendors", "Thank vendors, partners and volunteers",
     "A short, specific thank-you builds the team for next time. Offer a review if they did well.",
     "wrap", -2, -5, 1, category="vendors", draft="thank_you_vendors")
task("recap_post", "Post a recap with photos",
     "Thank people by name only with their permission, and share the result if it's good news.",
     "wrap", -2, -7, 2, category="promo", draft="social_recap")
task("follow_up", "Follow up with new contacts and buyers",
     "The people who came are your warmest leads. Follow up while they remember you.",
     "wrap", -3, -10, 1, when={"type": ["launch", "popup", "open_house", "workshop", "other"]}, category="guests", draft="follow_up")
task("donor_receipts", "Make sure donors get receipts and thank-yous from the charity",
     "Agree who sends what, and share the real total raised.",
     "wrap", -3, -14, 1, when={"type": ["fundraiser"]}, category="budget", link="charity_receipts")
task("survey", "Send a short feedback survey",
     "Three or four questions at most, sent within a few days.",
     "wrap", -2, -7, 3, category="guests", draft="feedback_survey")
task("reconcile", "Pay final invoices and close out the budget",
     "Enter every actual cost so the tracker shows the true total and what to change next time.",
     "wrap", -7, -14, 1, category="budget")
task("results", "Compare results with your goal and write down what to repeat and what to change",
     "Three things to keep, three to change, while it's fresh.",
     "wrap", -7, -14, 1)

TASKS = T

# Budget categories: empty slots the owner fills from real quotes and costs.
# No starting split, no suggested amounts and no default cushion. An owner may
# set their own cushion percentage; it is never suggested.
BUDGET_CATEGORIES = [
    ("venue", "Venue and rentals"),
    ("food", "Food and drink"),
    ("people", "Staff, entertainment and speakers"),
    ("marketing", "Marketing and printing"),
    ("decor", "Decor and signage"),
    ("supplies", "Supplies, materials and giveaways"),
    ("permits", "Permits, licenses and insurance"),
]

# Order rules: a task is never due before the tasks it depends on (when both are in the plan).
AFTER = {
    "site_visit": ["venue_inquiries", "popup_host"],
    "venue_book": ["venue_inquiries", "popup_host", "site_visit"],
    "caterer_book": ["caterer_quotes"],
    "final_count": ["caterer_book"],
    "vendor_coi": ["venue_book", "caterer_book", "food_sellers", "rentals", "extras_book"],
    "vendor_confirm": ["venue_book", "caterer_book", "food_sellers", "rentals", "extras_book", "workshop_materials"],
    "invitation": ["goal", "date_check"],
    "rsvp_reminder": ["invitation", "signup_setup"],
    "know_before": ["invitation", "rsvp_reminder"],
    "announce_post": ["goal"],
    "countdown_post": ["announce_post"],
    "go_no_go": ["signup_setup"],
    "run_of_show": ["venue_book", "own_layout"],
    "staff_brief": ["run_of_show"],
    "alcohol_license": ["alcohol_plan"],
    "sponsors": ["fundraising_goal"],
    "weather_call": ["weather_plan"],
}
for t in TASKS:
    t["after"] = AFTER.get(t["id"], [])

# Skip a task when the runway is shorter than this many days (it no longer makes sense).
MIN_RUNWAY = {"save_the_date": 28, "press_note": 14, "sponsors": 21, "survey": 0}
for t in TASKS:
    t["min_runway"] = MIN_RUNWAY.get(t["id"], 0)
