# Projection manifest v1

`2-src/projection.yaml` is declarative wiring. It may say where a source lives
and where its candidate lands; it must not contain manuscript prose.

```yaml
schema: haipipe.paper.projection/v1
master: Paper-Venue2026.tex
target_roots: [sections, appendices]
dependency_roots: [displays]
candidate_root: 3-dist/tex

units:
  main-1:
    source:
      page: 0-lifecycle/4-main/S-Main-1-introduction.md
      select: content
    gate: S-Main-1
    entry: sections/01_introduction.tex
    outputs:
      - path: sections/01_introduction.tex
        role: prose

unreachable:
  - path: sections/legacy.tex
    disposition: retain
    reason: legacy leaf awaiting a separate backport decision
```

## Fields

- `schema`: exactly `haipipe.paper.projection/v1`.
- `master`: unnumbered LaTeX master relative to the paper root.
- `target_roots`: unnumbered directories whose `.tex` files G0 inventories.
- `dependency_roots`: unnumbered build dependencies copied for isolated G4.
- `candidate_root`: must resolve below `3-dist/`.
- `units`: stable ids. Each unit declares one source S page, one gate S-page
  id, its entry output, and one or more outputs.
- `source.select`:
  - `content`: the body beneath `## Content`, stopping at the next `##`.
  - `heading:<text>`: the body beneath the exact Markdown heading whose visible
    text is `<text>`, stopping at a heading of equal or higher depth.
- output `role`:
  - `prose`: render selected Markdown manuscript prose to LaTeX.
  - `wrapper`: emit only declared `inputs` as `\input{…}` lines.
- `unreachable`: an existing target-root `.tex` intentionally outside the
  projection. Both `disposition` and `reason` are required.

An output-level `select` overrides `source.select`, allowing one S page to feed
several appendix leaves. All paths are POSIX-style, paper-relative paths.

## G0 exactness

Let:

```text
inventory = every existing *.tex beneath target_roots
declared  = every units.*.outputs[].path
excluded  = every unreachable[].path
```

The manifest is valid only when `inventory == declared ∪ excluded`, declared
and excluded do not overlap, and every output/entry sits beneath a declared
target root. New or renamed submission files therefore force an explicit
manifest decision.

## G1 gate convention

`gate` must match exactly one S-page filename: either the whole stem or the
stem prefix before its descriptive suffix. That gate page's first `state:`
line must begin:

```text
state: ✅ GATED
```

The gate page may also be the source page. A rollup source may supply several
units, each controlled by its own gate page. A rendered/open/revise-blocked
gate page is not projectable.
