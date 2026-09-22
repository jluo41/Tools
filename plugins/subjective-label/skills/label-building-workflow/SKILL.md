---
name: label-building-workflow
description: >-
  The Building Run Spec guide for the subjective-label Workflow: describes
  operation order, item-level resume, and Run receipts for contract setup,
  calibration, and handoff. P0-P2 are compatibility capability tags, not
  lifecycle owners. The shared Workflow Definition owns the Run graph and
  Routes; this guide owns no semantic law, gate authority, or separate
  frontier. Use when setting up a new labeling job or running or resuming a
  calibration round, opening a round card, resuming a Session, closing a
  checkpoint, or /label-building-workflow.
metadata:
  version: "0.10.0"
  last_updated: "2026-09-20"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /label-building-workflow · Building Run Specs and internal steps

When a request says “two labels,” ask whether that means two class values for
one construct (one job, with both values in its schema) or two separate
constructs (one job per construct). Do not infer which they mean. Before using
a real corpus, do a scratch-workspace check with synthetic rows. There is no
non-writing `--dry-run` command: `fence_source.py` and `job.py create` write
artifacts, while `job.py status` is read-only. For the scratch check, create a
temporary Page Markdown file in the temporary workspace because `create`
requires an existing Page file and writes `<page-folder>/labeling/` plus a
Run/Result. Remove the whole scratch workspace, including that Page and the
Run/Result, after checking `status`; do not put scratch artifacts in a real
Page folder.

Load `subjective-label` (family), `subjective-label-workflow` (the Run Spec
graph and Routes), and `label-building` (semantic authority and restrictions)
first. **A Workflow is a list of Runs.** The operation names below are Run
Types used by the shared Workflow's Run Specs. This file describes their
Building-side prerequisites and internal Steps; the source Run Spec owns its
commission, actor, entry/exit gates, Route, and completion rule. P0-P2 are
compatibility capability tags only and do not create an independent frontier.

## Run allocation

Read `../../ref/ref-run.md` before allocating. This machine may allocate:

```text
P0 (compat tag)  corpus-contract · discovery-search* · guideline-seed · test-reserve · embedding-build
P1 (compat tag)  round-prepare · weak-prelabel* · human-calibration · guideline-learn
    · round-measure · round-close
P2 (compat tag)  handoff-freeze
```

Write each Ticket to `runs/<RUNNAME>.yaml` and its runtime/Result envelope to
`results/<RUNNAME>/`. Point the Result at the canonical domain files named
below; never copy them. One round folder is an episode, not a Run. While its
Card is merely proposed, it has no allocated `round-prepare` Run. Card release
commissions that operation; subsequent operations allocate only when their own
inputs freeze. Work exactly one non-parallel operation per dispatch.

## Contract operations · P0 compatibility tag

```text
pre-job      build the fenced source                             → engine/fence_source.py, no Run
first Run    import fenced corpus, initial policy, reservation  → corpus-contract
optional    bounded external-evidence query, if commissioned   → discovery-search*
optional    revise the inspectable policy, if commissioned     → guideline-seed
optional    supersede the sealed frame under custody           → test-reserve
optional    embed one corpus × embedder, when commissioned      → embedding-build
entry gate  configured semantic authority explicitly attests → G0 evidence; no gate Run
```

G0 is the entry predicate for commissioning `round-prepare` in the shared
Workflow graph; it is not a phase-owned gate Run. The five P0 authority files
are `config.yaml`, `corpus/manifest.json`, `test/sealed/status.json`,
`register.md`, and `policy/versions/G_00/manifest.yaml`. A complete,
integrity-valid `corpus-contract` Result with valid human authority but no
meaning receipt is G0-pending, not `HOLD`: the identified human owes the
confirmation. Missing or invalid P0 files, checksum failure, or invalid human
authority requires repair or `HOLD` before any dependent work proceeds.

