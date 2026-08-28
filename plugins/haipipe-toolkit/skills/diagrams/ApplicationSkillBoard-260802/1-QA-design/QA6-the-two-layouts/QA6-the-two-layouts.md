# Two InsightBoard layouts, and the verdict that licenses a third board

state: ✅ SETTLED · partition-major ruled 260823 · grammar in ref/partition.md
owner: JL

## Opening

When one dataset is read as several subgroups, does each subgroup get its own board?

No. It gets a PARTITION inside one board. An InsightBoard reads ONE dataset, either as a single story (rung-major, the default) or as several told the same way (partition-major, groups are partitions). A subgroup earns its own board only by citing a SPLIT verdict, which the cross group alone may issue.

### Writing Style

State the default before the alternative. A page that opens with the exotic layout teaches the reader to reach for it.

## Diagram

```text
RUNG-MAJOR · groups are the rungs        PARTITION-MAJOR · groups are partitions
0-MT-meta/                               0-MT-meta/          MT00 + the registers,
1-D-data/D<NN>-<slug>/                                       shared by every partition
2-I-information/I<NN>-<slug>/            1-F-full/F<rung><NN>-<slug>/   the TEMPLATE
3-K-knowledge/K<NN>-<slug>/              2-B-<subgroup>/B<rung><NN>-<slug>/  a MIRROR
4-W-wisdom/W<NN>-<slug>/                 9-X-cross/X<rung><NN>-<slug>/  the COMPARISON
                                            └── pinned at 9 so a new partition
one story, one ladder                          never renumbers it
```

## Content

### 1 · One dataset, one board

**The rule**: what makes a second board, and what does not.

```text
a new source extract      ──▶ a NEW InsightBoard
a new question            ──▶ a new chain INSIDE the board
a subgroup of the extract ──▶ a PARTITION inside the board, never a board
a subgroup + SPLIT verdict ──▶ a child board, and the verdict is its birth certificate
```

A board is one head page's scope: one Meta is one source scope. Minting a board per subgroup would give each its own Meta, which asserts that the subgroups came from different extracts, and they did not.

#### 2 · The mirror rule

Every partition group mirrors the template group slug for slug. A partition that cannot produce a page its template has does not silently omit it; it registers a 🚫 refusal with a reason. Silence and refusal look identical on disk otherwise, and only one of them is a finding.

#### 3 · The letters are reserved

```text
F   the full/template partition       X   the cross group, index-free
Q   question              S  source              M  meta
```

Reserved letters may not name a subgroup, because a partition letter prefixes every page id in its group and a collision would make `XK02` ambiguous. `X` carries no index at all: letters sort after digits, so `X-cross/` seats itself last in every listing and adding a partition never renumbers the group every W page cites. Boards carrying the legacy pin `9-X-cross/` stay legal; a live board is never renamed for this.

#### 4 · Only X compares

A partition group answers within itself; it may not reach sideways into a sibling. The comparison happens once, in the cross group, and it unlocks two contract exceptions found necessary in practice: an X contrast page derives from MIRRORED I rows rather than local D rows, and the pooling-verdict K page cites the heterogeneity K row directly, one step, rather than climbing from I.

#### 5 · The verdict conditions every W page

```text
XK02 POOL   ──▶ every W page counsels the pooled action; a partition W page that
                would differ closes as a DEFERRAL and exports no handoff
XK02 SPLIT  ──▶ the partition may become its own board, citing this verdict
```

The template W page never defers, because there is nothing above it to defer to. This is what stops a subgroup story from quietly becoming a separate programme without anyone deciding it.

#### 6 · A partition is a config, never a fork

The task that produces a partition's evidence is the SAME task with a different config, and the thresholds it applies come from one `_thresholds.yaml` at the task group's root. A partition that needed its own code would not be a partition of one dataset. A first flight found a task that had hardcoded its segment filter, which made the template partition unrunnable and proved the rule by breaking it; the Log dates it.

## Aims

### A1 · One dataset, one board
- A1.1 · A subgroup cannot become a board by accident.
  **Done when:** the only path to a child board names a SPLIT verdict.

#### A2 · Mirror
- A2.1 · A gap in a partition is visible as a refusal, not as an absence.
  **Done when:** every template slug has a mirror page or a registered 🚫.

#### A5 · Verdict
- A5.1 · No W page counsels a partition-specific action under POOL.
  **Done when:** a differing partition W closes as a DEFERRAL with no handoff.

## States

### A1 · One dataset, one board
- ✅ A1.1 · Ruled 260823; `ref/partition.md` carries the grammar and the door carries the layout choice.

#### A2 · Mirror
- ✅ A2.1 · Ruled; a partition added by a second session on 260824 exercised it and its missing census page was the rule catching a real gap.

#### A5 · Verdict
- ✅ A5.1 · Ruled with the DEFERRAL close, and the template exemption stated.

## Files

### 📋 Contracts
- `../../../../application/haipipe-application/ref/partition.md`
  The partition grammar: reserved letters, the mirror rule, the verdict.
- `../../../../application/haipipe-application/SKILL.md`
  The layout choice, made once at scaffold.
- `../../../../application/haipipe-application-workflow/SKILL.md`
  The climb ORDER a partition-major board must follow: template first, mirrors in parallel, cross, then every W.

## Law

An InsightBoard reads ONE dataset. A subgroup is a partition inside it, and becomes a board only by citing a SPLIT verdict.

## Log

260823 · Partition-major layout ruled, with `X` pinned at 9, the reserved letters, and the mirror rule (JL: one board links to one dataset; the DIKW is grouped by partition, and the question registers carry one column per partition).

260824 · The cross group's contract exceptions recorded after the first build found three pages otherwise unclosable: I-from-I on the contrast page, K-from-K on the pooling verdict, and the wisdom DEFERRAL close under POOL.
260827 · The partition test now guards this ruling's door (QI3, the workflow's I0): audience stratum only, three named properties, with time's three guises routed to their existing homes instead of into partitions.

260827 · The pin retired (JL): X carries no index, since letters sort after digits the seat is permanent without a magic number; `9-X-cross/` grandfathered on live boards.
