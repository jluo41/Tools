---
name: haipipe-paper-claims
description: "The venue-FREE claim ledger (0-lifecycle/1b-claims/) -- THE ONLY home of a claim's status (supported | refuted | inconclusive + confidence + claim_type). It also RUNS THE EXPERIMENT: training this paper's model (fit) + evaluating it (eval) settles each claim; resource supplies the ingredients. Three sections -- Hypotheses, Claims, Q-consumer. Use for claim ledger, claims, supported/weak/GAP, blocked-on-resource, evidence plan, probes, model training, evaluate, 1-claims."
argument-hint: "[paper-dir] [--backfill <PPNN>] [--source <path>...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "5.2.0"
  last_updated: "2026-07-18"
  summary: "Claims stage (stage 1b, venue-FREE) -- the ONLY home of a claim's status (supported|refuted|inconclusive + confidence + claim_type, per-claim, private; no '## Verdict', no 'verdicted' state). It OWNS the experiment: train this paper's model (fit) + evaluate (eval) -> the verdict; resource supplies the ingredients (data/models/code), and a claim without them is BLOCKED-ON-RESOURCE. Three sections -- Hypotheses, Claims, Q-consumer. The PROBE phase raises questions as SECTIONS in 1-probes/ and runs the five-step loop; a section's a-consumer FEEDS this ledger. History: ./CHANGELOG.md."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-paper-claims
===========================

The **claims** stage is venue-FREE, and it settles the paper's argument.

It answers: which claims are supported, refuted, or inconclusive?
And it is the ONLY home of that status.

Read first: `../../../PHILOSOPHY.md`, `../../ref/04-lifecycle-map.md`, `../../../haipipe-paper/SKILL.md` (Delivery Need Routing).


## What's special: two things make claims claims

**1. It is the ONLY home of a claim's status.**
`supported | refuted | inconclusive` + confidence + claim_type live HERE, per-claim, private to this paper -- never in a probe file (there is no `## Verdict`, no `verdicted` state).
A probe section carries the evidence's MEANING for this paper (its `a-consumer:`); the judgment is ours to write.
Two papers reading the same bank fact may judge their own claims differently -- the fact is shared, the judgment is not.

**2. It runs the experiment.**
Training this paper's model and evaluating it is claims' work; resource only checked the ingredients exist.

```text
does the DATA / a reusable model / producing-CODE exist?   -> RESOURCE (ingredients)
train THIS paper's model (fit) + evaluate it (eval)         -> CLAIMS (the experiment -> the verdict)
```

Decompose the experiment -- one probe per task type, never a bundled fit+eval -- so a null is interpretable (a stalled fit does not force a rebuild; a null eval means the effect is absent, not that training failed).
The GPU-weeks SPEND gate lives here now.
A claim whose ingredients are not ready is `BLOCKED-ON-RESOURCE`: it cites the resource row it waits on (`-> N<n>` in 1a-resource.md) and gets no build probe here.


## The four phases, in claims

```text
DRAFT   read 1a-resource.md (what exists / what's BLOCKED-ON-RESOURCE), then list the hypotheses
        (H1, H2, H3), write the claims (short: statement + status + `Evidence: [Q-Claim-<n> …]`, the
        list that settles it), and the Q-consumer (each Q-Claim-<n> a SPECIFIC, answerable check;
        decompose a claim into several angles — fit/eval/robustness/placebo; a question may settle several claims)
PROBE   one worker call; the five-step loop dispatches the experiment (fit -> eval) to the
        task/discovery executors and COLLECTS -- the claim's status FLIPS here, numbers -> _VALUES_.
        Routing mechanics are the probe layer's: see ../../../2-phase/1-probe/haipipe-paper-probe/SKILL.md
REVISE  refine claim statements and evidence-plan clarity; each Answer feeds the status of every claim it settles
CHECK   every claim backed? every GAP has a plan and a question SECTION? every settled claim
        traced to a RESOLVING QA file? no aspirational anchors cited as evidence?
```

Claims RECEIVES evidence, never PRODUCES it inline (LAW 1): it raises questions; `haipipe-paper-probe` binds them.
Task settles an internal experimental claim; discovery supplies external cohorts/context/citations and never settles one alone.


## The artifact

`0-lifecycle/1b-claims/1b-claims.md`, three sections -- full skeleton + fill rules (inline `<!-- RULE -->` comments) in `ref/claims-template.md`; cross-stage charter in `../../TEMPLATES.md`:

```text
Hypotheses  what we test (H1, H2, H3), venue-neutral
Claims      one C<n>: statement + status + `Evidence: [Q-Claim-<n> …]` (the questions that settle it; thinking in Q-consumer)
Q-consumer  one `## Q-Claim-<n>` (Description/Reason/Answer): a SPECIFIC answerable check + which C<n>(s) it settles
```

Status is settled by the judgment fields, written at INTERPRET when a probe section's `a-consumer:` lands:
`status: supported | refuted | inconclusive` · `confidence` · `claim_type: associational | causal | in-sample | generalizing` (the author's own overclaim check -- never say "causes" from associational evidence, and keep in-sample-only evidence `weak` if the claim generalizes).

A claim is `supported` only via BOTH: stage 1, the cited file exists and the number appears in it; and stage 2, a probe section whose `target:` QA file RESOLVES on disk and whose `a-consumer:` says that number carries the claim.
Verified numbers live in `_VALUES_1b-claims.md`; citation candidates in `_CITATION_1b-claims.md`.


## Exits

```text
promote -> /haipipe-paper venue    pin the target journal (claims is venue-free; venue comes next)
promote -> /haipipe-paper pitch    if the venue is already pinned
```

End every reply with the stage strip (`../../../haipipe-paper/stage-strip.sh`); comment threads follow the Comment lifecycle section in `../../../haipipe-paper/SKILL.md`.