At the Workflow Runtime level, record the human's G0 control in
`resource_controls`, referencing the completed `corpus-contract` Result and
the five authority files. The current engine persists the attestation and G0
receipt in `config.yaml` and `gates/g0/receipt.json`; these are storage details,
not a new Run or a reason to rewrite the closed Result. Optional discovery,
policy revision, and frame-supersession Specs may run only when separately
commissioned; they are not prerequisites when the contract Result already
contains valid initial policy and reservation artifacts. `embedding-build` is
also separately commissioned and may run once the P0 files pass integrity and
the job is not on HOLD; it does not depend on G0. Skip every uncommissioned
Spec. Discovery and embeddings are provenance, not gate inputs. A changed
corpus checksum creates a new job; a materially changed query, seed,
reservation frame, or embedder receives a new Run only under the owner
contract.

The fenced source that `create` imports is built by `engine/fence_source.py`.
A fenced source is a corpus snapshot whose sealed test is reserved before any
development read. The tool does the test-reserve work before the job exists,
so it allocates no Run; the reservation reaches the job inside
`corpus-contract`. It draws the sealed ids with a declared seed, optionally
stratified evenly by one item-level field read from a side JSONL (a field with
two values for one item is refused). It requires a non-empty value in the
configured `corpus.text_field`, computes `text_hash` from that field, and
canonicalizes the configured source ID as `item_id`. Only eligible rows are
written to `corpus/items.jsonl`; sealed text is omitted from both the fenced
source and imported Page corpus. The public corpus manifest records counts,
while `test/sealed/manifest.protected.jsonl` contains sealed IDs and hashes
only. The custodian retains any raw source separately; the engine does not
provide a sealed-text release reader. `test/sealed/status.json` records the
custodian, frame rule, seed, strata, checksum, and access policy. The tool
renders G_00 `guideline.md` and `cheatsheet.md` from the config meanings (see
`../../ref/ref-config.md` §3a). Like `create`, it is additive: an existing
different file is refused.

```bash
# Run from the repository root.
python3 plugins/subjective-label/engine/fence_source.py \
  --items <items.jsonl> --config <config.seed.yaml> --out <fenced-source> \
  --sealed-n <n> --seed <seed> --custodian <human> \
  [--stratify-jsonl <rows.jsonl> --stratify-field <field>]
```

Historical example: `S-Label-4-dices-unsafe-response` (DICES-350, target
`unsafe_response`) sealed 50 of 350 items, stratified by `safety_gold`, and
left 300 development items. That external example corpus is not bundled in
this repository; use the real local path supplied for the current project.

The canonical technical entry is `engine/job.py create`. It imports one
already-fenced corpus snapshot and its opaque sealed-test reservation into the
Page's direct `labeling/` lane, writes the five P0 artifacts through an
additive/idempotent writer, and leaves `authority.meaning_confirmed: false`.
It hashes and byte-copies the protected manifest as an opaque payload, but
never parses, prints, or renders it; it never copies a historical round, proxy
judgment, or model-derived gold. `engine/job.py status` rehashes the corpus,
opaque reservation, policy components, and P0 receipt without writing. It
never raises on a bad or unreadable file; it lists each defect in
`integrity_errors`. It reports `hold` and `hold_reason` from
`authority_hold(config)`, the one HOLD rule every host uses. It always anchors
on the immutable P0 receipt, and it checks that the G0 receipt binds the
current five P0 files, so editing a P0 file after G0 is caught. It refuses a
policy component name outside `POLICY_COMPONENTS` and any symlinked authority
file. A differing existing artifact is a hard refusal, not an overwrite. The
created `corpus-contract` Run is the first native Run. Its Result does not make
`round-prepare` eligible until G0 evidence from the identified human is valid
and bound to the current files; mere file presence or a bare boolean does not
satisfy that gate. A valid confirmation needs the human's receipt in
`config.yaml`.

`authority_hold(config)` is true for simulation/proxy authority, imported
source labels without a locally appointed human, a missing human id, or any
mode except `single_human_semantic_authority` with
`creates_human_gold: true`. With valid authority and intact P0 files, an
absent meaning receipt and G0 receipt is the expected pending-confirmation
state: `status` names explicit caller attestation as `next_action`, not
`HOLD`. The confirmation API checks that the caller-supplied id matches the
configured semantic authority and refuses on HOLD or P0 integrity failure;
the CLI and local Board do not authenticate the caller's identity. If semantic confirmation exists but its G0 receipt is
missing, invalid, or no longer binds the current files, status reports an
integrity defect and `round-prepare` remains ineligible. Repeating confirmation
can write a missing G0 receipt. A prior bound receipt can be upgraded only
when its existing G0 receipt still verifies; the old receipt is archived by
checksum before replacement. Corrupt or unverified receipts are never
overwritten.

