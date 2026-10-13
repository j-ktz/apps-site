#!/usr/bin/env python3
"""Shared landing-page sections, metadata and structured data for apps.johnkatez.com.

Run from the repo root:  python3 tools/landing.py
It rewrites only the parts between markers, so it is safe to run again:
  <!-- lp:head --> ... <!-- /lp:head -->    stylesheet + JSON-LD, before </head>
  <!-- lp:body --> ... <!-- /lp:body -->    shared sections, at each page's anchor
  <!-- lp:legal --> ... <!-- /lp:legal -->  house line + Apple credit, after the brand footer
Titles and descriptions (title, meta description, og:, twitter:) are set from CONTENT.
Facts come from each app's App Store listing, privacy page and repo notes (checked 2026-10-12).
No em dashes in copy (house style). Plain English.
"""
import html, json, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://apps.johnkatez.com"
HOUSE_LINE = "Small apps that each do one job well. No ads, fair prices, and only the data the app needs."
APPLE_CREDIT = "Apple, the Apple logo and iPhone are trademarks of Apple Inc., registered in the U.S. and other countries. App Store is a service mark of Apple Inc."
PUBLISHER = {"@type": "Person", "name": "John Katez", "url": "https://johnkatez.com/"}

SVG = {
 "check": '<path d="m5 12.5 4.2 4.2L19 7"/>',
 "lock": '<rect x="5" y="10.5" width="14" height="10" rx="2.5"/><path d="M8 10.5V8a4 4 0 0 1 8 0v2.5"/>',
 "noads": '<circle cx="12" cy="12" r="8.5"/><path d="m6 6 12 12"/>',
 "cloud": '<path d="M7 18h10a4 4 0 0 0 .6-7.95A6 6 0 0 0 6.2 9.2 4.5 4.5 0 0 0 7 18z"/>',
 "bell": '<path d="M6 16V11a6 6 0 0 1 12 0v5l1.5 2h-15z"/><path d="M10 20.5a2 2 0 0 0 4 0"/>',
 "chart": '<path d="M4 20V11M10 20V5M16 20v-7M21 20H3"/>',
 "calendar": '<rect x="3.5" y="5" width="17" height="15" rx="2.5"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
 "users": '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><circle cx="17" cy="9" r="2.5"/><path d="M15.5 14.2c3 .2 5.5 2.6 5.5 5.8"/>',
 "spark": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/>',
 "camera": '<rect x="3" y="7" width="18" height="13" rx="2.5"/><path d="M8 7l2-3h4l2 3"/><circle cx="12" cy="13.5" r="3.5"/>',
 "barcode": '<path d="M4 6v12M7 6v12M10 6v12M14 6v12M16 6v12M20 6v12"/>',
 "search": '<circle cx="11" cy="11" r="6.5"/><path d="m16 16 4.5 4.5"/>',
 "message": '<path d="M4 5h16v11H9l-5 4z"/>',
 "heart": '<path d="M12 20s-7-4.4-7-9.5A4 4 0 0 1 12 8a4 4 0 0 1 7 2.5C19 15.6 12 20 12 20z"/>',
 "watch": '<rect x="7" y="6" width="10" height="12" rx="3"/><path d="M9 6l.6-3h4.8l.6 3M9 18l.6 3h4.8l.6-3"/>',
 "target": '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1.2"/>',
 "book": '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 19V5"/>',
 "timer": '<circle cx="12" cy="13" r="7.5"/><path d="M12 9v4l2.5 2M9.5 2.5h5"/>',
 "calc": '<rect x="5" y="3" width="14" height="18" rx="2.5"/><path d="M8 7h8M8 11h.01M12 11h.01M16 11h.01M8 15h.01M12 15h.01M16 15h.01M8 18.5h8"/>',
 "offline": '<path d="M2 8.5a15 15 0 0 1 20 0M5 12a10 10 0 0 1 14 0M8.5 15.5a5 5 0 0 1 7 0"/><circle cx="12" cy="19" r="1"/><path d="m3 3 18 18"/>',
 "pin": '<path d="M12 21s-6.5-6.1-6.5-11A6.5 6.5 0 0 1 18.5 10c0 4.9-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.4"/>',
 "doc": '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 12h6M9 16h6"/>',
 "crown": '<path d="M3 18 4.5 7l5 4.5L12 5l2.5 6.5 5-4.5L21 18z"/><path d="M3 21h18"/>',
 "home": '<path d="M4 11 12 4l8 7v9H4z"/><path d="M10 20v-5h4v5"/>',
 "list": '<path d="M9 6h11M9 12h11M9 18h11M4.5 6h.01M4.5 12h.01M4.5 18h.01"/>',
 "shield": '<path d="M12 3 5 6v6c0 4.4 3 7.6 7 9 4-1.4 7-4.6 7-9V6z"/><path d="m9 12 2 2 4-4"/>',
 "repeat": '<path d="M17 2.5 20.5 6 17 9.5"/><path d="M3.5 11V9a3 3 0 0 1 3-3h14M7 21.5 3.5 18 7 14.5"/><path d="M20.5 13v2a3 3 0 0 1-3 3h-14"/>',
 "gift": '<rect x="3.5" y="8" width="17" height="4" rx="1"/><path d="M5 12v8.5h14V12M12 8v12.5M12 8S10.5 3.5 8 4.5 9 8 12 8zm0 0s1.5-4.5 4-3.5S15 8 12 8z"/>',
}


