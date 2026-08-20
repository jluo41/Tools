# QBt15 · page-type NARRATIVE · the story architecture between Opening and Section

state: ✅ SETTLED · contract, resolver, Board, and fresh-context validation complete
page-type: narrative
owner: JL
method: test whether a new agent turns an accepted Opening and existing Pages into an executable Section map

## Opening
How should the paper order its claims so every Section changes the reader in the intended sequence?

Narrative owns that order and the Section map that executes it.
It does not absorb Opening, rediscover evidence, or write section prose.

**Covered here**: the contract boundary, the source routes, and the downstream handoff.

**Covered elsewhere**: Opening identity lives on `QBt18`; reusable venue knowledge lives in `QBv`; Section execution lives on `QBt6`.

## Writing Style
Plain English for a reader who has never opened the paper.
One sentence per line, and no em dashes.

## Content
### 1 · Promise and claim roles
**Narrative ownership**: the accepted promise becomes explicit rhetorical roles.

```text
Opening handoff ──▶ setup · peak · consequence · mechanism · boundary
```

Narrative starts from the accepted Opening handoff.
It assigns each important claim a rhetorical role such as setup, peak, consequence, mechanism, support, or boundary.
It does not become a second canonical Claims ledger.

### 2 · Arc and reader journey
**Reader movement**: every claim changes what the reader can understand next.

```text
belief₀ ─ claim₁ ─▶ question₁ ─ claim₂ ─▶ belief₂
```

The arc states what the reader must understand before each claim can land.
The reader journey states what the reader believes, asks, and learns at each step.
Together they make claim order testable rather than intuitive.

### 3 · Section map and handoff
**Section handoff**: one global order becomes one bounded assignment per Section.

```text
section-id | reader job | claim role | must establish | PageX sources |
display moment | allocation/limit | enters from | hands to
```

One row governs each manuscript or appendix Section in reader order.
A Section page executes exactly one current row.
Reordering rows reopens every affected assignment.

### 4 · PageX and Probe boundary
**Source routes**: both routes meet only after Probe work has an owning Page.

```text
existing Page ── PageX ──▶ Narrative
Task / Discovery ─ Probe ─▶ owning Page ─ PageX ─▶ Narrative
```

PageX allocates existing Board Pages to claims and Sections.
Probe separately reaches Task and Discovery folders through the evidence Page that owns that work.
Narrative records an evidence gap and routes it out.
It does not open a local Probe investigation.

### 5 · Runtime ownership

**Narrative folder**: architecture and Page bindings stay together without local evidence work.

```text
<NarrativePage>.md
├── outline/
└── pagex/
```

It owns no `probe/`, `proof/`, manuscript `.tex`, bibliography bank, or display unit.

## Aims
### A1 · 🧭 Promise and claim roles
- A1.1 · Narrative receives the promise and assigns every important claim a role.
  **Done when:** the contract keeps identity upstream and rhetorical roles here.

### A2 · 🎼 Arc and reader journey
- A2.1 · Claim order changes the reader in a stated sequence.
  **Done when:** setup, peak, consequence, and boundary dependencies are inspectable.

### A3 · 📐 Section map and handoff
- A3.1 · Every Section receives one executable row.
  **Done when:** the row carries reader job, claim role, establishment, sources, transition, and limit.

### A4 · 🔎 PageX and Probe boundary
- A4.1 · Existing Pages use PageX and Task or Discovery folders use Probe through an owning Page.
  **Done when:** Narrative owns no local evidence investigation.

### A5 · 📂 Runtime ownership
- A5.1 · Narrative owns only architecture and Page bindings.
  **Done when:** runtime ownership is limited to `outline/` and `pagex/`.
- A5.2 · A new agent follows this boundary without copying evidence or prose.
  **Done when:** the required fresh-context validation passes.

## States
### A1 · 🧭 Promise and claim roles
- ✅ A1.1 · The v0.2.0 contract receives Opening and assigns rhetorical roles here.

### A2 · 🎼 Arc and reader journey
- ✅ A2.1 · The contract requires both dependency order and reader-state change.

### A3 · 📐 Section map and handoff
- ✅ A3.1 · The governing row schema is explicit in the contract and specimen.

### A4 · 🔎 PageX and Probe boundary
- ✅ A4.1 · The routes remain parallel and meet at the owning Page boundary.

### A5 · 📂 Runtime ownership
- ✅ A5.1 · Runtime ownership is `outline/` plus `pagex/` only.
- ✅ A5.2 · Fresh agent produced an executable Section map without copying evidence or prose.

## Files
- `../../paper/page-types/haipipe-page-for-narrative/SKILL.md`
  The v0.2.0 Narrative contract.
- `4-QBt-page-types/QBt18-for-opening/QBt18-for-opening.md`
  The upstream Opening specimen and decision record.

## Log
260817 · JL · ruled that Paper uses Opening, Narrative, and Section; PageX and Probe remain parallel
260817 · Codex · rewrote the Narrative specimen and contract around the Opening-to-Section handoff
260817 · fresh agent · passed P1-P3 PageX allocation and routed the unpaged Task gap through Probe
