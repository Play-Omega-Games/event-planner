"""Draft templates for the drafting desk. Omega Games' own words.
Every draft is for the owner to review, edit and send themselves.
Placeholders in {braces} are filled from the profile and plan; anything the
bot doesn't know stays as a visible [bracketed blank] for the owner to fill.
"""
D = []
def draft(id, name, audience, purpose, must_include, skeleton, channel="email"):
    D.append(dict(id=id, name=name, audience=audience, purpose=purpose, must_include=must_include,
                  skeleton=skeleton.strip(), channel=channel))

# Vendors
draft("venue_inquiry", "Venue or host space inquiry", "vendor",
      "Get comparable quotes and terms from two or three spaces.",
      ["event type and goal", "date and backup date", "hours including setup and teardown", "headcount", "food and drink plans",
       "questions: what's included, deposit and cancellation, weather policy, insurance requirements, end time and noise rules, accessibility, load-in and parking, preferred or required vendors"],
      """
Subject: Event inquiry for {date_short}: {event_name}

Hi [name],

I run {business_name} and I'm planning a {event_type_lower} for about {headcount} guests on {date_long}, from {time_window}, with a backup date of [backup date]. We'd need access from [setup time] for setup and until [teardown time] to clear out.

Could you tell me:
1. Is the space available on either date, and what's the cost for those hours?
2. What's included (tables, chairs, sound, Wi-Fi, cleanup), and what's extra?
3. The deposit, payment dates, and cancellation and weather terms?
4. Insurance you require from us and from our vendors?
5. Any rules on end time, noise, decorations, food, drink or outside vendors?
6. Step-free access, restrooms, parking and the load-in route?

Happy to visit. Thanks so much,
{owner_name}
{business_name}
""")
draft("caterer_inquiry", "Caterer inquiry", "vendor",
      "Get comparable food quotes.",
      ["headcount", "service style", "timing", "dietary needs", "what's included", "final headcount deadline", "insurance and permits"],
      """
Subject: Catering quote for {date_short}: about {headcount} guests

Hi [name],

I'm planning a {event_type_lower} on {date_long} at {venue_name}, with food served from [serving time]. We expect about {headcount} guests and are thinking of {food_style}.

Could you send a quote, including:
1. Suggested menu and price per person or per item
2. Staff, rentals, setup and cleanup: included or extra?
3. How you handle allergies and dietary needs ([list any you know])
4. Deposit, payment dates and cancellation terms
5. The date you need our final headcount
6. Your insurance certificate and any permits for serving at {venue_name}

Thank you,
{owner_name}
""")
draft("vendor_inquiry", "Vendor inquiry (photographer, entertainment, speaker, food seller)", "vendor",
      "Check availability, price and needs for one vendor.",
      ["what you want them to do", "date, times, place", "audience size", "their needs (power, space, parking)", "price, deposit, cancellation", "insurance or permits where relevant"],
      """
Subject: Are you free on {date_short}? {event_name}

Hi [name],

I'm planning {event_name}, a {event_type_lower} for about {headcount} guests on {date_long} at {venue_name}, {time_window}. I'd love to have you [what you'd do].

Could you let me know your availability and rate, what you'd need from us on the day (power, space, parking, a meal), your deposit and cancellation terms, and [insurance certificate or permits, if relevant]?

Thanks,
{owner_name}
""")
draft("rentals_inquiry", "Rentals inquiry", "vendor",
      "Reserve tables, chairs, tent, linens or sound.",
      ["item list with quantities", "delivery and pickup windows", "who sets up", "weather and cancellation terms", "deposit"],
      """
Subject: Rental quote for {date_short}

Hi [name],

Could you quote the following for {date_long} at {venue_address}?
[item and quantity list]

Please include delivery and pickup windows, whether your team sets up, the deposit, and your terms for weather and cancellation.

Thank you,
{owner_name}
""")
draft("booking_confirmation", "Booking confirmation (put the deal in writing)", "vendor",
      "Recap the agreed terms so both sides have the same record.",
      ["date and times", "what's included", "price, deposit, balance and due dates", "cancellation terms as you understood them", "contact on the day"],
      """
Subject: Confirming {event_name} on {date_short}

Hi [name],

Thanks for confirming. Here's what I have, so we're on the same page:
- Date and times: {date_long}, access from [time], event {time_window}, cleared by [time]
- Included: [list]
- Price: [total], deposit [amount] paid on [date], balance [amount] due [date]
- Cancellation and weather: [as agreed]
- Day-of contact: {owner_name}, [phone]

Please let me know if anything here differs from your records.

Best,
{owner_name}
""")
draft("coi_request", "Certificate of insurance request", "vendor",
      "Collect proof of a vendor's insurance before the event.",
      ["event name, date and place", "what the venue requires", "deadline"],
      """
Subject: Insurance certificate for {event_name}

Hi [name],

Could you send a certificate of insurance for {event_name} on {date_long} at {venue_name} by [date]? [The venue asks to be listed as additional insured: venue legal name and address.]

Thanks so much,
{owner_name}
""")
draft("vendor_final_details", "Final details to a vendor", "vendor",
      "Confirm logistics a week or so out.",
      ["arrival and setup time and place", "parking and load-in", "day-of contact", "what they bring", "final amount and when it's paid"],
      """
Subject: Final details for {date_short}: {event_name}

Hi [name],

Looking forward to {date_weekday}! The final details:
- Arrival: [time] at [entrance], setup in [location]
- Parking and load-in: [details]
- Doors open {start_time}; you're on from [time] to [time]
- Day-of contact: [name], [phone]
- Final amount: [amount], paid [how and when]

Anything you need from us before then?

Thanks,
{owner_name}
""")
draft("thank_you_vendors", "Thank-you to vendors, partners and volunteers", "vendor",
      "Say thanks specifically and keep the relationship.",
      ["one specific thing they did well", "the result if good", "an offer of a review or referral"],
      """
Subject: Thank you for {event_name}

Hi [name],

Thank you for [specific thing]. [A guest said, or a result, only if real.] It made a real difference, and I'd be glad to [leave a review / recommend you].

Hope to work together again,
{owner_name}
""")
draft("vendor_decline", "Polite no-thank-you to a vendor not chosen", "vendor",
      "Close the loop kindly with vendors who quoted.",
      ["thanks for the quote", "brief reason if comfortable", "door open for next time"],
      """
Subject: Thanks for your quote

Hi [name],

Thank you for the quote for {event_name}. We've gone another way this time, but I appreciated your quick, clear reply and would be glad to ask you again.

Best,
{owner_name}
""")
draft("sponsor_ask", "Sponsorship or in-kind donation ask", "sponsor",
      "Invite a local business to support the fundraiser.",
      ["the cause and goal", "the ask (amount or item)", "what they get in return", "deadline", "that the charity has approved the use of its name, if it has"],
      """
Subject: Would {sponsor_name} help us support [cause]?

Hi [name],

On {date_long}, {business_name} is hosting {event_name} to raise money for [cause], with a goal of [goal]. I'm reaching out to a few neighbors we admire.

Would you consider [the ask]? In return we'd [thank you on signs and posts / a table / a mention from the stage]. If you can let me know by [date], we'll include you in all the materials.

Thank you for considering it,
{owner_name}
""")