def icon(name, size=20):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{SVG[name]}</svg>'


APPS = {  # for "more apps" tiles
 "mvn": ("Music Video Night", "The party game where everyone picks a music video"),
 "tanklog": ("TankLog: Aquascape", "A free, offline journal for planted tanks and shrimp"),
 "mackro": ("Mackro", "A macro tracker with a squirrel in it"),
 "stashday": ("Stashday", "One number to set aside each payday"),
 "tabbed": ("Tabbed Electrician", "Journeyman electrician exam prep"),
 "tabbed-plumber": ("Tabbed Plumber", "Journeyman plumber exam prep"),
 "fantasyqueens": ("Fantasy Queens", "Fantasy houses for drag watch parties"),
 "sitout": ("Sitout", "Fair pickleball round robins"),
 "statecount": ("Statecount", "A private 183-day residency tracker"),
}

# ---------------------------------------------------------------- content
C = {}

C["mackro"] = dict(
 name="Mackro", category="HealthApplication", sub="Macro tracker", live=True, appid="6771991453", os="iOS",
 title="Mackro: AI Macro Tracker and Calorie Counter for iPhone",
 desc="A macro tracker with a squirrel in it. Scan a barcode, search, describe a meal or snap a photo, and Mack does the macros. No ads. Free to start.",
 og_title="Mackro: the macro tracker that never judges",
 anchor='<section class="end">',
 vars="--lp-ink:var(--ink);--lp-muted:var(--muted);--lp-card:#FFFFFF;--lp-line:var(--line);--lp-accent:#B9820F;--lp-accent-ink:#fff;--lp-display:var(--display);--lp-font:var(--body);--lp-paper:var(--paper)",
 trust=[("noads", "No ads, ever"), ("users", "No account"), ("barcode", "Barcode and search are free"), ("cloud", "Your log stays in your iCloud")],
 who=[("Lifters", "Hit a protein goal every day and switch between training and rest day targets."),
      ("Restarters", "Getting back to eating well without a lecture. Log a meal in seconds and see the trend, not one bad day."),
      ("Tracker refugees", "Done with ads, upsells and homework. Mackro does the basics free and keeps out of the way.")],
 priv=("Your food log stays yours.", ["No account and no ads. Your log lives on your iPhone and in your own iCloud, where we can't see it.",
       "AI logging (Pro) sends only the meal description or photo you submit, to estimate the macros. Apple Health data never leaves your phone."]),
 plans=[("Free", "$0", "forever, no ads", ["Barcode scanning and food search", "Calories, macros and water", "Streaks and check-ins from Mack", "7-day trends"], False),
        ("Mackro Pro", "$39.99/yr", "or $5.99/month. 7 days free first.", ["Describe a meal or snap a photo", "30 and 90-day trends, full history", "Weekly targets that follow your weight trend", "Training and rest day targets", "Apple Health sync and meal templates"], True)],
 fine="Mackro Pro arrives with version 2.1. Subscriptions renew automatically unless canceled at least 24 hours before the end of the period, and are managed in Settings, then your name, then Subscriptions. Prices shown in US dollars.",
 faq=[("Is Mackro free?", "Yes. Barcode scanning, food search, calories, macros, water, streaks and 7-day trends are free, with no ads. Mackro Pro is optional."),
      ("What does Mackro Pro add?", "Logging by describing a meal or snapping a photo, 30 and 90-day trends with full history, weekly targets that follow your weight trend, training and rest day targets, Apple Health sync and meal templates. It's $5.99 a month or $39.99 a year, with a 7-day free trial, and arrives with version 2.1."),
      ("How does photo logging work?", "Take a photo of your plate and Mack estimates the calories and macros in a few seconds using AI. It's an estimate, so mixed dishes can be off. You can edit any entry."),
      ("Do I need an account?", "No. Mackro never asks for your name, email or a password. Your food log is stored on your iPhone and in your own iCloud."),
      ("Does Mackro work with Apple Health and Apple Watch?", "With Mackro Pro, Mackro can write calories, macros, water and weight to Apple Health, and you can log a meal by dictating on Apple Watch. Health data never leaves your phone."),
      ("What data does Mackro collect?", "Anonymous product analytics that never include your food, health or weight data. If you use AI logging, only the description or photo you submit is sent to estimate macros. No ads and no data sales. Details are in the privacy policy."),
      ("Is Mackro medical or diet advice?", "No. Targets are estimates from what you enter. For medical or diet guidance, talk to a doctor or a registered dietitian."),
      ("Who makes Mackro?", "John Katez, an independent developer who also makes Stashday, Statecount and other small iPhone apps.")],
 more=["stashday", "statecount", "sitout", "tanklog"],
)

