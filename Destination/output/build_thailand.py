import json, re, sys

SRC = "SQ_airlines.html"

with open(SRC, encoding="utf-8") as f:
    c = f.read()

orig_len = len(c)

# ---------------------------------------------------------------
# 1. JSON-LD: FAQPage + BreadcrumbList
# ---------------------------------------------------------------
faq_start = c.find('<script type="application/ld+json">')
faq_end = c.find('</script>', faq_start) + len('</script>')
assert faq_start != -1 and faq_end != -1

faqs = [
    ("Which airlines fly direct to Thailand (Bangkok)?",
     "Thai Airways, AirAsia, Singapore Airlines, Emirates, Cathay Pacific, and Malaysia Airlines are among the carriers offering direct or one-stop flights to Bangkok's Suvarnabhumi Airport (BKK). From Southeast Asian hubs like Singapore, Kuala Lumpur, and Hong Kong, direct flights are widely available. You can compare all available routes and fares on Laters.com."),
    ("What is the cheapest month to fly to Thailand?",
     "May and June typically offer the lowest fares to Bangkok, sitting in the low-demand shoulder period before the peak cool-season rush. Expect one-way fares from regional hubs to start around USD 80-120. Booking 6-8 weeks ahead during this window generally secures the best prices."),
    ("Can I pay for flights to Thailand in instalments on Laters.com?",
     "Yes. Laters.com supports BNPL providers including Atome, Kredivo, Klarna, and GrabPay for flights to Thailand. Approval is instant at checkout, and your e-ticket is issued immediately after payment is confirmed. You can split the fare into 3 or 4 payments depending on the provider."),
    ("Does using BNPL affect my credit score?",
     "This depends on the provider. Most BNPL plans for smaller fare amounts use a soft credit check that does not affect your credit score. Some providers may perform a hard check for larger instalment amounts. Check the terms of your chosen provider at Laters.com checkout before confirming."),
    ("Do I need a visa to visit Thailand?",
     "Thailand offers visa-on-arrival and e-visa options for many nationalities, and citizens of over 60 countries can enter visa-free for stays of up to 30 days. Requirements change periodically, so always verify the latest entry rules on the official Thai Ministry of Foreign Affairs website or your country's embassy before travel."),
    ("How do I get from Bangkok's Suvarnabhumi Airport (BKK) to the city centre?",
     "The Airport Rail Link connects Suvarnabhumi to central Bangkok (Phaya Thai station) in around 30 minutes for approximately THB 45-90. Metered taxis are available from the official rank on Level 1 and cost roughly THB 250-400 to the city centre including the expressway toll. Ride-hailing via Grab is also reliable and often price-competitive."),
    ("What is the best time of year to visit Thailand?",
     "November through February is widely considered the best period to visit Thailand: temperatures are cooler (around 25-30°C in Bangkok), humidity is lower, and rainfall is minimal. December and January are peak tourist months, particularly in Bangkok and the southern islands, so fares and hotel prices rise accordingly. The shoulder months of March-April offer warmth with thinner crowds."),
    ("How long is the flight to Bangkok from common origins?",
     "From Singapore it is roughly 2 hours 20 minutes; from Kuala Lumpur about 2 hours; from Sydney approximately 9-10 hours with a connection; from London around 11-12 hours non-stop on select carriers. Flight times vary depending on the route, airline, and whether a connection is involved."),
    ("When does my e-ticket arrive after booking on Laters.com?",
     "Your e-ticket is issued immediately after payment is confirmed, regardless of which BNPL provider you use. You will receive a confirmation email with your booking reference and itinerary details within minutes. If you do not receive it, check your spam folder or contact Laters.com support."),
    ("Are there hidden fees when booking flights to Thailand on Laters.com?",
     "Laters.com displays the full fare breakdown before you confirm, including taxes, carrier surcharges, and any selected extras. There are no booking fees added by Laters.com itself. Airline baggage fees and seat selection charges vary by carrier and are shown clearly at checkout."),
]

faqpage = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in faqs
    ],
}
breadcrumb = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://laters.com"},
        {"@type": "ListItem", "position": 2, "name": "Flights to Thailand — Search, Compare & Pay in Instalments", "item": "https://laters.com/destination/thailand"},
    ],
}
new_ld = (
    '<script type="application/ld+json">' + json.dumps(breadcrumb) + '</script>'
    + '<script type="application/ld+json">' + json.dumps(faqpage) + '</script>'
)
c = c[:faq_start] + new_ld + c[faq_end:]

print("stage1 done, len", len(c), "delta", len(c) - orig_len)

# ---------------------------------------------------------------
# 2. Hero section
# ---------------------------------------------------------------
def repl1(old, new, n=1):
    global c
    cnt = c.count(old)
    assert cnt == n, f"expected {n} got {cnt} for: {old[:80]!r}"
    c = c.replace(old, new, n)

repl1(
    '<h1 class="homepage-heading-xl text-balance" style="--homepage-heading-xl-size:clamp(1.75rem, 6vw, 3.75rem)">Singapore Airlines Flights — <span class="text-homepage-accent">Buy Now Pay Later</span></h1>',
    '<h1 class="homepage-heading-xl text-balance" style="--homepage-heading-xl-size:clamp(1.75rem, 6vw, 3.75rem)">Flights to Thailand — <span class="text-homepage-accent">Search, Compare &amp; Pay in Instalments</span></h1>'
)
repl1(
    '<p class="homepage-copy homepage-copy-extra-wide">Search and compare Singapore Airlines fares on Laters, then split the cost with Atome, Kredivo, or PayNow.</p>',
    '<p class="homepage-copy homepage-copy-extra-wide">25+ airlines to Thailand (TH) · BNPL at checkout · Instant e-ticket delivery. Search and compare Thailand flights on Laters, then split the cost with Atome, Kredivo, Grab, or Klarna.</p>'
)
repl1(
    'alt="Singapore Airlines A380 taking off" class="object-cover" data-nimg="fill" decoding="async" src="./SQ_airlines_files/Singapore_Airlines_A380-841_(9V-SKA)_taking_off_from_London_Heathrow_Airport_(2).jpg"',
    'alt="Thailand destination hero" class="object-cover" data-nimg="fill" decoding="async" src="./SQ_airlines_files/thailand-hero.jpg"'
)
repl1('>Jakarta</span>', '>Add a city</span>', n=2)
repl1(
    '>Singapore</span><span class="min-w-0 shrink-[9999] truncate text-xs font-semibold text-[#090315]/45">All airports</span>',
    '>Bangkok</span><span class="min-w-0 shrink-[9999] truncate text-xs font-semibold text-[#090315]/45">All airports</span>',
    n=2
)