`create` intentionally leaves `cache/embeddings/` empty. `embedding-build` is
an explicit non-gating operation because choosing or invoking an embedding
model is a separate execution decision; the scaffold API never makes a
network/model call implicitly.

`embedding-build` runs only when a person asks for it: the identified human presses
`Run embedding` in `Data → Embedding`, or names themselves with `--started-by`
on the command line. No agent starts a build on its own, not even when the job
has no embedding yet; the CLI refuses a build without `--started-by`, and the
Ticket and manifest record who asked and how (`started_by`).

The `embedding-build` action is `engine/embedding_build.py build`. It embeds every
`population_status: eligible` item once and never reads a sealed row into the
model. Each input is the response, a blank line, then the context, so a
word-piece cut only ever drops the end of the context. It writes
`cache/embeddings/<version>/` (`manifest.json`, `vectors.npy`, `rows.jsonl`,
`map.jsonl`, `groups.json`) and one `rlNN_embedding-build_<version>` Run,
where `<version>` is the model name in lower case. The embedder choice lives on
the Ticket, so `config.yaml` is never edited. Because a vector sets no label,
the build is not gated on G0; it refuses only a HOLD job or P0 files that do
not verify. Rerunning with the same model and corpus is a no-op. The retrieval
subcommands in `engine/embed.py` (`nearest`, `stratify`, `project`) keep their
G0 guard. The Board shows the result in `Data → Embedding`, where the person
also chooses the model: `CATALOG` in `embedding_build.py` lists the open-weight
models allowed, `--device auto` picks cuda, then mps, then cpu, and the 4B and
8B Qwen3 models load in bfloat16. Each model is its own `<version>` folder and
its own Run, so a second model never changes the first. A person may also set
`--input` (`reply_context`, `reply`, `context`), `--instruction` (Qwen3 and
e5-instruct only), `--groups` (2-20), `--map` (`tsne`, `pca`), and `--seed`.
Each non-default setting adds a tag to `<version>`, for example
`qwen3-embedding-0-6b-reply-only-instr-d30f16-k5-pca-seed3`, so every setting
combination is its own folder and Run. Every build also writes `map3d.jsonl`
for the rotating view; `embedding_build.py map3d` adds it to an older build
without touching its vectors.

```bash
python3 plugins/subjective-label/engine/embedding_build.py build \
  --job-root <page-folder>/labeling --started-by <the person who asked> \
  --model Qwen/Qwen3-Embedding-0.6B
```

`engine/job.py create` writes the P0 domain scaffold and allocates exactly one
completed `rlNN_corpus-contract_*` Ticket/runtime/Result envelope. It does not
speculatively allocate the optional or later operations above. Do not count
historical scaffold files as Runs; `engine/run_catalog.py plan` remains a
truthful planning tool for operations that have not been commissioned.

`create` is idempotent only while the P0 scaffold is unchanged. After the
human-confirmation action legitimately changes `config.yaml`, rerunning
`create` must refuse rather than roll the job backward; use `status` or resume
the phase API instead.

The create call must name the real Page source file; the API resolves it and
accepts only `<page-file.parent>/labeling` as `--job-root`. It refuses a
detached same-basename folder. The incoming sealed status must already carry a
valid custodian, frame, exclusion access policy, invalidation state, and the
matching opaque-manifest checksum. The P0 receipt binds all five authority
artifacts by checksum, and `status` rehashes each of them.

```bash
# Run from the repository root.
python3 plugins/subjective-label/engine/job.py create \
  --source-job <fenced-source> \
  --page-file <page-home>/<page>.md \
  --job-root <page-home>/labeling \
  --job-id <id> --target <target> --human-id <human>
```

The read-only status invocation is exact and requires no Page-file argument:

```bash
python3 plugins/subjective-label/engine/job.py status \
  --job-root <page-home>/labeling
```

