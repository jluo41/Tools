---
name: call-peer
description: >-
  Work with a paired native Claude Code or Codex CLI session as an equal peer:
  create or resume either side, ask one peer to read the other's transcript,
  or delegate a concrete task through the provider's normal CLI.
metadata:
  version: "1.2.0"
  last_updated: "2026-09-06"
---

# Call Peer

Use this skill when a Claude session and a Codex session work as counterparts.
Neither side is a master or subordinate. The direction of one request is
temporary: either peer may read the other peer's session or delegate work.

The pair has one human-readable name and two independent native sessions:

```text
pair_name
├── Claude native session
└── Codex native session
```

The native transcripts, tools, Skills, permissions, and provider limits remain
separate. The pair manifest only maps the relationship and the two stable
session IDs.

## Transport contract

`call-peer` is CLI-only. Invoke the installed `claude` or `codex` executable
through the helper scripts below, using the provider's ordinary native home.
Do not use an Agent SDK, a custom SDK home, an `agent-calls` store, a mirrored
transcript, or a hidden mailbox for ordinary peer work. The two sessions remain
independent native sessions.

## Public operations

### Ask a peer to read the other peer's session

Use the normal paired CLI and make transcript reading part of the task. The
target peer must read the source peer's persisted native transcript itself; the
source peer does not summarize it first.

```bash
.venv/bin/python Tools/plugins/haipipe-toolkit/skills/0_utils/scripts/run_paired_cli.py \
  --pair-name "Call-Peer" \
  --caller-provider codex \
  --caller-session-id <codex_session_id> \
  --callee-provider claude \
  --cwd /Users/jluo41/Desktop/Physician-SPACE \
  --prompt "Read the Codex peer's native session for this pair in read-only mode. Locate it using the provider, session ID, and working directory. Explain the current goal, decisions, completed work, open questions, and next steps in your own words."
```

Use the symmetric provider values when Claude asks Codex to read Claude's
session. A session name is for orientation; use the provider, stable session
ID, and working directory to locate the exact transcript. Provider-specific
native stores may be JSONL, SQLite, or another supported format, so do not
guess a path from the name alone.

The target peer can read only persisted transcript content. It cannot see the
source peer's hidden system context, private reasoning, or text that has not
yet been written. Read after the source turn has finished so the snapshot is
complete. The target must not edit the transcript or start the source peer
unless the user explicitly asks.

### Delegate a concrete task to a peer

The same command can carry an ordinary task. By default, every delegation has
a read-before-work precondition: the target peer must first read the caller's
latest persisted native session itself, understand the current progress, and
only then perform the task. The caller does not summarize the session first.
Skip this precondition only when the user explicitly asks for a context-free
delegation.

```text
First read the paired caller session directly in read-only mode and understand
its current goal, decisions, completed work, and open questions. Do not ask
the caller to summarize it first.
Then inspect the requested files and perform the delegated task.
Return your findings and any changes to the requesting peer.
```

`run_paired_cli.py` creates the native partner on first use, resumes the
registered partner when the pair name already exists, and returns the target
session ID and response. Use `--new-session` only when a new partner is
intentional. Do not create a second empty session because a lookup failed.

## CLI workflow

Normal peer work uses the provider's ordinary native home, configured model,
Tools, Skills, plugins, approvals, and network behavior.

To create or resume the other peer and send one task, use:

```bash
.venv/bin/python Tools/plugins/haipipe-toolkit/skills/0_utils/scripts/run_paired_cli.py \
  --pair-name "Call-Peer" \
  --caller-provider <claude|codex> \
  --caller-session-id <current_session_id> \
  --callee-provider <codex|claude> \
  --cwd /Users/jluo41/Desktop/Physician-SPACE \
  --prompt "<read-peer or delegated task>"
```

To call an already registered side directly by pair name, use:

```bash
.venv/bin/python Tools/plugins/haipipe-toolkit/skills/0_utils/scripts/run_cli_agent.py \
  --provider <claude|codex> \
  --pair-name "Call-Peer" \
  --cwd /Users/jluo41/Desktop/Physician-SPACE \
  --out-dir call-peer-runs/turn-001 \
  --prompt "<task>"
```

Before each paired run, the wrapper injects identity context containing the
pair name, working directory, self provider/session ID, and partner
provider/session ID. This is identity context only. It does not mirror later
turns, call the other peer automatically, or append a mailbox event.

The wrapper resolves the exact native session ID from
`~/.config/haipipe/pairs/`, scoped to the current workspace. Claude resumes
with its native `--resume` form; Codex resumes with its native `codex exec
resume` form. Do not use an implicit `--continue` or `--last` selector when a
paired session is involved.

The pair manifest is a relationship registry, not a shared transcript:

```text
~/.config/haipipe/pairs/<pair-name-and-workspace>.json
```

## Resume visibility

Claude's non-interactive CLI can label the first persisted entry as
`sdk-cli`, even though the call was made through the installed `claude`
executable. The helper normalizes only that first metadata marker to `cli`
after a successful call. It does not change the session ID or conversation
content. This keeps the native session visible in Claude Code's normal
`/resume` picker.

If a lookup fails, inspect the existing native session and its first persisted
entrypoint before creating anything. Never create a duplicate empty partner
just to make it appear in the picker.

## Rules and boundaries

- Use the shared pair name for human orientation, but use provider + session ID
  + working directory for exact lookup.
- Either peer may initiate a request. `caller` and `callee` in the CLI are
  per-request direction labels, not permanent roles.
- A normal delegation is read-before-work: the callee reads the caller's
  latest persisted native transcript before acting. This is a prompt-level
  protocol, not hidden shared context; make the exception explicit when the
  user requests a context-free task.
- Only one process should write a given native session at a time.
- Native CLI calls can modify files, use configured Tools and Skills, and
  consume the provider's normal account/model quota.
- Do not enable legacy mailbox or provider hooks for ordinary peer context.
  The legacy `pair_sync.py` path remains disabled by default and is not part of
  this skill's normal workflow.
- Do not claim that the two providers share hidden context. They share only
  explicitly readable persisted progress and task instructions.
