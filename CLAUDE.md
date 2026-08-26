# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A personal CV / portfolio asset folder for Mohamed Magdy Ibrahim (Flutter developer) — **not** a software project. There is no package manager, build step, or test suite here. It holds:

- `index.html` — the portfolio site: one self-contained page (HTML + CSS + JS, ~1070 lines, ~530 KB)
- `v2/index.html` — a second, separate portfolio page served at `/v2`, with the project case-study
  view (see below)
- `Mohamed_Magdy.pdf` — the résumé the pages link to. Both pages link it by relative path
  (`Mohamed_Magdy.pdf` from the root, `../Mohamed_Magdy.pdf` from `v2/`), so it must keep this exact
  name at the repo root or every résumé button 404s.
- `assets/` — source material, referenced by nothing at runtime (see below), one folder per kind:
  - `cv/` — `cv-plaintext.txt` (the canonical CV content; source of truth for dates, metrics and
    wording), `cv.docx` (the document `Mohamed_Magdy.pdf` is exported from), `cv-previous.pdf`
    (the résumé it replaced) and `linkedin-profile.md`
  - `art/` — app artwork originals: `escore-store-poster.webp`, `escore-splash.webp`,
    `sound-to-read-screenshot.webp`, `tarkibat-hand-mockup.webp`, `tarkibat-icon.webp`,
    `curai-logo.png`
  - `portraits/` — `portrait-suit.jpeg`, `portrait-closeup.jpeg`
  - `certificates/` — `eelu-bsc-certificate.webp`
  - `shots/` — app screenshots, one folder per project, embedded into the `v2` case studies by
    `tools/embed-shots.py`; see `assets/shots/README.md`
- `tools/embed-shots.py` — the only script in the repo; it rewrites the `SHOTS` registry in
  `v2/index.html`

Nothing in `assets/` is loaded by either page — both are fully self-contained, with every image
inlined as base64. The folder is the archive of originals the embedded copies were cropped from, so
edit an image there and it changes nothing until you re-embed it (`assets/shots/` is the exception
only in that a script does the re-embedding for you). A portrait used on the page (the graduation
photo) has no original in `assets/`; it exists only as embedded base64.

To view the page: open `index.html` directly in a browser. No server, no build, no dependencies to install.

Filenames are kebab-case with no spaces, and describe the content rather than its origin — the
originals arrived as `WhatsApp Image 2026-08-25 at 3.19.50 PM.jpeg` and `Tarkibat-wide.webp` (which
was in fact a 240×240 square icon, not a wide image). Keep new files to that convention.

## index.html architecture

Everything lives in one file: a single `<style>` block in `<head>`, markup in `<body>`, a single `<script>` at the end. Keep it that way — the page is meant to be openable from disk and mailed as one file. The only external requests are the Google Fonts link (Sora / Plus Jakarta Sans / JetBrains Mono / Tajawal) and, on the published site only, the GoatCounter loader (see *Analytics* below); all images are inlined as `data:image/…;base64` (20 of them), which is why the file is large.

### Bilingual EN/AR with runtime switching

The `T` object at the top of the script holds two flat dictionaries, `T.en` and `T.ar`, keyed by short strings (`"j1.b4"`, `"p.escore"`, `"cta.wa"`). `apply(lang)` sets `documentElement.lang` / `dir`, then rewrites every `[data-i18n]` element's `innerHTML` from the dictionary. **Any new user-visible string needs a `data-i18n` key present in both dictionaries**, or it will silently freeze in English on switch. Values may contain inline HTML (`<b>`) — they are assigned via `innerHTML`, not `textContent`.

The `h1` key is the exception: an array of lines, rendered by `paintH1()` into per-character `<span class="ch">` elements with staggered animation delays; the last line gets `.grad`. It must be re-run after every language change.

