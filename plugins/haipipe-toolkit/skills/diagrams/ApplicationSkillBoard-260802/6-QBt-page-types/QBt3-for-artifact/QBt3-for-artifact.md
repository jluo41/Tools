# Artifact retired: a Page Type that only relocated a signature

state: ✅ SETTLED · `page-type: artifact` deleted 260820 · absorbed into a per-division row
owner: JL

## Opening

Does a delivery unit need its own Page Type, or is it already a part of the Design Page it came from?

It is already a part. `page-type: artifact` shipped on 260820 at 0.2.0 and was deleted the same day, once JL asked to keep one concept instead of two. Six Content roles were compared against a Design Page's `R<n>` unit division, and five of them already existed there character for character. The sixth, acceptance, differed only in where a reviewer's name and date got written.

### Writing Style

Name the role that was compared and where it already lived. A retirement record earns its place by showing the comparison, not by asserting the verdict.

## Diagram

```text
📦 for-artifact · role            🎨 where it already was
──────────────────────────        ────────────────────────────────────────
Unit contract               ══▶   R<n>: unit id · audience job · rail
Authored content            ══▶   R<n>: "exact content or interaction"
Variants / arms             ══▶   R<n>: "declared variants"
Trace                       ══▶   R<n>: "Insight/Handoff refs · design move"
Render / preview            ══▶   page: "Render and acceptance"
Acceptance                  ══▶   page: "Render and acceptance"   ← the only delta
```

## Content

### 1 · Contract

**Contract map**: the subparts below refine the Page decision into one bounded handoff.

```text
inputs → bounded contract → observable handoff
```

The admission rule read: *this unit may be accepted, rejected, revised, versioned, or deployed while a neighboring unit is not.* That sentence describes a signature grain, not a page kind.

#### 2 · What replaced it

Acceptance moved from the Page down to the division:

```text
R4 · abtest arm
     accepted: JL 260818 · handoff I03@v1 · render v5
```

One division may be accepted while a sibling is mid-revision, which is the case the type existed for. The Page's `state:` line reports the system; each division's row reports the unit.

#### 3 · What would have been lost the other way

Collapsing in the opposite direction was rejected. A Design Page holds the audience/job strategy, the design principles, and the cross-unit rails covering escalation order, prohibited moves, and uncertainty language. Those exist only because the set is reviewed together. Keeping Artifact and dropping Design would have left coherence with no owner.

#### 4 · What survives under the name

`2-artifacts/` remains a folder under each DesignBoard, holding versioned projections rendered from accepted divisions. It holds no Pages, and `fn/artifact.md` is now a render verb with no promotion route.

## Aims

### A1 · Contract
- A1.1 · No Page Type exists solely to relocate a signature.
  **Done when:** the contract is deleted and its one real rule lives on the division.

#### A2 · Coverage
- A2.1 · The case the type existed for still works.
  **Done when:** one unit can be accepted while a sibling is mid-revision.

## States

### A1 · Contract
- ✅ A1.1 · `page-types/haipipe-page-for-artifact/` deleted 260820; `check.py` no longer accepts the key.

#### A2 · Coverage
- ✅ A2.1 · Design Page Type 0.3.0 carries the per-division `accepted:` row.

## Files

### 📋 Contracts
- `../../../../application/page-types/haipipe-page-for-design/SKILL.md`
  The absorbing contract; see its acceptance-per-division section.
- `../../../../application/haipipe-application/fn/artifact.md`
  The surviving render verb.

## Law

A page kind must change how a page CLOSES. A kind that changes only where a signature is written is a field, not a type.

## Log

260820 · Shipped `page-type: artifact` 0.2.0 as an optional promotion.
260820 · Retired it the same day (JL: "I think we only need to keep one conception"). Acceptance became a per-division row on the Design Page; the projections folder survives.
