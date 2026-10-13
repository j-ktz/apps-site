#!/usr/bin/env python3
"""Answer-first guide pages (SEO + AI answers). Run from the repo root: python3 tools/guides.py
Each guide: one question, the answer in the first paragraph, sources, and the app as one honest option.
"""
import html, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://apps.johnkatez.com"
PUB = {"@type": "Person", "name": "John Katez", "url": "https://johnkatez.com/"}
CREDIT = "Apple, the Apple logo and iPhone are trademarks of Apple Inc., registered in the U.S. and other countries. App Store is a service mark of Apple Inc."
HOUSE = "Small apps that each do one job well. No ads, fair prices, and only the data the app needs."
e = lambda s: html.escape(s, quote=True)


def page(slug, file, app, theme, title, desc, h1, answer_html, body_html, faq, sources, note, date="2026-10-12"):
    url = f"{SITE}/{slug}/guide/{file}"
    og_img = {"statecount": f"{SITE}/statecount/img/og.jpg", "stashday": f"{SITE}/stashday/hero.jpg", "tabbed": f"{SITE}/tabbed/og-image.png"}[slug]
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": h1, "description": desc, "datePublished": date, "dateModified": date,
           "author": PUB, "publisher": PUB, "mainEntityOfPage": url, "image": og_img},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "Apps by John Katez", "item": f"{SITE}/"},
              {"@type": "ListItem", "position": 2, "name": app, "item": f"{SITE}/{slug}/"},
              {"@type": "ListItem", "position": 3, "name": h1, "item": url}]}]
    if faq:
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]})
    faq_html = ""
    if faq:
        faq_html = '<h2>Quick answers</h2><div class="lp-faq">' + "".join(f'<details><summary>{e(q)}</summary><div class="a"><p>{e(a)}</p></div></details>' for q, a in faq) + "</div>"
    src = "<h2>Sources</h2><ul>" + "".join(f'<li><a href="{u}">{e(t)}</a></li>' for t, u in sources) + "</ul>" if sources else ""
    paper, ink, muted, card, line, accent = theme
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}">
<meta property="og:type" content="article"><meta property="og:site_name" content="{e(app)}"><meta property="og:title" content="{e(h1)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{og_img}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(h1)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{og_img}">
<link rel="icon" href="/{slug}/img/icon.png"><link rel="stylesheet" href="/assets/lp.css">
<style>:root{{--lp-paper:{paper};--lp-ink:{ink};--lp-muted:{muted};--lp-card:{card};--lp-line:{line};--lp-accent:{accent};--lp-accent-ink:#fff}}
body{{margin:0;background:{paper};color:{ink};font:18px/1.6 -apple-system,BlinkMacSystemFont,"SF Pro Text",system-ui,sans-serif}}
header.g{{max-width:720px;margin:0 auto;padding:18px 20px;display:flex;justify-content:space-between;align-items:center}}
header.g a{{color:{ink};text-decoration:none;font-weight:700;display:flex;gap:10px;align-items:center}} header.g img{{width:30px;height:30px;border-radius:8px}}
</style>
{''.join(f'<script type="application/ld+json">{json.dumps(o, ensure_ascii=False)}</script>' for o in ld)}
</head><body class="lp">
<header class="g"><a href="/{slug}/"><img src="/{slug}/img/icon.png" alt="">{e(app)}</a><a href="/" style="font-weight:500;color:{muted}">All apps</a></header>
<main class="lp-article"><p class="crumbs"><a href="/">Apps</a> / <a href="/{slug}/">{e(app)}</a> / Guide</p>
<h1>{e(h1)}</h1><div class="answer">{answer_html}</div>{body_html}{faq_html}{src}<p class="note">{note}</p><p class="note">Published {date}.</p></main>
<footer data-brand-footer style="max-width:680px;margin:0 auto;padding:24px 16px 40px;text-align:center;font:14px -apple-system,sans-serif;opacity:.6">© 2026 {e(app)} · <a href="mailto:support@johnkatez.com" style="color:inherit">support@johnkatez.com</a> · <a href="/" style="color:inherit">All apps</a></footer>
<!-- lp:legal --><div class="lp-legal"><p>{e(HOUSE)}</p><p>{e(CREDIT)}</p></div><!-- /lp:legal -->
</body></html>"""


def cta(slug, app, line, soon=True):
    act = '<span class="lp-soon" style="padding:8px 14px;font-size:14px">Coming soon to the App Store</span>' if soon else f'<a href="/{slug}/">See {e(app)}</a>'
    return f'<div class="cta"><img src="/{slug}/img/icon.png" alt=""><div><b>{e(app)}</b><p style="margin:4px 0 8px;font-size:16px">{e(line)}</p>{act}</div></div>'


def write(slug, file, text):
    d = ROOT / slug / "guide"; d.mkdir(exist_ok=True)
    (d / file).write_text(text); print("wrote", slug, file)


# ---------------- Statecount
sc_body = f"""
<h2>Two different "183-day rules"</h2>
<p>People say "the 183-day rule" for two separate tests.</p>
<table><thead><tr><th>Test</th><th>Who it's about</th><th>The day count</th></tr></thead><tbody>
<tr><td><b>State residency</b> (New York, for example)</td><td>People domiciled elsewhere who keep a home in the state</td><td>New York treats you as a resident if you keep a permanent place of abode there for substantially all of the year <b>and</b> spend 184 days or more in the state.</td></tr>
<tr><td><b>Federal substantial presence test</b> (IRS)</td><td>People who aren't US citizens or green card holders</td><td>At least 31 days this year, and 183 days over three years counting all days this year, a third of last year's days and a sixth of the year before.</td></tr>
</tbody></table>
<p>Other states have their own versions. Many use a similar "more than 183 days plus a home" test, but the details differ.</p>
<h2>How a day is counted</h2>
<p>The key word is <b>presence</b>, not nights. New York's tax department puts it in one line: "Any part of a day is a day for this purpose." The IRS says you are treated as present on any day you are physically present in the country.</p>
<table><thead><tr><th>What happened (example)</th><th>How it usually counts</th></tr></thead><tbody>
<tr><td>You drove into New York for lunch and left at 3 PM</td><td>A New York day, under New York's rule</td></tr>
<tr><td>You flew out of New York at 7 AM</td><td>A New York day</td></tr>
<tr><td>You were in New Jersey and New York on the same date</td><td>Each state applies its own rule, so one date can count in both</td></tr>
<tr><td>A layover under 24 hours, between two places outside the US</td><td>Not counted for the IRS test (an exception)</td></tr>
</tbody></table>
<p>There are other exceptions (for example, some commuters from Canada or Mexico, and certain visa holders for the IRS test), so check the exact rule that applies to you.</p>
<h2>Why a day-by-day record matters</h2>
<p>If a tax department asks where you were, you're the one who has to show it, and memory doesn't hold up well a year later. Practitioners commonly point to records like receipts, calendars and phone location history. A record kept as you go, with where each entry came from, is easier to stand behind than one rebuilt from a credit card statement.</p>
{cta("statecount", "Statecount", "Keeps a private, day-by-day record of the state or country you were in, with alerts before a limit you set. Your location never leaves your phone.")}
"""
sc_faq = [("Does part of a day count as a day?", "Under many state rules, yes. New York's tax department says any part of a day is a day for its residency count. The IRS treats you as present on any day you are physically in the US, with some exceptions."),
          ("Is the 183-day rule the same in every state?", "No. Each state sets its own test, and the federal substantial presence test is a separate rule with its own weighted formula."),
          ("Does Statecount tell me if I'm a resident?", "No. Statecount keeps records. It is not tax or legal advice. A tax professional can tell you how the rules apply to you.")]
sc_src = [("New York State Department of Taxation and Finance: definitions of resident, nonresident and part-year resident", "https://www.tax.ny.gov/pit/file/pit_definitions.htm"),
          ("IRS: Substantial presence test", "https://www.irs.gov/individuals/international-taxpayers/substantial-presence-test"),
          ("IRS Publication 519: U.S. Tax Guide for Aliens", "https://www.irs.gov/publications/p519")]
write("statecount", "how-the-183-day-rule-counts-a-day.html", page("statecount", "how-the-183-day-rule-counts-a-day.html", "Statecount",
      ("#FFFFFF", "#1C1C1E", "#5F6368", "#EEF3F9", "rgba(0,0,0,.10)", "#1E5799"),
      "How the 183-Day Rule Counts a Day (State and IRS)", "Under many residency rules, any part of a day in a place counts as a full day there. Here's how New York and the IRS count days, with examples and sources.",
      "How the 183-day rule counts a day",
      "<p><b>Under many residency rules, any part of a day in a place counts as a full day there.</b> New York's tax department says it plainly: \"Any part of a day is a day for this purpose.\" So a morning flight out or a lunch stop can each add a day. There are exceptions, so check the rule that applies to you with a tax professional.</p>",
      sc_body, sc_faq, sc_src, "Statecount keeps records. It is not tax or legal advice. Rules change and have exceptions: confirm with a tax professional."))

# ---------------- Stashday
bills = [("Car registration", 268, 10), ("Holiday gifts", 900, 5), ("Car insurance", 1200, 26), ("Vet checkup", 300, 26)]
rows = ""; total = 0
for n, amt, pays in bills:
    per = amt / pays; total += per
    rows += f"<tr><td>{n}</td><td>${amt:,}</td><td>{pays}</td><td>${per:,.2f}</td></tr>"
rows += f"<tr><td><b>Set aside each paycheck</b></td><td></td><td></td><td><b>${total:,.2f}</b></td></tr>"
sd_body = f"""
<h2>The method, step by step</h2>
<ol><li><b>List every bill that doesn't come monthly:</b> car registration, insurance, holidays and birthdays, the vet, subscriptions you pay yearly, property tax.</li>
<li><b>Write down each amount and due date.</b> Use last year's amount if you don't know this year's.</li>
<li><b>Count the paychecks left before each due date.</b> Paid every two weeks, that's roughly one paycheck per two weeks between now and the bill.</li>
<li><b>Divide each bill by its paychecks.</b> That's the amount for that fund each payday.</li>
<li><b>Add them up.</b> That total is the one number to move into savings every payday.</li></ol>
<h2>A worked example (made-up numbers)</h2>
<table><thead><tr><th>Bill</th><th>Amount</th><th>Paychecks until due</th><th>Per paycheck</th></tr></thead><tbody>{rows}</tbody></table>
<p class="note">Example only. Your bills, dates and paychecks will differ.</p>
<h2>The biweekly bonus: three-paycheck months</h2>
<p>Paid every two weeks, you get 26 paychecks in most years (27 in some). Since a year has 12 months, two months bring a third paycheck. That extra check is a good moment to catch up on a fund that started late, or to get ahead on next year's big bill.</p>
<h2>When a bill is close and the fund is behind</h2>
<p>A bill due soon with few paychecks left needs a bigger amount per payday. You can either accept a higher number for a few paydays, or move that bill to next year's plan and cover this one from savings. Starting early is what keeps each payday's number small.</p>
{cta("stashday", "Stashday", "Does this math for you: add your bills once and see one number to set aside each payday. No bank login.")}
"""
sd_faq = [("How much should I put in a sinking fund each paycheck?", "Divide the bill's amount by the number of paychecks left before it's due, then add up all your funds. That total is what to set aside each payday."),
          ("How many paychecks do biweekly earners get a year?", "26 in most years, and 27 in some, depending on how the paydays fall. That means two months a year usually bring a third paycheck."),
          ("Is a sinking fund the same as an emergency fund?", "No. A sinking fund is for a bill you know is coming. An emergency fund is for the ones you don't see coming.")]
write("stashday", "sinking-funds-biweekly-paycheck.html", page("stashday", "sinking-funds-biweekly-paycheck.html", "Stashday",
      ("#FBF8F3", "#12201A", "#5d6a63", "#FFFFFF", "#E6E0D3", "#16805F"),
      "How to Plan Sinking Funds on a Biweekly Paycheck", "Divide each irregular bill by the paychecks left before it's due, add them up, and set aside that one number every payday. A worked example for biweekly pay.",
      "How to plan sinking funds on a biweekly paycheck",
      f"<p><b>Divide each irregular bill by the number of paychecks left before it's due, add the results, and set aside that total every payday.</b> Paid every two weeks, a $520 bill due in a year needs $20 a paycheck. In the example below, four common bills come to <b>${total:,.2f}</b> a paycheck.</p>",
      sd_body, sd_faq, [], "Stashday does arithmetic for the bills you enter. It is not financial advice."))

# ---------------- Tabbed
tb_body = f"""
<h2>1. Check what your exam allows</h2>
<p>Rules on tabs, highlighting and notes in the code book vary by state and testing provider. Read your candidate handbook first, so the book you practice with is the book they'll let you bring.</p>
<h2>2. Tab the book before exam day</h2>
<p>Tab the parts you'll reach for most, so you can open close to the answer and finish with the index. A common starting set:</p>
<ul><li><b>Article 100</b> (definitions)</li><li><b>Articles 210 and 220</b> (branch circuits and load calculations)</li><li><b>Articles 230 and 240</b> (services and overcurrent protection)</li><li><b>Article 250</b> (grounding and bonding)</li><li><b>Articles 300, 310 and 314</b> (wiring methods, conductors and ampacity tables, boxes)</li><li><b>Article 430</b> (motors) and <b>Article 450</b> (transformers)</li><li><b>Chapter 9 tables</b> and <b>Annex C</b> (conduit and tubing fill)</li></ul>
<p>Use one color per group and keep the tabs readable from the edge. Some candidates add a tab for each table they use in calculations.</p>
<h2>3. Use the index, not the table of contents</h2>
<p>Pick the most specific word in the question ("receptacle", "bathroom", "ground-fault") and look it up in the index. It points to the section, and your tab gets you to the right part of the book quickly.</p>
<h2>4. Practice against a clock</h2>
<p>Divide your exam's time limit by its number of questions. That's your average time per question. Practice lookups until most take less than that, and skip anything that's eating your time. You can come back to it at the end.</p>
<h2>5. For calculations, write the reference first</h2>
<p>Before doing the math, note the section or table you're using. It keeps you from mixing up tables, and it lets you check your work quickly if time allows.</p>
{cta("tabbed", "Tabbed: Journeyman Electrician", "Timed lookup drills for your own tabbed code book, practice questions that cite the code section, and exams in your state's format.")}
"""
tb_faq = [("Are journeyman electrician exams open book?", "Many are, but not all, and the rules on tabs and notes vary. Check your state's candidate handbook."),
          ("What should I tab in the NEC?", "Most people tab the articles they use most (definitions, branch circuits and load calculations, services, overcurrent protection, grounding and bonding, wiring methods and conductors, motors, transformers) plus the Chapter 9 tables and Annex C."),
          ("How do I get faster at looking things up?", "Practice with a timer, start from the index with the most specific word in the question, and skip anything that runs long.")]
write("tabbed", "find-answers-fast-open-book-electrical-exam.html", page("tabbed", "find-answers-fast-open-book-electrical-exam.html", "Tabbed",
      ("#ECE6D6", "#14181F", "#59616d", "#F6F4EE", "#D8D0BB", "#0064D2"),
      "How to Find Answers Fast in an Open-Book Electrical Exam", "Tab your code book before exam day, start from the index, and practice lookups against a clock. A practical guide for journeyman electrician candidates.",
      "How to find answers fast in an open-book electrical exam",
      "<p><b>Tab your code book before exam day, start every lookup from the index, and practice against a clock.</b> Most journeyman electrician exams are open book with a time limit, so the skill that matters is finding the right section quickly, not memorizing it.</p>",
      tb_body, tb_faq, [], "Tabbed is an independent study aid, not affiliated with or approved by NFPA or any licensing board. NEC® and National Electrical Code® are registered trademarks of the National Fire Protection Association, Quincy, MA. Check your own exam's rules."))