print("stage2 (hero) done, len", len(c))

# ---------------------------------------------------------------
# 3. Rebuild the entire "landing-page-sections" inner content
# ---------------------------------------------------------------

def eyebrow(text):
    return (
        '<span class="relative mb-4 inline-block -rotate-2 bg-[#090315] p-1 shadow-[6px_6px_0px_0px_rgba(0,0,0,1)]">'
        '<span class="block bg-[#ff00ff] px-6 py-2 font-heading text-[0.8rem] font-black tracking-tighter text-[#090315] uppercase md:text-base">'
        f'{text}</span></span>'
    )

# ---- 3a. BNPL providers section ----
providers = [
    ("Atome", "Pay in 3 interest-free",
     "Atome splits your Thailand fare into three equal payments over 30 days, with zero interest and no hidden fees. The first instalment is charged at booking; the remaining two follow automatically. For a SGD 350 fare from Singapore to Bangkok, that works out to roughly SGD 117 per payment.",
     "Available in Singapore, Malaysia, Thailand, Indonesia, Philippines, Hong Kong"),
    ("Kredivo Indonesia", "Pay in 3 or 12 months",
     "Kredivo offers Indonesian travellers a 0% interest 3-month plan or an extended 12-month plan for larger fares. Approval is based on your Kredivo credit limit and takes seconds at checkout. A Jakarta-to-Bangkok fare of around IDR 1,800,000 becomes three payments of IDR 600,000.",
     "Available in Indonesia"),
    ("Grab", "Pay later via GrabPay",
     "GrabPay Later lets you book your Bangkok flight now and pay within the next billing cycle, making it a natural fit for travellers already using the Grab ecosystem. No separate sign-up is needed if you have an active GrabPay account. Available on select routes from Singapore and Kuala Lumpur.",
     "Available in Singapore, Malaysia, Philippines, Thailand, Indonesia, Vietnam"),
    ("Klarna", "Pay in 3 interest-free",
     "Klarna's Pay in 3 plan is ideal for European and Australian travellers booking long-haul flights to Bangkok. Split a GBP 550 London-to-Bangkok fare into three payments of roughly GBP 183, interest-free. Klarna runs a soft credit check that does not affect your credit score.",
     "Available in UK, Germany, Australia, US, Sweden, and more"),
]
provider_cards = "".join(
    f'<article class="homepage-card flex h-full flex-col gap-3 p-5"><div class="flex items-start gap-3">'
    f'<div class="flex flex-col gap-1.5"><h3 class="homepage-provider-title">{name}</h3>'
    f'<span class="inline-flex self-start rounded-full bg-homepage-accent/10 px-2.5 py-0.5 text-[0.7rem] font-semibold text-homepage-accent">{badge}</span>'
    f'</div></div><p class="homepage-copy text-sm">{body}</p>'
    f'<p class="mt-auto text-xs text-homepage-muted">{avail}</p></article>'
    for name, badge, body, avail in providers
)
bnpl_section = (
    '<section class="homepage-section"><div class="homepage-container">'
    '<div style="display:flex;align-items:center;gap:56px;flex-wrap:wrap">'
    '<div style="flex:1 1 480px;min-width:280px">'
    + eyebrow("BNPL at checkout")
    + '<h2 class="homepage-heading mb-4">Pay for Your Thailand Flight in Instalments</h2>'
    '<p class="homepage-copy homepage-copy-extra-wide">Book your Thailand flight today and spread the cost across instalments with the region\'s leading BNPL providers at Laters.com checkout. Atome, Kredivo, Klarna, and GrabPay are all available for routes to Bangkok. Approval is instant and your e-ticket lands in your inbox the moment payment is confirmed.</p>'
    '</div>'
    '<div style="flex:0 0 auto;display:flex;justify-content:center;align-items:center">'
    '<img alt="Thailand BNPL providers" src="./SQ_airlines_files/thailand-bnplproviders.jpg" style="width:260px;height:180px;object-fit:cover;background:#ffffff;border-radius:16px">'
    '</div></div>'
    f'<div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4 mt-10">{provider_cards}</div>'
    '</div></section>'
)

print("bnpl_section built, len", len(bnpl_section))

# ---- 3b. 3 steps section (reuse original slider skeleton, swap text) ----
steps_marker_start = c.find('<section class="homepage-section homepage-section-alt"><div class="homepage-container"><div class="mb-8 max-w-3xl md:mb-10">' + eyebrow("3 simple steps"))
assert steps_marker_start != -1, "steps section start not found"
steps_marker_end = c.find('</section>', steps_marker_start) + len('</section>')
steps_block = c[steps_marker_start:steps_marker_end]

def steps_repl(old, new, n=1):
    global steps_block
    cnt = steps_block.count(old)
    assert cnt == n, f"steps: expected {n} got {cnt} for {old[:80]!r}"
    steps_block = steps_block.replace(old, new, n)

steps_repl(
    '<h2 class="homepage-heading mb-4">How to Book Singapore Airlines Flights with BNPL</h2>',
    '<h2 class="homepage-heading mb-4">How to Book Thailand Flights with BNPL</h2>'
)
steps_repl(
    'alt="Booking Thailand flights with BNPL"', 'alt="Booking Thailand flights with BNPL"'
)  # already generic, no-op sanity check
steps_repl(
    'Search <span class="block text-transparent [-webkit-text-stroke:2px_#000] md:[-webkit-text-stroke:3px_#000]">Singapore Airlines</span>',
    'Search <span class="block text-transparent [-webkit-text-stroke:2px_#000] md:[-webkit-text-stroke:3px_#000]">Thailand flights</span>'
)
steps_repl(
    'Enter your origin city and destination, pick your travel dates and passenger count, and compare price side by side.',
    'Enter your origin city, select Thailand (TH) as destination, pick your travel dates and passenger count, and compare airlines side by side.'
)
steps_repl(
    'Select  on the payment screen and pick your instalment plan. Instant approval — no hard credit check for most plans.',
    'Select BNPL on the payment screen and pick your instalment plan. Instant approval — no hard credit check for most plans.'
)
steps_repl(
    'Your Singapore Airlines e-ticket arrives in your inbox immediately. Your BNPL provider manages payments automatically. Pack your bags.',
    'Your Thailand e-ticket arrives in your inbox immediately. Your BNPL provider manages payments automatically. Pack your bags.'
)
print("steps_block edited, len", len(steps_block))

