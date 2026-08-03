# 2-phase -- how to use it

Concrete recipes for the phase engine. You never invoke a phase skill directly:
run a **stage skill** from `1-lifecycle/`; it drives the phases and gates
declared by `stage.md`. All current stages stop once, at CHECK. Paths below use
a real example manuscript:

```
PAPER=examples/Project-Personality-OpioidRx/papers/Paper-Personality2Opioid-MISQ2026
SEC=$PAPER/0-lifecycle/4-main
```

## TL;DR

```
1. /haipipe-paper-stage section-edit introduction → DRAFT writes real prose + Q-consumers
2. PROBE authors/matches entries and dispatches only within the supplied --depth ceiling
3. REVISE workers place answers, polish, and sync to tex
4. CHECK opens: checker report + probe flags + %% {CC-*} why-comments
5. You decide: proceed / restart <phase> / accept with edits / park
```

One current human gate: quality review at CHECK. In autopilot, a fresh-context
reviewer subagent may stand in at that gate. Venue omits REVISE; the stage
contract, not this recipe, is authoritative.

## A. Run a stage (the normal path)

> /haipipe-paper section-edit introduction

What happens, phase by phase:

- **DRAFT** 🤖 -- settles structure + writes real prose and Q-consumer questions. It does not author probe entries or add an extra gate.
- **PROBE** 🤖 -- authors each entry, MATCHes existing QA, dispatches only work allowed by `--depth`, points targets, and harvests answers.
- **REVISE** 🤖 -- when declared, runs `-place` FIRST, then the prose workers. Its `[REVISE]` record and `workers:` line live in the owning S page's `## Log`.
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

Rules: the agent replies in one line under your comment; the thread stays in
place until you confirm; on resolve it moves verbatim to the owning S page's
`## Log`. Full convention: `../haipipe-paper/SKILL.md`, Comment lifecycle.

## D. Restart a phase after CHECK feedback

Phase order follows the stage's declared list, so a restart re-runs the named
phase and the declared phases downstream of it:

> The Table 2 numbers changed -- re-probe values for the results section.

> Restart revise on the introduction; the humanizer missed P3.

> Restart draft -- the outline needs a new beat for the discretion boundary.

Restarts run automatically through the remaining declared phases and land back at CHECK.

## E. The effort dial

- **Light** -- read the CHECK report, answer proceed/restart. Minutes per section.
- **Medium** -- thread `> USER:` comments on specific sentences, ask to apply.
- **Heavy** -- reopen DRAFT, renegotiate the outline, run multiple CHECK rounds.

## F. Boundaries (always true)

- DRAFT authors content and questions; unresolved taste choices remain inline for CHECK.
- Nothing enters `.bib` and no number is invented -- probe proposes, you verify in CHECK.
- Unresolved `> USER:` threads keep a section open; silence is not consent.
- No ad-hoc plots: display needs become `displays/` units backed by tasks.
