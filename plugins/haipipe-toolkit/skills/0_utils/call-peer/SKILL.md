---
name: call-peer
description: >-
  Work with paired native Claude Code and Codex sessions through two explicit
  modes: inspect an already registered peer read-only, or explicitly create,
  resume, and message the other provider.
metadata:
  version: "1.6.0"
  last_updated: "2026-09-10"
---

# Call Peer

This skill has two different operations. Decide which operation the user
requested before using any provider CLI, app action, or pair helper.

~~~text
READ_EXISTING_PEER
    Read an already registered native transcript yourself.
    No Claude/Codex process, no resume, no new session, no message.

START_OR_RESUME_PEER
    Explicitly create or resume the other native provider and send a task.
    This may write a manifest, modify files, acquire a provider lock, and
    consume normal provider quota.
~~~

The pair is a relationship between two independent native sessions:

~~~text
pair_name
├── Claude native session
└── Codex native session
~~~

The pair manifest maps the relationship and stable session IDs. It does not
provide hidden shared context. Native transcripts, tools, Skills, permissions,
locks, and provider limits remain separate.

## Intent router: mandatory first step

Use the user's action verb, not merely the presence of the word "peer".

| User intent | Mode | Required behavior |
|---|---|---|
| read, inspect, review, look at, see what it did, current progress, latest status | READ_EXISTING_PEER | Read the persisted partner transcript directly; do not invoke a provider. |
| start, call, wake, ask, send, delegate, continue, have the peer do something | START_OR_RESUME_PEER | Verify the pair and explicitly call the native provider. |
| first read it, then ask it to do something | READ_EXISTING_PEER, then START_OR_RESUME_PEER | Complete the read-only phase first; only then perform the explicitly requested call. |
| ask Claude to read the Codex session, or ask Codex to read the Claude session | START_OR_RESUME_PEER | The target provider must be called to perform that read; this is different from the current agent reading the transcript itself. |
| create a new peer only so it can supply historical progress from a missing peer | READ_EXISTING_PEER | A new session has no old transcript. Return PAIR_NOT_REGISTERED; do not create a substitute. |
| ambiguous wording | READ_EXISTING_PEER | Choose the safe read-only interpretation and report what was found. Never start a provider merely to clarify. |

Examples:

- "读一下 Claude session 现在干了啥" means READ_EXISTING_PEER.
- "启动 Claude peer，让它读 Codex session" means START_OR_RESUME_PEER.
- "你自己读一下 peer，不要启动 Claude" is an explicit READ_EXISTING_PEER
  request and forbids all provider CLI calls.

## Pair identity and naming

Use one human-readable name for both sides. Never use a generic name such as
Call-Peer. Prefer the user's exact task or session name; otherwise derive a
recognizable name from the current task and workspace. For example:

~~~text
T01 C-data VisitLBP_1stPair
~~~

The wrapper forwards this exact name to Claude's native --name option.
Codex has no corresponding native name flag, so the manifest and session ID
are authoritative for Codex.

The pair registry is normally under:

~~~text
~/.config/haipipe/pairs/<pair-name-and-workspace>.json
~~~

Resolve a pair by exact pair name and resolved working directory. Do not
guess a manifest filename, infer a session ID from a display title, or reuse a
same-named pair from another workspace.

## READ_EXISTING_PEER: strict read-only procedure

This is the default for progress questions. It must not start a native
provider.

1. Resolve the existing manifest using the pair name and the exact resolved
   working directory. The read-only pair_sync.resolve_pair_session resolver
   may be used. Verify that the manifest's pair_name and cwd match.
2. Identify the partner provider and its registered session_id. Record the
   manifest path, provider, session ID, and snapshot time.
3. Locate the provider's persisted native transcript by exact provider and
   session ID:

   - For Claude, use the configured native Claude home
     (CLAUDE_CONFIG_DIR when set, otherwise ~/.claude) and locate the unique
     file named exactly <session_id>.jsonl under projects/. The existing
     native locator may be reused; do not search by display name.
   - For Codex, prefer the native Codex app's read-only thread reader when it
     is available, using the registered thread/session ID and host. Otherwise
     inspect exact-ID rollout files under the configured Codex sessions home
     (CODEX_HOME when set, otherwise ~/.codex/sessions).
   - Codex forks can leave multiple rollout files containing the same original
     thread ID. Do not choose the first glob result. Compare their persisted
     event times and lineage, read the newest relevant snapshot, and report
     ambiguity if the files cannot be joined confidently.

4. Read only persisted content. If the provider is currently active, report
   that the result is a snapshot and include its last persisted timestamp.
5. Summarize:

   - current goal;
   - decisions and completed work;
   - files or artifacts changed, if visible in the transcript;
   - open questions, blockers, and next steps;
   - what cannot be observed because it is hidden context, unpersisted work,
     or an inaccessible native store.

6. End the report with an explicit safety line:

~~~text
Provider call: none.
New/resumed session: none.
Files/manifests/transcripts changed: none.
~~~

### Prohibited during READ_EXISTING_PEER