# ---- 3c. Destination Score section ----
sub_scores = [
    ("Value for Money", 9, "Bangkok fares sit among the most competitive in Southeast Asia, with a deep bench of low-cost and full-service carriers keeping prices honest even in peak months."),
    ("Flight Frequency", 9, "Dozens of daily departures from regional hubs and multiple long-haul options from Europe, Australia, and the Middle East make scheduling a Thailand trip painless."),
    ("BNPL Availability", 8, "Atome, Kredivo, Grab, and Klarna all cover Thailand routes, though coverage varies by origin market and provider."),
    ("Airport Experience", 7, "Suvarnabhumi handles huge volumes well outside peak season, but immigration queues can be long in December-January."),
    ("Visa Ease", 9, "Visa-on-arrival, e-visa, and visa-free entry for 60+ nationalities make Thailand one of the most accessible destinations in the region."),
    ("Destination Appeal", 9, "From backpacker islands to Bangkok's street food scene, Thailand rewards both first-timers and repeat visitors."),
]
score_cards = "".join(
    f'<div class="homepage-card flex flex-col gap-1 p-4"><p class="text-xs font-semibold uppercase text-homepage-muted">{label}</p>'
    f'<p class="font-heading text-2xl font-black">{val}<span class="text-sm font-semibold text-homepage-muted">/10</span></p>'
    f'<p class="text-xs text-homepage-muted">{desc}</p></div>'
    for label, val, desc in sub_scores
)
destscore_section = (
    '<section class="homepage-section"><div class="homepage-container">'
    '<div class="mb-8 max-w-3xl">'
    + eyebrow("Proprietary research")
    + '<h2 class="homepage-heading mb-4">Laters.com Destination Score — Thailand</h2>'
    '<p class="homepage-copy">Scored by our editorial team using booking data, traveller feedback, and independent research. No destination pays to be rated.</p>'
    '</div>'
    '<div class="grid gap-6 lg:grid-cols-[320px_1fr]">'
    '<div class="homepage-card flex flex-col gap-4 p-6">'
    '<div><p class="font-heading text-6xl font-black text-homepage-accent">8.0<span class="text-2xl text-homepage-muted">/10</span></p>'
    '<p class="mt-1 text-xs font-semibold uppercase text-homepage-muted">Thailand · TH</p>'
    '<img alt="Thailand destination score" src="./SQ_airlines_files/thailand-destinationscore.jpg" style="width:100%;height:140px;object-fit:cover;border-radius:12px;margin-top:12px">'
    '</div>'
    '<p class="homepage-copy text-sm">Flights to Bangkok are frequent, competitively priced, and served by an impressive roster of full-service and low-cost carriers. The sweet spot for booking is 6-10 weeks out during the shoulder months of May-June or September-October. Peak season (December-January) sees fares climb sharply, so early planning pays off. This destination suits everyone from solo backpackers to families, with the city rewarding repeat visitors as much as first-timers.</p>'
    '<div class="flex flex-wrap gap-2">'
    '<span class="homepage-chip bg-homepage-accent/10 text-xs font-semibold text-homepage-accent">✓ Excellent value</span>'
    '<span class="homepage-chip bg-homepage-accent/10 text-xs font-semibold text-homepage-accent">✓ High flight frequency</span>'
    '<span class="homepage-chip bg-homepage-accent/10 text-xs font-semibold text-homepage-accent">✓ Strong BNPL coverage</span>'
    '<span class="homepage-chip bg-homepage-surface text-xs font-semibold">! Book early Dec-Jan</span>'
    '<span class="homepage-chip bg-homepage-surface text-xs font-semibold">! Peak queues at BKK</span>'
    '</div></div>'
    '<div class="flex flex-col gap-6">'
    f'<div class="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">{score_cards}</div>'
    '<div class="homepage-card p-5"><h3 class="homepage-provider-title mb-2">Where Thailand leads</h3>'
    '<ul class="flex flex-col gap-1.5">'
    '<li class="flex items-start gap-2 text-sm"><span class="text-homepage-accent">✓</span>25+ airlines serve Bangkok, keeping fares competitive year-round</li>'
    '<li class="flex items-start gap-2 text-sm"><span class="text-homepage-accent">✓</span>Visa-free or visa-on-arrival access for the vast majority of travellers</li>'
    '<li class="flex items-start gap-2 text-sm"><span class="text-homepage-accent">✓</span>Strong BNPL coverage across Atome, Kredivo, Grab, and Klarna</li>'
    '<li class="flex items-start gap-2 text-sm"><span class="text-homepage-accent">✓</span>September fares average around $85 one-way for flexible travellers</li>'
    '</ul></div>'
    '<div class="homepage-card p-5"><h3 class="homepage-provider-title mb-2">Worth knowing</h3>'
    '<ul class="flex flex-col gap-1.5">'
    '<li class="text-sm text-homepage-muted">December-January and Songkran (April) fares rise 40-60% above average — book 10-12 weeks ahead.</li>'
    '<li class="text-sm text-homepage-muted">Suvarnabhumi immigration queues can be substantial during peak season; use e-gates if eligible.</li>'
    '<li class="text-sm text-homepage-muted">Rainy season (May-October) brings the cheapest fares but afternoon showers are typical.</li>'
    '<li class="text-sm text-homepage-muted">AirAsia and Nok Air charge counter check-in fees — check in online to avoid them.</li>'
    '</ul></div>'
    '</div></div></div></section>'
)
print("destscore_section built, len", len(destscore_section))