C["stashday"] = dict(
 name="Stashday", category="FinanceApplication", sub="Sinking fund planner", live=False, os="iOS",
 title="Stashday: Sinking Fund Planner for Every Paycheck",
 desc="Stashday turns car registration, holidays, insurance and the vet into one number: how much to set aside this paycheck. No bank login. Free for 3 funds.",
 og_title="Stashday: every bill covered, one paycheck at a time",
 anchor='<section class="priv">',
 vars="--lp-ink:var(--ink);--lp-muted:var(--muted);--lp-line:var(--line);--lp-card:rgba(127,127,127,.09);--lp-accent:var(--green);--lp-accent-ink:#fff;--lp-display:var(--display);--lp-font:var(--body)",
 trust=[("lock", "No bank login"), ("shield", "Data Not Collected"), ("noads", "No ads"), ("calendar", "Weekly, every 2 weeks, twice a month or monthly pay")],
 who=[("Every-other-Friday earners", "Paid every two weeks and tired of guessing what to keep back each time."),
      ("Annual-bill victims", "Car registration, insurance and property tax all landing at once. Stashday spreads them out."),
      ("Cash stuffers going digital", "The same envelope idea, with the math done for you and no cash to carry.")],
 guide=("guide/sinking-funds-biweekly-paycheck.html", "How to plan sinking funds on a biweekly paycheck"),
 faq=[("What is a sinking fund?", "Money you set aside a little at a time for a bill you know is coming but don't pay every month, like car registration, holidays, insurance or the vet. When the bill arrives, the money is already there."),
      ("How does Stashday work out how much to set aside?", "You tell it when you get paid and add your bills with their amounts and due dates. Stashday works out how much each fund needs from every paycheck between now and the due date, and adds them into one number."),
      ("Does Stashday connect to my bank?", "No, on purpose. You type in your bills once and Stashday does the math. Nothing about your bank ever touches the app."),
      ("Which pay schedules does it support?", "Weekly, every two weeks, twice a month and monthly."),
      ("Is it free?", "Yes, for up to 3 funds, with the payday checklist, reminders and a shareable summary. Stashday Pro is $14.99 a year with a 7-day free trial, or $29.99 once, and adds unlimited funds, Home and Lock Screen widgets and CSV export."),
      ("Can I use it with YNAB or my budget app?", "Yes. Your budget app runs everything. Stashday does one job: the bills that don't come every month. Many people keep both."),
      ("Does Stashday collect my data?", "No. Your funds stay on your iPhone. The App Store privacy label is Data Not Collected."),
      ("Is this financial advice?", "No. Stashday does the arithmetic for the bills you enter. For advice about your situation, talk to a financial professional.")],
 more=["statecount", "mackro", "sitout", "tanklog"],
)

C["tabbed"] = dict(
 name="Tabbed: Journeyman Electrician", short="Tabbed Electrician", category="EducationalApplication", sub="Exam prep", live=False, os="iOS",
 title="Tabbed: Journeyman Electrician Exam Prep for iPhone",
 desc="Practice questions that cite the code section, timed lookup drills for your tabbed code book, step-by-step calcs and exams in your state's format. Pay once.",
 og_title="Tabbed Electrician: know the answer, know where it lives",
 anchor='<section class="pay">',
 vars="--lp-ink:var(--ink);--lp-muted:var(--muted);--lp-card:var(--card);--lp-line:var(--rule);--lp-accent:var(--blue);--lp-accent-ink:#fff;--lp-font:var(--font);--lp-display:var(--font);--lp-paper:var(--page)",
 trust=[("book", "Every answer cites the code section"), ("shield", "A separate blind check on every answer"), ("offline", "Works offline"), ("check", "Pay once, no subscription")],
 who=[("Apprentices with a test date", "3rd to 5th year apprentices getting ready for the journeyman exam, studying on breaks and at night."),
      ("Texas candidates", "Practice exams in Texas's real format, run as two separately scored parts."),
      ("Instructors", "Point your class at questions they can check against the book.")],
 guide=("guide/find-answers-fast-open-book-electrical-exam.html", "How to find answers fast in an open-book electrical exam"),
 faq=[("Which code editions does Tabbed Electrician cover?", "The 2023 and 2026 editions of the National Electrical Code. Your state licensing board tells you which edition your exam uses."),
      ("Does it match my state's exam?", "You set up Tabbed Electrician for your state, and practice exams run in that state's format. Texas, for example, runs as two separately scored parts."),
      ("How do you know the answers are right?", "Every answer cites the code section it comes from and passes a separate blind check before it ships. If you spot a problem, tap Report a problem under the explanation. Fixes ship in updates and the release notes list them."),
      ("Do I need my own code book?", "Yes. Most journeyman exams are open book, and Tabbed Electrician's lookup drills train you to find things fast in your own tabbed book. The app cites sections but doesn't reproduce code text."),
      ("Does Tabbed Electrician work offline?", "Yes. Everything works without a connection, on the job site or in the truck."),
      ("How much is it?", "Free to start: 10 questions a day with explanations, key drills, a 25-question diagnostic and a 10-question sample exam. The Exam Pass is $29.99, a one-time purchase per code edition. No subscription."),
      ("Can Tabbed Electrician guarantee I pass?", "No study tool can. Passing depends on your own preparation. Tabbed Electrician shows a readiness estimate so you can see where to focus."),
      ("Is Tabbed Electrician affiliated with NFPA?", "No. Tabbed Electrician is an independent study aid, not affiliated with or approved by NFPA or any licensing board.")],
 more=["stashday", "sitout", "statecount"],
)

