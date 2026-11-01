# s51 · Server runtime: ideas

The open ideas of this topic, one per slide: written from its face as a quick scratch (261031); a person edits them here, and its pictures come when asked.

## Server runtime
- how the workbench server runs today: how it starts, which folders make it up, how one request…
- It is the first server topic: s01-s13 design the ladder and the screens
- s51 on are the served side of that design

## What it hands over
- a deck, and how the workbench server starts, finds a page and answers its routes, for the people who build the workbench
- a code

## Still open
- Every theme is on the frame (261007)
- A theme that fails to import falls back to vanilla without a word: say so on the page?
- No reload on a code change, and old processes keep serving old code: a restart command, or a
ask: Decided: /w/<block> opens the frame now, before the theme files