# ---- 3d. Price Calendar section ----
calendar_rows = [
    ("January", "Peak", "High", "Peak cool-season tourism; book at least 10 weeks ahead."),
    ("February", "Peak", "High", "Valentine's and Chinese New Year drive demand and fares."),
    ("March", "Mid", "Medium", "Warm and dry; good value before Songkran season begins."),
    ("April", "Peak", "High", "Songkran (Thai New Year) festival; prices spike mid-month."),
    ("May", "Budget", "Low", "Rainy season starts; lowest fares of the year."),
    ("June", "Budget", "Low", "Good shoulder-season value; afternoon showers typical."),
    ("July", "Mid", "Medium", "European summer holidays nudge fares slightly upward."),
    ("August", "Mid", "Medium", "Wet season continues; indoor attractions shine."),
    ("September", "Budget", "Low", "Quietest month; excellent deals for flexible travellers."),
    ("October", "Mid", "Medium", "Rains ease; shoulder season begins picking up."),
    ("November", "Mid", "Medium", "Loy Krathong festival; pleasant weather returns."),
    ("December", "Peak", "High", "Christmas and New Year; fares at annual highs."),
]
calendar_rows_html = "".join(
    f'<tr class="border-b border-homepage-border/20"><td class="py-2.5 pr-3 font-semibold">{m}</td>'
    f'<td class="py-2.5 pr-3 text-homepage-muted">{band}</td>'
    f'<td class="py-2.5 pr-3 text-homepage-muted">{demand}</td>'
    f'<td class="py-2.5 text-homepage-muted">{note}</td></tr>'
    for m, band, demand, note in calendar_rows
)
pricecal_section = (
    '<section class="homepage-section"><div class="homepage-container">'
    '<div style="display:flex;align-items:flex-start;gap:56px;flex-wrap:wrap">'
    '<div style="flex:1 1 480px;min-width:280px">'
    + eyebrow("Price calendar")
    + '<h2 class="homepage-heading mb-4">When to Book Flights to Thailand</h2>'
    '<p class="homepage-copy homepage-copy-extra-wide">The cheapest fares to Bangkok cluster around May and June, when the rainy season begins and demand drops sharply. The most expensive months are December and January, driven by the cool-season peak and the holiday period. March and April are warm but increasingly popular, with Songkran in April pushing prices up.</p>'
    '</div>'
    '<div style="flex:0 0 auto;display:flex;justify-content:center;align-items:center">'
    '<img alt="When to book Thailand flights" src="./SQ_airlines_files/thailand-whentobook.jpg" style="width:260px;height:180px;object-fit:cover;border-radius:16px">'
    '</div></div>'
    '<div class="homepage-card mt-8 overflow-x-auto p-5">'
    '<table class="w-full text-left text-sm" style="border-collapse:collapse">'
    '<thead><tr class="border-b border-homepage-border/40 text-xs font-semibold uppercase text-homepage-muted">'
    '<th class="py-2 pr-3">Month</th><th class="py-2 pr-3">Price band</th><th class="py-2 pr-3">Demand</th><th class="py-2">Travel note</th></tr></thead>'
    f'<tbody>{calendar_rows_html}</tbody></table></div>'
    '<div class="grid gap-4 sm:grid-cols-2 mt-6">'
    '<div class="homepage-card p-5"><h3 class="homepage-provider-title mb-1">Cheapest month</h3>'
    '<p class="homepage-copy text-sm">September — average fares around $85 one-way</p></div>'
    '<div class="homepage-card p-5"><h3 class="homepage-provider-title mb-1">Peak season warning</h3>'
    '<p class="homepage-copy text-sm">December-January and Songkran (April): fares rise 40-60% above average. Book 10-12 weeks ahead to secure reasonable prices.</p></div>'
    '</div>'
    '<p class="mt-4 text-xs text-homepage-muted">Fares are estimates based on typical prices and may vary by date and availability.</p>'
    '</div></section>'
)
print("pricecal_section built, len", len(pricecal_section))

# ---- 3e. Airport Arrival Guide section ----
def transport_table(rows):
    body = "".join(
        f'<tr class="border-b border-homepage-border/20"><td class="py-2 pr-3 font-semibold">{t}</td>'
        f'<td class="py-2 pr-3 text-homepage-muted">{cost}</td><td class="py-2 text-homepage-muted">{dur}</td></tr>'
        for t, cost, dur in rows
    )
    return (
        '<table class="w-full text-left text-sm mt-3" style="border-collapse:collapse">'
        '<thead><tr class="border-b border-homepage-border/40 text-xs font-semibold uppercase text-homepage-muted">'
        '<th class="py-2 pr-3">Transport</th><th class="py-2 pr-3">Cost (approx)</th><th class="py-2">Duration</th></tr></thead>'
        f'<tbody>{body}</tbody></table>'
    )

