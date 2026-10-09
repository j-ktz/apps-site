# Landing pages v3 and johnkatez.com — design

Approved by John on 2026-10-08. Bar: every page as immersive as the MVN hero (dark or saturated stage,
huge type, a playable piece of the real product).

## Fixes
- Mackro: the side-by-side phones stretched in a flex row, so `object-fit: cover` cropped the screenshot.
  Fix: `align-items: flex-start`.
- Tabbed: "iPhone, pay once" wrapped beside the button on phones. Put the note on its own line.
- Every page sets `theme-color` so Safari's toolbar matches the stage.

## apps.johnkatez.com (hub)
An iPhone home screen. One live widget per app, each a tiny version of its page's demo
(Mackro ring fills, Stashday number ticks, Tabbed timer runs, MVN vote reveals). The page background
shifts to the brand color of the widget you hover or focus. Widgets link to each app page.

## App pages
- Mackro: sun-yellow stage, huge Mack, the food demo as the hero. Rest of the page keeps its sections.
- Stashday: forest-green hero with three fund rings that fill while the number counts up.
  Payday scroll scene stays; tighter on phones.
- Tabbed: dark blueprint "after hours" hero with the live drill and a CSS code book whose
  fore-edge tabs slide out. Chapters keep their content.
- MVN: unchanged (it is the reference).

## johnkatez.com
Rebuilt in the existing Astro repo (`j-ktz/johnkatez-portfolio`, Cloudflare Pages).
Sections: short intro in John's voice, Apps (links into the hub), Work (anonymized case studies,
"a national healthcare system", resume link kept), contact.
Rules: no job-search language, no freelance pitch, no superlatives. Reviewed on a preview URL before
anything reaches the live domain.

## Constraints (all pages)
No third-party fonts, scripts or trackers. Reduced motion respected. Visible focus. No horizontal
scroll at 390px. Copy names only features that exist or are labeled as coming.
