# Patent: the one venue where a single sentence is the deliverable and everything else supports it

state: 🟡 PARTIAL · 3 jurisdictions as README delta tables · no outlet tree · no exemplars
owner: JL
method: state what a claim means in a filing as against in a paper, record the three jurisdiction deltas, and keep this pack's word collision with the Claims stage from doing damage

## Opening

Every other venue in this tree accepts a document. A patent office accepts a sentence, and the rest of the filing exists to support it. What does that inversion change?

It also produces the most dangerous word collision in the paper system. The lifecycle has a Claims stage. A filing has claims. They are not the same object and the pack's `-> Claims` map runs straight through the ambiguity.

**Where this page sits**: it is one pack under `QBv0`, which owns what any pack owes.
This page owns only what is true of `playbook-patent`.

**Why this pack has no outlet tree**: jurisdictions are not journals.
CNIPA, USPTO, and EPO prescribe different specification orders, different claim forms, and different abstract limits, and the pack encodes them as delta tables in `README.md`. That is the same declared exception `QBv6` carries.

**What is unusual about its lifecycle**: the pack documents a drafting process, which no journal pack does, because a filing is prosecuted over years rather than submitted once.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `QB4-overall.md` and are not restated here.

**Never transcribe the jurisdiction table**: it lives in `playbook-patent/README.md` and is cited, never copied.

**Always disambiguate the word claim on this page**: write `patent claim` or `lifecycle claim`, never a bare one.
The collision is the single most likely source of a wrong action anywhere in this group.

✅ `a patent claim is the deliverable`  ❌ `the claim is the deliverable`

**Say the jurisdiction office, not the country**: CNIPA, USPTO, EPO, because the deltas are the offices' rules.

## Diagram

**One sentence, three jurisdictions**: and a word that means two different things.

```text
  ⚖️ THE INVERSION
     journal ── the DOCUMENT is the deliverable
     patent  ── the CLAIM is the deliverable,
                the specification exists to support it

  🌍 THREE JURISDICTIONS
  ┌──────────────┬──────────────┬─────────────┬──────────────┐
  │              │ CN · CNIPA   │ US · USPTO  │ EP · EPO     │
  ├──────────────┼──────────────┼─────────────┼──────────────┤
  │ claim form   │ two-part,    │ single-     │ two-part     │
  │              │ character-   │ clause      │ "character-  │
  │              │ izing clause │ "compris-   │ ised in      │
  │              │              │ ing"        │ that", Rule  │
  │              │              │             │ 43(1), where │
  │              │              │             │ appropriate  │
  │ abstract     │ <=300 chars  │ <=150 words │ ~150 words   │
  │              │              │ / 2500 ch   │ no merits    │
  │ drawings     │ "Figure 1"   │ FIG. 1      │ FIG./Figure 1│
  │ ref signs    │ in the       │ inline      │ separate list│
  │              │ drawings     │             │              │
  │              │ description  │             │              │
  │ utility mdl  │ 10 yr, avail │ none        │ none         │
  └──────────────┴──────────────┴─────────────┴──────────────┘

  ⚠️ WORD COLLISION
     lifecycle "Claims" stage  ≠  patent claims
     and the pack's  ->Claims  map crosses exactly here

  🚫 no outlet tree · 🚫 no exemplars · taste.md at FAMILY level
```

## Content

### 1 · The inversion, and what it does to the lifecycle

**The specification supports the claim**: every artifact the paper system produces changes role.

```text
  📄 journal            📑 filing
  ──────────            ─────────
  the document IS   ▶   the CLAIM is the deliverable
  the deliverable       the specification SUPPORTS it

  ── a figure is not illustration, it is support for a
     limitation, and its reference signs are load-bearing
  ── background is not motivation, it is what the claim
     must be distinguished FROM
  ── the abstract is a length-capped formality, and the
     EPO forbids stating merits in it
```

⚖️ Establishes the inversion as the pack's core content, which is why every stage map here reads differently from a journal pack's.

#### 1.1 · Prosecution is a lifecycle no journal pack has
(so this pack documents a drafting process rather than a submission)
The pack's README carries a drafting process under its Write/Edit map.
A filing is amended against office actions over years, which makes the closest paper analogue `QB10` Round rather than a submission.

### 2 · The word collision, and how to survive it

**Two objects, one word, and a stage map that crosses between them**: this is the pack's real hazard.