Arabic is handled by CSS, not a second stylesheet: `html[lang="ar"]` selectors override font family, weight, letter-spacing and `text-transform` (the mono/uppercase treatment is dropped for Arabic and Tajawal substituted). Direction is handled by writing **logical properties throughout** — `inset-inline-start/end`, `margin-inline-end`, `padding-inline-start` — so RTL works from the `dir` attribute alone. New CSS must follow this; a physical `left`/`right` will break the Arabic layout.

### Motion and interaction layers

- `.rv` (reveal) elements start hidden and get `.in` from an `IntersectionObserver`; `.d1`/`.d2`/`.d3` add stagger delays.
- `.cnt` stat numbers animate via a second observer with an ease-out cubic over 1400 ms.
- Desktop-only pointer effects are gated behind `matchMedia('(pointer:fine)')` **and** not-reduced-motion: the cursor spotlight, card glow (`--mx`/`--my` CSS vars), 3D tilt on `.tilt` / `.card.glow`, magnetic `.mag` buttons.
- The "Hot reload" FAB (and the `R` key) replays the entrance: repaints the headline, resets and reruns the counters, and re-adds `.in` to every revealed element on a 22 ms stagger. `L` toggles language.
- Phone mockups parallax on scroll by writing a `--drift` var into `style.translate` — deliberately `translate`, not `transform`, so it does not fight the tilt handler writing `transform`.

Every animated feature has a `@media (prefers-reduced-motion:reduce)` escape, and a global rule at the end of the stylesheet kills all animation and transition. Keep new motion inside that contract, and keep hover-dependent affordances behind `@media(hover:none)` fallbacks.

### The hero portrait / orbit, and two traps it sets

`.port` is a self-contained radial system: a portrait in the middle (`.face`), four app icons
orbiting on a ring (`.orbit` > `.sat` > `.fix` > `.cw` > `img`), plus a dashed `.path` and a
rotating `.sweep` arc. Geometry is driven by two custom properties — `--tile` (icon size) and
`--r`, derived as `(--pw - --tile)/2` so the tiles are always tangent to the column edge rather
than spilling out of it. Change the icon size via `--tile` (including in the mobile media query),
never by setting `width`/`height` on `.sat img`, or the ring stops matching the tiles.

Two CSS traps live here, both already fixed — do not reintroduce them:

- **`@keyframes spin` sets `transform`,** so it wipes out any `transform` declared on the same
  element. Any rotating element that also needs `translate(-50%,-50%)` to centre itself must carry
  that translate through its own keyframes — that is what `cspin` / `cspinr` exist for. Using plain
  `spin` on such an element makes the browser matrix-interpolate `translate` → `rotate`, and the
  element visibly drifts and skews around its orbit.
- **`.fix` and `.cw` are absolutely positioned and must keep `left:0;top:0`.** With `auto` offsets
  they fall back to the static position, which is right-aligned under `dir="rtl"` — that shifted
  every satellite a full tile off the ring in the Arabic view while looking perfect in English.
  Verify any change to this section in *both* directions.

The three `.face .pf` portraits are stacked and crossfaded by a `setInterval` that toggles `.on`;
they are square source images sized with `object-fit:cover`, so the CSS must stay for the photo to
fill the circle at all.

### The phone showcase (`.stage`)

The three `.dev` frames are a bezel only — there is deliberately **no fake notch element**. Every
embedded screenshot already carries its own status bar (Escore an iOS notch, Sound To Read an
Android status bar, Tarkibat a punch-hole camera), so drawing one over the top produced a black
blob on the light screenshots.

`.dev` has no `aspect-ratio`; its height comes from `.dev .scr{aspect-ratio:468/988}`, which
matches the embedded screenshots so `object-fit:cover` crops nothing. If you swap in a screenshot
with a different aspect, update that ratio and re-normalise the other two — otherwise `cover`
silently eats the edges of the UI.

Screenshots must be **bare app UI**, not store posters. The original Escore asset was a marketing
poster containing a phone mockup on a green background, which rendered as a phone inside a poster
inside a frame; it was replaced by the screen cropped out of that poster, its own background
extended downward to reach the shared aspect ratio. If a full-length Escore screenshot ever turns
up, prefer it — the current one is a recovered crop, so it is shorter than the source UI.