Human confirmation is a separate explicit caller attestation; never infer it
from chat or flip a boolean by hand. `--attest-as-human` records the caller's
claim to be the configured human; neither the CLI nor the Board authenticates
that identity. Do not treat this receipt as identity proof in a multi-user or
adversarial environment. `--accept-current-schema` means the caller confirms
the current construct, class schema, seven regions,
uncertainty/unresolved disposition, and G_00 manifest. `confirm` binds those
semantics in `authority.meaning_receipt`, rewrites `config.yaml` only from the
exact P0 receipt checksum, and writes `gates/g0/receipt.json` binding the final
five artifacts. It is idempotent. Without both semantic and G0 receipts,
the compatibility status remains P0. The G0 receipt must declare the canonical schema,
`status: passed`, the same identified human, and the exact semantic-receipt
checksum; presence alone never passes the gate.

```bash
python3 plugins/subjective-label/engine/job.py confirm \
  --page-file <page-home>/<page>.md \
  --job-root <page-home>/labeling \
  --human-id <human> --accept-current-schema --attest-as-human
```

The Board Labeling screen is a second confirmation channel:
`Data → Contract → Confirm meaning`, after the caller ticks the attestation
box and accepts the browser confirmation dialog. The receipt explicitly says
`identity_assurance: caller_attested_not_authenticated`; the Board origin check
reduces cross-origin writes but does not authenticate the caller. Both channels
refuse before writing a byte when the submitted id differs from the configured
id, when the job is on HOLD, or when P0 integrity fails. The
door's own checks are in
`haipipe-workbench-labeling/SKILL.md` §Write and authority law.

## Calibration Run Specs · P1 compatibility tag

```text
CARD      round card proposed → a person releases it            card.md
PREPARE   pool → batch → evidence → prospect                     round-prepare
                                                                manifest.yaml · candidate_pool.jsonl
                                                                human_batch.jsonl · prelabels/<executor>.jsonl
PRELABEL  each weak executor, independently and sealed          weak-prelabel*
JUDGE     per item: show → first record → lock → reveal → final human-calibration
                                                                sessions/ (append-only events)
                                                                human_final.jsonl
LEARN     propose patches → backward impact → human ruling      guideline-learn · policy_draft/
MEASURE   metrics → coverage → risk                              round-measure
                                                                metrics.json · coverage.json · risk_ledger.jsonl
CLOSE     Checkpoint Keeper verifies → promotes → routes        round-close
                                                                checkpoint.json · README.md closed:
                                                                policy/versions/G_<t>/ · gold/cumulative.jsonl
                                                                register.md cells settled · view/
```

### What the engine builds today

`engine/calibration.py` is the P1 writer. It builds three steps, for round_01
only:

```text
step      engine call or missing Run    state
CARD      release_round    built · round_01 only
PREPARE   release_round    built · random development draw only
PRELABEL  none             not built (round 1 needs none)
JUDGE     open_item · record_first · record_final · verify_events    built
LEARN     guideline-learn  not built
MEASURE   round-measure    not built
CLOSE     round-close      not built (no Checkpoint Keeper)
round 2+  release_round    refuses
```

So the machine stops after JUDGE. When every batch row of round_01 has a
`final`, the round state is `judged` and the next step is guideline-learn,
round-measure, and round-close. None of them has an engine, so this is a named
stop: report the missing owner (the Checkpoint Keeper) as `HOLD`, per
`label-building`, with the frontier preserved. Nothing promotes gold:
`gold/cumulative.jsonl` stays empty and `policy/current` stays `G_00`.
`release_round` refuses a second round until a checkpoint exists, and even then
refuses, because only round_01's random draw is built.

Two read-only helpers: `state` derives every round's state, and `verify`
rehashes one round's events chain.

```bash
python3 plugins/subjective-label/engine/calibration.py state \
  --job-root <page-home>/labeling
python3 plugins/subjective-label/engine/calibration.py verify \
  --job-root <page-home>/labeling --round round_01
```

### CARD

`card.md` is the folder's first file. It names the register cell(s) the round
targets, the two arms (challenge n, audit n), the seed, and the expected
finding. Round 1's card names no cell: its arm is one random development draw.
Nothing else may exist in the folder while `state: proposed`. A person flips
it to `released:`; the machine never does. On that release, allocate the next
job-wide `round-prepare` address and write its Ticket/runtime envelope before
PREPARE begins. Do not allocate the later episode Runs early.

