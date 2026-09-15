# Draft inside the Outline Markdown

Draft Space is a read-only projection of the selected Outline Markdown. The
Outline is the only authoring source for the Shape, Bullet, tag, Draft prose,
and Evidence decision shown in the space.

## Single-file contract

One Page has one selected Outline file:

```text
outline/<stem>-outline-v<version>.md
```

Each Bullet keeps its planning metadata and its candidate prose together:

```markdown
### C1.P1 · Measurement

- B1 · [Evidence] Report the validated measure
  Note: Keep the reported range and denominator explicit.
  Evidence: E11 · validation result
  Draft: Across six language models, mean absolute error ranges from ... .
```

`Draft:` may wrap across indented lines. It is part of the same Bullet record;
it is not a second Markdown file. An optional page-level Opening candidate is
stored under `## Opening Draft` in that same Outline.

## Space behavior

- The browser reads the selected Outline on every request.
- Draft Space never edits a file and never shows an editor or comment form.
- The owning Structure/Content Run writes the next Markdown revision.
- A promoted Page Content Markdown is a later output; it is not a second Draft
  source.
- There is no `*-preview.md`, no Draft hash comparison, and no `Draft changed`
  warning.

Evidence results remain in `results/` and are linked by the Bullet's Evidence
decision. Their status is independent from the Draft text.

## Versioning

Older Outline versions remain historical records. The active version is the
only one rendered by Draft Space. A structural or substantive revision should
create the next Outline version and carry its Draft fields forward explicitly.

The old standalone `*-preview.md` format is migration input only. It must be
embedded into the selected Outline and then moved to the Outline's recoverable
`outline/_archive/legacy-outline-preview/` lane.
