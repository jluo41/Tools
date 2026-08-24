# Projections: the rendered message is derived, and it is not a Page

state: ✅ SETTLED · projection-only `2-artifacts/` ruled 260820
owner: JL

## Opening

Where does the rendered message live, if it is not a Page of its own?

Under the DesignBoard's `2-artifacts/` folder, as a projection. A projection is the rendered form of an accepted division: the SMS text as it will send, the report as a docx, the dashboard as html. It carries three version stamps and is derived rather than authored. The Page is the source, so a hand edit made to a projection has to travel back to its division before anyone uses it.

### Writing Style

Keep the direction of authority visible in every sentence. Prose that treats the projection as the thing being written is how a hand edit becomes the truth by accident.

## Diagram

```text
🎨 R4 · abtest arm                         the SOURCE
   accepted: JL 260818 · handoff I03@v1 · render v5
              │
              │  fn/artifact.md · render, never author
              ▼
📦 2-artifacts/D01-R4-abtest-arm-v5.txt    the PROJECTION
   stamped: design v3 · handoff I03@v1 · render v5
              │
              └─ hand edited?  ──▶  reconcile back into R4 FIRST,
                                    which clears R4's accepted: row
```

## Content

### 1 · Contract

**Contract map**: the subparts below refine the Page decision into one bounded handoff.

```text
inputs → bounded contract → observable handoff
```

`fn/artifact.md` takes one accepted division and writes one stamped file. It refuses a division whose `accepted:` row is absent or cleared, because a projection of unaccepted content is how a draft reaches a patient.

#### 2 · The three stamps

Every projection names the design version it came from, the handoff version that division cited, and its own render version. Three stamps rather than one, because the same content can be re-rendered without changing, and the same render can become stale when the evidence under it moves.

#### 3 · Why it holds no Pages

A Page exists to close a question. A projection closes nothing: it is regenerated whenever its division changes, so it has no state a reader could settle. That is the same test that retired `page-type: artifact`, applied one level down.

#### 4 · Reconciling a hand edit

Someone will edit a rendered file directly, usually while reading it aloud in a review. The edit is real feedback and must not be discarded, but it lands in the wrong place. Copy it into the owning division, which clears that division's acceptance, then re-render. Never re-render over an unreconciled edit, because that silently deletes it.

## Aims

### A1 · Contract
- A1.1 · A projection is never authored, only rendered.
  **Done when:** the render verb refuses an unaccepted division and stamps every output.

#### A2 · Direction
- A2.1 · A hand edit reaches its division before it reaches a reader.
  **Done when:** reconciliation clears the division's acceptance rather than bypassing it.

## States

### A1 · Contract
- ✅ A1.1 · `fn/artifact.md` is a render-only verb with no promotion route since Application 0.9.0.

#### A2 · Direction
- ✅ A2.1 · Step 5 of the render procedure requires reconciliation before use.

## Files

### 📋 Contracts
- `../../../../application/haipipe-application/fn/render.md`
  The render procedure, its refusal condition, and the stamps.
- `../../../../application/page-types/haipipe-page-for-design/SKILL.md`
  Where `2-artifacts/` is declared a projections folder holding no Pages.

## Law

The division is the source and the projection is derived. An edit that lands on the derived side is feedback, not truth, until it is copied back.

## Log

260820 · Reduced `2-artifacts/` to projections when `page-type: artifact` retired, and rewrote `fn/artifact.md` as a render-only verb.