bkk_table = transport_table([
    ("Airport Rail Link", "THB 45-90", "30 min to Phaya Thai station"),
    ("Metered taxi", "THB 250-400 plus expressway toll", "45-75 min to central Bangkok"),
    ("Grab ride-hail", "THB 300-500", "45-90 min depending on traffic"),
])
dmk_table = transport_table([
    ("Airport Bus A1/A2", "THB 30", "50-70 min to Mo Chit BTS station"),
    ("Metered taxi", "THB 200-350 plus expressway toll", "40-60 min to central Bangkok"),
    ("Grab ride-hail", "THB 250-450", "40-70 min depending on traffic"),
])
arrivalguide_section = (
    '<section class="homepage-section"><div class="homepage-container">'
    '<div style="display:flex;align-items:flex-start;gap:56px;flex-wrap:wrap">'
    '<div style="flex:1 1 480px;min-width:280px">'
    + eyebrow("Arrival guide")
    + '<h2 class="homepage-heading mb-4">Thailand Airport — What You Need to Know</h2>'
    '</div>'
    '<div style="flex:0 0 auto;display:flex;justify-content:center;align-items:center">'
    '<img alt="Thailand airport arrival guide" src="./SQ_airlines_files/thailand-airportguide.jpg" style="width:260px;height:180px;object-fit:cover;border-radius:16px">'
    '</div></div>'
    '<div class="grid gap-6 lg:grid-cols-2 mt-8">'
    '<div class="homepage-card p-5">'
    '<h3 class="homepage-provider-title">Suvarnabhumi Airport</h3>'
    '<p class="text-xs text-homepage-muted mt-1">IATA: BKK · 30 km from central Bangkok · 35 km from Khao San Road</p>'
    '<span class="inline-flex self-start rounded-full bg-homepage-accent/10 px-2.5 py-0.5 text-[0.7rem] font-semibold text-homepage-accent mt-2">Best for international arrivals</span>'
    '<p class="homepage-copy text-sm mt-3">Suvarnabhumi is Thailand\'s primary international gateway, handling the vast majority of long-haul and regional flights. The single main terminal is large and modern, with two concourses (A-G gates) and a well-signed arrivals hall. Immigration queues can be substantial during peak season; the automated e-gates for eligible passport holders move considerably faster.</p>'
    + bkk_table +
    '</div>'
    '<div class="homepage-card p-5">'
    '<h3 class="homepage-provider-title">Don Mueang International Airport</h3>'
    '<p class="text-xs text-homepage-muted mt-1">IATA: DMK · 24 km from central Bangkok · 29 km from Chatuchak</p>'
    '<span class="inline-flex self-start rounded-full bg-homepage-accent/10 px-2.5 py-0.5 text-[0.7rem] font-semibold text-homepage-accent mt-2">Best for low-cost carrier arrivals</span>'
    '<p class="homepage-copy text-sm mt-3">Don Mueang is Bangkok\'s second airport, used primarily by AirAsia, Nok Air, and other budget carriers on domestic and regional routes. Terminal 1 handles international flights; Terminal 2 covers most domestic services. The airport is functional rather than luxurious, but connections to the city are straightforward.</p>'
    + dmk_table +
    '</div></div>'
    '<div class="homepage-card p-5 mt-6"><h3 class="homepage-provider-title mb-2">Check-in tips</h3>'
    '<ul class="flex flex-col gap-1.5">'
    '<li class="flex items-start gap-2 text-sm"><span class="text-homepage-accent">✓</span>Use Suvarnabhumi\'s e-gates if your passport is eligible; saves 20-30 minutes.</li>'
    '<li class="flex items-start gap-2 text-sm"><span class="text-homepage-accent">✓</span>Check in online 24 hours ahead; AirAsia and Nok Air charge fees at the counter.</li>'
    '<li class="flex items-start gap-2 text-sm"><span class="text-homepage-accent">✓</span>Arrive 3 hours early for international departures during December and January peak.</li>'
    '</ul></div>'
    '<p class="mt-4 text-xs text-homepage-muted">At Laters.com checkout you can split seat upgrades, lounge access passes, and extra baggage allowances into instalments alongside your fare, using Atome, Kredivo, or Klarna. No separate application needed.</p>'
    '</div></section>'
)
print("arrivalguide_section built, len", len(arrivalguide_section))

# ---- 3f. Extras section ("split more than the fare") ----
extras = [
    ("Seat Selection", "Choose a window seat for your first view of Bangkok's sprawling skyline on approach.", "Available with all providers"),
    ("Extra Baggage", "Pack that extra pair of shoes and the Thai silk you know you will buy.", "Split across 3 payments"),
    ("Travel Insurance", "Cover medical costs and trip disruptions, including Thailand's tropical weather delays.", "Available with Klarna, Atome"),
    ("Hotel Package", "Bundle a Bangkok riverside hotel and save versus booking accommodation separately.", "Pay in 3 or 4 months"),
    ("Airport Transfer", "Pre-book a private transfer from Suvarnabhumi and skip the taxi queue entirely.", "Available with all providers"),
    ("Travel SIM", "Stay connected on Bangkok's BTS Skytrain and in Chiang Mai's mountain villages.", "Add at checkout"),
]
extras_cards = "".join(
    f'<article class="homepage-card flex h-full flex-col gap-2 p-5"><h3 class="homepage-provider-title">{name}</h3>'
    f'<p class="homepage-copy text-sm">{desc}</p>'
    f'<p class="mt-auto text-xs text-homepage-muted">{tag}</p></article>'
    for name, desc, tag in extras
)
extras_section = (
    '<section class="homepage-section homepage-section-alt"><div class="homepage-container">'
    '<div class="mb-8 max-w-3xl md:mb-10">'
    + eyebrow("More than just the fare")
    + '<h2 class="homepage-heading mb-4">Split More Than Just the Fare to Thailand</h2>'
    '<p class="homepage-copy homepage-copy-extra-wide">Make your Thailand trip go further by splitting every extra at checkout.</p>'
    '</div>'
    f'<div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">{extras_cards}</div>'
    '</div></section>'
)
print("extras_section built, len", len(extras_section))

