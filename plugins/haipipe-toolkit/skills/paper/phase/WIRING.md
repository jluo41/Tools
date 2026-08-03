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
| `0-draft/` | `haipipe-paper-draft` | `haipipe-paper-draft-citation` / `-values` / `-display` (the hole sweep; the hub reads the stage template from `1-lifecycle/`) |
| `1-probe/` | `haipipe-paper-probe` | (none -- ③DISPATCH ④POINT ⑤INTERPRET all run in the hub; harvest is inline in ⑤) |
| `2-revise/` | `haipipe-paper-revise` | `haipipe-paper-revise-place` (first) / `-content` / `-humanizer` / `-results` |
| `3-check/` | `haipipe-paper-check` | `haipipe-paper-proof-checker` (math proofs) / `haipipe-paper-check-evidence` (pre-submission evidence walk) |

Not registered: `REF/` (plain reference .md, no SKILL.md -- workers load it by path) and the paper-root `_archive/` (kept for history; nothing routes to it, and it is not symlinked into top-level `agents/`).

## Dispatch chain (who calls whom)

**Phase skills are internal workers called by stage skills via the Skill tool; they are not user entry points.** The user steers with phase VERBS on the stage skill (`/haipipe-paper-stage section-edit <section> [draft|probe|revise|check]`): the verb picks which phase the stage drives; the stage still supplies all context and still dispatches the internal workers.

```
user → /haipipe-paper <stage> [<target>] [draft|probe|revise|check]
        (seed | claims | pitch | narrative | display | section-edit — skills in 1-lifecycle/)
             │
             ▼  the stage skill (the STAGE CONTRACT: aim + template + rules)
                dispatches the phase engine via Skill(), in order:
       haipipe-paper-draft    → drafts from the stage template and raises Q-consumers
       haipipe-paper-probe    → owns ①ORGANIZE ②MATCH ③DISPATCH ④POINT ⑤INTERPRET;
                                ③ hands each entry's `### q-executor` block VERBATIM to
                                Agent(haipipe-probe-q-executor-agent) — the stake-free collector,
                                which is the ONLY door to the bank (LAW 1: this worker never calls
                                an executor orchestrator itself).
       haipipe-paper-revise   → when declared, runs -place (FIRST) → -content → -humanizer → -results;
                                proof: workers line in the owning S page's ## Log
       haipipe-paper-check    → 6-axis report, presented to the human (CHECK 🧑)
```

`stage.md` is authoritative for phase order and gates. All current stages have
one human gate at CHECK; Venue omits REVISE. The agent never self-advances past
a declared gate. Hubs own worker fan-out, and a phase executed without its
`Skill()` dispatch did not happen.

## Related, but not in 2-phase/

- Whole-paper passes (`haipipe-paper-polish`, `-diffpdf`, …) live in `3-deliver/` -- same discovery convention, different scope.
- The section-edit stage hub is `1-lifecycle/haipipe-paper-stage/stages/5-section-edit/`; its per-paper Board pages land in the manuscript's `0-lifecycle/4-main/` (appendix pages in `0-lifecycle/5-appendix/`).
- Comment threads produced during CHECK follow the Comment lifecycle section in `../haipipe-paper/SKILL.md`.
