## 0.2.1 · 2026-08-31

Category-folder sweep: lane paths read `<page>/evidence/<lane>` or
`<page>/delivery/<lane>` (haipipe-page 0.47.0 §📁); flat names are the same
lane during migration (stubs).

## 0.2.0 · 2026-08-16

- **The docx opens with the Page's complete H1 title** via `--document-title`,
  emitted once in Word's editable Title style, independent of paper-section H1
  inference.
- **Display evidence embeds through the temp ref bridge (JL 260816)**:
  `export.py` hands md2docx a TEMP copy with `(\ref{<label>})` appended to each
  unit's first prose mention, plus `--display-root` and `--lanes`; aliases
  identify one unit and embed it once. Booktabs tables stay native and editable.
- *(Entry reconstructed 260819 from the 0.2.0 frontmatter summary and commit
  ca6b48ea — the bump shipped without its CHANGELOG entry; agree.py caught the
  disagreement.)*


## 0.1.1 · 2026-08-16
- The page's display evidence now reaches this projection (JL 260816: "both word and latex didn't include the display?"): a unit under <page>/display/ cited by short id in prose is embedded after the citing paragraph, per the rule added to SKILL.md.