# Guests
draft("save_the_date", "Save the date", "guest",
      "Get the date on calendars early.",
      ["what, when, where (or the area)", "one line on why", "invite to follow"],
      """
Subject: Save the date: {event_name}, {date_short}

Mark your calendar: {event_name} at {venue_name} on {date_long}. [One line on why it's worth coming.] The full invitation is coming soon.

{owner_name}, {business_name}
""")
draft("invitation", "Invitation", "guest",
      "Invite guests with everything they need to say yes.",
      ["the hook", "date, time, place", "what to expect", "how to respond and by when", "access or parking note"],
      """
Subject: You're invited: {event_name}, {date_short}

Hi [first name],

[The hook in one or two sentences.]

When: {date_long}, {time_window}
Where: {venue_name}, {venue_address}
What to expect: [food, demo, talk, shopping, the cause]

[RSVP or get tickets: link, by date]. [Parking, entrance or accessibility note.]

Hope to see you there,
{owner_name}
""")
draft("rsvp_reminder", "RSVP or ticket reminder", "guest",
      "Nudge people who haven't responded.",
      ["friendly tone", "key details", "the link and deadline"],
      """
Subject: Still hoping to see you on {date_weekday}

Quick reminder that {event_name} is on {date_long}, {time_window}, at {venue_name}. [One reason to come.] [RSVP link] by [date] so we can plan for you.
""")
draft("know_before_you_go", "Know before you go", "guest",
      "Smooth arrival for confirmed guests.",
      ["start time", "address and entrance", "parking or transit", "accessibility", "what to bring", "a contact for the day"],
      """
Subject: See you tomorrow: {event_name}

We're all set for tomorrow, {date_long}, from {start_time}.
- Address and entrance: {venue_address}, [entrance]
- Parking: [details]
- Accessibility: [step-free entrance, seating, restrooms]
- Bring: [ticket, ID, nothing at all]
- Questions on the day: [phone]
""")
draft("weather_update", "Weather update", "guest",
      "Tell guests and vendors the weather call, the same day it's made.",
      ["the decision", "what changes", "what stays the same"],
      """
Subject: Weather update for {event_name}

[We're still on, moving inside to (place) / postponing to (date).] [What guests should do differently.] Everything else stays the same. Thanks for rolling with it!
""")
draft("thank_you_guests", "Thank-you to guests", "guest",
      "Thank guests and give them a next step.",
      ["thanks", "a highlight or real result", "a next step or offer", "photos link if any"],
      """
Subject: Thank you for coming to {event_name}

Thank you for joining us on {date_weekday}. [A highlight, or the real total raised.] [Photos link.]

[Next step: an offer, the next session, a way to stay in touch.]

{owner_name}
""")
draft("follow_up", "Follow-up to new contacts", "guest",
      "Turn a visit into a relationship, only for people who agreed to hear from you.",
      ["personal touch", "one clear next step"],
      """
Subject: Great to meet you at {event_name}

Hi [first name], thanks for stopping by. [Something specific you talked about.] [One next step: an offer, a booking link, a question.]

{owner_name}
""")
draft("feedback_survey", "Feedback survey", "guest",
      "Learn what to repeat and change.",
      ["three or four short questions", "one open question"],
      """
Subject: Two minutes to help us do it better?

1. How would you rate {event_name}? (1 to 5)
2. What was the best part?
3. What would you change?
4. Would you come to the next one? (Yes, maybe, no)
""")