### Editing content

Content changes usually touch three places at once: the markup, `T.en`, and `T.ar`. Facts (job dates, the 65%/54%/5,000+/74% figures, store URLs, education) should stay consistent with `assets/cv/cv-plaintext.txt`. To swap an image, base64-encode it and replace the `src` inline — do not introduce an external image path.

## v2/index.html — the case-study view

`v2` is its own page with its own dictionary and its own CSS; it shares no code with `index.html`.
It follows the same contracts (one file, `T.en`/`T.ar` for every user-visible string, logical
properties for RTL, a reduced-motion escape) and adds a project case study on top.

Clicking a card's `.open` button opens `#pv`, a full-sheet dialog rendered from JS. Three pieces
drive it, all near the end of the script:

- `SHOTS` — screenshots per project. An entry is either a `data:` URI or `'#some-id'`, which reuses
  an `<img>` already on the page instead of embedding the bytes twice. **Generated —
  `tools/embed-shots.py` rewrites this whole object from `assets/shots/<key>/`, so hand edits are
  lost on the next run.** Numbered files set the gallery order; an `extra/` subfolder is ignored.
- `PROJ` — the case-study copy, keyed the same way, with `en` and `ar` objects per project holding
  `eyebrow`, `lede`, `role`, `org`, `when`, `plat`, `ov[]`, `feats[]` and `metrics[][]`. Chrome
  labels ("Overview", "The facts", …) live in `T` under `pv.*` keys instead.
- `pvRender()` — builds the sheet's HTML. The status tag, the icon (read off the card's `--art`)
  and the "next project" link are all derived, not stored.

The sheet is deep-linked as `#p/<key>` through `pushState`, so Escape and the browser back button
both close it; `pvDepth` counts how many projects deep the visit went so one Escape leaves
altogether. A gallery image whose aspect ratio is not within 0.06 of the phone frame's (468/988)
loses the bezel and renders as a plain card — that is what keeps store thumbnails from being
cropped into a fake phone.

## Analytics

Both pages carry an identical GoatCounter snippet just before `</head>` — a privacy-friendly,
cookieless hit counter reporting to https://mohamedmagdy.goatcounter.com. The account name lives in
one `CODE` constant per page; blank it to switch counting off everywhere. When the page is opened
over `file:` or from localhost the loader returns before creating any script tag, which is what
keeps a mailed or offline copy free of requests beyond the fonts. Match that host check exactly if
you touch it — an earlier anchored regex (`/^(localhost|127\.|…)$/`) silently failed to exclude
`127.0.0.1`, so local previews were counted.

Nothing was ever collected before this was added, and it cannot backfill: the counts start from the
moment the code is filled in and deployed. It reports aggregates only — visits, country, browser,
device, referrer, page — never visitor identity.

`v2` additionally defines `window.gcCount(path, title)` and calls it from `pvOpen()`, so opening a
case study is counted as `/v2/p/<key>` instead of vanishing into the `#p/<key>` hash. Calls made
before the loader arrives are queued and flushed on its `onload`, which is the deep-link-on-load
case (`/v2/#p/escore`). Keep `gcCount` defined **before** the body script — `pvFromHash()` runs at
the end of it and can reach `pvOpen()` immediately. In `index.html` there is no `gcCount`; the
plain pageview is all that page needs.

## Deployment

The folder is a git repo pushed to `https://github.com/mohamedmagdy2301/mohamed-magdy.git` and served
by GitHub Pages from the `main` branch, root directory — which is why the page is named `index.html`.
Everything committed here is public — including `assets/`, so treat anything placed there as
published. `v2/index.html` is served at `/v2`; keep both pages' résumé links pointing at
`Mohamed_Magdy.pdf` at the repo root (see the file inventory above).
