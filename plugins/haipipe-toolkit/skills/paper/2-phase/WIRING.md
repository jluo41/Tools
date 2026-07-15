# 2-phase -- wiring

How the `haipipe` plugin discovers and exposes the phase workers, and how they get invoked at runtime.

## Discovery model (convention-based)

`.claude-plugin/plugin.json` lists no skills/agents/commands explicitly -- the plugin auto-discovers by convention:

| Piece | Discovered from | How it's invoked |
|-------|-----------------|------------------|
| **Skills** | `skills/**/SKILL.md` with a `name:` frontmatter | by skill name via the Skill tool (e.g. `haipipe-paper-revise`) |
| **Agents** | top-level `agents/*.md` | as a `subagent_type` for the Agent tool |
| **Commands** | top-level `commands/*.md` | as `/command` (none shipped; skills are invoked by name) |

Skills created or renamed mid-session aren't hot-loaded; they appear after the next Claude Code reload.

## What registers from 2-phase/

Each phase folder holds a hub skill plus its workers, every one a `SKILL.md` with a valid `name:`:

| Folder | Hub | Workers |
|--------|-----|---------|
| `0-draft/` | `haipipe-paper-draft` | (none -- the hub reads the stage template from `1-lifecycle/`; retired venue-style write skills live in the paper-root `_archive/`) |
| `1-probe/` | `haipipe-paper-probe` | `haipipe-paper-probe-citation` / `-values` / `-display` |
| `2-revise/` | `haipipe-paper-revise` | `haipipe-paper-revise-content` / `-humanizer` / `-results` (weaving merged into content 2026-07-07) |
| `3-check/` | `haipipe-paper-check` | `haipipe-paper-proof-checker` (math proofs) |

Not registered: `REF/` (plain reference .md, no SKILL.md -- workers load it by path) and the paper-root `_archive/` (retired edit-cycle skills, the old `paper-edit-*` stage agents, the retired venue-style `draft-write-*` skills, and the old draft LaTeX templates; kept for history, nothing routes to them, and they are not symlinked into top-level `agents/`).

## Dispatch chain (who calls whom)

**Phase skills are internal workers called by stage skills via the Skill tool; they are not user entry points.** The user steers with phase VERBS on the stage skill (`/haipipe-paper-section-edit <section> [draft|probe|revise|check]`): the verb picks which phase the stage drives; the stage still supplies all context and still dispatches the internal workers.

```
user → /haipipe-paper <stage> [<target>] [draft|probe|revise|check]
        (seed | claims | pitch | narrative | display | section-edit — skills in 1-lifecycle/)
             │
             ▼  the stage skill (the STAGE CONTRACT: aim + template + rules)
                dispatches the phase engine via Skill(), in order:
       haipipe-paper-draft    → drafts from the stage's template → ⛔ STOP: user structure review
       haipipe-paper-probe    → five-step loop (ORGANIZE→MATCH→DISPATCH→POINT→INTERPRET); fans out
                                -citation / -values / -display; DISPATCH hands the section's `q-executor:`
                                block VERBATIM to Agent(haipipe-task-orchestrator-agent) /
                                Agent(haipipe-discovery-orchestrator-agent)   [no gateway]
       haipipe-paper-revise   → runs -content / -humanizer (+ -results); proof: workers line in _LOG
       haipipe-paper-check    → 6-axis report, presented to the human (CHECK 🧑)
```

Two human gates: after DRAFT (structure) and at CHECK (quality). PROBE/REVISE run automatic between them. The agent never self-advances past a gate — the user's verb is the approval. Hubs own the fan-out to their workers, so a stage skill only ever names the four hubs, and a phase executed without its `Skill()` dispatch did not happen.

## Related, but not in 2-phase/

- Whole-paper passes (`haipipe-paper-edit-consistency`, `-format`, `-typeset`, `-diffpdf`, …) live in `3-build-submit/` -- same discovery convention, different scope.
- The section-edit stage hub is `1-lifecycle/5-section-edit/haipipe-paper-section-edit/`; its per-paper working files land in the manuscript's `0-lifecycle/5-section-edit/`.
- Comment threads produced during CHECK follow `../wiki/02-comment-lifecycle.md`.
