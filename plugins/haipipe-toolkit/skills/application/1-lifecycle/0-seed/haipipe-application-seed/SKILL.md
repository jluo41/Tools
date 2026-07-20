---
name: haipipe-application-seed
description: "Stage 0 of the intervention lifecycle (venue-FREE). Answers 'why might this intervention work?' Documents the opportunity, expected impact, audience, channel hunch, mechanism hypothesis. Output: 0-lifecycle/0-seed/0-seed.md + _LOG_0-seed.md (+ 1-probes/ feasibility questions). Markdown only. Modeled on haipipe-paper-seed. Trigger: seed, opportunity, why this intervention, /haipipe-application seed."
argument-hint: "[intervention-path] [intent...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "6.1.0"
  last_updated: "2026-07-19"
  summary: "Seed stage (stage 0, venue-FREE ROOT of the DIKW ladder) — states why this intervention might work before evidence is mature: opportunity, impact, audience, channel hunch, mechanism. DRAFT may WebSearch to orient; PROBE is FEASIBILITY-light (novelty + external-data obtainable); internal-data needs FORWARD to the ladder as [FORWARD -> CLAIMS] pointers. History: ./CHANGELOG.md."
---

Skill: haipipe-application-seed
================================

Stage **0** of the intervention lifecycle: the venue-FREE ROOT the whole DIKW ladder grows from.
It answers one question — why might this intervention work? — and keeps that possibility alive before the evidence is mature.

```text
0-seed            why this might work (the opportunity)   <- THIS STAGE
1a-descriptions   what the data looks like
1b-themes         what patterns/topics emerge
1c-claims         what generalizes (the ledger)
1d-advice         what the evidence advises (the deliverable)
```

The user invokes this skill; it drives DRAFT → PROBE → REVISE → CHECK internally via the `2-phase/` workers.
Read first: `../../../PHILOSOPHY.md`.


## What's special: three things make a seed a seed

**1. Venue-FREE, and the root every rung above depends on.**
The channel hunch (sms / push / in-app / dashboard / email) is context, not a commitment — the venue is pinned AFTER the ladder via `/haipipe-application venue`, and the seed survives that retargeting untouched.
Seed writes `[FORWARD -> CLAIMS]` pointer lines in `_LOG_0-seed.md` for any internal-data need it surfaces (the token stays `CLAIMS` for grep-stability); rung 1a CONSUMES them at its DRAFT open, and an unconsumed pointer fails the 1a gate.

**2. Its probes are FEASIBILITY only — "can this intervention exist at all?"**
Two shapes, both light and both `discovery`-side: is the angle NOVEL (landscape / prior interventions / 查新), and is the EXTERNAL data OBTAINABLE (benchmarks, field norms, outside labeled data)?
Profiling OUR OWN cohort/engagement data is `task` work that belongs to rung 1a — never a seed probe; it leaves as a FORWARD pointer (need + why, no card).
This bounds the seed's cost to the feasibility question and stops it doing ladder evidence work early.

**3. DRAFT may search; PROBE must dispatch.**
Inline WebSearch is legitimate DRAFT fuel — orientation that becomes prose AND buffered `state: planned` question skeletons — but it is NEVER evidence.
The PROBE phase must ALWAYS run the real worker; an inline result has no project-side ledger, so the PROBE phase did not happen.
The invariant is section STATE: `planned` (DRAFT) vs `read` with a resolving `target:` (PROBE), mechanically enforced by the probe checker.


## The four phases, in seed

```text
DRAFT   settle the five content sections with the user (haipipe-application-draft); MAY WebSearch to
        ORIENT (crowded space? prior interventions? benchmark rates?) — weave the result into prose AND
        AUTHOR the probe plan: ① ORGANIZE each feasibility question into a `## QX<n>` ENTRY in
        1-probes/, ② MATCH it against the bank (a read-only grep is legal), leaving it `state: planned`;
        register internal-data needs as [FORWARD -> CLAIMS] pointers in _LOG_0-seed.md
PROBE   EXACTLY ONE worker call — `Skill("haipipe-application-probe", args="from-buffer <root>")` —
        feasibility only (novelty + external-data obtainable). It RUNS THE DRAFT-AUTHORED PLAN FORWARD:
        ③ DISPATCH what the bank still owes, ④ POINT each `target`, ⑤ INTERPRET. ①② already happened at
        DRAFT and are AUTHORITATIVE — PROBE does not re-raise and does not re-match.
        Inline search is FORBIDDEN here.
        Routing mechanics + seed specifics: ../../../2-phase/1-probe/haipipe-application-probe/SKILL.md
