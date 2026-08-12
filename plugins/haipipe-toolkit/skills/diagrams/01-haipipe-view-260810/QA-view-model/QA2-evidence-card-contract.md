# The View Card contract: one clickable interface for evidence and relationships
state: ✅ SETTLED · source, payload, and Display preview-first behavior passed browser validation
owner: JL
method: unify existing Card source forms behind one View-facing interface

## Opening
How does a Card exist in a View, and what must open when a reader clicks it?
A Card is a rendered inspection interface, not an independent evidence file.
In source Markdown it exists as a sentence annotation or a resolver marker.
Its binding points to the real Probe, bibliography entry, value run, Display, or consumer.
A View uses the same clickable interaction for both evidence and relationships while preserving each kind's specialized payload.

**Existing interaction**: `haipipe-sentence` renders `> Card <exact words>: <payload>` as a clickable popover on those words.

**Existing rich resolvers**: citation keys, Q references, checked numbers, and Display markers already open specialized Cards backed by real files.

**View addition**: Probe/QA-input and Consumer become explicit Card kinds, and every kind exposes its binding plus current state.

## Diagram

**The three layers**: source annotation, bound object, and rendered interaction are separate.

```text
SOURCE IN CANONICAL VIEW PAGE        REAL BINDING                         BROWSER

> Card exact words: ... ───────────▶ Probe / QA-bank ───────────────┐
\citep{key} ──────────────────────▶ references.bib                 │
3 [Q-View-1] ────────────────────▶ Probe / run / QA answer         ├─▶ clickable Card
QBt1-Display1 ───────────────────▶ Display artifact + state        │
> Card Section: Consumer ... ─────▶ downstream Page + placement ───┘
```

## Content

### 1 · Source form
**The source contract**: Cards live beside the words they annotate or in a recognized resolver marker.

```markdown
Sentence containing exact words.

> Card exact words: ID · kind · binding · role · state
```

The generic record is stored directly below the sentence in the canonical View Page.
The renderer hides that record, wraps the first exact non-overlapping span, and opens its payload in a popover.
A missing or ambiguous span fails visibly rather than silently dropping the Card.

Rich source markers remain legal:

```text
\citep{key}       Citation Card
3 [Q-View-1]     checked Value Card + Probe Card
QBt1-Display1   Display Card
```

The View skill normalizes these source forms into one reader-facing Card interface; it does not duplicate the existing resolvers.

### 2 · Kinds and common payload
**The common interface**: every Card answers what this thing is, where it resolves, why it matters here, and whether it is current.

```text
id          stable within the View
kind        qa-input · probe · citation · value · evidence · display · consumer
binding     real file, record, run, artifact, or Page
role        what the bound object does for this View
state       answered/current/stale/waiting/planned/accepted as applicable
used by     View-body subsection, Display, or consumer
boundary    only when the content needs one
```

Specialized fields extend rather than replace the common payload:

```text
Citation   key · proposition · source place · citation job
Value      run · population · quantity · unit · uncertainty · stale when
Display    preview PNG/PDF · artifact · selected View content · acceptance
Consumer   target · selected View/Display · placement · handoff gate
Probe      QA-bank · question · answer state · consumer interpretation
```

A first-class Board consumer names both its exact Page id and its binding path.
The id is the live route inside the Card; the path is provenance, and the target Page owns prose placement plus acceptance state.

A Card may omit a specialized field only when it does not apply.
It may never invent a binding or present an unresolved target as current.

### 3 · Self-reference gate
**The View is the first reader**: every promised Card must work inside the View before the same binding is handed downstream.

```text
source record exists
        ▼
View uses the marker
        ▼
Card opens the real binding
        ▼
browser check records pass
        ▼
human acceptance may release selected outputs
```

Evidence validity, Display acceptance, and consumer handoff remain independent.
A generated review build may be current while a Display or consumer is still waiting for human acceptance.
For a Display Card, the current preview is the first payload, not a file link buried after status prose. PNG leads because it renders reliably in the Board browser; PDF remains one click away.

