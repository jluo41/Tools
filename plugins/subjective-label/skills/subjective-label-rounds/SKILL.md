---
name: subjective-label-rounds
description: >-
  The Labeling › Rounds view skill of the subjective-label family: it
  runs one calibration round: card, draw, weak pre-labels, the human's judgments by chat, measure and close. Every Run in this view names this skill, and no other view uses it.
  Use for starting a round, round card, round-prepare, labeling a round in chat, open_item, record_first, record_final, events.jsonl, resuming a round, measuring or closing a round, or /subjective-label-rounds.
metadata:
  version: "0.1.0"
  last_updated: "2026-09-29"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /subjective-label-rounds · Labeling Space › Rounds

This skill owns the Runs of the labeling workbench's Labeling › Rounds
view: every Run card there names it, and no other view uses it (JL 260929:
one skill per view). Load `subjective-label` (the family door),
`subjective-label-workflow` (the Run graph) and `label-building` (who decides what) first. Which Run
comes before and after these is in `label-building-workflow`.

## Runs in this view

```text
step  run                          state
 7    run-round-prepare        built · engine/calibration.py release_round (round 1 only)
 8    run-weak-prelabel        not built
 9    run-human-calibration    built · open_item, record_first, record_final
11    run-round-measure        not built
12    run-round-close          not built (no Checkpoint Keeper)
```

A Run is named `rlNN_<operation>_<target>` on disk and shown as
`run-<operation>-<target>` on the page. Its Ticket is `<Page>/runs/<run>.yaml`
and its Result `<Page>/results/<run>/`, beside `labeling/`.

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
checks one round's events sequence.

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
3. Write `evidence.md`: the versions of `G_(t-1)` and `D_(t-1)`, the pool, and
   the custody status; never a sealed-test id.
4. Before the first item is shown, write `prospect.md`: disagreement count per
   targeted cell, the rule the evidence is expected to force, and the audit-arm
   metric it should move. `result.md` at CLOSE is scored against it.

Engine, round 1: the same `release_round` call draws `n` ids at random from
the development pool, which is exactly the `corpus/items.jsonl` rows with
`population_status: eligible`. It refuses when the pool is smaller than `n`.
It writes, once each: `candidate_pool.jsonl` and `human_batch.jsonl` (seed and
inclusion probability `n / pool` on every row), `manifest.yaml` (policy
version, corpus, card, pool, and batch), `evidence.md`, `prospect.md` (round 1
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
talks the items through in chat; `Resume` on the round's `human-calibration`
Run in the Runs panel copies the text that starts or resumes that chat. The chat records
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
   `reveal.reference_observations` (`../label-building/ref/ref-config.md` §3a) and is marked
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
run             rlNN_human-calibration_round-NN
round_id        round_NN
item_id         the batch item
kind            show | first | lock | reveal | final
human_id        the identified human
session_id      the browser or CLI session
payload         show: prelabels_visible false
                first: class_label · diagnostic_region · uncertainty.level · rationale
                       · prelabels_visible false
                lock: the seq of the first event
                reveal: the comparison, marked not_gold
                final: class_label · diagnostic_region · uncertainty.level · rationale
                       · change_type · terminal_disposition (labeled | unresolved)
```

Writers take the lock file `sessions/.lock`. `verify_events` checks the sequence
and names every gap and missing field; a
round whose sequence fails does not complete its Run.

### MEASURE

After LEARN, allocate `round-measure`: compute audit-arm metrics separately from
challenge-arm metrics, coverage per register cell, and risk rows; write
`metrics.json`, `coverage.json`, and `risk_ledger.jsonl`.

### CLOSE

The Checkpoint Keeper, in order: completeness (every batch row has a typed
disposition), blinding (every seal precedes its first event), leakage (no
sealed id in the round), regression (accepted patches applied, flipped rows
recorded), coverage, risk. Then it promotes `D_t` and `G_t`,
writes `checkpoint.json`, appends `closed:` to `README.md`, settles the
targeted `register.md` cells, renders `view/judgments.md`, `view/rules.md`,
`view/result.md` (prospect vs actual, one line per gate), and records the
route: `another round`, `freeze`, or `HOLD`. A round with an unmet check does
not close; it stays `judged` with the failing check named.

## Return

Return the Run address or `none`, the files written, and exactly one next
runnable Run or named human gate.
