# Consumer-safe distribution from a View
state: ✅ SETTLED · authored resources stay private; consumers read generated fixtures
owner: JL
method: separate authorship, inspection, and downstream placement

## Opening
What may leave a View for Paper or another consumer, and what must remain inside the authored resource folder?
The canonical Page and `views/<stem>/` are working sources that include Probes, notes, recipes, and acceptance state.
Consumers need selected review formats, Displays, references, and safe metadata rather than those internals.
The generated `_fixture` boundary performs that handoff without becoming another semantic source.
This Page decides the distribution surface and the consumer's responsibilities.

**Human-readable handoff**: a consumer may select the whole View or named Displays, but it must preserve placement and gate state.

**No direct reach-through**: Paper does not treat QA Probes, source notes, `output.md`, recipes, or candidates as Paper-ready artifacts.

## Diagram

**Authored to distributed**: build publishes a narrow surface and leaves private provenance behind.

```text
canonical Page + views/<stem>/
        │ build
        ▼
_fixture/
├── views/<stem>/{tex,pdf,docx,manifest}
├── displays/<Display>/{float,assets,previews,manifest}
└── references.bib
        │ accepted handoff
        ▼
Paper · Appendix · Application
```

## Content

### 1 · Authored boundary

**The private side**: full evidence and renderer working files remain authored resources.

```text
Page + Probes + sources + intake + recipes + candidates ──▶ authored only
```

The canonical View Page is the only semantic source.
Its resource folder keeps full QA Probes, source notes, editable BibTeX, optional code, Display intake, recipes, candidates, versions, and semantic `output.md` files.
Cards bind these authored sources, never generated fixture files.

### 2 · Distribution boundary

**The public side**: build selects only reproducible consumer artifacts.

```text
authored resources ── build ──▶ review formats + floats + manifests + bibliography
```

`build` generates View review formats, safe View and Display manifests, selected floats and assets, previews, and one merged bibliography.
It excludes private inputs and renderer internals.
The generated fixture can always be replaced from authored sources and is never edited by hand.

### 3 · Consumer boundary

**The handoff record**: use, placement, and gate travel together.

```text
accepted View or Display ──▶ target + uses + placement + handoff state
```

A consumer names a real target, what it uses, placement, and handoff state.
The consumer owns downstream prose and placement acceptance.
The View owns the evidence organization; each Display owns its artifact acceptance.
A current fixture does not authorize use while any required human gate remains waiting.

## Aims

### A1 · Authored boundary
- A1.1 · Keep the complete evidence trail editable and inspectable without publishing it as consumer output.
  **Done when:** Cards resolve to authored files and private inputs remain outside `_fixture`.

### A2 · Distribution boundary
- A2.1 · Publish one reproducible, source-free handoff surface.
  **Done when:** View formats, Display assets, manifests, and bibliography rebuild deterministically.

### A3 · Consumer boundary
- A3.1 · Keep placement and handoff explicit.
  **Done when:** each consumer declares its target, selected View or Displays, placement, and blocker.

## States

### A1 · Authored boundary
- ✅ A1.1 · QBt1 Cards bind authored inputs and its fixture excludes QA Probes, source notes, recipes, candidates, and semantic `output.md`.

### A2 · Distribution boundary
- ✅ A2.1 · The isolated multi-View regressions verify owned cleanup, merged BibTeX, and stale-build detection.

### A3 · Consumer boundary
- ✅ A3.1 · S-Main-4 receives QBt1-Display1 as a planned placement while both human gates remain visible.

## Files

- `../QBt-page-types/views/QBt1-for-view/manifest.json`
  The authored input, Display, consumer, and build contract.
- `../QBt-page-types/_fixture/`
  The generated consumer-safe distribution.
- `../QBt-page-types/consumer/S-Main-4-results.md`
  The live downstream placement specimen.

## Log

- 260811 · [RULING-JL] Paper consumes accepted View outputs rather than reaching back into Probe internals.
- 260810 · [RULING-JL] Generated TeX, PDF, Word, Display floats, and bibliography belong in `_fixture`, outside authored View resources.