## Aims

### A1 · Source form
- A1.1 · Keep Card source readable in raw Markdown.
  **Done when:** A writer can see the annotated words, kind, and binding without opening generated HTML.
- A1.2 · Preserve rich citation, value, Q-reference, and Display resolvers.
  **Done when:** View uses the existing marker dialect rather than implementing parallel lookups.

### A2 · Kinds and common payload
- A2.1 · Define one common Card interface across evidence and relationships.
  **Done when:** Probe, Citation, Value, Evidence, Display, and Consumer all expose a binding, role, and state.
- A2.2 · Make Consumer a real tested Card kind.
  **Done when:** QBt1's exact consumer words open a target file, selected Display, placement, and gate state.

### A3 · Self-reference gate
- A3.1 · Fail visibly on missing spans or bindings.
  **Done when:** no promised Card can disappear or claim current without a resolvable object.
- A3.2 · Prove the View-first interaction in a real browser.
  **Done when:** one run clicks QA input, sentence, citation, value, Probe, Display, and Consumer Cards.
- A3.3 · Make a Display Card open on the artifact itself.
  **Done when:** QBt1-Display1 and QBt1-Display2 both show a loaded PNG before metadata and expose their PDF in the same Card.

## States

### A1 · Source form
- ✅ A1.1 · Content 1 records the exact Markdown annotation and its visible-failure rule.
- ✅ A1.2 · QBt1 continues to use the existing citation, checked-number, Q-reference, and Display markers.

### A2 · Kinds and common payload
- ✅ A2.1 · Content 2 defines the common fields and five specialized extensions.
- ✅ A2.2 · The exact words “Main Results section” open C1 with its live S-Main-4 Page link, target file, QBt1-Display1 binding, placement, and handoff state.

### A3 · Self-reference gate
- ✅ A3.1 · The inherited sentence Card renderer already emits a loud miss row for an absent span.
- ✅ A3.2 · The real-browser run passes 45 of 45 across QA input, Citation, Value, Probe, Evidence, Display, and Consumer Cards, including Consumer-to-Page navigation.
- ✅ A3.3 · The 45 of 45 browser run confirms both Display Cards load preview.png as the first payload and expose preview.pdf.

## Files

- `../QBt-page-types/QBt1-for-view.md`
  The rendered specimen containing every tested Card kind.
- `../QBt-page-types/views/QBt1-for-view/manifest.json`
  The resource contract bound to the canonical View Page.
- `../../board/haipipe-sentence/SKILL.md`
  The existing exact-span Card source and interaction contract.

## Log

- 260810 · [CHECK-CC] Owner-indexed markers QBt1-Display1 and QBt1-Display2 now open the same preview-first Cards as their full Display folders; the browser suite passes 45 of 45.
- 260810 · [CHECK-CC] Generic Card payloads now turn exact Board Page ids into live routes; C1 follows S-Main-4 successfully in the 45 of 45 browser run.
- 260810 · [CHECK-CC] Both revised Display Cards open on a loaded PNG before metadata and retain their PDF link; the full browser suite passes 43 of 43.
- 260810 · [CORRECTION-JL] A Display Card that exposes metadata but hides its actual PDF/PNG below the fold does not work as an inspection interface.
- 260810 · [CHECK-CC] The unified Card interface passed 40 of 40 browser checks, including the new QA-input and Consumer relations.
- 260810 · [RULING-JL] Card is a source annotation or resolver marker backed by a real object; the clickable popover is its rendered form.
- 260810 · [RULING-JL] QA Consumer is a Card kind, and Probe/QA-bank relationships belong to the same interface.
- 260810 · [REVISE-CC] Expanded the old evidence-only payload into one Card interface with specialized Probe, Citation, Value, Display, and Consumer fields.
