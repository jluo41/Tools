---
name: chronicle-session
description: Log the current Claude Code session as a concise YYMMDD-HHMM-<slug>.txt under ~/Daily/YYYY-MM-DD/, then sync to the private jluo41/Daily git repo (pull --rebase → commit → push). Use when a working session ends OR on the user's explicit "log this session" request. The .txt is the input to chronicle-daily's evening rollup. Day-close aware — if today's folder has `.closed`, write to tomorrow instead.
---

# /chronicle-session — Per-session log writer

## What this skill does

At the end of a working session, write **one** concise `.txt` file into
`~/Daily/<date>/` and sync it to `github.com/jluo41/Daily`. The file is
the unit of truth for that session — `chronicle-daily` later rolls all
of a day's `.txt` files into one Excalidraw canvas.

## When to invoke

- 🛑 Stop hook fires at end of a Claude Code session
- 🧑 user says "log this session" / "/chronicle-session" / "记录一下这次"
- 📦 wrapping up a discrete piece of work that should be findable later

**Do NOT invoke** mid-session for trivial sub-tasks. One session = one log.

## File format

```
~/Daily/YYYY-MM-DD/YYMMDD-HHMM-<slug>.txt
                   ▲▲▲▲▲▲ ▲▲▲▲
                   date   write-time (24h, local) — lexical sort = chronological
```

- `<slug>`: 2–4 hyphenated words naming the topic (e.g. `ref-repo-agent-stack`, `voice-bot-debug`). Derive from the most concrete noun phrase in the session, not the verb.
- `YYMMDD` matches the parent folder's date.
- `HHMM` is the moment `write-session.sh` runs, NOT the session start. Sessions logged later in the day sort later — what we want.

## Authoring rule: diagrams, not bullets

**This skill defers content authoring to `diagram-ascii`.** Every section
must be an ASCII diagram, not a bullet list. Bullets are allowed only
inside a diagram cell (e.g. a table row), never as the section body.

Before drafting the `.txt`, mentally pick the right diagram primitive
from `diagram-ascii` for each section:

| Section | Recommended primitive | From diagram-ascii |
|---|---|---|
| What shipped | annotated folder tree | "Folder tree — annotated" |
| Flow / architecture | pipeline (left→right or top↓) | "Pipeline" / "Layered" |
| Decisions | comparison or decision table | "Table" |
| X vs Y comparison | side-by-side boxes + tagline | "Contrast / reversal" |
| Cumulative progress | progress tracker | "Progress tracker" |
| Takeaway | one boxed callout, ≤ 3 lines | (free form) |

If you catch yourself writing `• something` as the body of a section,
stop and convert it to one of the primitives above.

## Required `.txt` template (concise — 3-4 sections, each is a diagram)

```
💻 <platform> · 🕐 HH:MM-HH:MM · 🏷️ <slug>
═══════════════════════════════════════════

─§ What shipped ──
  <annotated folder tree showing files/folders touched>
  <or a pipeline if the work was a flow>

─§ Flow / architecture (optional) ──
  <pipeline or layered diagram of the new behavior>

─§ Decisions ──
  +---------+---------+
  | Topic   | Choice  |
  +---------+---------+
  | ...     | ✅ ...  |
  | ...     | ⏳ ...  |
  +---------+---------+

─§ Takeaway ──
  🔑 single-sentence takeaway, boxed if it deserves it
```

**Style rules**:

- 🌐 **English by default** — section titles, prose, slugs, commit msgs.
  Quote the user verbatim if they spoke another language; otherwise English.
- 🎨 **diagrams > bullets**: every section is a diagram. Heavy emoji per
  the diagram-ascii palette (every box, header, label, status).
- ≤ ~12 lines of diagram per section; whole file should fit on one screen.
- Use `─§ Title ─` dividers (canvas tool splits on these — see
  `diagram-ascii-canvas`).
- The "Takeaway" section is mandatory — it's the next-day-reader's scan target.
- See `diagram-ascii` SKILL for the full primitive library.

## Day-close check

Before writing, decide the target date:

```
target_date = today
if exists(~/Daily/<today>/.closed):
    target_date = today + 1 day      # day already finalized; write to tomorrow
mkdir -p ~/Daily/<target_date>/
```

This keeps post-rollup work from polluting the closed day.

## Sync workflow (use the bin script — don't reimplement)

```
~/Daily/.bin/  →  symlink to bin/write-session.sh
   OR  call directly:
   chronicle-session/bin/write-session.sh <slug> < session.txt
```

Internals (see `bin/write-session.sh`):

```
1. cd ~/Daily
2. git pull --rebase --autostash       (handles unstaged work safely)
3. determine target_date (today vs tomorrow if .closed)
4. write file to <target_date>/<filename>.txt
5. git add <new file>
6. git commit -m "session(<date>): <slug>"
7. git push                              (retry once on rejection:
                                          git pull --rebase; git push)
```

If the remote isn't configured yet, the script logs and skips push.

## How Claude actually authors the .txt

Claude writes the .txt content to stdin of the script. Workflow:

1. **Outline** what was done, decided, and is worth remembering.
2. **Pick a diagram primitive** for each section from `diagram-ascii`'s
   library (folder tree, pipeline, table, contrast, progress tracker).
   If you can't think of one, the section probably doesn't deserve to
   exist — drop it.
3. **Draft** the `.txt` content directly in the chat as a fenced block,
   using only diagram-ascii primitives. NO plain bullet sections.
4. **Show the user the preview** in chat for ✅ / ✏️ feedback.
5. On user confirm, run `bin/write-session.sh <slug>` piping the content.

If the user invokes via Stop hook (no human-in-loop), skip step 4 and
just write + push.

**Anti-pattern check** — before showing the preview, scan it:

- ❌ section body is a bullet list with no boxes / trees / arrows → redraft
- ❌ all sections are the same shape (e.g. all tables) → mix primitives
- ❌ no `─§` dividers between sections → the canvas can't split it
- ✅ each section's primitive is visibly different from its neighbors

## What this skill does NOT do

- ❌ Build the canvas — that's `chronicle-daily`
- ❌ Read transcripts — Claude has the conversation in context already
- ❌ Multi-platform collection — each platform calls this skill (or its
     CLI script) on its own; this skill assumes "the current session"
- ❌ Edit prior sessions — append-only, by design

## Sister skill

- `chronicle-daily` — 22:00 rollup, builds the canvas, writes `.closed`