C["tabbed-plumber"] = dict(
 name="Tabbed: Journeyman Plumber", short="Tabbed Plumber", category="EducationalApplication", sub="Exam prep", live=False, os="iOS",
 title="Tabbed: Journeyman Plumber Exam Prep for iPhone",
 desc="Practice questions that cite the UPC or IPC section, timed lookup drills for your tabbed code book, step-by-step plumbing calcs and exams in your state's format. Pay once.",
 og_title="Tabbed Plumber: know the answer, know where it lives",
 anchor='<section class="pay">',
 vars="--lp-ink:var(--ink);--lp-muted:var(--muted);--lp-card:var(--card);--lp-line:var(--rule);--lp-accent:var(--blue);--lp-accent-ink:#fff;--lp-font:var(--font);--lp-display:var(--font);--lp-paper:var(--page)",
 trust=[("book", "Every answer cites the code section"), ("shield", "A separate blind check on every answer"), ("offline", "Works offline"), ("check", "Pay once, no subscription")],
 who=[("Apprentices with a test date", "Plumbing apprentices getting ready for the journeyman exam, studying on breaks and at night."),
      ("UPC and IPC states", "Choose the Uniform Plumbing Code or the International Plumbing Code, and the edition your board uses."),
      ("Instructors", "Point your class at questions they can check against the book.")],
 faq=[("Which codes does Tabbed Plumber cover?", "The Uniform Plumbing Code (2021) and the International Plumbing Code (2018), with fuel gas questions from the International Fuel Gas Code. Your licensing board tells you which code and edition your exam uses."),
      ("Does it match my exam's format?", "You pick the exam you are taking, and practice exams run in that format: the ICC national exams, Kansas, Maryland, Montana, Nebraska, Washington and a UPC exam in the IAPMO format."),
      ("How do you know the answers are right?", "Every answer cites the code section it comes from and passes a separate blind check before it ships. If you spot a problem, tap Report a problem under the explanation. Fixes ship in updates."),
      ("Do I need my own code book?", "Yes. Most journeyman exams are open book, and Tabbed Plumber's lookup drills train you to find things fast in your own tabbed book. The app cites sections but doesn't reproduce code text or tables."),
      ("Does it work offline?", "Yes. Everything works without a connection, on the job site or in the truck. Nothing leaves your phone."),
      ("How much is it?", "Free to start: 10 questions a day with explanations, plus free calc practice. The Exam Pass is $24.99, a one-time purchase that unlocks everything for both codes. No subscription."),
      ("Can it guarantee I pass?", "No study tool can. Passing depends on your own preparation. Tabbed Plumber shows a readiness estimate so you can see where to focus."),
      ("Is it affiliated with IAPMO or ICC?", "No. Tabbed Plumber is an independent study aid, not affiliated with or approved by IAPMO, the International Code Council, PSI, Prometric, Pearson VUE or any licensing board.")],
 more=["tabbed", "stashday", "sitout"],
)

