# 2-phase -- how to use it

Concrete recipes for the phase engine. You never invoke a phase skill directly: you run a **stage skill** from `1-lifecycle/` and it drives DRAFT → PROBE → REVISE internally, then stops at CHECK for you. Paths below use a real example manuscript:

```
PAPER=examples/ProjB-PhyTrait-OpioidRx/paper/Paper-Personality2Opioid-MISQ2026
SEC=$PAPER/0-lifecycle/5-section-edit
```

## TL;DR

```
1. /haipipe-paper section-edit introduction   → stage skill runs DRAFT → PROBE → REVISE (automatic)
2. It stops at CHECK: checker report + probe flags (🔍 citations, values, display links)
3. You reply in the working .md as  > USER: …  threads, or decide: proceed / restart / accept / park
4. Ask to apply → the stage restarts the affected phase, re-runs everything downstream, re-CHECKs
5. Loop until CHECK is clean → sync to tex → compile
```

Same engine behind every stage: `seed | claims | pitch | narrative | display | section-edit`.

## A. Run a stage (the normal path)

> /haipipe-paper section-edit introduction

What happens, phase by phase:

- **DRAFT** 🤖 -- `haipipe-paper-draft` settles structure + draft sentences into `$SEC/1-introduction/1-introduction.md`, reading the stage's template from `1-lifecycle/` (venue style is applied later, in REVISE, from the `_venue/` pack). Content decisions are negotiated with you here.
- **PROBE** 🤖 -- `haipipe-paper-probe` fans out: `-citation` writes candidates to `_CITATION_1-introduction.md` and flags them 🔍, `-values` traces numbers to source into `_VALUES_…md`, `-display` routes figure/table needs to `0-displays/` units. Evidence questions beyond the documents dispatch through `/haipipe-probe`. Agent-only; nothing gates on you.
- **REVISE** 🤖 -- `haipipe-paper-revise` changes the prose directly per `REF/prose-quality.md` through `-content` (incl. its weave step for paragraph flow), `-humanizer` (plus `-results` for results sections), leaving `%% {CC-*}:` why-comments. No comment-first pause.
- **CHECK** 🧑 -- `haipipe-paper-check` presents the 6-axis report with all probe flags. This is where you come in.

## B. Review a CHECK report

The report lists what passed, what is flagged, and what needs your verdict. Four decisions:

| You say | Meaning |
|---------|---------|
| proceed | section done, move on |
| restart <phase> | rerun that phase and everything after it (recipe D) |
| accept with edits | reply in comment threads (recipe C), then ask to apply |
| park | leave the section as-is, flags stay open |

Citation flags 🔍 are yours to close: verify each candidate on Scholar, then add the bibtex yourself. The agent never writes to `.bib`.

## C. Comment threads (`> USER:` / `> CC:`)

Feedback lives as blockquote threads in the working `.md`, directly under the text it refers to. The human actor id is `> USER:` (unified vocabulary, JL 2026-07-07: "统一 user"). Sweeps and skills grep for `> USER:`; personal initials (e.g. `> JL:`) are tolerated as a human alias when reading, but every documented example and every agent-written slot uses `> USER:`.

```markdown
> USER: this buries the contribution -- lead with the gradient result
> CC: agreed; moved it to P1.S2 and demoted the old opener to P2
```

Rules: the agent replies in one line under your comment; the thread stays in place until you confirm; on resolve it moves to `_LOG_1-introduction.md`. Full convention: `../wiki/02-comment-lifecycle.md`.

## D. Restart a phase after CHECK feedback

Phase order is fixed (draft → probe → revise → check), so a restart re-runs the named phase **and everything downstream**:

> The Table 2 numbers changed -- re-probe values for the results section.

> Restart revise on the introduction; the humanizer missed P3.

> Restart draft -- the outline needs a new beat for the discretion boundary.

Restarting DRAFT reopens content decisions with you; PROBE/REVISE restarts run automatic and land back at CHECK.

## E. The effort dial

- **Light** -- read the CHECK report, answer proceed/restart. Minutes per section.
- **Medium** -- thread `> USER:` comments on specific sentences, ask to apply.
- **Heavy** -- reopen DRAFT, renegotiate the outline, run multiple CHECK rounds.

## F. Boundaries (always true)

- DRAFT is the only phase that negotiates content with you; PROBE and REVISE never wait on a human.
- Nothing enters `.bib` and no number is invented -- probe proposes, you verify in CHECK.
- Unresolved `> USER:` threads keep a section open; silence is not consent.
- No ad-hoc plots: display needs become `0-displays/` units backed by tasks.