# Social and promo
draft("social_announce", "Announcement post", "social", "Announce the event.",
      ["hook", "date, time, place", "how to sign up", "one image idea"],
      "[Hook]. Join us for {event_name} on {date_short}, {time_window}, at {venue_name}. [What's happening.] [Sign-up link or 'no RSVP needed'.] [Image idea.]",
      channel="post")
draft("social_bts", "Behind-the-scenes post", "social", "Keep momentum.",
      ["a real prep moment", "the date"],
      "[A real prep moment.] {event_name} is {days_to_go} days away. [Small teaser.]", channel="post")
draft("social_countdown", "One-week countdown post", "social", "Remind and excite.",
      ["one specific thing guests will see or get", "date, time, place"],
      "One week until {event_name}! [One specific thing.] {date_short}, {time_window}, {venue_name}.", channel="post")
draft("social_day_before", "Day-before post", "social", "Last call.",
      ["tomorrow", "time and place", "one reason"],
      "Tomorrow! {event_name}, {time_window} at {venue_name}. [One reason not to miss it.]", channel="post")
draft("social_live", "Live post", "social", "Share the moment.",
      ["one photo idea", "short caption"], "[Photo idea.] We're live at {venue_name} until [time]. Come say hi!", channel="post")
draft("social_recap", "Recap post", "social", "Thank and show the result.",
      ["thanks", "best photo idea", "real result only if shared"],
      "Thank you to everyone who came to {event_name}! [Real highlight or result.] [Thanks to partners, with their permission.]",
      channel="post")
draft("partner_share", "Ready-to-share text for partners", "social", "Make it easy for partners to promote.",
      ["short text", "date and link"],
      "We're excited to be part of {event_name} with {business_name} on {date_short} at {venue_name}! [Link.]", channel="post")
draft("listing_blurb", "Event listing blurb", "social", "One description for every calendar.",
      ["50 to 80 words", "what, when, where, cost, how to sign up"],
      "{event_name}: [what it is in one sentence]. {date_long}, {time_window}, at {venue_name}, {venue_address}. [Cost or free.] [How to sign up.]",
      channel="listing")
draft("press_note", "Local press or newsletter note", "press", "Pitch a short story.",
      ["what's new", "who it helps", "key details", "contact"],
      """
Subject: Local story: {event_name} on {date_short}

Hi [name],

[What's new and why it matters locally, in two sentences.] {event_name} is on {date_long} at {venue_name}, {time_window}, and it's [free / ticketed].

Happy to share photos or answer questions: {owner_name}, [phone or email].
""")

# Team
draft("staff_brief", "Staff and volunteer brief", "team", "Everyone knows their job.",
      ["goal", "schedule", "each person's role", "where things are", "who to ask", "what to do if something goes wrong"],
      """
{event_name}: team brief for {date_long}
Goal: {goal}
Arrive: [time]. Doors: {start_time}. Wrap: [time].
Roles: [name: job] for each person
Where things are: [check-in, supplies, first aid kit, restrooms, exits]
Ask: [lead name and phone]
If something goes wrong: [safety plan in one line, and who calls emergency services]
""", channel="doc")
draft("run_of_show", "Run of show", "team", "A shared minute-by-minute plan.",
      ["setup to teardown in time order", "owner of each item", "vendor arrivals and contacts", "the peak moment", "backup notes"],
      """
{event_name}, {date_long}, run of show
[time]  Setup starts: [who]
[time]  [Vendor] arrives at [entrance]: contact [phone]
[time]  Sound, lights, Wi-Fi and payments test: [who]
{start_time}  Doors open: [who greets]
[time]  [Peak moment: welcome, reveal, demo]: [who]
[time]  Last call or closing words: [who]
[time]  Teardown and cleanup: [who]
Backup notes: [weather, no-shows, power]
""", channel="doc")

DRAFTS = D
