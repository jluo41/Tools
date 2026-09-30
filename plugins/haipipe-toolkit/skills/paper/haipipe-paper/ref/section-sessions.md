# Section sessions · one Claude session and one Codex thread per Section

`/haipipe-paper sessions [paper]` gives every Section its own named Claude Code
session and its own named Codex thread, paired, so each Section is written,
checked and messaged in its own context on either provider. Run it once the
Story's §8 Section Narrative has fixed the Section structure; before that there
is nothing stable to own.

## When

1. The Story page carries its `haipipe:compile-order` block (§8 is settled).
2. Every Section Page folder exists under `B?-<desk>-Main/` and `B?-<desk>-Appendix/`.
3. Rerun after a Section Page is added; live sessions are kept, existing pairs are bound.

## Units: what one session owns

```text
Main Section Page      one unit per page       <Short>-<page id>
Appendix group         one unit for all pages  <Short>-Appendix        --appendix one (default)
                       or one per page         <Short>-<page id>       --appendix each
```

The appendix defaults to ONE unit (JL 260928): appendix pages are small and
coupled. They share letters and table numbers, and their rulings cross pages
(withdrawing one appendix renumbers the rest and edits its neighbours), so one
session makes those changes in one pass. A folded or not-compiled page still
belongs to its unit.

## What it does

Run it from the repository root with the workspace Python; the script lives in
this skill's `scripts/` folder:

```text
.venv/bin/python <this skill>/scripts/create_section_sessions.py <paper-root> [--prefix <Short>]            plan only
.venv/bin/python <this skill>/scripts/create_section_sessions.py <paper-root> [--prefix <Short>] --apply    create
    [--providers claude,codex]  default both; or one of them
    [--appendix one|each]       default one
    [--pages <page id> ...]     only the units holding these pages
    [--replace]                 new sessions even where live ones exist
    [--codex-map FILE]          bind existing Codex threads: '<unit> <thread id> [name]'
    [--keep-running]            skip the stop after the first turn
```

For each unit it:

1. **Claude**: starts `claude --bg -n <Short>-<unit>` from the repository root with a read-only first turn, writes the UUID into each page header's `session:` line, and stops it once that turn is idle, because `/resume` refuses a running background session;
2. **Codex**: starts a thread through `codex app-server`, names it `<Short>-<unit>-Codex` with `thread/name/set`, runs the same first turn, and writes its id into each page header's `codex-session:` line;
3. **Pair**: registers an identity-only call-peer pair `<Short>-<unit>` (sync off).

A Claude session counts as the unit's own only when its saved name is exactly
`<Short>-<unit>`. A page copied from a predecessor paper keeps that paper's
`session:` line; the plan names it (`is '<name>', not this unit`) and creates a
new session instead of pairing a new Codex thread to someone else's. An owned
session that is already paired to a Codex thread is bound, not duplicated. To
carry a predecessor's Codex threads over on purpose, list them in `--codex-map`. Before creating Codex threads, look for ones the paper already has (search the thread names in `~/.codex/session_index.jsonl`) and bind them with `--codex-map`. An Appendix whose pages each already have their own Codex thread keeps them: each page header names its own `codex-session:`, each gets a pair `<Short>-Appendix-<letter>` with the one Appendix Claude session, and the plan shows `one per page` instead of creating a new thread. Codex threads are made through the app-server on purpose: a
`codex exec` thread is `exec`-sourced, so the Codex app never lists it and the
CLI cannot name it. An app-server thread is listed under its name.

## Naming

`<Short>` names the paper in two or three words (`AgreeableRx`), distinct from
every other paper's prefix in the workspace; the unit names the Section. The
first `--apply` records it in `board.md` as `session-prefix:`, later runs read it
from there, and a different `--prefix` is refused so one paper never ends up
with two naming schemes. Together they pass the stranger test in the `/resume` picker, in
`claude agents`, and in the Codex app: `AgreeableRx-S-MISQ-Main-1-Introduction`,
`AgreeableRx-Appendix-Codex`. The page header lines `session:` and
`codex-session:` are the binding; the Paper Workbench's Narrative view reads
them and shows each Section's Claude session and Codex thread.

## The first turn's scope rules

Every session starts with the same five rules, written into its first prompt:

1. write only inside its own page folder (the Appendix unit: the Appendix group folder); list other pages' problems, never fix them;
2. never edit `Tools/`, `code/`, the Story page, or the paper-level `delivery/` unasked;
3. never start a compute or regression Run unasked;
4. load `haipipe-paper-section` (and `haipipe-page`) before any edit;
5. while the author has a Run open, edit only the Draft file `draft/<stem>-draft-v<N>.md`; Page Content, logs, receipts, `results/` and delivery wait for the close.

## Talking to Section sessions afterwards

```text
provider · state          how a message reaches it
Claude · open             SendMessage to its name
Claude · stopped          claude --bg --resume <uuid> "<message>", then claude stop <id> when idle
Codex                     call-peer START_OR_RESUME_PEER with the unit's pair name
```

A background Claude session cannot edit the shared checkout (the harness
requires a worktree, and a worktree lacks uncommitted `draft/` files), so a
background turn is for reading and reporting. Work that edits a page is done
after the author opens that session with `/resume`.

Route a cross-page ruling to the owner of each affected unit, once, with the
exact lines; the owner applies it inside its own folder.

## Not in scope

The command creates no Page, Run, Result or receipt and never decides which
Section exists: §8 does. Pairing is identity-only (`sync` stays off); reading a
peer's history is the call-peer skill's `READ_EXISTING_PEER`.
