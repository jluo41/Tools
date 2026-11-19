# Three views

How a paper Board is seen three ways: where things are stored, where the page shows them, and which sessions
worked on them. Each topic below is one rule or view, with its requests.

## 🧭 Topic: Three views ▸ Folder, Element, Session

Every theme gets three linked views: Folder (how things are stored), Element (where the page shows each folder),
Session (the important session history, each episode beside the folders and elements it touched). The shared
Session view is built once in `servers/workbench/page`; each theme fills a hook. Join key: the folder path,
relative to the Block.

For the paper theme, two things need more than the folder path:

1. A Section session lives long (one per Section, many rounds), so an episode is better keyed by the Draft
   version it made (v0.3 to v0.4) or the revise Pass, not by one Run.
2. Inside a Section, the page's elements are sentences (C3.P5.S14), so an episode should also name the sentence
   addresses it changed.

| When | Asked | Through | What changed |
| --- | --- | --- | --- |
| 11-17 | "For the theme design, we should have three views. Folder Structure ... Element Structure ... Session Structure" | tools-space-bc, relaying JL | the paper theme's map sent back; no code change yet |