C["fantasyqueens"] = dict(
 name="Fantasy Queens: Drag League", short="Fantasy Queens", category="GameApplication", sub="Fantasy league", live=False, os="iOS",
 title="Fantasy Queens: Drag Fantasy League for Watch Parties",
 desc="Start a private house for your watch-party group. Pick your queens, vote on the rules and see who's leading after every episode. Free to play. Coming soon.",
 og_title="Fantasy Queens: your watch party, scored",
 anchor='<p style="color:var(--muted);font-size:15px;margin-top:36px">Fantasy Queens is an unofficial fan app.',
 vars="--lp-ink:var(--cream);--lp-muted:var(--muted);--lp-card:var(--plum-2);--lp-line:rgba(255,200,87,.18);--lp-accent:var(--gold);--lp-accent-ink:var(--plum)",
 trust=[("noads", "No ads"), ("shield", "No analytics or tracking"), ("users", "Private houses for your group"), ("check", "Free to play")],
 steps=[("Start a house", "Name it, add a photo and send your group the invite link or code."),
        ("Vote on the rules", "Team size, the pick window, what a late pick costs. The majority wins and the rules lock when the season starts."),
        ("Pick every episode", "Picks open when the last episode ends, so nobody picks with spoilers in hand."),
        ("Watch the leaderboard", "Scores post after each episode. See who's leading and who moved up.")],
 feats=[("crown", "Four ways to play", "Weekly Call, Survival Bracket, Team and Boot Pick."),
        ("home", "Host cards", "Time, address and notes for the watch party, with RSVPs and a bring list."),
        ("message", "A house board", "Trash talk, reminders and an episode chat that opens when it airs."),
        ("list", "A rule book", "Every rule your house voted on, in one place anyone can read."),
        ("calendar", "Every season", "Including ones that haven't started, with premiere dates."),
        ("check", "Who's paid", "If your group chips in, the House Mother can mark who's paid. The app never touches money.")],
 faq=[("What is Fantasy Queens?", "A fantasy league app for drag watch-party groups. Your group starts a private house, everyone makes picks each episode, and a leaderboard shows who's leading after every episode."),
      ("How do we join a house?", "Whoever starts the house shares an invite link or code. Open it on your iPhone and you're in."),
      ("What are the ways to play?", "Weekly Call (one queen for the top, one safe, one for the bottom), Survival Bracket (rank the whole cast before the season), Team (pick a team each week) and Boot Pick (call who goes home, with a backup for a double elimination)."),
      ("When do picks lock?", "Picks for each episode open when the last one ends. Pick before or during the episode, or late for a small penalty your house sets. Everyone's picks show once the episode starts."),
      ("Does the app handle money?", "No. If your group chips in, the House Mother can mark who's paid, but payments stay between you and your friends."),
      ("Do I need an account?", "Yes, so your house knows it's you. Sign in with Apple, Google or email."),
      ("Is it free?", "Yes, it's free to play. If the app offers an optional purchase, its price is shown before you buy."),
      ("Is Fantasy Queens official?", "No. It's an unofficial fan app, not affiliated with, endorsed by or sponsored by any television network, production company or performer.")],
 more=["mvn", "sitout", "mackro"],
)

C["statecount"] = dict(
 name="Statecount: Residency Tracker", short="Statecount", category="FinanceApplication", sub="Residency day counter", live=False, os="iOS",
 title="Statecount: 183-Day Residency Tracker for iPhone",
 desc="A private, day-by-day record of which state or country you were in, with alerts before a day limit like 183 days. Your location never leaves your phone.",
 og_title="Statecount: count your days in every state, privately",
 anchor='<p><strong>Coming soon to the App Store.</strong></p>',
 vars="--lp-ink:var(--ink);--lp-muted:var(--muted);--lp-card:var(--wash);--lp-line:rgba(127,127,127,.22);--lp-accent:var(--green);--lp-accent-ink:#fff",
 steps=[("Turn it on", "Statecount works out which state or country you're in on your iPhone, each day."),
        ("Set a limit", "Like 183 days in New York. Statecount counts days used and days left."),
        ("Get a heads-up", "Alerts at 30, 14 and 7 days left, before you reach the limit."),
        ("Keep the record", "Every day, with where the entry came from, ready to export as a PDF and CSV for your tax professional.")],
 plans=[("Free", "$0", "forever", ["Log each day by hand", "One limit", "The current year"], False),
        ("Statecount Pro", "$29.99/yr", "or $59.99 once. 7 days free on the yearly plan.", ["Automatic logging in the background", "As many limits as you need", "Every year, all your history", "Widgets and alerts"], True)],
 fine="Coming soon to the App Store. The yearly plan renews automatically unless canceled at least 24 hours before the end of the period, managed in Settings, then your name, then Subscriptions. Prices shown in US dollars.",
 guide=("guide/how-the-183-day-rule-counts-a-day.html", "How the 183-day rule counts a day"),
 faq=[("How does Statecount know which state I'm in?", "Your iPhone's location is matched, on the phone, against map boundaries built into the app (US Census and Natural Earth data). The app makes no network calls of its own."),
      ("Does my location leave my phone?", "No. There's no account, no server and no analytics, and the App Store privacy label is Data Not Collected. If you turn on iCloud sync, your days sync through your own private iCloud."),
      ("What counts as a day?", "Statecount records every state or country you were in on each date, so a travel day shows both places. How a day counts depends on the rule. New York's tax department, for example, says any part of a day is a day. Your tax professional can tell you how a rule applies to you."),
      ("Can I fix or add days?", "Yes. You can add or edit any day by hand. Each record shows whether it came from your phone's location or from you, and days with no record are flagged so you can fill them in."),
      ("What's in the report?", "Every day of the year and where it was recorded, exported as a PDF and a CSV you can share with your tax professional."),
      ("Does it work outside the US?", "Statecount records countries as well as US states, so a week in Canada shows as Canada."),
      ("Is it free?", "Yes, to log by hand with one limit for the current year. Statecount Pro is $29.99 a year with a 7-day free trial, or $59.99 once, and adds automatic logging, as many limits as you need, every year of history, widgets and alerts."),
      ("Is Statecount tax advice?", "No. Statecount keeps records. It is not tax or legal advice, and it doesn't know which rules apply to you.")],
 more=["stashday", "mackro", "sitout"],
)

