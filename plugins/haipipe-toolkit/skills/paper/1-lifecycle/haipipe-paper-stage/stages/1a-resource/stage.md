---
# CONTRACT — machine-readable. No `name:` field: this is DATA the router reads,
# not a registered skill.
key: resource
order: "1a"
title: Resource
one_line: "Does what this paper needs EXIST, and can it CARRY the claim?"

phases: [draft, probe, revise, check]
probe_depth: 0             # THE CEILING on what PROBE may dispatch, on the bank's own ladder
                           # (task/haipipe-task/fn/qa.md:102-107), which maps 1:1 onto the
                           # consumer's `bank:` verdict:
                           #   0 READ        reuse  results already answer it   free, nothing runs
                           #   1 NEW RUN     run    old script, new config      costs
                           #   2 NEW SCRIPT  code   must write new code         costs
                           #   3 NEW FOLDER  new    open a new task-folder      costs most
                           # Rule: dispatch when depth(bank) <= probe_depth, else DEFER.
                           # At 0 the stage can only HARVEST, so a run of it is free and needs
                           # no gate. Raise it per invocation with `probe --depth N`.
runs: once
needs_paper: true
venue_free: true          # does not change when retargeting to another journal

artifact: 0-lifecycle/1a-resource/1a-resource.md
log: 0-lifecycle/1a-resource/_LOG_1a-resource.md
probes: 1-probes/PPNN_<topic>.md
template: template.md

exit_when: "GATE 1 (approve the questions + the SPEND), GATE 2 (exit)"

gates:                    # TWO human stops, per JL ruling; the agent self-advances past neither
  gate_1: "after DRAFT — the human approves WHICH questions get asked AND authorizes the SPEND
           on every BUILD row, per row: build it · cut it · authorize a cross-project reuse.
           Logged `[GATE] draft-review: approved` + `[GATE] spend-authorized: …`, quoting the user.
           A declined Q is LOGGED in the _LOG, never deleted."
  gate_2: "at CHECK — the exit. Picks one of `exits:` below."

exits:                    # THREE, not the usual two — see the craft body
  proceed: "-> claims — every H<n> has a HAVE+FIT resource, a COMMISSIONED acquisition, or a stated cut"
  reseed:  "[LOOPBACK -> SEED] — every hypothesis's resource is unobtainable; the paper cannot be
            written as seeded. 🔥 moves back to seed; 🚀 stays at the frontier."
  park:    "maturity: resource-blocked — the demand is real, the resource is in flight or behind a DUA"

sections:                 # in order; both must carry real content
  - Resource Description
  - Q-consumer

keyed_on: "H<n> — never C<n>; claim ids do not exist yet at resource time"

formatting:
  title_rule: "====="
  section_rule: "-----"
  headings: "`## Resource <n> · <name>` with `### <topic>` sub-topics, closing on `### Serves & carries`;
             `## Q-Resource-<n> · <title>` in the Q-consumer"
  line_breaks: "one sentence per line (semantic line breaks); no dense paragraphs"

q_id_pattern: "## Q-Resource-<n> · <title>"
q_anchor: "[Q-Resource-<n>] cited inline in the `### Serves & carries` (or topic) line it tests"
closed_when: "PROBE writes the Answer from the answering QA file — existence AND fitness AND what it
              KILLS, carrying [source: PP<NN>]. The bracket STAYS; a ledger keeps its questions."

probe_lanes:              # what a Q costs to answer
  scan:  "minutes — a store scan, a capability grep, an access-rung check. Cheap; ask freely."
  build: "an acquisition — a DUA, a pipeline, a labeling run; cost in calendar-months or GPU-weeks.
          Nothing in this lane dispatches before `[GATE] spend-authorized` exists in the _LOG."
build_requires: "`cross-project:` on every BUILD question — a sibling-project path or `none-found`.
                 Empty is a FAIL: it makes the gate authorize spend blind."

done_criteria:
  - "both sections filled with real content; every <!-- RULE --> comment deleted"
  - "every `## Resource <n>` closes with a `### Serves & carries` naming its H<n> and whether it
     carries them — or, if it cannot, what that KILLS"
  - "every hypothesis has a resource that is HAVE+FIT, or a COMMISSIONED acquisition with an OWNER
     and a DATE, or a SCOPE CUT the human said out loud"
  - "every question is a `## Q-Resource-<n>` block, cited inline in the line it tests"
  - "no woolly Answer — 'probably fine' is a DEFECT; the Answer names existence, fitness, and the kill"
  - "every BUILD question carries `cross-project:` (path or `none-found`)"
  - "`[GATE] spend-authorized` in the _LOG before any BUILD dispatched (or `n/a -- no BUILD questions`)"
  - "_LOG entry records the current state"
  - "check-probe-cards.sh <paper_root> --stage resource exits 0"

