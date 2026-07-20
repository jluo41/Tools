---
name: haipipe-skill-diagnose
description: "Skill-set health review. Runs a 6-phase diagnose-first pass over ONE skill bucket: SCOPE inventory, DIAGNOSE (read-only auditors + root-cause taxonomy), REPORT ledger for the user's eyeball, FIX ([M] direct, [J] via in-file {CC->JL} threads), RESOLVE decisions into owning CHANGELOGs verbatim, COMMIT scope-limited on explicit go. Never fixes before the user has seen the report. Trigger: diagnose skills, review skill set, skill audit, skill 体检, review this bucket, skillset review, /haipipe-skill-diagnose."
argument-hint: "[bucket-path] (e.g. skills/task, skills/discovery, skills/0_utils)"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Agent
metadata:
  version: "1.3.0"
  last_updated: "2026-07-19"
  summary: "Diagnose-first health review of a skill bucket with user-gated fixes and verbatim decision archival. v1.3.0: the review LEDGER moves out of the bucket — it is written to `skills/_console/<YYMMDD>-<SLUG>.md` (see `_console/README.md`), because a process artifact must never ship inside the skill it reviews. REPORT, RESOLVE's reply sweep, the COMMIT gate + add-scope, and the return contract all follow it there."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-skill-diagnose
==============================

Operates on a SKILL BUCKET (a folder of skills), not on pipeline code.
Sibling: `/haipipe-qa` reviews pipeline code and data one issue at a time; this skill reviews the skills themselves.
Proven shape: the discovery-set review (v2.6.0 round) and the task-set review (95+ findings, 44 skills, Tools commit 84d14bd).

Contract in one line
--------------------

Diagnose everything first, show the user the full report, fix only after their eyeball, archive every user decision verbatim, commit only on explicit go.


Six phases
----------

### 1️⃣ SCOPE

- Target = one bucket path (from the argument; ask if absent).
- Inventory: skill count, file count, frontmatter validity (valid YAML, `name` == folder, version + last_updated + CHANGELOG pointer present).
- Output: a one-paragraph scope statement in chat.
- No file writes in this phase.

### 2️⃣ DIAGNOSE

- The main session reads the bucket core (orchestrator SKILL.md, root docs) line by line.
- Large buckets: dispatch READ-ONLY subagent auditors, one per sub-bucket, in a single parallel batch.
- Trust gate: spot-check at least 3 of each auditor's claims on disk before accepting the batch; one false claim means re-verifying that auditor's report item by item.
- Warn the user up front that auditor panels will appear and should not be manually stopped.
- Classify every finding per `ref/finding-taxonomy.md`: root-cause class, severity 🔴🟡🟢, [M] mechanical vs [J] judgment, `file:line`.

### 3️⃣ REPORT  (hard gate: nothing is fixed before this is eyeballed)

- Write the review to `skills/_console/<YYMMDD>-<SLUG>.md`, NOT into the bucket (see `../../_console/README.md`).
  A review is a PROCESS artifact and must never ship inside the skill it reviews.
  The date is the day the file is BORN and is never re-dated; one file per TOPIC, and a later session APPENDS to it.
  Part 1 = root causes (先看这个, one line each with counts);
  Part 2 = findings grouped by class, each with checkbox, id, severity, [M]/[J], file:line, proposed fix;
  Part 3 = coverage honesty (what was NOT audited and why).
- [J] findings: open their `> {CC->JL}:` threads AT the judgment points NOW, as part of report delivery, and MIRROR each full block under its finding in the console file so the user replies in ONE file (JL 2026-07-05: "我觉得这个comment 必须要先生成好" / "我在哪里加入我的comments呀"). Either copy's `> JL:` slot counts; first reply wins; both copies are removed together at RESOLVE. Opening a thread is a question, not a fix; the gate below still holds.
- Announce in chat with clickable bare `path:line` refs (report + each open thread), then STOP and wait for the user.

### 4️⃣ FIX  (only after the user approves the report)

- [M] items: fix directly, batched by root-cause class; verify each fixed family greps to zero afterwards.
- [J] items: never decide silently.
  Their threads are already open from Phase 3; execute replies as they land (per RESOLVE). Arbitrate by evidence (code + shipped templates beat prose; LESSON files beat stale SKILL claims; the newest deliberate design beats leftovers), apply the best reading, and for any [J] first discovered mid-FIX open its `> {CC->JL}:` thread AT the judgment point per `ref/thread-protocol.md`.
  Every thread carries a concrete worked EXAMPLE (real values, behavior under each option) and quotes the exact before/after text; an abstract-only thread is defective (JL 2026-07-05: "inline 的每个comments 都很难understand，try to provide more information and examples"). When the decision is drawable (two options / flow / before-after), the 例子 IS a compact diagram-ascii block, not prose (JL 2026-07-05: "如果可以用diagram-ascii，就用这个来explain").
- ONE TAG PER BODY OF WORK, assigned at the END. Do NOT bump a version or open a new CHANGELOG heading per round — a review that lands in four passes gets ONE tag, written when the work is actually final, with every finding folded into it. While the round is open, mark the entry `⚠️ IN PROGRESS` and keep appending to it. (JL 2026-07-19: "only add it or assign the new tags until we really have the final version, not everytime, we have a new tag".)
- If the user says anything is unclear (没讲清楚), stop writing prose and draw the decision with `/diagram-ascii`: what actually differs, what each option costs, one crisp question.

### 5️⃣ RESOLVE  (loop until zero threads)

- Sweep for replies: `grep -rn "^> JL:" <bucket> skills/_console/<the console file>` filtered to non-empty lines — the console file is where the user actually types, so it is never optional in the sweep.
- For each reply: execute the decision, archive the verbatim quote into the owning skill's CHANGELOG as `### Changed (JL: "...")`, then remove the thread from the doc.
- An owner ruling may overturn a recorded LESSON: keep the lesson body as history and add a `⚠️ SUPERSEDED <date> by owner decision ("<quote>")` banner so a future reviewer does not revert the docs.
- Process feedback (how to work, not what to change) goes to agent memory, not to CHANGELOGs.
- Close every turn with a clickable eyeball list of bare `path:line` in backticks; never markdown links with `#L` anchors (they do not open from the terminal).

### 6️⃣ COMMIT  (only on explicit user go)

- Gate: grep for `{CC->JL}` and for non-empty `> JL:` must BOTH return zero in the bucket AND in the console file.
- `git add` scoped to the bucket path plus the one `skills/_console/<YYMMDD>-<SLUG>.md` this review owns; never touch other sessions' changes elsewhere in the repo.
- Commit message: one line per major ruling carrying the user's quotes; the detailed history lives in the per-skill CHANGELOGs.


MUST NOT
---------

- Fix anything before the user has eyeballed the report (改前必报).
- Present my inference as the user's decision; quotes are verbatim or absent.
- Delete or rewrite a LESSON the owner overruled; banner it SUPERSEDED instead.
- Ship a finished round with no CHANGELOG entry — or fragment one round across several version tags.
- Commit without the zero-thread gate, or beyond the bucket scope.
- Write the review ledger into the bucket being reviewed; it goes to `skills/_console/`, never beside its subject.


Return contract
---------------

```
status:    ok | blocked
summary:   <phase reached; counts: findings by severity, threads open/closed>
artifacts: [skills/_console/<YYMMDD>-<SLUG>.md, changed skill paths...]
next:      <the gate the user currently holds>
```
