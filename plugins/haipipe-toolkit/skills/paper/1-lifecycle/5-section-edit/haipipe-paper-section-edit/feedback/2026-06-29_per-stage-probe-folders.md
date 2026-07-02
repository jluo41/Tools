---
status: fixed
created: 2026-06-29
updated: 2026-06-29
occurrences: 1
context: §3 theory session, skill architecture redesign
fixed_in: "v2.1.0 (per-stage _PROBE/ folders, 1-probe-plans/ as index)"
regressed: ""
---

Probe plans should live in per-stage _PROBE/ folders, not flat in 1-probe-plans/. 1-probe-plans/README.md becomes a cross-paper index only.

Each stage (paper-level or section-level) is self-contained: claims has _EVIDENCE_ + _PROBE/, narrative has _DISPLAY_ + _PROBE/, display has _PROBE/, each editing section has _CITATION_ + _VALUES_ + _PROBE/.

Fix: implemented in v2.1.0. Moved all PP files to per-stage _PROBE/ folders. Index links to them.
