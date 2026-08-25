# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A personal CV / portfolio asset folder for Mohamed Magdy Ibrahim (Flutter developer) — **not** a software project. There is no package manager, build step, test suite, or version control here. It holds:

- `index.html` — the portfolio site: one self-contained page (HTML + CSS + JS, ~1070 lines, ~550 KB)
- `Mohamed_Magdy_Ibrahim_CV_PlainText.txt` — the canonical CV content; the source of truth for dates, metrics and wording
- `Mohamed_Magdy_Ibrahim_Flutter_Developer_ATS.{pdf,docx}`, `Mohamed_Magdy_Ibrahim.pdf` — résumé exports
- `*.webp`, `*.jpeg`, `*.png` — source artwork (app icons, screenshots, portrait) that is embedded into the HTML as base64

To view the page: open `index.html` directly in a browser. No server, no build, no dependencies to install.

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

### Editing content

Content changes usually touch three places at once: the markup, `T.en`, and `T.ar`. Facts (job dates, the 65%/54%/5,000+/74% figures, store URLs, education) should stay consistent with `Mohamed_Magdy_Ibrahim_CV_PlainText.txt`. To swap an image, base64-encode it and replace the `src` inline — do not introduce an external image path.

## Deployment

The folder is a git repo pushed to `https://github.com/mohamedmagdy2301/mohamed-magdy.git` and served
by GitHub Pages from the `main` branch, root directory — which is why the page is named `index.html`.
Everything committed here is public. The résumé links (`nav`, hero CTA, contact dial) point at the
relative path `Mohamed_Magdy_Ibrahim_Flutter_Developer_ATS.pdf`, so that file must stay in the repo
root under that exact name.
