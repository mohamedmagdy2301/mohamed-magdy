# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A personal CV / portfolio asset folder for Mohamed Magdy Ibrahim (Flutter developer) — **not** a software project. There is no package manager, build step, or test suite here. It holds:

- `index.html` — the portfolio site: one self-contained page (HTML + CSS + JS, ~1070 lines, ~530 KB)
- `v2/index.html` — a second, separate portfolio page served at `/v2`
- `Mohamed_Magdy.pdf` — the résumé the pages link to. Both pages link it by relative path
  (`Mohamed_Magdy.pdf` from the root, `../Mohamed_Magdy.pdf` from `v2/`), so it must keep this exact
  name at the repo root or every résumé button 404s.
- `assets/` — source material, referenced by nothing at runtime (see below):
  - `cv-plaintext.txt` — the canonical CV content; source of truth for dates, metrics and wording
  - `cv-ats.docx` — the ATS résumé document
  - `portrait-suit.jpeg`, `portrait-closeup.jpeg` — portrait originals
  - `escore-store-poster.webp`, `escore-splash.webp`, `sound-to-read-screenshot.webp`,
    `tarkibat-hand-mockup.webp`, `tarkibat-icon.webp` — app artwork originals

Nothing in `assets/` is loaded by either page — both are fully self-contained, with every image
inlined as base64. The folder is the archive of originals the embedded copies were cropped from, so
edit an image there and it changes nothing until you re-embed it. A portrait used on the page (the
graduation photo) has no original in `assets/`; it exists only as embedded base64.

To view the page: open `index.html` directly in a browser. No server, no build, no dependencies to install.

Filenames are kebab-case with no spaces, and describe the content rather than its origin — the
originals arrived as `WhatsApp Image 2026-08-25 at 3.19.50 PM.jpeg` and `Tarkibat-wide.webp` (which
was in fact a 240×240 square icon, not a wide image). Keep new files to that convention.

## index.html architecture

Everything lives in one file: a single `<style>` block in `<head>`, markup in `<body>`, a single `<script>` at the end. Keep it that way — the page is meant to be openable from disk and mailed as one file. The only external requests are the Google Fonts link (Sora / Plus Jakarta Sans / JetBrains Mono / Tajawal); all images are inlined as `data:image/…;base64` (20 of them), which is why the file is large.

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

Content changes usually touch three places at once: the markup, `T.en`, and `T.ar`. Facts (job dates, the 65%/54%/5,000+/74% figures, store URLs, education) should stay consistent with `assets/cv-plaintext.txt`. To swap an image, base64-encode it and replace the `src` inline — do not introduce an external image path.

## Deployment

The folder is a git repo pushed to `https://github.com/mohamedmagdy2301/mohamed-magdy.git` and served
by GitHub Pages from the `main` branch, root directory — which is why the page is named `index.html`.
Everything committed here is public — including `assets/`, so treat anything placed there as
published. `v2/index.html` is served at `/v2`; keep both pages' résumé links pointing at
`Mohamed_Magdy.pdf` at the repo root (see the file inventory above).