C["tanklog"] = dict(
 name="TankLog: Aquascape", short="TankLog", category="UtilitiesApplication", sub="Aquarium journal", live=True, appid="6762062161", os="iOS",
 title="TankLog: Aquarium Journal for Planted Tanks and Shrimp",
 desc="A free, offline aquarium journal for planted tank and shrimp keepers. Water tests, CO₂, care schedules and dosing. No login, no ads. Your data stays on your device.",
 og_title="TankLog: the tank journal for people who track everything",
 anchor='<div class="end">',
 vars="--lp-ink:var(--fg);--lp-muted:var(--muted);--lp-card:var(--card);--lp-line:var(--line);--lp-accent:var(--teal);--lp-accent-ink:#04202a;--lp-font:var(--font)",
 who=[("Planted tank keepers", "Watch pH, KH and CO₂ together, and see when a number starts to drift."),
      ("Shrimp keepers", "Log KH, GH, TDS and water changes for a neocaridina or caridina colony."),
      ("Anyone who logs everything", "Water tests, dosing, feeding and cleaning in one place, with a history you can export.")],
 faq=[("What is TankLog?", "A free aquarium journal for freshwater planted tank and shrimp keepers. You log water tests, care tasks, dosing, livestock, plants and equipment, and watch the trends."),
      ("Is TankLog free?", "Yes. TankLog is free, with no ads and no subscription. An optional Cloud Sync, a one-time purchase, is planned for a coming update."),
      ("Do I need an account?", "No. There's no login. Everything you enter is stored on your device."),
      ("Does it work offline?", "Yes. TankLog works without a signal."),
      ("Which water parameters can I log?", "pH, ammonia, nitrite, nitrate, KH, GH, phosphate, TDS and temperature, graded against your own target ranges."),
      ("How does the CO₂ estimate work?", "TankLog works out dissolved CO₂ from your pH and KH and shows it as a color-coded zone. It's an estimate, so use it as a guide."),
      ("How many tanks can I track?", "Up to three, each with its own parameters, schedules and history."),
      ("Can I export my data?", "Yes. Export your full history as a file you control and import it on a new device. You can also delete your data any time."),
      ("Does it run on iPad?", "Yes. TankLog runs on iPhone and iPad."),
      ("Who makes TankLog?", "TankLog is built by an aquascaper, for aquascapers, and is published here alongside the other apps from John Katez.")],
 more=["stashday", "mackro", "statecount"],
)

C["mvn"] = dict(
 name="Music Video Night", category="GameApplication", live=True, appid="6811704618", keep_jsonld=True,
 title="Music Video Night: The Music Video Party Game for iPhone",
 desc="Everyone picks a music video, watches together and votes. One person wins the Night. A party game for iPhone that plays on your TV. Free to join.",
 og_title="Music Video Night: the music video party game",
 og_desc="Everyone picks a music video. Everyone watches together. Everyone votes. One person wins the Night.",
 anchor="<footer data-brand-footer",
 vars="--lp-ink:var(--ink);--lp-muted:var(--ink-2);--lp-accent:#7B3DFF;--lp-accent-ink:#fff",
 more=["fantasyqueens", "sitout", "mackro"],
)


C[""] = dict(
 name="Apps by John Katez", hub=True,
 title="Apps by John Katez: Small, Fair iPhone Apps",
 desc="Nine iPhone apps: Music Video Night, Mackro, TankLog, Stashday, Tabbed Electrician, Tabbed Plumber, Fantasy Queens, Sitout and Statecount. Small apps, no ads.",
 og_title="Apps by John Katez",
 og_image="https://apps.johnkatez.com/img/og-hub.jpg",
 anchor="<footer",
 vars="--lp-ink:#F2F2F7;--lp-muted:#A1A1A6;--lp-card:rgba(255,255,255,.06);--lp-line:rgba(255,255,255,.12);--lp-accent:#9867FF;--lp-accent-ink:#fff;--lp-font:var(--font);--lp-display:var(--round)",
 faq=[("Who makes these apps?", "John Katez, an independent iPhone developer. TankLog was built by an aquascaper and is published here too. Each app does one job and has its own support and privacy page."),
      ("Do the apps have ads?", "No. None of the apps show ads."),
      ("What data do the apps collect?", "Each app's privacy page says exactly. Stashday, Statecount, Sitout, Tabbed Electrician, Tabbed Plumber and TankLog collect no data. Music Video Night has no accounts, analytics or servers. Mackro uses anonymous analytics and sends only what you submit for AI logging. Fantasy Queens collects only what a house needs to work."),
      ("How much do they cost?", "Every app is free to download. Some offer an optional upgrade, one-time or yearly, with the price shown in the app before you buy."),
      ("Are the apps on Android?", "Not yet. They're made for iPhone, and some also run on iPad."),
      ("How do I get help?", "Email support@johnkatez.com, or open the Support page for the app you're using.")],
)

