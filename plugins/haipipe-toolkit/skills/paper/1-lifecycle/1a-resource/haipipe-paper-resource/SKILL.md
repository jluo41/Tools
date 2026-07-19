---
name: haipipe-paper-resource
description: "The venue-FREE prerequisite stage (0-lifecycle/1a-resource/): does what this paper needs EXIST, and can it CARRY the claim? Two sections -- Resource Description (each resource described, keyed to H) + Q-consumer (uniform Q-Resource-<n>) -- covering data, checkpoints, and producing-code. Use for resource, prerequisite, do we have the data, does the checkpoint exist, can this corpus carry the claim, 1-resource."
argument-hint: "[paper-dir] [draft|probe|revise|check]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "2.3.0"
  last_updated: "2026-07-18"
  summary: "Resource stage (stage 1a, venue-FREE): do the paper's prerequisites EXIST and can they CARRY the claim? It is INVENTORY + FEASIBILITY, not the experiment -- training this paper's model and evaluating it is the CLAIMS stage's job. Two sections -- Resource Description + Q-consumer. The stage ASKS; the probe layer ROUTES. History: ./CHANGELOG.md."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-paper-resource
=============================

The **resource** stage sits between seed and claims, and it is venue-FREE.

It settles ONE thing: does what this paper needs already EXIST, and can it CARRY the claim?
It stops there.
It does **not** run the experiment — training this paper's model and evaluating it is the **claims** stage's job.

Read first: `../../../PHILOSOPHY.md`, `../../ref/04-lifecycle-map.md`, `../../ref/08-stage-gate.md`.


## What's special: inventory + feasibility, not the experiment

This is the one line that separates resource from claims:

```text
does the DATA exist, and can this corpus carry the claim?          -> RESOURCE
is there a reusable model / backbone / producing-CODE we can use?  -> RESOURCE
train THIS paper's model (fit) and evaluate it -> the verdict      -> CLAIMS
```

Resource checks that the ingredients EXIST and are FIT; it never trains the claim's model or runs an eval.
The test for an edge case is one question: *is this the thing the paper is claiming about?*
A reusable dataset, backbone, or code is an ingredient (resource); the model the paper's result IS about gets trained and evaluated in claims.

This is also what keeps a null interpretable: resource rules out "this corpus can't carry the claim" up front, so when claims finally trains and evaluates, a null means the effect is absent -- not that the ingredients were wrong.
(Resource may still commission a missing *dataset* -- data is an ingredient -- but the claim's model-training is the experiment, and the experiment is claims.)


## The four phases, in resource

```text
DRAFT   describe each resource the paper HAS -- one `## Resource <n>` (with `### topics` + a
        `### Serves & carries` naming its H<n> and whether it carries them) -- then write the
        Q-consumer (`## Q-Resource-<n>`) -- does each EXIST, and can it CARRY the claim it serves?
        cite each question inline in the `Serves & carries` line it tests, e.g. [Q-Resource-1].
PROBE   one worker call; each Q runs a lane --
          SCAN   minutes: a store scan / capability grep / access-rung check
          BUILD  a data acquisition (a DUA / pipeline, calendar-cost), behind the SPEND gate
        Routing mechanics are the probe layer's: see ../../../2-phase/1-probe/haipipe-paper-probe/SKILL.md
REVISE  usually skipped (this is a ledger); only sharpen a woolly A into one that says what it KILLS
CHECK   GATE 2 -- does every hypothesis have a resource that is HAVE+FIT, or a COMMISSIONED
        acquisition with an owner and a DATE, or a SCOPE CUT the human said out loud?
```

Two human gates: **GATE 1** approves which questions to ask (cheap -- a SCAN is minutes); **GATE 1b** fires only if a BUILD/acquisition exists, and authorizes the spend *after* the SCAN answers land -- informed by any `cross-project:` reuse candidate MATCH named (MATCH may name a sibling source; only the user consumes it).


## The artifact

`0-lifecycle/1a-resource/1a-resource.md`, two sections -- full skeleton + fill rules (inline `<!-- RULE -->` comments) in `ref/resource-template.md`; cross-stage template charter in `../../TEMPLATES.md`:

```text
Resource Description  one `## Resource <n>` (+ `### topics` + `### Serves & carries`, keyed on H<n>) -- what the paper HAS
Q-consumer            one `## Q-Resource-<n>` (Description/Reason/Answer) -- does it exist, and can it CARRY the claim?
```

A resource that exists but cannot carry the claim says so in its `### Serves & carries` (and in the answering Q's Answer), in one sentence naming what it KILLS.
Keyed on H<n>, not C<n> -- claim ids do not exist yet at resource time.


## Exits

```text
proceed  -> /haipipe-paper claims        every hypothesis has a fit resource, or a cut
reseed   -> /haipipe-paper seed          every hypothesis's resource is unobtainable -- can't be written as seeded
park     -> maturity: resource-blocked   real, but in flight / behind a DUA
```

End every reply with the stage strip (`../../../haipipe-paper/stage-strip.sh`); comment threads follow the Comment lifecycle section in `../../../haipipe-paper/SKILL.md`.