Do not run or call any of the following:

- claude, codex, run_paired_cli.py, or run_cli_agent.py;
- --resume, --continue, --last, or --new-session;
- a message/send operation to either peer;
- transcript normalization, including changing Claude's sdk-cli entrypoint
  marker;
- manifest registration/update, mailbox synchronization, or pair repair;
- lock deletion, stale-process termination, or any attempt to unlock a peer.

If the manifest is missing, return PAIR_NOT_REGISTERED. Do not create a pair
as a side effect of a read request. If a transcript is missing or ambiguous,
return that limitation instead of starting the provider to obtain a summary.

## START_OR_RESUME_PEER: explicit provider-call procedure

Use this mode only when the user explicitly asks to start, call, resume, ask,
send, or delegate to the other peer.

### Preflight

1. Resolve the exact current working directory and choose a task-specific
   pair_name. Do not use Call-Peer.
2. Determine the current caller's real native session ID. Pass it explicitly
   as --caller-session-id; do not rely on an inherited environment value or
   on the registered manifest value.
3. If a manifest already exists, verify:

   - exact pair_name;
   - exact working directory;
   - caller provider and caller session ID match the current session;
   - callee provider is the opposite provider;
   - callee session ID is not the caller's own session ID.

   If the caller session does not match, stop and report
   PAIR_CALLER_MISMATCH. Do not silently resume the old pair or overwrite
   its caller entry.
4. If no manifest exists, create the partner only because the user explicitly
   requested START_OR_RESUME_PEER for a new, concrete task. A read lookup
   failure is never a reason to create one. In particular, do not create a new
   session merely to recover historical progress: the new session cannot have
   the missing peer's transcript.
5. Use --new-session only when the user explicitly asks for a fresh/new
   partner and the new pair name is deliberate. Do not create a duplicate
   because a lookup, picker, or resume was inconvenient.

### Normal paired command

Use the paired wrapper for ordinary cross-provider work:

~~~bash
.venv/bin/python Tools/plugins/haipipe-toolkit/skills/0_utils/scripts/run_paired_cli.py \
  --pair-name "<pair_name>" \
  --caller-provider <claude|codex> \
  --caller-session-id <current_caller_session_id> \
  --callee-provider <codex|claude> \
  --cwd /Users/jluo41/Desktop/Physician-SPACE \
  --prompt "<explicit task>"
~~~

The wrapper creates a first-use partner or resumes the registered partner by
exact session ID. It uses the provider's normal native home and may acquire a
provider lock. The pair name is for orientation; provider, session ID, and
working directory are the exact identity.

If the user asks the callee to understand the caller's work before acting,
include this precondition in the delegated prompt:

~~~text
First read the paired caller's persisted native transcript directly in
read-only mode. Understand its current goal, decisions, completed work, and
open questions. Do not call the caller, edit the transcript, or create a
second peer. Then perform the requested task and return the findings and
changes.
~~~

This prompt-level read-before-work rule is for a provider that has actually
been called. It must not be used as an excuse to call a provider when the
current user only asked this agent to read an existing transcript.

### Call result handling

- Claim a peer was established only when the native provider returns a
  complete response and a valid session ID.
- Preserve and report provider errors, timeouts, lock errors, session limits,
  quota limits, and reset times exactly when supplied.
- Never switch to an older pair with a different caller session.
- Never retry a failed call by creating duplicate sessions.
- After success, report the pair name, caller/callee providers, returned
  session ID, and any receipt/manifest path.

run_cli_agent.py is a lower-level direct native-call wrapper. It is not a
read operation and must not be used for READ_EXISTING_PEER. Use it only when
the user explicitly requests a direct provider call and the same identity and
resume checks have been completed.

## Transcript and transport boundaries

Ordinary peer calls are CLI-only and use the provider's normal native home,
configured model, Tools, Skills, permissions, and network behavior. Do not
use an Agent SDK, a custom provider home, a mirrored transcript, a hidden
mailbox, or a legacy synchronization hook for ordinary peer work.

The pair name does not synchronize turns. The two providers share only the
persisted transcript that one side is explicitly instructed and authorized to
read. They do not share hidden system context, private reasoning, active
in-memory state, or text that has not been persisted.

Only one process should write a given native session at a time. A read-only
inspection may proceed from persisted content while a provider is active, but
it must be labeled as a snapshot. Do not kill a process or edit a lock from
this skill.

## Compact return formats

For READ_EXISTING_PEER:

~~~text
Mode: READ_EXISTING_PEER
Pair: <pair_name>
Partner: <provider> / <session_id>
Snapshot: <timestamp or unavailable>
Current goal: ...
Completed: ...
Open/blocking: ...
Next: ...
Provider call: none.
~~~

For START_OR_RESUME_PEER:

~~~text
Mode: START_OR_RESUME_PEER
Pair: <pair_name>
Caller: <provider> / <session_id>
Callee: <provider> / <session_id>
Result: <completed | failed | timed out | provider limit>
Summary: ...
Receipt/manifest: ...
~~~
