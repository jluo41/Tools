---
name: haipipe-page-for-knowledge
description: >-
  The Page Type contract for one KNOWLEDGE page on an InsightBoard: a supported proposition carrying strength, rival explanations and boundary conditions, derived from named Information rows. It claims; it does not advise. Use when a pattern must become something the design can lean on, when rivals must be recorded before a claim travels, or when a Wisdom page is about to counsel from an unstated claim. Trigger: knowledge page, proposition, strength, rivals, boundary conditions, page-type knowledge, /haipipe-page-for-knowledge.
metadata:
  version: "0.3.0"
  last_updated: "2026-08-28"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
  group-token: "K"
  outline:
    mode: fixed
    source: "this SKILL.md"
    shape: "Claim → Information Cited → Strength → Rivals → Boundary; the pooling-verdict page reads Knowledge Cited at division 2"
  parent: haipipe-page-for-task
---

# /haipipe-page-for-knowledge · state the proposition, with its strength and its boundary

Load `haipipe-page`, then `haipipe-page-for-task`, then this contract. Load `haipipe-plugin-probe` when reaching Task or Discovery sources and `haipipe-plugin-pagex` when citing another page on this board.

Declare `page-type: knowledge`. On a rung-major board this page lives in `<InsightBoard>/3-K-knowledge/K<NN>-<slug>/`; on a partition-major board (`haipipe-application` `ref/partition.md`) it lives in its partition group, `<NN>-<L>-<slug>/<L>K<NN>-<slug>/`, and the group token is the partition letter.

One page owes a reader exactly this: **what is true, how strongly, and where it stops being true**.

## Boundary

```text
I page                   what pattern the observations form   derives, never claims
MT03-question-knowledge  what is ASKED of this rung           asks, never concludes
K page                   what is TRUE, how strongly, and      claims, never advises
                         where it stops being true
W page                   what to DO about it here             counsels, cites a K row
```

**A K page never advises.** A proposition carrying a strength, its uneliminated rivals and a boundary is a K row; do, avoid, send, prioritise, recommend and leave-undecided are W verbs. The test is mechanical: a row an implementer could ACT on without reading anything else has counselled, and belongs one rung up where the audience and the context are allowed to enter.

A POOL or SPLIT verdict is a claim about EXCHANGEABILITY, not a recommendation, and the obligations it places on W pages come from `ref/partition.md` — never from a sentence on this page.

## Fixed Content outline

```text
### 1 · Claim               K<n> ids · one proposition each, stated plainly
### 2 · Information Cited   which I pages and which I rows, by id
### 3 · Strength            STRONG | MODERATE | WEAK, with the reason
### 4 · Rivals              other explanations, and which are not eliminated
### 5 · Boundary            population, window, unit, and what it cannot cover
```

- **Claim** states one proposition per `K<n>`. A claim spanning two mechanisms is two claims. On the pooling-verdict page (partition-major only) division 2 is **Knowledge Cited**: the verdict's subject is the heterogeneity claim itself, so its parent is that K row, one step and no further. Its verdict states exchangeability, POOL or SPLIT; the W-page obligations that follow are imposed by `ref/partition.md`, never asserted by the row.
- **Strength** is one of three words plus the reason, never a number implying precision the design cannot use.
- **Rivals** is required. A claim with no rivals listed has not been tested, it has been asserted.
- **Boundary** is what travels downstream with the claim and constrains every Wisdom row built on it.

A claim may be WEAK and still belong here. What it may not do is reach Wisdom without its strength travelling with it.

## Closing rule

This page closes when the proposition names its Information parents, its strength, its uneliminated rivals and its boundary.

## Closing checks

- Every K row cites the I rows it rests on; the pooling-verdict K row instead cites the heterogeneity K row, one step and no further.
- Strength is one of STRONG, MODERATE, WEAK, with a stated reason.
- Rivals are listed and each is marked eliminated or not.
- No K row recommends an action: that is Wisdom. A POOL/SPLIT verdict is a claim about exchangeability, not a recommendation; its consequences for W pages are `ref/partition.md`'s rules.
- The boundary is specific enough that a Wisdom page can test applicability against it.
- If a register cell names this page `🟡 <id> final`, a `## Log` row here names that question id and why the remainder cannot close.

## Chain law

This rung sits in the six-level lifting chain stated ONCE for the family, at `haipipe-insight` §The Climb Law: MT00's extract → D → I → K → W → a signed Handoff, each rung citing only named ROWS of the rung below, nulls and contradictions surviving upward, a level free to narrow what its parent said and never to broaden it, and a parent's change REOPENING every child row that cited it. It is cited here and deliberately not copied: four contracts restating one law in four places is how a patch comes to contradict itself.

This rung owns ONE exception: the pooling-verdict page cites the heterogeneity K row directly, one step and no further, because its subject is a claim ABOUT claims (division 1 above).

## Register

The question this page answers is registered once on `MT03-question-knowledge`, the register facing this rung; the board rollup on `MT04-question-wisdom` is what reassembles a chain spanning four pages. When the page is created, the LAP'S REGISTER PEN records this page's id in its question's Queue row (`⬜ <id>`): the write is the register's even when the mint occasions it, so the three pens stay uncrossed.

**The 🟡 receipt duty.** When this page closes part of its question and cannot close the rest, its register cell reads `🟡 <this page> final` (`haipipe-page-for-question`) and THIS page owes the sentence licensing it: a `## Log` row naming the question id and why the remainder cannot close. The register pen writes the cell, the page writes the reason, and neither may write the other's half. A cell reading final over a page carrying no such row is the defect the pair exists to prevent, because settled-partial and abandoned are indistinguishable on disk otherwise.

This variant owns no scripts.
