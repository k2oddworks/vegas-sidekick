# Vegas Sidekick — Brand Bible

**What this is:** the brand, voice and editorial rulebook for `vegassidekick.com`.
Paste it into a fresh chat to bring it up to speed on *what we sound like and why*.

**Its sibling:** `CLAUDE.md` in this repo is the **technical** doc — file layout, build
conventions, the price-change and show-closing checklists, JSON-LD requirements. This
doc deliberately does not repeat it. When the two touch the same subject, CLAUDE.md
wins on mechanics, BRAND.md wins on wording.

*Accurate as of 2026-08-26.*

---

## 1. The business in one paragraph

Vegas Sidekick is a static affiliate site that helps people pick and book Las Vegas
shows. We do not sell tickets. Every "Get Tickets" button hands the visitor to
**Spotlight.vegas** with `/ref/vegassidekick` appended, and we earn a commission. That
single fact shapes everything: we make money only when someone books a show they're
glad they booked. There is no upsell, no membership, no email wall, no fee we collect.
Our incentive and the visitor's are pointed the same direction, and the writing should
make that obvious without ever saying "trust us."

Hosted on Cloudflare Pages. No build step, no framework, no npm. Deploying is pushing
to `main`.

---

## 2. Positioning

**We are the local friend who works in tickets, not a listings site.**

The category is crowded with two kinds of competitor: giant OTAs with a million SKUs
and no opinion, and thin SEO affiliate blogs with opinions but no expertise. We sit in
the gap — a real Vegas local, actually in the industry, who has seen the shows and
will tell you which ones are worth it and which are not.

**The promise, verbatim from the site:**

> Handpicked Las Vegas show tickets at legit discounts. No membership, no hidden fees,
> no markup games. Your Vegas insider — guaranteed.

**The homepage headline:** *More Vegas. Less "how much?"*

**What we are not:** a coupon site, a hype machine, a review aggregator, or a
comprehensive database. We list ~60 shows because we have something to say about ~60
shows. Coverage is a means, not the goal.

---

## 3. Kris Kidd — the author entity

Every article, guide and recommendation carries Kris's byline and links to
`/about/kris-kidd/`, the canonical `Person` entity page. This is deliberate E-E-A-T
work: Google needs a real, consistent human behind the opinions.

**Use these facts. Do not invent new ones.**

- Las Vegas local since **2005**
- In show **ticketing since 2006** — roughly 15+ years across ticketing and concierge
- Most recently high-end concierge at **Hilton Grand Vacation Club**
- Has seen **100+** Vegas shows
- Personal favourites: **VEGAS! The Show**, **Atomic Saloon Show**, **Mac King**
- Founded the site because he was **tired of being told what to recommend** — the
  concierge desk pays out on whoever pays the most, not on what the guest would enjoy

That last line is the origin story and the moral centre of the brand. When the writing
drifts into generic affiliate mush, it's because it forgot this.

---

## 4. Spike — the mascot

A friendly saguaro cactus. 3D-rendered, glossy deep green with soft vertical ribbing,
golden-yellow star-shaped spine clusters, **gold-framed aviator sunglasses** with dark
gradient lenses, and a warm closed-mouth smile. Two thick arm-branches. Assets live in
`/images/spike-*.png`.

