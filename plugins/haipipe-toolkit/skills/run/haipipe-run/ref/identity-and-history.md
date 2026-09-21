# Run identity, storage, and history

Read before allocating, retrying, reopening, or resolving a cross-owner Run.
The [catalogue](run-catalog.md) identifies the authoritative domain profile.

## Address and resolver

Use `(owner namespace/path, native Run id)` to identify a logical Run. Carry
the owner's global address where one exists; local `r01` alone is ambiguous.
A Result path/hash and any execution version travel with cross-Folder reuse.
Never rename a producer to match its consumer or copy/symlink its Result merely
to imitate a local dialect.

| Dialect | Authored Ticket | Generated Result / receipt |
|---|---|---|
| Folder-local executable | `<folder>/runs/<run>.sh` | `<folder>/results/<run>/runtime.yaml` |
| Current Job-backed Task | `<job>/<task>/runs/<run>.sh` | `$OUTPUT_ROOT/<task>/results/<run>/runtime.yaml` |
| Page interaction / delivery | `<page>/runs/<native-run>.md` | resolved `results/<native-run>/`; exact profile controls journals and build pointers |
| Design | `<design>/runs/rdNN_<operation>_<slug>.yaml` | `<design>/results/<same-stem>/runtime.yaml` |
| Labeling | `<job>/runs/rlNN_<operation>_<target>.yaml` | `<job>/results/<same-stem>/runtime.yaml`; domain artifacts referenced |
| Insight RI | `<instance>/runs/riNN_<slug>.yaml` | `<instance>/results/<ri>/vNNN/{input,runtime,result}.yaml` |

The current Task [runner contract](../../../task/haipipe-task/fn/run.md) and
[Ticket template](../../../task/haipipe-task/ref/run-sh-template.sh) resolve
`RESULT_STORE`, then the Job's `store:`, then the Job itself. In self-serving
mode the generated Task projection can physically lie under the Task Folder.
Older `$OUTPUT_ROOT/results/<task>/<run>` stores remain readable through their
recorded resolver; do not move historical output or guess from one path shape.
For a dispatcher-only `RESULT_STORE`, retain the exact resolved Result pointer
in durable owner/consumer records. A reader scanning only the Job's declared
store cannot rediscover an unrecorded one-off external destination; disclose
that inventory gap rather than claiming complete coverage.

Other extensions/storage layouts require an owner-declared deterministic
resolver. Scripts, config, notebooks and heavy external stores are supporting
projections only; their existence is conditional. A config file or bare output
directory is not proof of a commissioned Run. A Page DISPLAY unit may be the
renderer's direct, caller-authorized output destination; the governed Result
envelope records its path/hashes without a duplicate payload copy. Where a
consumer-serving Task profile permits this narrow Page-authority exception,
its `result.yaml` and `runtime.yaml` remain in the resolved Task Result store.

### Allocation

Check the owner's existing Tickets and receipts for collisions and compatible
work. Use its monotonic counter; never renumber. Generic slug text is lowercase
ASCII, but fixed dialect tokens such as Page `P01` and Scratch `C1.P1` retain
their required case. Do not normalize a valid native identity globally.

RP kind counters and RE kind counters are independent. Design's `rdNN` is
Folder-wide; Page's RD delivery ids belong to a different owner namespace.
RI, RL and Task R retain their own counters. Paper's current naming and its
historical `pm-/pa-/pr-/pj` adapters are controlled by
[Paper naming](../../../paper/haipipe-paper/ref/run-naming.md).

Planning candidates and reserved names stay outside actual inventory until
the owner authors the Ticket and receipt. A broken partial allocation remains
a recovery finding; do not hide it or manufacture the missing half.

## Reuse, attempts, and new commissions

Reuse a current accepted Result by exact identity/version/hash. Resume a
compatible open Run through its owner. Neither action allocates a duplicate.
A delegated retry may retain its Run id only while intent, target, frozen
inputs and acceptance remain unchanged. Preserve previous failure/attempt
records before dispatch; if the native runner cannot preserve them, use its
declared history adapter or report the gap before a destructive rerun.

A material contract change requires a new commission and identity. Use
`supersedes` only when the new work replaces the old target/result. Independent
datasets and separate questions are not automatically superseding lineages.
Published Results and closed history are immutable.

## Page interaction

Read the [interactive profile](../../../page/page-workflows/haipipe-page-workflow/ref/interactive-writing-run.md)
for concrete journals, working state and human closure.

- Structure `rp-struct-01` combines SHAPE and SURVEY; participants share that
  commission. Its accepted Mermaid structure and Page-global P index precede
  Section/paragraph writing allocations.
- Scratch can be commissioned against the selected Outline's Section or
  paragraph group before Structure closes. It does not satisfy that gate.
- Feedback within a fixed goal appends a Step. Same-goal reopening appends a
  Version. An open Version is append-only; closed Version records are immutable.
- A changed goal/target requires a new Run. A later independently commissioned
  Section session also receives the next `rp-sec-NN` under the Page profile.
- Paragraph groups can share one commission only when accepted together. An
  N-paragraph Page can have K bounded writing groups, with `1 <= K <= N`;
  allocation follows commissioned work, not every paragraph automatically.
- Waiting for feedback is ordinary work state. Scoped human acceptance does
  not prove evidence ready or close whole-Page CHECK.

`SELF`, `NEW_VERSION`, `CLOSE`, `NEW_RUN` and any declared HOLD route follow
the native profile. A session restart resumes compatible work. Neither a
participant, feedback turn, sentence, nor Version creates a child Run.
Delegated paragraph-writing uses its separate profile and acceptance contract.

## Insight binding and execution version

The [Insight item contract](../../../task/page-types/haipipe-page-insight/ref/instance-items.md)
owns one immutable `riNN` binding to a base R Ticket/hash plus frozen
research data, question, target and acceptance. Cross-owner evidence uses:

```text
logical binding: <instance>#riNN_<slug>
exact execution: <instance>#riNN_<slug>@vNNN
```

A new dataset, base R, question, target or acceptance creates a new RI.
Unchanged-input retry appends attempts to the same version; a corrected or
newly reviewed publication may use the next version under the unchanged RI.
Independent datasets never supersede one another. Preserve the base R.

Count logical RI bindings once in Run inventory; expand versions only in an
explicit execution-history view with its own count. Always pin the exact
execution version/hash when consuming evidence. A base recipe is not another
executed Run merely because RI references it. Separately commissioned upstream
production has its own native receipt and is counted separately.
Read [Task calls](../../../task/page-types/haipipe-page-insight/ref/task-calls.md)
for actual recipe invocation/isolation support; a contract does not create an
unimplemented input override.

## Projections and compatibility

A Supporting Run is a producer viewed by a consumer, not another family
allocation. RE/RD aliases and native Tickets can identify one execution; group
those aliases by owner identity. RE can also perform a distinct local evidence
transformation over separately commissioned supporting production.

Keep historical schemas/ids readable via their owner adapters. Do not promote
old naming examples to new allocation rules or rewrite their stored family
based on the prefix. Missing ownership or closure is an explicit finding.