# ---------------------------------------------------------------- render
def esc(s):
    return html.escape(s, quote=True)


def jsonld(slug, c):
    url = f"{SITE}/{slug}/" if slug else f"{SITE}/"
    out = []
    if c.get("hub"):
        items = [{"@type": "ListItem", "position": i + 1, "url": f"{SITE}/{s}/", "name": APPS[s][0]} for i, s in enumerate(["mvn", "mackro", "tanklog", "stashday", "tabbed", "tabbed-plumber", "fantasyqueens", "sitout", "statecount"])]
        out.append({"@context": "https://schema.org", "@type": "WebSite", "name": "Apps by John Katez", "url": url, "publisher": PUBLISHER})
        out.append({"@context": "https://schema.org", "@type": "ItemList", "name": "iPhone apps by John Katez", "itemListElement": items})
        out.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in c["faq"]]})
        return "".join(f'<script type="application/ld+json">{json.dumps(o, ensure_ascii=False)}</script>' for o in out)
    if not c.get("keep_jsonld"):
        app = {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": c["name"], "applicationCategory": c["category"],
               "operatingSystem": "iOS", "url": url, "description": c["desc"], "image": f"{SITE}/{slug}/img/icon.png", "publisher": PUBLISHER,
               "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
        if c.get("sub"):
            app["applicationSubCategory"] = c["sub"]
        if c.get("live"):
            app["installUrl"] = app["downloadUrl"] = f"https://apps.apple.com/app/id{c['appid']}"
            app["sameAs"] = [app["installUrl"]]
        out.append(app)
        if c.get("faq"):
            out.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in c["faq"]]})
    out.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Apps by John Katez", "item": f"{SITE}/"},
        {"@type": "ListItem", "position": 2, "name": c.get("short", c["name"]), "item": url}]})
    return "".join(f'<script type="application/ld+json">{json.dumps(o, ensure_ascii=False)}</script>' for o in out)


def head_block(slug, c):
    depth = "../" if slug else ""
    return f'<!-- lp:head --><link rel="stylesheet" href="/assets/lp.css">{jsonld(slug, c)}<!-- /lp:head -->'


def sec(inner, extra=""):
    return f'<section class="lp"{extra}><div class="lp-in">{inner}</div></section>'


def body_block(slug, c):
    short = c.get("short", c["name"])
    parts = []
    if c.get("trust"):
        parts.append('<ul class="lp-trust" aria-label="At a glance">' + "".join(f"<li>{icon(i, 18)}{esc(t)}</li>" for i, t in c["trust"]) + "</ul>")
    if c.get("steps"):
        parts.append(f'<h2>How it works</h2><ol class="lp-steps">' + "".join(f"<li><b>{esc(a)}</b><span>{esc(b)}</span></li>" for a, b in c["steps"]) + "</ol>")
    if c.get("feats"):
        parts.append(f'<h2>What\'s inside</h2><ul class="lp-feat">' + "".join(f'<li><span class="ic">{icon(i)}</span><div><b>{esc(a)}</b><span>{esc(b)}</span></div></li>' for i, a, b in c["feats"]) + "</ul>")
    blocks = []
    if parts:
        blocks.append(sec('<div style="display:grid;gap:44px">' + "".join(parts) + "</div>"))
    if c.get("who"):
        blocks.append(sec(f"<h2>Who it's for</h2>" + '<div class="lp-who">' + "".join(f"<div><b>{esc(a)}</b><p>{esc(b)}</p></div>" for a, b in c["who"]) + "</div>"))
    if c.get("priv"):
        h, ps = c["priv"]
        blocks.append(sec(f'<div class="lp-priv"><span class="ic">{icon("lock", 30)}</span><div><h3>{esc(h)}</h3>' + "".join(f"<p>{esc(p)}</p>" for p in ps) + f'<p><a href="privacy.html">Read the privacy policy</a></p></div></div>'))
    if c.get("plans"):
        cards = "".join(f'<div class="lp-plan{" hl" if hl else ""}"><h3>{esc(n)}</h3><div class="price">{esc(p)}</div><div class="per">{esc(per)}</div><ul>' + "".join(f"<li>{esc(x)}</li>" for x in items) + "</ul></div>" for n, p, per, items, hl in c["plans"])
        blocks.append(sec(f'<h2>Pricing</h2><div class="lp-plans">{cards}</div><p class="lp-fine">{esc(c.get("fine", ""))}</p>', ' id="pricing"'))
    if c.get("faq"):
        qa = "".join(f'<details><summary>{esc(q)}</summary><div class="a"><p>{esc(a)}</p></div></details>' for q, a in c["faq"])
        g = ""
        if c.get("guide"):
            gp, gt = c["guide"]
            g = f'<p class="lp-fine" style="font-size:15.5px">Guide: <a href="{gp}">{esc(gt)}</a></p>'
        blocks.append(sec(f'<h2>Questions people ask</h2><div class="lp-faq">{qa}</div>{g}', ' id="faq"'))
    if c.get("hub") and blocks:
        pass
    if c.get("more"):
        tiles = "".join(f'<a href="/{s}/"><img src="/{s}/img/icon.png" alt="" width="52" height="52" loading="lazy"><div><b>{esc(APPS[s][0])}</b><span>{esc(APPS[s][1])}</span></div></a>' for s in c["more"])
        blocks.append(sec(f'<h2 style="font-size:24px">More small apps from the same maker</h2><div class="lp-more">{tiles}</div><p class="lp-fine"><a href="/">See all the apps</a></p>'))
    style = f'<style>:root{{{c["vars"]}}}</style>' if c.get("vars") else ""
    return f"<!-- lp:body -->{style}{''.join(blocks)}<!-- /lp:body -->"