**What Spike is for:** Spike is the *voice of the recommendation*. Where the page is
being factual — venue, running time, age limit — that's the site talking. Where the
page says "here's what I'd actually do," that's Spike, in a `Spike's Take` or
`Sidekick Note` block.

**Spike's register:** direct, warm, a little dry. He gives you the answer, not the
options. He is never zany, never puns for the sake of it, never talks in third person
about himself.

**Real examples from the site — this is the target:**

> Booking one show for a mixed-age crew? Blue Man Group, every time — nobody's too old
> or too young for it. Traveling with little ones? Make it a matinee.

> $32 for a ticket to the Laugh Factory. The regular price is $86. That's a 63%
> discount on a club with a 47-year track record. If you're choosing between comedy
> shows on the Strip, this is the one.

> Nobody makes you do anything here. Raising your hand to volunteer is completely your
> call — and staying in your seat is just as valid.

Note the shape: a question the reader is actually asking, then a decision, then the
one fact that justifies it. No throat-clearing.

---

## 5. Voice and tone

**Write like a knowledgeable friend texting you back, not like a brochure.**

| Do | Don't |
|---|---|
| "Dark Tuesday and Wednesday." | "Please note the show does not perform on select days." |
| "$56, and it's worth it." | "Tickets start at an affordable $56!" |
| "Skip the VIP upgrade here — the room is small enough that it doesn't buy you much." | "VIP packages are available for an enhanced experience." |
| "Absinthe will have you both crying laughing." | "Absinthe offers a unique and memorable evening." |
| "Nathan Burton at $32 is a steal." | "Nathan Burton offers exceptional value for money." |

**Rules that matter:**

1. **Give the answer.** A recommendation that lists five options and picks none is not
   a recommendation. Every guide's "Spike's take" ends with a name.
2. **Lead with the number.** Prices, run times and showtimes are the information people
   came for. Put them early and plainly.
3. **Earn superlatives.** "Best" needs a reason in the same sentence. If the reason is
   just "it's popular," cut the superlative.
4. **Say the downside.** Off-Strip, late start, no intermission, tight seats, 18+ —
   these get said out loud. It is the single cheapest way to be believed.
5. **No fake urgency.** "Selling fast" only if it is. "Prices may increase closer to
   show date" is true and is as far as we go.
6. **Second person, present tense.** "You're out by 9:15 with the whole night ahead."
7. **Contractions always.** "You'll," "it's," "don't."
8. **Em dashes are fine.** They're part of the rhythm. Don't overuse them in one graf.
9. **Never use exclamation marks in body copy.** They read as sales. Show names that
   contain one (RuPaul's Drag Race LIVE!) are the exception.

**Length discipline:** a paragraph is three to five sentences. If it's longer, it's
two paragraphs. Show pages are long *in total* but never long *in a block*.

---

## 6. Visual identity

Redesigned **August 2026** to the current neon system. Any page still showing navy +
orange + Bebas Neue is stale and should be migrated, not matched.

**Palette**

```
--ink     #171225   primary text
--bg      #ffffff   page background
--soft    #f5f4fb   soft section background
--blue    #3b82f6   PRIMARY — CTAs and price (locked in)
--pink    #ff2e7e   highlight accent, use sparingly
--lime    #c6f22e   lime accent
--purple  #7c3aed   eyebrows and secondary
--teal    #0fb5c9   tertiary accent
```

Hero gradient: `linear-gradient(#1c0a3a → #2b0f5c → #12061f)` — deep-purple neon, white
text, starburst speckles.

**Type**

- Display and headlines — **Plus Jakarta Sans** 700/800
- Body — **Inter** 400–700
- Editorial accent — **Cormorant Garamond italic**, used only for a show page's hero
  tagline and the opening `.lede` paragraph. It is a seasoning, not a font choice.

**Layout and motion**

Light page ground with deep-purple neon-gradient hero sections. Rounded cards
(`--radius: 18px`), soft shadows, glassy hero pills, purple uppercase `.eyebrow`
section labels. Scroll-reveal `fadeUp` via `IntersectionObserver`, Ken Burns hero
sliders, `pulseGlowCta` on primary buttons. Breakpoints: 900px tablet, 480px mobile.
Every page must honour `prefers-reduced-motion`.

**The CTA is blue.** Pink is a highlight, not a button.

---

## 7. Editorial rules that are non-negotiable

These exist because breaking them costs real money or real trust.

**Affiliate links — never guess the URL.** Spotlight's slugs do not follow a pattern
(`/show/` vs `/shows/`, odd sub-categories, reworded names). Kris supplies the real
listing URL; we append `/ref/vegassidekick`. A wrong link silently loses the
commission and nobody notices for weeks. If the URL isn't available yet, leave a
flagged placeholder — never invent one.

**Prices are denormalised across ~10 files.** A single show's price lives on its own
page, in `components/search-data.js` (twice — the field *and* the keyword blob), in
two listing arrays, on the homepage, on venue pages and inside guides — including
inside `FAQPage` JSON-LD prose. Changing one is never enough. And a price change can
break **claims**, not just digits: "cheapest," "under $30," "from $X" hero stats,
price-sorted rankings. Re-read the superlatives near anything you touch.

**`offers.price` must be a bare number string** — `"39"`, never `"$39"`. Google rejects
the dollar sign. This one gotcha caused nearly every Search Console error the site has
ever had.

**Photo policy — one wording, site-wide:** *"Still photos may be allowed as long as
they aren't distracting — please check with your usher on the way in. No flash
photography."* Use it even when the source listing says cameras are banned.

**"Sidekick Pick" ≠ "Sweet Spot."** A **Sidekick Pick** recommends the *whole show*
(`sp:true`). A **Sweet Spot** recommends a *seating section within a venue*. Never
write "Sidekick Pick — VIP"; that's a seating claim wearing the wrong badge. And
`sp:true` is never set by default — only when Kris names that specific show.

**Closed shows never get deleted.** Shows come back. The page stays, gets a banner,
and every buy CTA is neutralised. Current approved wording:

> **ENDED ITS RUN**
> *[Show] has ended its run at [venue].*
> Shows have a way of coming back — we'll update this page if it does.
> **No current Las Vegas dates.**

The softening lives in the headline. The last line stays blunt, because someone
arrived from a Google search wanting to buy tickets and must not be left guessing.

**Never rewrite `index.html` from scratch.** In August 2026 a routine article publish
rebuilt the homepage from a stale copy, reverting the redesign and dropping 74 URLs
from the sitemap. It was live for a week. Make targeted edits.

---

## 8. Catalogue snapshot — 2026-08-26

60 shows, **$27–$156**.

| Category | Shows |
|---|---|
| Music | 14 |
| Magic | 13 |
| Adult | 11 |
| Comedy | 10 |
| Cirque | 5 |
| Spectaculars | 4 |
| Family | 3 |

*(Category **pages** cross-list — the Family page shows 26 because Cirque and Magic
titles are surfaced there too. These counts are the primary category assignment.)*

**Site:** 132 pages · 122 sitemap URLs · 6 guides · 5 venue pages · 21 news articles.

**Recently closed** (pages live, catalogue entries removed): Marriage Can Be Murder,
Las Vegas LIVE Comedy Club, David Goldrake.

**Cheapest ticket:** Jimmy Kimmel's Comedy Club, $27. **Priciest:** "O", $156.

**Known gap:** ~29 ongoing Spotlight residencies we don't yet list, including entire
venues — Alexis Park Resort (6 shows), LaMarre Theater (4), Notoriety at Neonopolis
(3). Mostly the $17–$65 value bracket that suits our audience best.

---

## 9. Architecture, briefly

```
index.html            homepage — curated, not comprehensive
shows/                60 show pages + 7 category listings + All Shows master
guides/               6 editorial roundups (the ranking pages)
venues/               5 hotel-cluster pages
news/                 21 dated articles ("Vegas Dispatch")
about/kris-kidd/      the Person entity
components/           header.js, footer.js, search-data.js, search.js
hq/                   private, encrypted internal hub
play/                 WebGL experiments (Vegas sign, Sphere, Mandalay Bay)
```

Search is a dependency-free client-side match over a local JS array. **Adding a show
page does not add it to search** — you must append to `search-data.js`.

The model show page is `shows/music/vegas-the-show/index.html`; the design and feature
benchmark is `shows/adult/absinthe/index.html`. Copy those, not older pages.

---

## 10. Standing operating procedures

Detailed steps live in `CLAUDE.md`. Invoke them by name and they fire:

- **Price Change Checklist** — updating any show's price
- **Show Closing Checklist** — a show ends its run (three parts: pull from catalogue,
  banner the page, never delete)
- **Adding a New Show Page** — includes registering it in search and the sitemap
- **"Make live"** — commit, fast-forward `main`, push, return the URL

Naming the checklist in the request measurably improves the result. "Mad Apple went
$56 → $59, run the Price Change Checklist" beats "update Mad Apple's price."

---

## 11. The one-line test

Before anything ships, read it and ask: **would a Vegas local who works in tickets
actually say this to a friend?**

If it sounds like a brochure, a press release, or an affiliate blog, it isn't ready.