REVISE  tighten wording; weave probe takeaways into Opportunity/Mechanism; the Q-consumer section holds the questions (haipipe-application-revise)
CHECK   exit criteria below → Gate Ledger row; the gate RUNS the probe checker (haipipe-application-check)
```

Seed RECEIVES its feasibility evidence, never PRODUCES it inline: it raises questions; `haipipe-application-probe` binds them via the stake-free collector `Agent(haipipe-probe-q-executor-agent)`, never an orchestrator directly.
If the intervention folder does not exist, route to `/haipipe-application enter <path>` (get-or-create owns scaffolding).
Migrate a legacy per-stage `_PROBE/` card into `1-probes/` in the new shape on first touch only.


## The artifact

`0-lifecycle/0-seed/0-seed.md` — full skeleton in `ref/seed-template.md`:

```text
Opportunity            2-3 sentences: what gap exists, what behavior we want to change
Expected impact        directional estimate ("increase refill adherence by 5-15pp")
Audience               who receives it — a specific subset, not "everyone"
Channel hunch          sms | push | in-app | dashboard | email — a HUNCH, not the venue pin
Mechanism hypothesis   one sentence: why this audience + this content might respond
Q-consumer             feasibility questions raised (novelty + external-data), one `## Q-Seed-<n>` block each
```

Each Q-consumer question is one `## Q-Seed-<n>` block. Its fields and their FILL RULES live inline in `ref/seed-template.md` as `<!-- RULE -->` comments — that template is the single home, and this file does not restate them (JL ruling 2026-07-19, D3(b): a second copy is what drifts). The id carries the stage name (`Seed-`) so the flat probe pool shows which stage raised the question. State is deliberately minimal — a question is OPEN while `Answer` is unfilled, ANSWERED once it is not; no `state:` field lives in the seed doc (that machinery belongs to the `1-probes/` ENTRY).

Sidecar: `_LOG_0-seed.md` (phase journal + the `[FORWARD -> CLAIMS]` pointers).
Formatting: `=====` title / `-----` section rules; content sections use no `#`, Q-consumer questions use `## Q-Seed-<n>`; one sentence per line.
Venue-FREE: the seed survives retargeting; the channel hunch is context, not a commitment.

Done: all five content sections carry real content (not placeholders); Audience and channel hunch are specific; the Q-consumer section raises at least the novelty/landscape question as a `## Q-Seed-<n>` block (Description/Reason/Probe/Answer, per `ref/seed-template.md`), with internal-data needs appearing only as `[FORWARD -> CLAIMS]` pointers; the probe checker exits clean at the gate — the APPLICATION family's copy, named explicitly:

```sh
CHK=$(find -L ~/.claude/skills ./.claude/skills "${CLAUDE_PLUGIN_ROOT:-/nonexistent}" -maxdepth 4 -path '*haipipe-application-probe/check-probe-cards.sh' 2>/dev/null | head -1)
[ -n "$CHK" ] || { echo 'FAIL: application probe checker not found'; exit 1; }
sh "$CHK" <intervention_root> --stage seed
```

TWO files named `check-probe-cards.sh` exist on disk (paper + application) and their invariants differ, so a bare `-name` find resolves to whichever the filesystem returns first and silently asserts this intervention against PAPER rules.


## Questions this stage typically raises

DRAFT's RAISE+PLAN step raises what the draft cannot answer. These are the kinds this stage is prone to — read this list, then walk the draft against it.

```
👣 occupied ground   Has this intervention already been tried on this population?
                     Name the closest prior programme, or name the ground as open.
🧪 mechanism         Is there evidence the hypothesised mechanism works AT ALL —
                     anywhere, for anyone? Not "is it plausible", but "who showed it".
📡 channel reach     Does this channel actually reach this audience? Name the
                     coverage, not the intention.
```

This list bounds DISPATCH, never RAISING. A question of any other shape — profiling OUR OWN cohort/engagement data, or any other prerequisite — is still RAISED: it keeps its `## Q-Seed-<n>` block, takes `Answer: deferred -> CLAIMS`, and carries a `[FORWARD -> CLAIMS]` pointer in `_LOG_0-seed.md`. What it does not get is an ENTRY in `1-probes/`.

⚠️ The pointer token is `[FORWARD -> CLAIMS]`, NOT `DESCRIPTIONS`, even though rung **1a-descriptions** is what consumes it. The token is frozen for grep-stability (see "Venue-FREE" above, and 1a's consume-grep). Writing `DESCRIPTIONS` produces a pointer that 1a's grep never finds — the need silently disappears.

## Exits

```text
promote -> /haipipe-application ladder   run the 1a-1d sweep (or `descriptions` to start rung-by-rung)
```

End every reply with the closing block (stage line via `../../../haipipe-application/stage-strip.sh`).