```text
  🧩 LIFECYCLE CLAIM        🧩 PATENT CLAIM
     an assertion the           a legally construed sentence
     paper argues and           defining the boundary of the
     evidence supports          monopoly
     lives in 1b-claims         lives in the filing itself
     can be softened            cannot be softened without
     during revision            narrowing the right

  💥 the pack's  ->Claims  map points the lifecycle stage at
     the filing's claim set, and nothing in the wording of
     either says they are different objects

  🛡 the mitigation is vocabulary, not structure:
     write "patent claim" or "lifecycle claim", always
```

⚠️ Establishes the collision as a naming hazard with a naming fix, rather than a structural problem to re-architect.

#### 2.1 · Softening is safe on one side and destructive on the other
(which is why the two must never share a revision pass)
A revise pass that hedges a lifecycle claim improves it.
The same pass applied to a patent claim narrows the granted right, and the pack has no guard that would stop it.

### 3 · Three jurisdictions, no exemplars

**The deltas are precise and there is nothing granted on disk to imitate**: the same hole `QBv6` carries.

```text
  ✅ the jurisdiction table is specific and correct
     claim form · spec order · reference signs · abstract
     limits · drawing labels · utility model availability
     · term

  📭 0 exemplars
     ── no granted CNIPA specification, no USPTO Detailed
        Description, no EPO Reference Signs List
     ── and the README again calls Write/Edit "the main
        purpose"

  🔀 taste.md at FAMILY level ── the same placement as
     playbook-grant and playbook-pnas, undeclared
```

⚠️ Establishes the pack as structurally correct and linguistically ungrounded.

## Aims

### A1 · ⚖️ The inversion, and what it does to the lifecycle
- A1.1 · The role change for figures, background, and abstract is stated where a paper is converted into a filing.
  **Done when:** converting a display into a supporting figure records the limitation it supports.

### A2 · ⚠️ The word collision, and how to survive it
- A2.1 · The vocabulary rule is written where either stage reads, not only on this page.
  **Done when:** no skill can act on the word claim in a patent context without meeting the disambiguation.
- A2.2 · A revise pass cannot silently soften a patent claim.
  **Done when:** the humanizer and content workers are barred from a filing's claim set, or the bar is written and checkable.

### A3 · ⚠️ Three jurisdictions, no exemplars
- A3.1 · At least one granted filing per jurisdiction this repo actually targets lands in the pack.
  **Done when:** the language guidance the README calls its main purpose has a source on disk.

## States

### A1 · ⚖️ The inversion, and what it does to the lifecycle
- ⬜ A1.1 · Not started. The stage maps carry the roles; the conversion is unwritten.

### A2 · ⚠️ The word collision, and how to survive it
- ⬜ A2.1 · Not started. The collision is recorded here for the first time.
- ⬜ A2.2 · Not started, and unguarded. Nothing prevents a revise worker from hedging a patent claim.

### A3 · ⚠️ Three jurisdictions, no exemplars
- ⬜ A3.1 · Not started. Zero exemplars, same as `playbook-grant`.

## Files

- `../../paper/venue/playbook-patent/README.md` · the jurisdiction delta table, the drafting process, the four stage maps
- `../../paper/venue/playbook-patent/taste.md` · the examiner's test, at family level
- `QBv6-grant.md` · the other non-journal pack, same shape exception and same exemplar hole
- `QBv0-venue-pack-contract.md` · what any pack owes

<!-- exemplars:begin -->

📚 **Exemplars** · 0 papers on disk, regenerated by `_tools/sync-exemplars.py`

Filed at FAMILY level under `../../paper/venue/playbook-patent/examples/`, not under the outlet (QBv0 A3.1).

- none. No `examples/` folder under `../../paper/venue/playbook-patent/`, so this outlet states section norms with no exemplar behind them.

<!-- exemplars:end -->

## Law

In a filing the patent claim is the deliverable and the specification supports it, which inverts the role of every artifact the paper lifecycle produces.
A patent claim and a lifecycle claim are different objects that share a word: softening one improves a paper and narrows a granted right, so no revision pass may treat them alike.

## Glossary

- **Patent claim**: the legally construed sentence defining the boundary of the monopoly, the filing's actual deliverable.
- **Lifecycle claim**: an assertion the paper argues, owned by the `1b-claims` stage, which may be softened during revision.
- **Reference sign**: a numeral tying a drawing element to the specification text, load-bearing in a filing and placed differently in each jurisdiction.

## Log

260802 · Opened with the QBv group, from `playbook-patent` at `Venue-Paper@fe25a88`.
