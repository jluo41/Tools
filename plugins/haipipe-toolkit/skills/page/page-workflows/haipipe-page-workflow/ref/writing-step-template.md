# Writing Run records · copy only the records needed now

Paths follow `interactive-writing-run.md` and the Folder owner's Run dialect.
Replace every placeholder with an actual value or explicit `not supplied`.
Record messages verbatim in fenced blocks; use a longer fence when the message
itself contains backticks. Do not invent a person, timestamp or message id.

## runs/<rp-struct-NN | rp-sec-NN | rp-para-NN_Pxx[-Pyy]>.md

```yaml
family: page
operation: interactive-writing
interaction: human-feedback
target: C1.P1, C1.P2
paragraphs: P01-P02
result: results/<same typed RP identity>
participants: [<stable human identities; omit when not supplied>]
coordinator: <stable identity or not supplied>
```

- Goal: <structure/Bullet, Section-level, or paragraph-level writing goal>
- RP kind: <rp-struct-NN | rp-sec-NN | rp-para-NN_Pxx[-Pyy]>
- Mermaid Structure description: <frozen paragraph job/reader move for each selected PNN; required for prose Runs>
- Page and Board: <resolved paths>
- Scope: <map, Section, paragraph/range; excluded and already accepted targets>
- Sources: <current Shape, preview, Context, Evidence table; exact style policy>
- Success: <structure/Bullet closure, completed Section draft/review/diagnose/revise Step, or human agreement on the fixed paragraph text>
- Review: <the exact fixed scope and its applicable Mermaid Structure descriptions>

For Section/Paragraph prose Runs only, add the shared Writing configuration:

```yaml
worker: haipipe-writing
writing:
  mode: revise                    # draft | revise | evaluate
  scope: paragraph                # section | paragraph | paragraph-group
  methods: []                     # explicit selected catalog ids/roles
  evaluation:
    rubric: haipipe-writing/base-v1
    max_revision_passes: 1
```

Resolve the actual target, baseline, plan/evidence, requirements and original
feedback using `../../../../writing/haipipe-writing/ref/writing-request.md`.
Freeze selected method entries/versions/hashes and rubric hash in this Ticket's
effective input packet; a Step references it and records any host-authorized
input change. Do not copy prose-worker fields into a pure Structure/Scratch Run.

## results/<run>/v001.md

One Version has one Markdown journal. Append Steps in order; do not create a
directory or separate input/result files for them.

```text
Run: <run>
Version: v001
State: open
Prior Version: none, or <closed vNNN.md · SHA-256>
```

## Step s001

A Step is a complete scoped cycle, not merely one chat turn. For a
Section-level Run, record the candidate draft, review/rating, diagnosis,
revision, and post-revision review/diagnosis before `### Saved result`.
Use `../../../../writing/haipipe-writing/ref/evaluation.md` for the compact
`#### Writing evaluation` record: actual candidate/hash, rubric, reviewer mode,
coverage, methods/status, criterion rows, initial/final findings, revision
budget and remaining issues. Store it in this Step's review before Saved result;
do not create per-evaluator files or Runs. If no revision is needed, record one
reviewed candidate without inventing a second pass. Acceptance/navigation-only
Steps record their disposition and do not re-review unchanged prose.

### Human feedback

```text
Source: <chat/message id if available; otherwise not supplied>
Reviewed output: <prior Step in this Version, closed prior Version, or initial state>
Mode: local-edit | paragraph-rewrite | structure
Scope: <exact editable targets; proposed extra work kept separate>
Base: <source paths and hashes immediately before edits>
Protected: <accepted and other out-of-scope targets + saved text/hash>
```

#### Reviewed baseline

<For the first edit of existing prose, preserve the full selected paragraphs
and affected planning text here. Later Steps may cite the immutable earlier
result containing that exact text. A hash of a mutable file alone is not a
recoverable baseline. Record any external edit before rebasing onto it.>

#### Original request

```text
<verbatim human message, including its reasons>
```

#### Feedback F01

- Target: <C.P.B / paragraph / Mermaid node>
- Selected quote: <verbatim; explicitly absent if none>
- Source Version/Step: <exact identity or unresolved>
- Human comment: <verbatim, retaining informal wording>
- Agent interpretation: <one bounded editing action; no preference analysis>

Repeat for every item; preserve original annotation indices when supplied.
If there is no itemized feedback, write `Initial brief; no annotation items`.

For `rp-struct-01`, add the people who actually contributed this Step without
creating a new Run:

```text
Contributors: <stable identities, or not supplied>
```

### Saved result

```text
Source after save: <current paths and hashes>
State: waiting-for-feedback
```

#### C1.P1

<Complete saved candidate paragraph, including unchanged sentences. Preserve
canonical evidence placeholders in this historical record; chat uses the
same reader projection as the live Workspace. Do not save only the diff.>

#### C1.P2

<Complete second paragraph, only when in the requested review window.>

#### Changes

| Feedback | Disposition | Target | Change and reason |
|---|---|---|---|
| F01 | applied / partly-applied / needs-decision / not-applied | <address> | <what changed and why; no inferred acceptance> |

#### Track changes