# ---- 3g. Popular Routes section ----
routes = [
    ("Singapore", "Singapore Airlines, Scoot, AirAsia", "2h 20m", "Direct", "3", "30"),
    ("Kuala Lumpur", "AirAsia, Malaysia Airlines, Batik Air", "2h 00m", "Direct", "3", "25"),
    ("Hong Kong", "Cathay Pacific, Thai Airways", "2h 45m", "Direct", "3", "50"),
    ("Tokyo", "Thai Airways, Japan Airlines, ANA", "6h 00m", "Direct", "3", "93"),
    ("London", "Thai Airways, British Airways, Emirates", "11h 30m", "Direct", "4", "130"),
    ("Sydney", "Thai Airways, Qantas, Jetstar", "9h 30m", "Via Singapore", "4", "105"),
    ("Mumbai", "Air India, Thai Airways, IndiGo", "4h 00m", "Direct", "3", "70"),
    ("Seoul", "Korean Air, Asiana Airlines, Thai Smile", "5h 30m", "Direct", "3", "80"),
    ("Dubai", "Emirates, Flydubai, Thai Airways", "6h 00m", "Direct", "4", "78"),
]
route_cards = "".join(
    f'<article class="homepage-card flex h-full flex-col gap-2 p-5">'
    f'<p class="font-heading text-lg font-black">{city} → Thailand</p>'
    f'<p class="text-xs text-homepage-muted">{airlines} · {dur} · {stops}</p>'
    f'<p class="mt-2 font-heading text-2xl font-black text-homepage-accent">${price}</p>'
    f'<p class="text-xs text-homepage-muted">× {n} payments</p>'
    f'<p class="mt-auto text-xs font-semibold">Pay in {n} from ${price}/instalment</p>'
    '</article>'
    for city, airlines, dur, stops, n, price in routes
)
popularroutes_section = (
    '<section class="homepage-section"><div class="homepage-container">'
    '<div class="mb-8 max-w-3xl">'
    + eyebrow("Popular routes")
    + '<h2 class="homepage-heading mb-4">Popular Flights to Thailand</h2>'
    '<p class="homepage-copy homepage-copy-extra-wide">The majority of travellers flying to Thailand arrive from Singapore, Kuala Lumpur, Hong Kong, and Tokyo, with strong long-haul demand from London, Sydney, and Mumbai. Short regional hops make Bangkok one of Southeast Asia\'s most connected cities.</p>'
    '</div>'
    f'<div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">{route_cards}</div>'
    '<p class="mt-4 text-xs text-homepage-muted">Fares are estimates based on typical prices and may vary by date and availability.</p>'
    '</div></section>'
)
print("popularroutes_section built, len", len(popularroutes_section))

# ---- 3h. Top Carriers section ----
carriers = [
    ("TG", "Thai Airways", "Thailand's flag carrier", "Direct",
     "The national carrier offers direct flights from major hubs with generous baggage allowance and a strong onboard product on long-haul routes.",
     "Atome · Klarna", "https://laters.com/airline/thai-airways"),
    ("FD", "AirAsia", "Southeast Asia's leading low-cost carrier", "Direct",
     "The region's leading low-cost carrier connects Bangkok to dozens of Southeast Asian cities with hard-to-beat base fares from Kuala Lumpur and Singapore.",
     "Atome · Grab", "https://laters.com/airline/airasia"),
    ("SQ", "Singapore Airlines", "5-star Skytrax carrier", "Direct",
     "Consistently top-rated for service, SIA offers a premium experience on the short Singapore-Bangkok hop and as a connecting carrier for long-haul travellers.",
     "Atome · Klarna", "https://laters.com/airline/singapore-airlines"),
    ("EK", "Emirates", "Dubai's flag carrier", "Via Dubai",
     "A popular choice for European and Middle Eastern travellers, with a well-regarded Dubai connection and strong business-class product.",
     "Klarna · Tabby", "https://laters.com/airline/emirates"),
    ("TR", "Scoot", "Singapore's low-cost long-haul carrier", "Direct",
     "Budget-friendly flights from Singapore with optional extras, ideal for short-break travellers who want a no-frills fare to Bangkok.",
     "Atome · Grab", "https://laters.com/airline/scoot"),
]
carrier_cards = "".join(
    f'<a class="block transition-transform hover:-translate-y-0.5" href="{href}">'
    f'<article class="homepage-card flex h-full flex-col gap-3 p-5"><div class="flex items-start gap-3">'
    f'<div class="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-homepage-accent/10 text-xs font-bold text-homepage-accent">{code}</div>'
    f'<div class="flex flex-col gap-1.5"><h3 class="homepage-provider-title">{name}</h3>'
    f'<span class="inline-flex self-start rounded-full bg-homepage-accent/10 px-2.5 py-0.5 text-[0.7rem] font-semibold text-homepage-accent">{tag}</span></div></div>'
    f'<p class="homepage-copy text-sm">{desc}</p>'
    f'<p class="mt-auto text-xs text-homepage-muted">{stops} · {providers}</p>'
    '</article></a>'
    for code, name, tag, stops, desc, providers, href in carriers
)
topcarriers_section = (
    '<section class="homepage-section homepage-section-alt"><div class="homepage-container">'
    '<div class="mb-8 max-w-3xl md:mb-10">'
    + eyebrow("Top carriers")
    + '<h2 class="homepage-heading mb-4">Airlines Flying to Thailand</h2>'
    '<p class="homepage-copy homepage-copy-extra-wide">Thailand is served by a strong mix of full-service carriers and low-cost airlines, with Thai Airways leading the national network and AirAsia dominating the budget end. Here are the airlines most worth considering for your Bangkok booking.</p>'
    '</div>'
    f'<div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">{carrier_cards}</div>'
    '</div></section>'
)
print("topcarriers_section built, len", len(topcarriers_section))

# ---- 3i. Nearby Destinations section ----
nearby = [
    ("Bali", "Indonesia", "Rice terraces, surf, and spiritual calm.", "110"),
    ("Tokyo", "Japan", "Ancient temples meet neon-lit modernity.", "280"),
    ("Kuala Lumpur", "Malaysia", "Street food capital with a striking skyline.", "75"),
    ("Ho Chi Minh City", "Vietnam", "History, chaos, and the world's best coffee.", "95"),
    ("Singapore", "Singapore", "Effortlessly efficient city with world-class food.", "90"),
]
nearby_cards = "".join(
    f'<article class="homepage-card flex h-full flex-col gap-2 p-5">'
    f'<p class="text-xs font-semibold uppercase text-homepage-accent">From ${price}</p>'
    f'<p class="font-heading text-lg font-black">{city}</p>'
    f'<p class="text-xs text-homepage-muted">{country}</p>'
    f'<p class="mt-2 text-sm text-homepage-muted">{tagline}</p>'
    '</article>'
    for city, country, tagline, price in nearby
)
nearbydest_section = (
    '<section class="homepage-section"><div class="homepage-container">'
    '<div class="mb-8 max-w-3xl md:mb-10">'
    + eyebrow("Explore more")
    + '<h2 class="homepage-heading mb-4">Other Destinations Near Thailand</h2>'
    '<p class="homepage-copy homepage-copy-extra-wide">These destinations are popular with travellers who also searched for Thailand.</p>'
    '</div>'
    f'<div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">{nearby_cards}</div>'
    '<p class="mt-4 text-xs text-homepage-muted">Fares are estimates based on typical prices and may vary by date and availability.</p>'
    '</div></section>'
)
print("nearbydest_section built, len", len(nearbydest_section))

