---
name: haipipe-probe-review
description: "The claim JUDGE of the probe layer — the G1/G2/G3 rulebook. G1 structural (is the comparison valid), G2 integrity (is the evidence honest — a MANUAL source-by-source walk), G3 claim (does the evidence support the claim → supported | refuted | inconclusive, + confidence + claim_type). Normally invoked HEADLESS by haipipe-probe-reviewer-agent, which the paper/application PROBE-phase worker dispatches at ⑤ INTERPRET for a `mode: full` question section. Writes NO files: the judgment is the RETURN, and the CALLER lands it in the consumer's 0-lifecycle/1-claims/1-claims.md — per-claim, per-consumer, private. It NEVER lands in a probe file: `## Verdict` and the `verdicted` state are DELETED (R7). Trigger: judge claim, claim verdict, G1 G2 G3, structural check, integrity audit, probe review."
argument-hint: "\"<claim>\" --refs <evidence artifact paths>   (normal path = the PROBE worker's INTERPRET step, `mode: full`)"
allowed-tools: Read, Grep, Glob, Bash
metadata:
  version: "2.2.0"
  last_updated: "2026-07-14"
  summary: "v2.2 (Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3, approved JL 2026-07-14). The G1/G2/G3 judgment rulebook, extracted from the reviewer agent so the process is a governed SKILL; the agent is a thin shell that calls this headless. THE JUDGMENT SURVIVES UNCHANGED — three gates, five fraud patterns, the >95/80-95/<80 thresholds, the confidence scale, the associational|causal guard. TWO THINGS MOVED. (1) The DISPATCHER: the probe GATEWAY is RETIRED, so the caller is now the paper/application PROBE-phase worker's INTERPRET step, for a `mode: full` section. (2) The LANDING SITE: R7 deletes the `## Verdict` block and the `verdicted` state, and R1 retires 1-probe-plans/, so supported|refuted|inconclusive + confidence + claim_type + gates land in the consumer's 0-lifecycle/1-claims/1-claims.md — per-claim, per-consumer, PRIVATE. v2.2 closes the last two dead doors in this skill: G2 now LEADS with the manual source walk and BANS g2_integrity_check.py on QA-file/sources.md/results shapes (its CLI is folder-era: probe.yaml + evidence.md, retired 2026-07-05, so it exits early and audits nothing); and probe-caveats-checklist.txt no longer tells the reviewer to commit caveats into verdict.md / probe.yaml.verdict.caveats — a YES is a caveat line in the RETURNED TEXT, transcribed by the CALLER into 1-claims.md (and, where relevant, a section's `reading:`)."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-probe-review — the claim JUDGE (G1/G2/G3)
========================================================

**Owns** — the rulebook for one question, and nothing else:

```text
Does this evidence mix support that claim — structurally valid (G1),
honestly grounded (G2), and sufficient for a committed judgment (G3)?
```

**Invoked** — headless by `Agent(haipipe-probe-reviewer-agent)`, which the paper/application
PROBE-phase worker dispatches at ⑤ INTERPRET for a question section on a `mode: full` probe file.

**Writes** — **NOTHING.** The judgment IS the return text. The CALLER lands it in the consumer's
`0-lifecycle/1-claims/1-claims.md`.

```text
   📄 CONSUMER (paper / application)                    ⚙️ BANK (probe-unaware)
   ─────────────────────────────────                    ──────────────────────
   PROBE worker ⑤ INTERPRET
   a `mode: full` section, answered           ◀──────── <leaf>/QA/<n>-<slug>.md
        │                                               (the executor wrote it)
        │  dispatches, with claim + evidence refs
        ▼
   🔍 Agent(haipipe-probe-reviewer-agent)   ← fresh context: it did NOT gather this evidence
        │  Skill(haipipe-probe-review)  ← YOU ARE HERE
        │  G1 structural → G2 integrity → G3 claim
        │
        ▼  returns TEXT (no file, anywhere)
   📒 0-lifecycle/1-claims/1-claims.md      ← the CALLER writes it. The ONLY home of a
      status · confidence · claim_type ·       claim's status (R7). Per-claim, per-consumer,
      gates · scope · caveats                  PRIVATE.
```

