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
- Table and Reading are strictly read-only. They never edit the Outline, the
  Page, or a Result, and they show no Draft editor or comment composer.
- Scratch is the one explicit human-writing lane. In Scratch view, a small `+`
  is available at Section (`C1`) and whole paragraph group (`C1.P1`) scope.
  The current Outline grammar has no separate subsection node, so it does not
  render a duplicate Subsection plus. Explicit subsection-scope records remain
  accepted for future Page schemas. B/symbol rows have no Scratch control. `Save` creates or updates an open
  `rp-scratch-NN_<target>` Run; the person manually clicks `Finish Scratch` to
  ask the AI for a concise Summary from the notes and close it. The browser
  writes the registry under `## Scratch` in this same
  selected Outline and the paired ticket/result under `runs/` and `results/`.
  It does not edit `Draft:` prose. A closed Scratch Run is immutable.
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

## Scratch record

The registry is intentionally close to the plan rather than in a second Draft
file:

```markdown
## Scratch

### rp-scratch-01_C1.P1 · paragraph · C1.P1
- Scope: paragraph
- Target: C1.P1
- Status: closed
- Run: rp-scratch-01_C1.P1
- Notes: |
  Start with the visit, then explain the mechanism.
- Summary: |
  The paragraph should make the visit the causal hinge.
```

The registry is a live index; the paired Run Result is the durable receipt of
the interaction: `runs/<run>.md`, `results/<run>/runtime.yaml`,
`results/<run>/v001.md`, and `results/<run>/working.md`. Scratch is not a
substitute for later Section/Paragraph prose writing and does not silently
promote rough notes into `Draft:` text.