In the engine, `release_round` IS the release. It requires the configured
authority id after G0 and not at HOLD (the Board button is
`Labeling → Rounds → Start round 1`). It writes `card.md` already at
`state: released`, with `released_by`, `released_at`, `channel`, `policy`,
`arm: random development draw`, `n`, and `seed`. The engine never writes a
`proposed` card. Batch size `n` must be 1 to 200; it defaults to config
`rounds.round1.human_batch_size` (else 20), and the seed to
`rounds.round1.seed` (else 42).

### PREPARE

1. Round 1: draw the declared random sample from the development pool.
   Later rounds: retrieve a candidate pool around the targeted cells, novelty,
   sparse coverage, risk, and unresolved items, with a selection reason per row.
2. Compose the batch from the card's arms; freeze membership, role, stratum,
   inclusion probability, seed, and blind-access state in `human_batch.jsonl`.
3. Write `evidence.md`: the checksums of `G_(t-1)`, `D_(t-1)`, the pool, and
   the custody status; never a sealed-test id.
4. Before the first item is shown, write `prospect.md`: disagreement count per
   targeted cell, the rule the evidence is expected to force, and the audit-arm
   metric it should move. `result.md` at CLOSE is scored against it.

Engine, round 1: the same `release_round` call draws `n` ids at random from
the development pool, which is exactly the `corpus/items.jsonl` rows with
`population_status: eligible`. It refuses when the pool is smaller than `n`.
It writes, once each: `candidate_pool.jsonl` and `human_batch.jsonl` (seed and
inclusion probability `n / pool` on every row), `manifest.yaml` (policy,
corpus, card, pool, and batch checksums), `evidence.md`, `prospect.md` (round 1
has no forecast), `README.md` (`state: prepared`), an empty `sessions/`, and a
complete `rlNN_round-prepare_round-01` Run.

After `round-prepare` closes, allocate one `weak-prelabel` Run per registered
weak executor under `G_(t-1)`. Each writes its sealed
`prelabels/<executor>.jsonl` before any human-first event. Round 1 has none.

### JUDGE

Per item, in this order, each step its own appended event in
`sessions/events.jsonl`:

```text
show      item text + G_(t-1) cheatsheet; no prelabel, no selection reason that reveals one
first     class · region · uncertainty · evidence · rejected alternative
lock      immutable; a locked event is never replayed
reveal    sealed comparisons, structured, only after lock
final     the human's final decision + change type
          (none · correction · clarification · concept_revision · unresolved)
```

Resume rule: the open item is the first batch row with no `final` event; a
row with `lock` and no `final` resumes at `reveal`. A dead chat changes nothing
on disk.

**By chat** (JL 260918): the person reads the round in `Labeling → Rounds`
(the open round's item table: #, Item, Text, Group, State, Feedback; text appears
once the item has been shown, and the chat shows an item with `open_item`) and
talks the items through in chat; the view's `Copy chat prompt` button gives
the text that starts or resumes that chat. The chat records
only answers the person states: `record_first` for a first answer (then shows
the comparison), `record_final` for keep or change, and `add_feedback` for a
note about an item (`sessions/feedback.jsonl`, author human or model, never a
label). The model gives its own view of an item only after the person's first
answer for it is recorded.

Engine calls, each refused unless the caller supplies the configured semantic
authority id, the job is past G0, and it is not at HOLD. This id check is not
identity authentication:

1. `open_item` returns the resume item (or a named batch item) and appends one
   `show` event per session, only while the item has no `first`. The first
   call allocates `rlNN_human-calibration_round-01` with `status: running`.
2. `record_first` needs a `show` and no earlier `first`. It appends `first`,
   `lock`, and `reveal` in one call. The reveal payload comes from config
   `reveal.reference_observations` (`../../ref/ref-config.md` §3a) and is marked
   `not_gold: true`; with no such block it is `kind: none`.
3. `record_final` needs `lock` and `reveal` and no earlier `final`. A final
   whose class or region differs from the first needs a change type other than
   `none`. `unresolved` records no class. When every batch row has a `final`,
   it runs `verify_events`, writes `human_final.jsonl`, sets `README.md` to
   `state: judged`, and completes the Run.