This is the SECOND review tier. Per-layer reviewers (discovery-reviewer, task-reviewer) judge
"is this artifact well-made"; this process judges "does this evidence MIX support this claim" —
across `discoveries/` + `tasks/` at once. The two tiers never merge (产审分离: **whoever assembled
the evidence does not grade it** — the EXECUTOR assembled it in its own clean session; this
reviewer, in a separate fresh context, grades it).


Who runs this
-------------

```text
normal   Agent(haipipe-probe-reviewer-agent) ← dispatched by the paper/application PROBE-phase
         worker at ⑤ INTERPRET, for a section on a `mode: full` probe file. The agent invokes
         this skill headless and returns its output verbatim. The WORKER then lands that return
         in the consumer's 0-lifecycle/1-claims/1-claims.md — never in a probe file.
direct   /haipipe-probe-review "<claim>" --refs <paths>  — only with a complete spec
         (claim + on-disk evidence refs, normally the section's `target:` QA file). No sweep,
         no evidence gathering here: if refs are missing, the answer is "run the probe's
         DISPATCH first" — the evidence comes from the executor, through the qa verb.
```

`mode: light` never judges — no claim status is settled, and this skill is not invoked.

💀 The probe GATEWAY agent that used to dispatch this is RETIRED (2026-07-14). This skill and the
reviewer agent SURVIVE; only the CALLER and the LANDING SITE changed. The judgment content below
is exactly what it always was.


Input spec
----------

```text
claim:  the exact sentence to judge (and, implicitly, what would refute it)
refs:   evidence artifact paths on disk — the section's target: QA file
        (<leaf>/QA/<n>-<slug>.md) plus the artifacts it anchors:
        tasks/<...>/results/... · discoveries/<...>/sources.md · verdict.md · landscape.md
```


The three gates (sequential; G2 gates G3)
------------------------------------------

If integrity fails, the claim status is `inconclusive` (blocked), **not** `refuted`.

**G1 — Structural: is the comparison valid?**

Read the referenced artifacts, then check:

```text
[ ] every evidence ref resolves to a real file on disk (unresolvable → name it; cannot judge)
[ ] the roles / contrast being compared are apples-to-apples
[ ] the linked task/discovery results actually match the claim's intended comparison
[ ] caveats cover the detectable confounds (./probe-caveats-checklist.txt)
[ ] any Review-type discovery verdict.md / landscape.md is accounted for
```

Return `G1: ✅` or `G1: ❌ <reason>`.

**G2 — Integrity: is the evidence honest?**

Five fraud-pattern categories:

```text
A. Ground-truth provenance       — every number traces to a real source file?
B. Metric/definition consistency — same metric name means the same computation?
C. Phantom results               — any cited result that does not appear in the source?
D. Scope-language mismatch       — does the claim overstate what the evidence covers?
E. Individual/split leakage      — any leakage across train/test or across individuals?
```

**RUN G2 MANUALLY.** Read each cited source file and confirm every cited number appears there,
verbatim. Score: cited-numbers-verified / cited-numbers-total.

Thresholds: **>95% verified** → `✅ pass` · **80–95%** → `⚠️ warn` (caps G3 confidence at
`medium`) · **<80%** → `❌ fail` (blocks G3). State `G2: … (manual)` in the return line.

⛔ DO NOT invoke `g2_integrity_check.py` on the shapes this model produces. Its CLI is folder-era:
it takes a legacy probe FOLDER positional and reads `evidence.md` + `probe.yaml` — both retired
2026-07-05. Handed a QA file, a `sources.md` or a `results/` CSV it exits early
(`evidence.md not found`) and audits nothing. The script survives ONLY for legacy folder-era
probes. Refitting its CLI (`--doc <file> --sources <paths...>`) is a flagged follow-up; until it
lands, the manual walk above IS G2.

