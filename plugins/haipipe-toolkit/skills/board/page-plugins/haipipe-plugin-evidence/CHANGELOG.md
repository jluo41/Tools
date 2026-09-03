# CHANGELOG · haipipe-plugin-evidence

## 0.6.0 — 2026-09-03

- Retire the standalone Evidence plugin and preserve this skill only as a
  compatibility redirect to `haipipe-plugin-outline`.
- Move the four active lane references under
  `haipipe-plugin-outline/ref/evidence/` and forbid a root `<page>/evidence/`.

## 0.5.5 — 2026-09-03

- Merge `By bullet` and `Run links` into one default `Evidence Items` panel.
- Use the Outline Table's canonical `E<n><kind>.<Label>` identity on every
  Evidence card and group each Supporting/Local Run item beneath it.
- Present only Run/Result vocabulary and reveal exact repository-relative
  paths in one compact, wrapping `Run & Result paths` disclosure.
- Preserve old `seg=bybullet` and `seg=runlinks` deep links as aliases.

## 0.5.4 — 2026-09-03

- Make `Run links` a compact Evidence Item index: short item names, clickable
  dotted Run chips, one Local state, and collapsed Ticket/receipt details.
- Preserve the global dotted identity and Ticket link for an allocated local
  Run while its Result receipt is still absent.

## 0.5.3 — 2026-09-02

- Accept Outline deep links that select `Run links` and focus the owning
  Evidence Item, while preserving parent-only routes as plans rather than Runs.

## 0.5.0 — 2026-09-02

- Absorb the former Value, Display, and PageX plugin contracts into the one
  Evidence plugin, alongside Citation/Bib. Their detailed lane laws now live
  under `ref/`; no standalone plugin skill remains.
- Define PageX as the optional exact source binding chosen in SURVEY and
  validated/frozen in LAND. It can feed VALUE, CITE, or DISPLAY local Results
  but is never itself a Result type. Probe remains separately governed.

## 0.4.0 — 2026-09-02

- Absorb the former Bibex plugin contract into the one Evidence plugin.
- Own ordinary Page Bibs, Discovery Result-Bib aggregation, citation
  verification, and the no-composition law in `ref/citations.md`.
- Keep `evidence/bibex/` as the compatible internal storage address without
  exposing a second plugin or skill.

## 0.3.2 — 2026-08-31
- Route `evidence/pagex/` to `haipipe-plugin-pagex`; Probe owns only its own
  `evidence/probe/` evidence-acquisition lane.

## 0.3.1 — 2026-08-31
- Name all presented lanes by their canonical `evidence/<lane>/` address.

## 0.3.0 — 2026-08-31
- PageX's whole-Folder cards now present Page Face plus Task plan/report/QA
  directly. The retired Task plugin contributes no lane or route.

## 0.2.0 — 2026-08-31
- Sixth segment 🔗 Pagex (the borrow view, pens inline); the standalone 🔗
  strip row folded in (85-plugin-pagex.js removed); five-lane wording
  throughout; the task lane's read lands here when a pagex card learns a
  task unit's status.

## 0.1.1 · 2026-08-31

The v3 category folder <page>/evidence/ is this tab's disk twin; lanes
live inside it, flat names are migration stubs.


## 0.1.0 · 2026-08-31

Born from JL's ruling ("not the evidence folder, the evidence PLUGIN — we
still have the subfolder for bibex etc, but one evidence plugin to present
bibex, display, etc"). One 🧾 Evidence tab with five segments (⧉ By bullet
default · 📚 Citations · 🚪 Cards · 🧮 Values · 🖼 Displays); presentation
only — the four lanes keep storage, writers, walls and their three distinct
human gates (verified: / read: / accepted:). Engine tab merge BUILT the same day
(live/evidence.py + serve.py routes + the JS fold: 84 one row, 82 minus
bibex, 08-plugin-value.js removed) and verified by driving real Chrome on
SM05-results: menu → tab → segments → live Values view.
