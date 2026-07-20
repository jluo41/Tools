Finding taxonomy: root causes, severity, [M]/[J]
==================================================

Every finding carries: root-cause class, severity, [M]/[J], `file:line`, proposed fix.
The classes below covered ~95 findings across two real reviews (discovery set, task set); extend the list only when a finding truly fits none.


Root-cause classes
-------------------

### ① 🚚 搬家没改地址 (migration debris)

A move, rename, split, or merge happened and the pointers were never updated.
Symptoms: dead relative paths, retired skill/agent names, references to files that became something else.
Real examples: `project/haipipe-workflow` after the move to `task/` (17 refs); `ref/layer-*.md` after the nn split (~30 refs); "Run Script Reviewer agent" after the reviewer merge (8 refs); `0-RawStore` for a store named `0-RawDataStore` (28 refs).
Almost always [M]: the correct target exists on disk, fix is mechanical.

### ② 📄 路由层失真 (routing drift)

The orchestrator/dispatcher doc no longer matches the skills on disk.
Symptoms: dispatch names that do not exist (`haipipe-task-<type>` vs `haipipe-task-for-<type>`), types missing from keyword tables, orphan skills that claim a dispatcher parent nothing routes to, verbs with no route.
Real examples: `endpoint` missing from every routing table while the type table listed it; `haipipe-data-external`/`-remote` on disk but unreachable.
Mostly [M] once direction is decided; wiring an orphan in vs archiving it is [J].

### ③ ⚔️ 内部矛盾 (internal contradictions)

The same contract is stated two or more incompatible ways in the bucket.
Symptoms: two letter schemes for task groups, two Fn-ownership maps, a flat ban next to an authorized exception, TARGET-AWARE here vs platform-agnostic there.
Always [J]: someone must pick the truth.
Arbitration evidence order: code + shipped templates beat prose; LESSON files beat stale SKILL claims; the newest deliberate design beats leftovers; when evidence still ties, ask the owner.

### ④ 🪝 层间耦合 (layer coupling)

A lower-layer doc names or routes to an upper layer.
Rule: work layers (task, discovery) are upper-layer-UNAWARE; whoever consumes results records the link on THEIR side.
Tolerated exemptions: agents/ files may name their CALLERS as trigger hints; toolkit-wide infra (haipipe-workflow) legitimately names all layers.
[J] the first time a class of coupling is judged, [M] for the repeats.


Severity
---------

```
🔴 broken     dead path, wrong name, or a contradiction that MISLEADS EXECUTION
              (an agent following the doc does the wrong thing or crashes)
🟡 stale      works but lies: doc does not match disk or itself, reader wastes time
🟢 cosmetic   style, ordering, wording; fix opportunistically
```


[M] vs [J]
-----------

```
[M] mechanical   the correct answer is already on disk; no owner input needed
[J] judgment     someone must choose; apply the best evidence-based reading,
                 then open a > {CC->JL}: thread per ref/thread-protocol.md
```


Finding line format (in the console file)
--------------------------------------------

```
- [ ] **<id>** 🔴 `[M]` <what is wrong, with file:line> Fix: <proposed fix>.
```

- id = class letter + number (A1, B2, ...), stable once assigned.
- `[x]` when fixed; append the outcome in bold: **FIXED: <what was done>.** / **RESOLVED per JL <date> ("<quote>"): ...**
- Skipped items stay `[ ]` with **SKIPPED (reason)**; deliberate skips are part of coverage honesty.
