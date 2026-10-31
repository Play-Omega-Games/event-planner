"""Official links only, by topic and country. Every URL is live-checked by
scripts/check_links.py for HTTP 200 and the expected phrase. Owner-facing
text names the page by what it is ("the federal small business guide to
licenses and permits"), and every topic also carries generic advice that
works anywhere, so owners outside these countries are never left without help.
"""
LINKS = {
    "permits": {
        "generic": "Ask your city or county (or local council) which permits apply and how much notice they need. Common ones: special event or temporary use, tent, amplified sound, street or sidewalk use, signs, temporary food, alcohol, and occupancy.",
        "US": [("Small business guide: licenses and permits (US federal)", "https://www.sba.gov/counseling/launch-your-business/#licenses-permits", "Apply for licenses and permits")],
        "UK": [("Find a licence (UK government)", "https://www.gov.uk/find-licences", "Find a licence"),
               ("Organising a voluntary event: a 'can do' guide (UK government)", "https://www.gov.uk/government/publications/can-do-guide-for-organisers-of-voluntary-events", "can do")],
        "CA": [("Permits and licences finder (Canada)", "https://bizpal.ca/", "permits and licences")],
        "AU": [("Business licence and information service (Australian government)", "https://ablis.business.gov.au/", "licences you need")],
    },
    "alcohol": {
        "generic": "Your local or state licensing office decides whether you need a license to sell or serve alcohol, and how long it takes. Selling usually needs one; free serving may too.",
        "UK": [("Temporary Events Notice (England and Wales)", "https://www.gov.uk/find-licences/temporary-events-notice", "Temporary Event Notice")],
    },
    "insurance": {
        "generic": "Ask your insurance agent whether your policy covers this event, guests and off-site locations, and about one-day event cover and liquor liability.",
        "US": [("Small business guide: business insurance (US federal)", "https://www.sba.gov/counseling/launch-your-business/#business-insurance", "Get business insurance")],
        "AU": [("Business insurance (Australian government)", "https://business.gov.au/risk-management/insurance", "insurance")],
    },
    "taxes": {
        "generic": "Selling at a temporary location may mean collecting sales tax there. Ask your tax office, accountant or the market organizer.",
        "US": [("Small business guide: pay taxes (US federal)", "https://www.sba.gov/counseling/manage-your-business/#pay-taxes", "Pay taxes")],
    },
    "accessibility": {
        "generic": "Plan step-free entry, clear routes, seating, an accessible restroom, readable signs and a microphone or captions for talks. Ask guests about access needs when they sign up.",
        "US": [("ADA guide for businesses open to the public (US Department of Justice)", "https://www.ada.gov/resources/title-iii-primer/", "public accommodations")],
    },
    "charity_receipts": {
        "generic": "Only a qualified charity can give donors a tax receipt. Agree with the charity who collects the money, who sends receipts and how its name and logo may be used.",
        "US": [("Charitable contributions: quid pro quo disclosures (IRS)", "https://www.irs.gov/charities-non-profits/charitable-organizations/charitable-contributions-quid-pro-quo-contributions", "quid pro quo"),
               ("Substantiating charitable contributions (IRS)", "https://www.irs.gov/charities-non-profits/substantiating-charitable-contributions", "written acknowledgment")],
    },
    "gaming": {
        "generic": "Raffles, auctions with chance elements and other games of chance are often restricted to registered charities and may need a permit. Check your state or local rules before selling tickets.",
        "US": [("Tax-exempt organizations and gaming (IRS Publication 3079, PDF)", "https://www.irs.gov/pub/irs-pdf/p3079.pdf", None)],
    },
    "emergency": {
        "generic": "Know your exits and the nearest hospital, keep a first aid kit, and decide who calls emergency services and from where.",
        "US": [("Emergency planning for businesses (US government)", "https://www.ready.gov/business", "business")],
    },
}