Return `G2: ✅ pass` | `⚠️ warn <reason>` | `❌ fail <reason>`.

**G3 — Claim: does the evidence support the claim?**

Only if G2 did not fail. Then:

```text
1. Re-read the claim and what would refute it.
2. Re-read the source artifacts (not a summary of them).
3. Assess: does the evidence meet the bar for support?
4. Separate supported scope from unsupported scope.
5. List the required caveats.
6. Set confidence: high | medium | low, with justification (a G2 warn caps this at medium).
```

The status vocabulary is the CLAIM LEDGER's — `0-lifecycle/1-claims/1-claims.md`, where this
judgment lands (owner: `haipipe-paper-claims` / `haipipe-application-claims`):

```text
supported     the evidence meets the bar (partial support = supported + an explicit unsupported scope)
refuted       the evidence meets the bar for the OPPOSITE / falsification
inconclusive  the evidence does not decide it — also the result when G2 failed (blocked)
```


Return contract (text, never a file)
------------------------------------

```text
gates:      G1 <✅/❌> · G2 <✅/⚠️/❌> · G3 <✅/❌>
status:     supported | refuted | inconclusive
confidence: high | medium | low
claim_type: associational | causal
scope:      supported "<...>"  /  unsupported "<...>"
caveats:    [ ... ]
reasoning:  one paragraph tying the evidence refs to the claim
judged-by:  haipipe-probe-review · <date>
```

`status:` / `confidence:` / `claim_type:` / the gates are exactly the fields `1-claims.md` carries
per claim — the return is shaped so the caller can transcribe it without translating.

**`claim_type` — the correlation→causation guard** (ported here 2026-07-12 when the insight layer
was retired; this is now its ONLY home). It is a SEPARATE axis from `confidence`, and conflating
them is the classic overclaim:

- `confidence` is about the SAMPLE→POPULATION leap: how sure are we this holds beyond the data we
  looked at?
- `claim_type` is about the CORRELATION→CAUSATION leap: does the evidence identify an effect, or
  only an association?

**NEVER upgrade `claim_type` because `confidence` is high.** A tight CI on an observational
association is a high-confidence ASSOCIATIONAL claim, not a causal one. `causal` is permitted ONLY
when the evidence carries a named identification strategy — an RCT, a strong and valid instrument,
a regression discontinuity, or difference-in-differences with checked parallel trends. Absent one,
the answer is `associational`, however clean the numbers are, and the consumer's prose must not say
"causes", "leads to", or "improves".


Where the judgment lands (not here)
-----------------------------------

The CALLER — the paper/application PROBE worker's ⑤ INTERPRET step — carries this return into the
consumer's `0-lifecycle/1-claims/1-claims.md`. That ledger is the ONLY home of a claim's status
(R7). Two consequences, both intended:

- **There is no `## Verdict` block and no `verdicted` state to write.** Both are DELETED. The probe
  section carries only its `reading:` — the paper's own one-line interpretation.
- **The judgment is PRIVATE to the consumer.** A second paper judging the same evidence against ITS
  claim re-runs this review and writes its own ledger line. Same facts, two readings — correct.


Hard boundaries
---------------

- **Writes NOTHING** — no verdict.md, no probe file, no claim ledger, no bank file. The judgment is
  the return text, and that is the whole output.
- **Gathers NOTHING** — no searches, no task runs, no sweep. Judges the given refs, only. Missing
  refs are not a reason to go find evidence; they are a reason to return "cannot judge".
- **Deposits NOTHING** — landing the judgment in `0-lifecycle/1-claims/1-claims.md` belongs to the
  CALLER (the consumer side). It never lands in a probe file, and never in the bank.