# ---- 3j. FAQ section: reuse original accordion skeleton, swap text ----
faq_sec_marker = c.find('FAQ</span></span><h2 class="homepage-heading mb-4">FAQs: Booking Singapore Airlines Flights</h2>')
assert faq_sec_marker != -1
faq_sec_start = c.rfind('<section', 0, faq_sec_marker)
faq_sec_end = c.find('</section>', faq_sec_marker) + len('</section>')
faq_block = c[faq_sec_start:faq_sec_end]

def faq_repl(old, new, n=1):
    global faq_block
    cnt = faq_block.count(old)
    assert cnt == n, f"faq: expected {n} got {cnt} for {old[:80]!r}"
    faq_block = faq_block.replace(old, new, n)

faq_repl(
    '<h2 class="homepage-heading mb-4">FAQs: Booking Singapore Airlines Flights</h2><p class="homepage-copy">Everything you need to know about booking Singapore Airlines flights and paying later on Laters.</p>',
    '<h2 class="homepage-heading mb-4">FAQs: Booking Thailand Flights</h2><p class="homepage-copy">Everything you need to know before booking your Thailand flight on Laters.</p>'
)

old_faqs = [
    ("How do I book Singapore Airlines flights on Laters?",
     "Search your route and travel dates on Laters, compare Singapore Airlines fares alongside other providers, and select your preferred option. You can personalise your booking with seat selection, baggage add-ons, and protection products before choosing your payment method at checkout."),
    ("Can I pay for Singapore Airlines flights in instalments on Laters?",
     "Yes — Laters supports a range of Buy Now Pay Later providers including Atome, Grab PayLater, Hoolah, Kredivo, Touch 'n Go, and GCash, depending on your market. You can split your total booking cost — including any add-ons — into manageable instalments."),
    ("Does Laters charge extra fees for booking Singapore Airlines?",
     "Laters does not charge hidden booking fees. The price you see when comparing fares is transparent, and any add-ons or protections are clearly itemised before you confirm your booking."),
    ("Can I compare Singapore Airlines prices with other airlines on Laters?",
     "Absolutely. Laters is a comparison platform, so you can search Singapore Airlines fares alongside other carriers on the same route — including connections — to find the best overall deal."),
    ("Does Singapore Airlines charge for airport check-in?",
     "Yes, Singapore Airlines charges a fee for airport counter check-in at select airports. To avoid this, check in online via the Singapore Airlines website or app, which opens 48 hours before departure. You can also manage your booking at singaporeair.com/managebooking."),
    ("What is Singapore Airlines' checked baggage allowance?",
     "Baggage allowances vary by route, fare type, and cabin class. Economy passengers typically receive 25–30 kg, while Business Class and Suites passengers generally receive higher allowances. Always confirm your specific allowance on your booking confirmation or the Singapore Airlines website."),
    ("Does Singapore Airlines charge for seat selection?",
     "Singapore Airlines typically charges for advance seat selection on many fare types, though complimentary seat selection is generally available closer to departure or for higher fare tiers and elite KrisFlyer members. Check the Singapore Airlines website for current seat selection fees and policies."),
    ("What cabin classes does Singapore Airlines offer?",
     "Singapore Airlines offers four cabin classes: Suites (available on select A380 routes), Business Class, Premium Economy, and Economy. Each class offers a distinct experience, with Business Class featuring full flat-bed seats on long-haul routes."),
    ("What is Singapore Airlines' KrisFlyer programme?",
     "KrisFlyer is Singapore Airlines' frequent flyer programme, allowing members to earn miles on SQ flights and partner airlines. Miles can be redeemed for flights, upgrades, and other rewards. Singapore Airlines is also a member of Star Alliance, enabling earning and redemption across a wide global network."),
    ("How do I manage my Singapore Airlines booking?",
     "You can manage your Singapore Airlines booking — including seat selection, meal preferences, and check-in — directly at singaporeair.com/managebooking. For bookings made through Laters, refer to your booking confirmation for specific management instructions."),
]

assert len(old_faqs) == len(faqs) == 10
for (oq, oa), (nq, na) in zip(old_faqs, faqs):
    faq_repl(f'<span class="homepage-faq-question">{oq}</span>', f'<span class="homepage-faq-question">{nq}</span>')
    faq_repl(f'<span class="text-sm leading-relaxed text-homepage-muted md:text-base">{oa}</span>', f'<span class="text-sm leading-relaxed text-homepage-muted md:text-base">{na}</span>')

print("faq_block edited, len", len(faq_block))

# ---- 3k. Newsletter section: reuse skeleton, swap text ----
news_sec_marker = c.find('<h2 class="homepage-heading mb-3">Get Singapore Airlines Deals by Email</h2>')
assert news_sec_marker != -1
news_sec_start = c.rfind('<section', 0, news_sec_marker)
news_sec_end = c.find('</section>', news_sec_marker) + len('</section>')
newsletter_block = c[news_sec_start:news_sec_end]

def news_repl(old, new, n=1):
    global newsletter_block
    cnt = newsletter_block.count(old)
    assert cnt == n, f"news: expected {n} got {cnt} for {old[:80]!r}"
    newsletter_block = newsletter_block.replace(old, new, n)

news_repl(
    '<h2 class="homepage-heading mb-3">Get Singapore Airlines Deals by Email</h2><p class="homepage-copy mb-6">Be first to hear about Singapore Airlines flight deals, BNPL promotions, and flash sales from Laters. No spam, unsubscribe anytime.</p>',
    '<h2 class="homepage-heading mb-3">Get Thailand Flight Deals by Email</h2><p class="homepage-copy mb-6">Be first to hear about Thailand flight deals, BNPL promotions, and flash sales from Laters. No spam, unsubscribe anytime.</p>'
)
print("newsletter_block edited, len", len(newsletter_block))

# ---- 3l. Assemble and splice the full inner blob ----
start_marker = '<div class="landing-page-sections flex flex-col bg-homepage-bg">'
end_marker = '<section class="homepage-section-accent py-14 md:py-20">'
si = c.find(start_marker)
ei = c.find(end_marker)
assert si != -1 and ei != -1

