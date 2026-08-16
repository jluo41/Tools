# Q — In the haipipe-toolkit (plugins/haipipe-toolkit), do the probe-related agent definitions and skills contain the literal path `1-probes/` in their instructions or code, and does any of them accept a caller-supplied landing directory for probe records? Accepted: hard-coded | parameterized | mixed.
- state:   answered
- started: 2026-08-16T01:28
- by:      haipipe-task-orchestrator-agent

## Answer

**Verdict: hard-coded.** The literal segment `1-probes/` appears throughout the live probe-dispatch instructions and code, always as a fixed path segment appended to a consumer root. Only the root above it (a positional `<paper_root>` / `<intervention_root>` argument, or the `papers/<P>/` · `applications/<A>/` prefix) is caller-supplied. No agent definition or skill accepts a caller-supplied landing directory for probe records; one agent explicitly refuses to choose destination folders.

All paths below are relative to `plugins/haipipe-toolkit/`. Full grep evidence: `tasks/A01_toolkit_probe_audit/01_probe_landing_path_scan/results/run_scan/` (grep-live.txt, 300 occurrences across live files; grep-history.txt, 127 in CHANGELOGs/_old/fixtures; file-inventory.txt, 572 files scanned).

### 1. Literal `1-probes/` occurrences — core probe-dispatch surfaces (live)

Shared probe skill and its agent definitions:

| file | lines | nature |
|---|---|---|
| `skills/probe/haipipe-probe/SKILL.md` | 52, 112, 125, 167, 290, 380 | instructions; line 167 fixes the landing spot: `papers/<P>/1-probes/PPNN_<topic>/`, "identically `applications/<A>/1-probes/PPNN_<topic>/`" |
| `skills/probe/haipipe-probe/ref/probe-template.md` | 9, 12, 21, 46, 52, 138 | template; line 9: "A probe TOPIC is a FOLDER `1-probes/PPNN_<topic>/`" |
| `skills/probe/agents/haipipe-probe-q-executor-agent.md` | 52 | agent definition; input described as "the consumer's 1-probes/ entries" |
| `skills/probe/agents/README.md` | 12 | names `papers/<P>/1-probes/PPNN_<topic>/` as the probe-file home |

Application probe phase:

| file | lines | nature |
|---|---|---|
| `skills/application/2-phase/1-probe/haipipe-application-probe/SKILL.md` | 54, 61, 71 | instructions; line 61: "create the persisted Probe files under `<intervention_root>/1-probes/PPNN_<topic>/`" |
| `skills/application/2-phase/1-probe/haipipe-application-probe/check-probe-cards.sh` | 18, 19, 90, 334, 590, 602 | code; line 334 is the executable glob `for probe in "$intervention_root"/1-probes/PP*/*.md` |
| `skills/application/2-phase/1-probe/haipipe-application-probe/ref/harvest-acceptance.md` | 5 | "`1-probes/` is the only consumer-side source of truth" |

Paper probe phase — the literal appears only to mark it RETIRED for papers:

| file | lines | nature |
|---|---|---|
| `skills/paper/haipipe-paper/fn/probes.md` | 65–66 | "There is no live top-level `1-probes/`"; archive-only under `0-lifecycle/_archive/1-probes/` |
| `skills/paper/haipipe-paper/probe/check_topic_entries.py` | 73–75 | code: hard-FAILs if `<paper_root>/1-probes` exists; live paper entries are globbed from the fixed `0-lifecycle/<stage>/probes/` (lines 81–90) |
| `skills/paper/haipipe-paper/probe/topic-entry-contract.md` | 32 | contract prose |

Top-level `agents/` directory (5 board/task agent definitions): **zero occurrences** — no probe-dispatch agents live there; the probe agent definitions sit under `skills/probe/agents/` and `skills/discovery/agents/`.

The literal also appears in the wider application-lifecycle skill family that raises probe entries (e.g. `skills/application/haipipe-application/SKILL.md` line 48: "the flat probe pool 1-probes/PPNN_<topic>/", 12 occurrences; `skills/application/haipipe-application/fn/probes.md`, 6; `skills/application/0-enter/haipipe-application-enter/SKILL.md`, 7) and in `skills/STRUCTURE.md` lines 37, 78–79. Per-file counts for all 300 live occurrences are in grep-live.txt.

### 2. Caller-supplied landing directory: none

- `check-probe-cards.sh` (application): usage `check-probe-cards.sh <intervention_root> [project_root] [--stage <key>]` — the ROOT is an argument; the `1-probes/` segment under it is a literal (line 334). No flag relocates it.
- `check_topic_entries.py` (paper): `check_topic_entries.py <paper_root> [project_root]` — same pattern; the landing segment `0-lifecycle/<stage>/probes/` is hard-coded, and a caller-side `1-probes/` is an error, not an option.
- `haipipe-probe-q-executor-agent.md`: states it does NOT "Choose or author a destination FOLDER for fresh work — the executor orchestrator owns its namespace ... I never invent a target folder". It receives entry file paths and writes only the `target:` field inside them.
- `skills/probe/haipipe-probe/SKILL.md` line 167 and `ref/probe-template.md` lines 9–21 fix the record location by convention (`1-probes/PPNN_<topic>/QXn_<slug>.md` relative to the consumer root); no verb or parameter overrides it.

## Caveats

- The two consumer families disagree on where the fixed landing spot IS: the shared probe skill (`SKILL.md:167`) and `skills/probe/agents/README.md:12` still name `papers/<P>/1-probes/` as live, while the paper family's own files (`fn/probes.md:65`, `check_topic_entries.py:73–75`) retire it for papers in favor of `0-lifecycle/<stage>/probes/`. Both locations are equally hard-coded; the verdict is unaffected, but the shared-skill text and the paper checker are out of step with each other.
- "Probe-related" was resolved by content match (any file under `agents/` or `skills/` mentioning "probe"), 572 files; design-board material under `skills/diagrams/` matched heavily (it discusses probe design, including a board card literally about the landing address) but is documentation of design sessions, not dispatch instructions or code — its hits are in grep-live.txt and were not treated as instruction surfaces.
- Line numbers are as of the scan date (2026-08-16) on the working tree, which has uncommitted modifications.

## Not-done

- Did not scan the toolkit's `mcp-servers/` directory (out of the stated agents/ + skills/ scope).
- Did not assess whether hard-coding is desirable, only whether it is present.