def legal_block():
    return f'<!-- lp:legal --><div class="lp-legal"><p>{esc(HOUSE_LINE)}</p><p>{esc(APPLE_CREDIT)}</p></div><!-- /lp:legal -->'


def set_meta(h, c):
    def sub(pattern, value, h):
        return re.sub(pattern, lambda m: m.group(1) + esc(value) + m.group(2), h, count=1)
    h = re.sub(r"<title>.*?</title>", f"<title>{esc(c['title'])}</title>", h, count=1, flags=re.S)
    h = sub(r'(<meta name="description" content=")[^"]*(")', c["desc"], h)
    ogt, ogd = c.get("og_title", c["title"]), c.get("og_desc", c["desc"])
    h = sub(r'(<meta property="og:title" content=")[^"]*(")', ogt, h)
    h = sub(r'(<meta property="og:description" content=")[^"]*(")', ogd, h)
    h = sub(r'(<meta name="twitter:title" content=")[^"]*(")', ogt, h)
    h = sub(r'(<meta name="twitter:description" content=")[^"]*(")', ogd, h)
    if '<meta name="twitter:title"' not in h:
        h = h.replace("</head>", f'<meta name="twitter:title" content="{esc(ogt)}"><meta name="twitter:description" content="{esc(ogd)}"></head>', 1)
    if 'name="twitter:card"' not in h:
        m = re.search(r'<meta property="og:image" content="([^"]+)"', h)
        img = m.group(1) if m else ""
        h = h.replace("</head>", f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{img}"></head>', 1)
    if c.get("og_image"):
        h = re.sub(r'(<meta property="og:image" content=")[^"]*(")', lambda m: m.group(1) + c["og_image"] + m.group(2), h, count=1)
        h = re.sub(r'(<meta name="twitter:image" content=")[^"]*(")', lambda m: m.group(1) + c["og_image"] + m.group(2), h, count=1)
    if c.get("live") and 'name="apple-itunes-app"' not in h:
        h = h.replace("</head>", f'<meta name="apple-itunes-app" content="app-id={c["appid"]}"></head>', 1)
    return h


def replace_or_insert(h, start, end, block, where):
    if start in h:
        return re.sub(re.escape(start) + r".*?" + re.escape(end), lambda m: block, h, count=1, flags=re.S)
    if where not in h:
        raise SystemExit(f"anchor not found: {where[:60]}")
    return h.replace(where, block + where, 1)


def patch(slug, c):
    p = (ROOT / slug / "index.html") if slug else (ROOT / "index.html")
    h = p.read_text()
    h = set_meta(h, c)
    h = replace_or_insert(h, "<!-- lp:head -->", "<!-- /lp:head -->", head_block(slug, c), "</head>")
    h = replace_or_insert(h, "<!-- lp:body -->", "<!-- /lp:body -->", body_block(slug, c), c["anchor"])
    if "<!-- lp:legal -->" in h:
        h = re.sub(r"<!-- lp:legal -->.*?<!-- /lp:legal -->", lambda m: legal_block(), h, count=1, flags=re.S)
    else:
        m = re.search(r"<footer data-brand-footer[^>]*>.*?</footer>", h, re.S)
        h = h[:m.end()] + legal_block() + h[m.end():] if m else h.replace("</body>", legal_block() + "</body>", 1)
    p.write_text(h)
    print("patched", slug)


if __name__ == "__main__":
    for s, c in C.items():
        patch(s, c)