new_inner = (
    bnpl_section + steps_block + destscore_section + pricecal_section
    + arrivalguide_section + extras_section + popularroutes_section
    + topcarriers_section + nearbydest_section + faq_block + newsletter_block
)

c = c[:si] + start_marker + new_inner + '</div>' + c[ei:]
print("inner blob spliced, total len", len(c))

# ---------------------------------------------------------------
# 4. CTA section (accent, right before footer)
# ---------------------------------------------------------------
repl1(
    '<h2 class="font-heading text-4xl font-black uppercase leading-none text-white md:text-5xl">Ready to Book Your Singapore Airlines Flight?</h2><p class="text-base text-white/85">Find the best deals on <span class="font-bold text-[#ff00ff]">Singapore Airlines flights</span>with Laters and split your fare at checkout.</p>',
    '<h2 class="font-heading text-4xl font-black uppercase leading-none text-white md:text-5xl">Ready to Book Your Thailand Flight?</h2><p class="text-base text-white/85">Compare 25+ airlines to <span class="font-bold text-[#ff00ff]">Thailand</span> and split your fare with Atome, Kredivo, or Grab.</p>'
)
repl1(
    '<a class="homepage-cta" href="https://laters.com/airline/singapore-airlines#top">Search Singapore Airlines Flights</a>',
    '<a class="homepage-cta" href="https://laters.com/destination/thailand#top">Search Flights to Thailand</a>'
)

print("stage4 (CTA) done, len", len(c))

# ---------------------------------------------------------------
# 5. Head / meta tags
# ---------------------------------------------------------------
repl1(
    '<title>Singapore Airlines Flights — Pay in Instalments | Laters</title>',
    '<title>Flights to Thailand — Book Now, Pay Later | Laters.com</title>'
)
repl1(
    '<meta content="Book Singapore Airlines flights and pay in instalments with Buy Now Pay Later. Compare SQ fares, choose Atome, Kredivo or GrabPay, and split your fare today on Laters." name="description">',
    '<meta content="Find and compare flights to Thailand from top airlines. Pay in instalments with Atome, Kredivo or Klarna — instant approval, e-ticket arrives immediately" name="description">'
)
repl1(
    '<meta content="Singapore Airlines flights,book Singapore Airlines online,singapore airlines pay in installments,singapore airlines flexible payment plans,cheap SQ flights,book now pay later singapore airlines,singapore airlines business class deals,compare singapore airlines fares" name="keywords">',
    '<meta content="flights to Thailand,cheap flights to Thailand,fly now pay later Thailand,Thailand flights pay in instalments,Bangkok flights,flights to Bangkok,book Thailand flights with Atome,Thai Airways flights Thailand,AirAsia flights to Bangkok,cheapest month to fly to Thailand,Thailand flexible payment flights,Singapore to Bangkok flights" name="keywords">'
)
repl1(
    '<link href="https://laters.com/airline/singapore-airlines" rel="canonical">',
    '<link href="https://laters.com/destination/thailand" rel="canonical">'
)
for hreflang in ["en", "ar", "zh-cn", "zh-tw", "zh-hk", "es-es", "pt-br", "ja", "ko", "fr", "ms", "my", "it", "de", "pt-pt", "nl", "x-default"]:
    old_href = f'href="https://laters.com/{hreflang}/payment/klarna" hreflang="{hreflang}"' if hreflang not in ("en", "x-default") else f'href="https://laters.com/payment/klarna" hreflang="{hreflang}"'
    new_href = f'href="https://laters.com/{hreflang}/destination/thailand" hreflang="{hreflang}"' if hreflang not in ("en", "x-default") else f'href="https://laters.com/destination/thailand" hreflang="{hreflang}"'
    repl1(old_href, new_href)
repl1(
    '<meta content="Singapore Airlines Flights — Pay in Instalments | Laters" property="og:title">',
    '<meta content="Flights to Thailand — Book Now, Pay Later | Laters.com" property="og:title">'
)
repl1(
    '<meta content="Book Singapore Airlines flights and pay in instalments with Buy Now Pay Later. Compare SQ fares, choose Atome, Kredivo or GrabPay, and split your fare today on Laters." property="og:description">',
    '<meta content="Find and compare flights to Thailand from top airlines. Pay in instalments with Atome, Kredivo or Klarna — instant approval, e-ticket arrives immediately" property="og:description">'
)
repl1(
    '<meta content="https://laters.com/airline/singapore-airlines" property="og:url">',
    '<meta content="https://laters.com/destination/thailand" property="og:url">'
)
repl1(
    '<meta content="https://cdn.sanity.io/images/t5ei3wo2/development/18f2948ad7177a2c19bc5c1cb91fa1ebae3bd1f2-1000x1000.png" property="og:image">',
    '<meta content="https://lzp87feda3ltjk4b.public.blob.vercel-storage.com/destination-thailand-th-hero-1781692462263.jpg" property="og:image">'
)
repl1(
    '<meta content="Klarna Flights: Split the Fare, Pay Later | Laters.com" name="twitter:title">',
    '<meta content="Flights to Thailand — Book Now, Pay Later | Laters.com" name="twitter:title">'
)
repl1(
    '<meta content="Spread your flight cost with Klarna on Laters.com. Choose pay-in-4, defer 30 days, or monthly financing. E-ticket issued on approval. Compare fares and pay over time." name="twitter:description">',
    '<meta content="Find and compare flights to Thailand from top airlines. Pay in instalments with Atome, Kredivo or Klarna — instant approval, e-ticket arrives immediately" name="twitter:description">'
)
repl1(
    '<meta content="https://lzp87feda3ltjk4b.public.blob.vercel-storage.com/payment-klarna-stripe-hero-1783578922018.webp" name="twitter:image">',
    '<meta content="https://lzp87feda3ltjk4b.public.blob.vercel-storage.com/destination-thailand-th-hero-1781692462263.jpg" name="twitter:image">'
)

print("stage5 (meta) done, len", len(c))

with open(SRC, "w", encoding="utf-8") as f:
    f.write(c)
print("WROTE FINAL FILE:", SRC, len(c))