A class that is not a config label value, a region outside the config regions,
or an uncertainty level outside the config levels is refused. An item that is
not in the frozen batch, or not `eligible`, is refused.

The events file shape (schema `subjective-label-calibration-event/v1`), one
JSON object per line, append-only:

```text
schema          subjective-label-calibration-event/v1
seq             1, 2, 3 … with no gap
at              timestamp with UTC offset
prev_checksum   the previous line's checksum (null on line 1)
checksum        sha256 of the canonical JSON of every other field (sorted keys, no spaces)
run             rlNN_human-calibration_round-NN
round_id        round_NN
item_id         the batch item
kind            show | first | lock | reveal | final
human_id        the identified human
session_id      the browser or CLI session
payload         show: prelabels_visible false
                first: class_label · diagnostic_region · uncertainty.level · rationale
                       · prelabels_visible false
                lock: first_checksum
                reveal: the comparison, marked not_gold
                final: class_label · diagnostic_region · uncertainty.level · rationale
                       · change_type · terminal_disposition (labeled | unresolved)
```

Writers take the lock file `sessions/.lock`. `verify_events` rehashes the chain
and names every sequence gap, broken chain link, and checksum mismatch; a
round whose chain fails does not complete its Run.

### LEARN

1. From accepted human evidence, draft the smallest general patch into
   `policy_draft/`, typed semantic / procedural / casebook / wrapper / editorial.
2. Compute backward impact: every prior gold row the patch would flip, into
   `policy_draft/regression.jsonl`.
3. Present each substantive patch with its impact for the human's ruling.
4. Close `guideline-learn` after every substantive patch has a human ruling.

Then allocate `round-measure`: compute audit-arm metrics separately from
challenge-arm metrics, coverage per register cell, and risk rows; write
`metrics.json`, `coverage.json`, and `risk_ledger.jsonl`.

### CLOSE

The Checkpoint Keeper, in order: completeness (every batch row has a typed
disposition), blinding (every seal precedes its first event), leakage (no
sealed id in the round), regression (accepted patches applied, flipped rows
recorded), coverage, risk, checksums. Then it promotes `D_t` and `G_t`,
writes `checkpoint.json`, appends `closed:` to `README.md`, settles the
targeted `register.md` cells, renders `view/judgments.md`, `view/rules.md`,
`view/result.md` (prospect vs actual, one line per gate), and records the
route: `another round`, `freeze`, or `HOLD`. A round with an unmet check does
not close; it stays `judged` with the failing check named.

## Handoff Run · P2 compatibility tag

```text
1 commission the `round-close` Route permits `handoff-freeze`
2 rehash     Label Handoff Keeper rehashes G* and D_cal*
3 custody    Test Custodian confirms protected ids never entered a round
4 sign       the human's signature naming exact checksums and lineage
5 write      handoff/label-v1.yaml, once, with its receipt block
6 close      validate the Result envelope and return to the family crossing
```

If step 1 fails, the source Run Routes to `round-prepare` or `HOLD` with the
failing predicate named. If
the Keeper or Custodian is absent, `label-building` §Ends at the handoff rules
`HOLD`; this machine stops at step 2 with the frontier preserved.

## Receipts this machine writes

```text
card.md released:        the person's release of the batch (before round-prepare)
runs/<RUNNAME>.yaml      one authored operation Ticket
results/<RUNNAME>/       runtime.yaml + safe result.yaml for that operation
sessions/events.jsonl    item-level, append-only, hash-chained, the resume source
human_final.jsonl        one row per batch item, written when the last final lands
checkpoint.json          the round receipt; the only artifact that promotes gold and policy
README.md closed:        keeper · date · route
handoff/label-v1.yaml    the handoff-freeze Result, written once by the Label Handoff Keeper;
                         its Run exit predicate carries the G3 compatibility label
```

## Return

Return the current Run address or `none`, Run Spec/operation, round episode and its
`state:`, the open item if any, the files written this Run, actual allocated
Run count, register cells still open, checkpoint route, and exactly one next
runnable Run Spec or named human gate.