Use one card only for each material wording change. The `F01 · <change type>`
heading carries a short local edit label, so do not duplicate it in a separate
classification table. Store clean text only; the Runs presenter computes
word/punctuation-level red deletion and green insertion. Unchanged context
remains plain, and whole-sentence red/green is reserved for a whole-sentence
removal/addition. Omit this section when no text changed. An acceptance,
status, navigation, or presenter-only Step uses the ordinary `Changes` table
and creates no Track Changes card. In record-first mode, do not write a broad
preference inference here; use `Analysis status` to point to the deferred
post-run analysis Task.

##### F01 · <change type>

###### Before

<exact prior text>

###### After

<exact saved text>

###### Why

<why this edit answers the human feedback>

###### Analysis status

Deferred to post-run analysis after explicit Page Run closure.

#### Planning snapshot

<Exact affected Bullet/Evidence contract text; typed Item ids and Supporting/
Local Run references. Include before/after for changed planning text so a later
session can recover the decision. Cite unchanged source identity instead of
copying unrelated inventories. Include the Mermaid source if changed; else
reference the earlier Step carrying the current map.>

#### Checks

- Saved prose read back: <match / discrepancy>
- Sentence/Bullet and evidence boundaries: <findings>
- Protected/out-of-scope text: <before/after identity; unchanged or conflict>
- Human acceptance: <none, or exact scoped quote + actor + reviewed identity>
- Foreground surface: <Draft Space refreshed from the selected Outline; no Content/delivery write>
- Dependencies: <evidence owed, Task Run ids, delivery deferred to Page release, next question>
- Post-run analysis: <none while open; after explicit close, queued/running/complete Task Run id and input hash>

## Reader-facing response after the Step save

This response is rendered from the saved candidate; it is not another stored
prose authority. Separate every paragraph with a visible `### PNN · Cn.Pm`
heading and its own blockquote. Number every sentence for review, but never
write the labels into the candidate, Version result, or final Content.

```markdown
## ✍️ <rp-struct-NN | rp-sec-NN | rp-para-NN_Pxx[-Pyy]> · <vNNN/sNNN>

### P01 · <C.P> · <Mermaid Structure description>

> **S1** <first complete saved sentence>
>
> **S2** <second complete saved sentence>

### P02 · <C.P> · <Mermaid Structure description>

> **S3** <first complete saved sentence in the next paragraph>
>
> **S4** <second complete saved sentence in the next paragraph>

<One concise explanation of what changed and why. Use separate bullets only
when multiple feedback items require separate dispositions. Omit an Evidence
section when no citation, value, or figure requirement changed or remains open.>

[Draft Space](<verified direct URL>) · [Evidence Space](<verified direct URL>) · [Current Run](<verified Runs URL with &run=<exact-run-id>>)
```

Nothing follows the three links. `S1`, `S2`, ... restart for the displayed
review window and remain chat-only coordinates.

Each paragraph heading must use the description frozen by the closed Mermaid
Structure. Resolve it from the Page-local `P01..PN` index or the authored
Mermaid source; do not infer a replacement from the candidate prose.

## working.md

```text
Run: <run>
Current: v001/s001
State: waiting-for-feedback
Review window: <targets>
Latest Version/Step: <vNNN.md#step-sNNN>
Effective decisions: <rulings with source Step references>
Accepted targets: <target → exact Step/text hash → human quote/source>
Open feedback: <ids; agent-applied is not human-accepted>
Next: <what the human/agent does next>
```

## Version closure · the Page Run close event

Append this section to `v001.md` only when the person explicitly closes the
Page Run. A completed Section Step does not by itself close the Run. This
seals the Version before any post-run analysis Task is launched.

### Human close

<Exact words, who, and source; scoped to this writing episode.>

### Closure record

- Accepted output: <full final passage/map and accepted target identities>
- Planning/evidence snapshot: <settled Bullets plus each `none` or ready bound CITE/VALUE/DISPLAY Result>
- Evidence closure: <all ready and bound; otherwise do not close the Page Run>
- Delivery: deferred until all Page Runs and required evidence Task Results complete
- Post-run analysis: <one output-only Task Run reads the sealed Version hash; it does not block the next Page Run>
- Sealed scope: <all Step ids in this Version and external source hashes>
- Continuation: <v002.md starts from the closed v001.md hash; never edits v001.md>

## runtime.yaml · current projection, not human-decision authority

```yaml
run: <rp-struct-NN | rp-sec-NN | rp-para-NN_Pxx[-Pyy]>
family: page
operation: interactive-writing
interaction: human-feedback
target: C1.P1, C1.P2
paragraphs: P01-P02
ticket: <Run path>
result: <resolved Result path>
status: waiting-for-feedback
version: v001
step: s001
version_file: <Result path>/v001.md
version_sha256: <current actual SHA-256; update after each append>
worker:
  kind: skill
  name: haipipe-writing
started_at: <actual timestamp or null if unavailable>
finished_at: null
supersedes: null
failure: null
analysis:
  status: deferred
  task_run: null
  input_sha256: null
  result: null
```

The mutable `working.md` and derived root `runtime.yaml` are not part of the
sealed Version. While a Version is open, only append a new Step or complete the
current pending Step; never rewrite a completed Step. After Version closure,
the entire `vNNN.md` is immutable. A future correction/acceptance belongs in a
new Step or reopened Version, never a retroactive edit.
