## 0.2.1 · 2026-08-21

## 0.2.2 · 2026-08-31

Category-folder sweep: lane paths read `<page>/evidence/<lane>` or
`<page>/delivery/<lane>` (haipipe-page 0.47.0 §📁); flat names are the same
lane during migration (stubs).


- **A PNG/JPG-rendered figure unit now embeds too.** `live/export.py`'s
  figure branch checked only for `assets/figure.pdf`; a `figure`-kind
  display unit whose winning render is `assets/figure.png` (the common
  case for `haipipe-display-figure` output) fell through to "no winning
  render yet" and was never printed, with no error anywhere. Found on
  `QAb11-npi2photo` (Display2): `check.py`'s `display-cited-not-embedded`
  only fires once a `latex/` projection exists to be checked against, so
  the gap was silent until the projection was built for the first time.
  lualatex reads the raster directly; the fix widens the check to
  `figure.pdf` / `figure.png` / `figure.jpg`, preferring `.pdf`.

## 0.2.0 · 2026-08-16

- **The Page title prints**: the standalone master opens with the complete
  canonical H1, TeX-escaped as plain text — document identity, not a Content
  division, so it is emitted independently of numbered `###` headings.
- **The page's display evidence prints (JL 260816)**: a unit under
  `<page>/display/` cited by `DisplayN` or `<stem>-DisplayN` embeds once as a
  real float after the citing paragraph, in citation order.
- *(Entry reconstructed 260819 from the 0.2.0 frontmatter summary and commit
  ca6b48ea — the bump shipped without its CHANGELOG entry; agree.py caught the
  disagreement.)*

# haipipe-plugin-latex · Changelog

## 0.1.0 · 2026-08-15
- Born in the thin-door round (JL 260815): the plugin's contract moves out of haipipe-board SKILL.md; engines stay with the engine.

## 0.1.1 · 2026-08-16
- The page's display evidence now reaches this projection (JL 260816: "both word and latex didn't include the display?"): a unit under <page>/display/ cited by short id in prose is embedded after the citing paragraph, per the rule added to SKILL.md.
