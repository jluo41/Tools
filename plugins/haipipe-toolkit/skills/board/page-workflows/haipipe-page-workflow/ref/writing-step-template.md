# Writing Run records · copy only the records needed now

Paths follow `interactive-writing-run.md` and the Folder owner's Run dialect.
Replace every placeholder with an actual value or explicit `not supplied`.
Record messages verbatim in fenced blocks; use a longer fence when the message
itself contains backticks. Do not invent a person, timestamp or message id.

## runs/<run>.md

```yaml
family: page
operation: interactive-writing
interaction: human-feedback
target: C1.P1, C1.P2
result: <resolved owner-native Result path>
```

- Goal: <one bounded writing goal, in the person's terms>
- Page and Board: <resolved paths>
- Scope: <paragraphs/map; excluded and already accepted targets>
- Sources: <current Shape, preview, Context, Evidence table; exact style policy>
- Success: <human agreement on the named text; separate final evidence gates>
- Review: <initial 1–3 paragraph window; not a separate Run per window>

## v001/s001-input.md

```text
Run: <run>
Version: v001
Step: s001
Source: <chat/message id if available; otherwise not supplied>
Reviewed output: <prior vNNN/sNNN-result.md or initial state>
Mode: local-edit | paragraph-rewrite | structure
Scope: <exact editable targets; proposed extra work kept separate>
Base: <source paths and hashes immediately before edits>
Protected: <accepted and other out-of-scope targets + saved text/hash>
```

### Reviewed baseline

<For the first edit of existing prose, preserve the full selected paragraphs
and affected planning text here. Later Steps may cite the immutable earlier
result containing that exact text. A hash of a mutable file alone is not a
recoverable baseline. Record any external edit before rebasing onto it.>

### Original request

```text
<verbatim human message, including its reasons>
```

### Feedback F01

- Target: <C.P.B / paragraph / Mermaid node>
- Selected quote: <verbatim; explicitly absent if none>
- Source Version/Step: <exact identity or unresolved>
- Human comment: <verbatim, retaining informal wording>
- Agent interpretation: <separate bounded action; never replaces the comment>

Repeat for every item; preserve original annotation indices when supplied.
If there is no itemized feedback, write `Initial brief; no annotation items`.

## v001/s001-result.md

```text
Run: <run>
Version: v001
Step: s001
Input: s001-input.md · <SHA-256>
Source after save: <current paths and hashes>
State: waiting-for-feedback
```

### C1.P1

<Complete saved candidate paragraph, including unchanged sentences. Preserve
canonical evidence placeholders in this historical record; chat uses the
same reader projection as the live Workspace. Do not save only the diff.>

### C1.P2

<Complete second paragraph, only when in the requested review window.>

### Changes

| Feedback | Disposition | Target | Change and reason |
|---|---|---|---|
| F01 | applied / partly-applied / needs-decision / not-applied | <address> | <what changed and why; no inferred acceptance> |

### Planning snapshot

<Exact affected Bullet/Evidence contract text; typed Item ids and Supporting/
Local Run references. Include before/after for changed planning text so a later
session can recover the decision. Cite unchanged source identity instead of
copying unrelated inventories. Include the Mermaid source if changed; else
reference the earlier Step carrying the current map.>

### Checks

- Saved prose read back: <match / discrepancy>
- Sentence/Bullet and evidence boundaries: <findings>
- Protected/out-of-scope text: <before/after identity; unchanged or conflict>
- Human acceptance: <none, or exact scoped quote + actor + reviewed identity>
- Dependencies: <evidence owed, background Run ids, stale export, next question>

## working.md

```text
Run: <run>
Current: v001/s001
State: waiting-for-feedback
Review window: <targets>
Latest input/result: <paths>
Effective decisions: <rulings with source Step references>
Accepted targets: <target → exact Step/text hash → human quote/source>
Open feedback: <ids; agent-applied is not human-accepted>
Next: <what the human/agent does next>
```

## v001/close.md · create only on explicit closure

- Human close: <exact words, who, source; scoped to this writing episode>
- Accepted output: <full final passage/map and accepted target identities>
- Planning/evidence snapshot: <Step references>
- Outstanding evidence/export: <explicit; writing-agreed is not published>
- Sealed records: <each v001 input/result path and actual SHA-256>
- Continuation: <next Version starts here, never edits these records>

## runtime.yaml · current projection, not human-decision authority

```yaml
run: <owner-native-run>
family: page
operation: interactive-writing
interaction: human-feedback
target: C1.P1, C1.P2
ticket: <Run path>
result: <resolved Result path>
status: waiting-for-feedback
version: v001
step: s001
inputs:
  - path: <current input record path>
    sha256: <actual SHA-256>
worker:
  kind: skill
  name: haipipe-writing
started_at: <actual timestamp or null if unavailable>
finished_at: null
supersedes: null
failure: null
```

The mutable `working.md` and derived root `runtime.yaml` are not part of the
sealed Version. A future correction/acceptance must be a new record, never a
retroactive edit to a completed Step.