upstream: [seed]
downstream: [claims]
handoff: "on CHECK confirm, update STATUS.md (current_layer, maturity: resource) -> claims"
---

Resource — the craft
====================

Resource is INVENTORY + FEASIBILITY. It settles whether what this paper needs already EXISTS and
whether it can CARRY the claim, and it stops there.

The boundary with the stage after it:

```text
does the DATA exist, and can this corpus carry the claim?          -> RESOURCE
is there a reusable model / backbone / producing-CODE we can use?  -> RESOURCE
train THIS paper's model (fit) and evaluate it -> the verdict      -> CLAIMS
```

The edge-case test is one question: **is this the thing the paper is claiming about?** A reusable
dataset, backbone, or repo is an INGREDIENT and belongs here; the model whose result the paper IS
about gets trained and evaluated in claims. Resource may still COMMISSION a missing dataset — data
is an ingredient — but never the claim's model-training, which is the experiment. This is what keeps
a null interpretable: resource rules out "this corpus can't carry the claim" up front, so when claims
finally evaluates, a null means the effect is ABSENT, not that the ingredients were wrong.

Two axes, three ways to get each
--------------------------------

Everything the draft raises sits on one of two axes, and each asks the same three-way question:
do we HAVE it, can we GET it, or must we BUILD it?

```text
                   📊 DATA                            🧠 ALGORITHM
                   ────────────────────────────       ────────────────────────────
🗄️ HAVE            Which store holds it? Name the     Which checkpoint or repo exists,
                   path, the producing pipeline,      and has it actually RUN on
                   and which years/cohorts ran.       anything like our data?

🌐 GET (outside)   A public dataset covering this     A published method or released
                   — named, licensed, obtainable.     implementation we can adopt
                   Not "surely someone has this".     instead of writing one?

🔨 BUILD (ours)    Derive, label, simulate, join?     Develop it ourselves? Then it is
                   Then it is a TASK, and the         the paper's METHOD CONTRIBUTION,
                   question becomes what it costs.    not a resource — say so here.

🔗 linkability     Cuts across both: can the two sides be JOINED at the unit of
                   analysis? Name the key. Data that cannot be linked to the
                   outcome is not a resource.
```

NOT here: whether the evidence SUPPORTS a claim. Resource settles what we have, what we can get, and
what we must build; claims settles what it shows.

Ask freely; SPEND at the gate
-----------------------------

A SCAN is minutes, so the Q-consumer is as generous as the draft needs — raise every existence or
fitness question the description actually rests on. The BUILD lane is what is expensive, and bounding
it is the gate's whole job.

The human decides PER BUILD ROW, and needs three things in front of them: what the row BLOCKS
(`H<n>`), what it COSTS (pipeline-days, GPU-weeks, or a DUA whose cost is calendar-MONTHS and not
compute), and its `cross-project:` candidate. That candidate is why the field is mandatory — without
it the gate authorizes spend blind while the thing sits scaffolded one repo over. An agent may NAME a
sibling-project source; only the USER may CONSUME it. A scope cut taken here is free; the same cut
after claims costs a CLAIM, and after display it costs a FIGURE.

Say what it KILLS
-----------------

A resource that exists but cannot carry the claim it serves must say so in its `### Serves & carries`
line and in the answering Q's Answer — one sentence naming what that KILLS. "Probably fine" is a
DEFECT, not an answer. A BUILD question's Answer records COMMISSIONED · owner · eta · blocks `H<n>` ·
cross-project · what it yields **and what it does NOT fix**.

REVISE is usually skipped here, and that is correct: this is a ledger, not prose. Reach for it only to
sharpen a woolly Answer into one that says what it kills.

The stage that is allowed to say NO
-----------------------------------

Every other stage exits forward or re-opens a phase. Resource has three exits, because a stage whose
PURPOSE is discovering that the paper CANNOT BE WRITTEN must be able to say so. Without `reseed` and
`park` its only exit would be `proceed` — mechanically handing a DEAD PAPER FORWARD, the exact
failure this stage was built to end.

Keep them scoped: `park` is a WAIT (the demand is real, the resource in flight); `reseed` is a VERDICT
on the seed (NO hypothesis has an obtainable resource). One unobtainable row among several is neither
— that is a SCOPE CUT, logged in the human's own words.
