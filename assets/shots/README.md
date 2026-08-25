# App screenshots

Raw screenshots live here, one folder per project. They are **source files** —
the page never loads them from disk. `python tools/embed-shots.py` resizes each
one, converts it to WebP and writes it into the `SHOTS` registry in
`v2/index.html` as a `data:` URI.

## How to add screens

1. Drop the phone screenshots into the folder for the project.
2. Name them `NN-what-it-is.png` — **the number sets the order in the gallery.**
3. Run:

   ```
   python tools/embed-shots.py
   ```

   Options: `--width 460` (default), `--quality 72`, `--dry` (report only).

Keep 5–8 per project. Every screenshot adds ~25–45 KB to the page, and the
gallery scrolls horizontally, so a tight selection reads better than everything.

Use bare app UI — no store posters, no device frames: the page draws its own
phone bezel around the image.

An `extra/` subfolder holds screens that are kept but not shown — the script
only reads the top level of each project folder, never subfolders. To promote
one, move it up and give it a number; to retire one, move it into `extra/`.

## What is in here now

### escore/ — 8 in the gallery
```
01-matches-live          matches tab: the day strip and live scores
02-tournaments           tournaments tab with the game filter
03-tournament-overview   stream, prize pool, organiser, venue
04-tournament-bracket    playoff bracket with the champion card
05-tournament-standings  standings: prize money and club points
06-match-preview         match page with the live stream
07-news                  news feed
08-player-profile        player page: earnings, team, nationality
extra/  splash · news-trending · transfers · tournament-participants
        game-profile · following-clubs · player-trophies · news-detail
        match-lineup
```

`01-matches-live` is also the Escore screen in the showcase strip at the top of
the page, which used to be a crop out of a store poster.

### str/ — 5 in the gallery
```
01-home · 02-consonants-vowels · 03-learn-letters
04-pronunciation-test · 05-parent-report
extra/  login-google · home-student · progress-student · level-details
        lesson-video · speech-test · more-settings · privacy-policy
        logout-dialog
```

These came from the Google Play listing, so they are only ~184x296 and are not
phone-shaped — the gallery drops the phone bezel for them and shows them at
their own ratio. Replacing them with real device screenshots (1080x2400) and
re-running the script is the one thing that would improve this page most.

`tark/`, `host/`, `curai/` and `azk/` are empty — a project with no folder falls
back to the screenshot already on the page, or shows a "screens coming soon"
note.
