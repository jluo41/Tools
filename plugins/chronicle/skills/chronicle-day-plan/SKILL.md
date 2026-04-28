---
name: chronicle-day-plan
description: Morning my-task planner. Pulls yesterday's takeaways, overnight emails, and git state as PROMPTS; then walks the user through 3 my-task buckets (paper/project, agent/skill, relationship/career) with sharp Socratic questions; synthesizes today's plan as YYMMDD-plan.txt + YYMMDD-plan.excalidraw under ~/Daily/<date>/. Use when the user says "plan today" / "morning plan" / "/chronicle-day-plan" / "make today's plan".
---

# /chronicle-day-plan — Morning my-task facilitator

## What this skill does

This is a **human-attention router**, not a task tracker.

```
my-task     = work that needs YOUR judgment, taste, or relationships.
NOT-my-task = anything an AI loop, script, or scheduled job already does.
```

The skill's whole job is to make sure your scarce brain-time goes to the
my-tasks — and only the my-tasks. AI-handled work is invisible here.

## When to invoke

- ☀️ user says "plan today" / "morning plan" / "做今天的计划" / `/chronicle-day-plan`
- 🔄 second invocation same day → ask: amend (re-render) or skip
- ⛔ never auto-trigger — plans are intentional, not automatic

## The three my-task buckets

```
🧠 paper / project          research output + project moves
                             (paper drafts, posters, grants, decks, project work)

🛠 agent / skill design     ARIS, agents, skills, infra design choices
                             (new skill, refactor, design discussion)

🤝 relationship / career    job search, networking, external comms,
                             follow-ups, coffee chats, mentor touches
```

If a bucket has nothing today → it's skipped. Empty buckets don't go in
the plan. Three sharp items beats fifteen vague ones.

## The four phases

```
PHASE 1 — PRE-BRIEFING   (silent — context is FUEL for prompts, not output)
PHASE 2 — SOCRATIC LOOP  (sharp questions per bucket, one at a time)
PHASE 3 — SYNTHESIZE     (cluster answers → 3-5 my-tasks max + the one bet)
PHASE 4 — WRITE          (txt + excalidraw + git sync)
```

---

### PHASE 1 — Pre-briefing (silent context pull)

Before asking a single question, gather:

| Source | Where | Use as |
|---|---|---|
| Yesterday's session txts | `~/Daily/<yesterday>/*.txt` | seed prompts for carryover thinking |
| Yesterday's takeaways | extract `─§ Takeaway ──` sections | seed "what did you decide to do next?" |
| Recent emails (last 7d) | `chronicle-email` recent-window mode | seed "anyone owed a real reply?" |
| Git state | `git status`, `git branch -vv`, `gh pr list` | seed "any half-done thread to land?" |

Read these but **do not surface as a checklist**. They are ammunition for
the sharp questions in Phase 2. The user should feel the briefing is
informed, not exhaustive.

**Email pull (concrete recipe)**

Call `mcp__ms365__list-mail-messages` directly:

```
filter:  receivedDateTime ge {today − 7 days}T00:00:00Z
orderby: receivedDateTime desc
select:  id,subject,from,receivedDateTime,bodyPreview,isRead,hasAttachments
top:     15
```

Then classify per `chronicle-email` recent-window rules (⭐ needs-reply,
📋 fyi-internal, 💸 financial, drop newsletters/security). Use the
**⭐ needs-reply** group as the seed for the relationship/career bucket
("you've got 4 emails awaiting a real reply — which one needs YOU today?").

**Auth fallbacks**:

```
1. Token cached in Keychain   → silent, no prompt
2. mcp__ms365__verify-login fails → tell user to /chronicle-email-login
                                     (or run mcp__ms365__login → device code)
3. CA-blocked / can't auth      → degrade gracefully: skip email seed,
                                   continue with sessions + git state only.
                                   Surface ONE-LINE warning, not a tutorial.
```

---

### PHASE 2 — The Socratic loop (sharp prompts, not gentle ones)

Walk the buckets one at a time. **Tone: sharper, not gentler.** The whole
point is to surface things the user would otherwise drift past.

**Per-bucket pattern**:

```
1. Lead with a SPECIFIC prompt drawn from Phase 1 context
   ("Your YYYY-MM-DD takeaway said you'd <X>. Did you?")
2. Force a concrete commit: "what's the ONE move today?"
3. If user says "nothing" → push once, then accept and move on
   ("really nothing? <name a stale thread from context>?")
```

**Sharp prompt examples per bucket** (use as inspiration, not literal text):

```
🧠 paper / project
  ─ "What's the ONE paper move that's been sitting >3 days untouched?"
  ─ "Yesterday you said <takeaway X>. What's the next concrete move?"
  ─ "Any reviewer/co-author waiting on YOU? Name them."
  ─ "What figure or claim will you defend out loud this week?"

🛠 agent / skill design
  ─ "What design decision are you avoiding because it's hard?"
  ─ "Any skill you've drafted in your head 3+ times but not built?"
  ─ "Where's the friction in your current loop — what's costing 10 min/day?"
  ─ "What's the ONE design discussion you owe yourself today?"

🤝 relationship / career
  ─ "Who haven't you talked to in 2+ weeks that matters?"
  ─ "Any application/intro/recommendation you're sitting on?"
  ─ "What's the email that's been in your head, unsent, for 3 days?"
  ─ "Who needs a 10-min call from you, not a Slack?"
```

**Anti-pattern guard** — if you catch yourself writing:

- "Let me know what you'd like to focus on" → too gentle, redraft
- "Here are some options for today" → menu, not Socratic, redraft
- A bullet list of *suggestions* → you're doing the user's thinking, redraft

---

### PHASE 3 — Synthesize

After all three buckets, cluster the user's answers into:

```
Today's my-task plan
├─ 1-3 items per bucket (only buckets that produced something)
├─ exactly ONE "today's one bet" — the single highest-leverage move
└─ optional: rough time blocks (HH:MM → bucket) if user wants
```

Hard cap: **5 total my-task items across all buckets**. If the user lists
more, force them to cut. The skill's value is the cut, not the capture.

---

### PHASE 4 — Write

Draft `YYMMDD-plan.txt` using `diagram-ascii` primitives, preview in chat,
on confirm run `bin/plan.sh` to write + render + commit + push.

## Required `.txt` template

```
☀️ <YYYY-MM-DD> · 🏷️ day-plan
═══════════════════════════════════════════

─§ Today's one bet ──
  ┌───────────────────────────────────────┐
  │ 🔑 single sentence — the highest-     │
  │    leverage move of the day           │
  └───────────────────────────────────────┘

─§ My-task swim-lanes ──
  ┌─ 🧠 paper/project ──┬─ 🛠 agent/skill ──┬─ 🤝 relationship ──┐
  │ • item 1            │ • item 1          │ • item 1            │
  │ • item 2            │                   │ • item 2            │
  └─────────────────────┴───────────────────┴─────────────────────┘

─§ Time blocks (optional) ──
  +-------+--------------------------------+
  | HH:MM | block / output                 |
  +-------+--------------------------------+
  | 09:00 | paper move — fig 3 redraft     |
  | 11:00 | comms — reply to <name>        |
  | 14:00 | skill — design Y               |
  +-------+--------------------------------+

─§ Carryover (if any) ──
  ⏳ items pulled forward from yesterday — keep brutally short

─§ Takeaway ──
  🔑 one-sentence framing of what today is REALLY about
```

**Style rules**:

- 🌐 English by default (quote user verbatim if they spoke another language)
- 🎨 every section is a diagram, not a bullet list (bullets only inside cells)
- 🪧 use `─§ Title ─` dividers (canvas tool splits on these)
- 🔑 the "one bet" and "Takeaway" sections are mandatory; everything else
  is optional and gets dropped if empty

## Idempotence — second invocation same day

```
if exists(<date>/<YYMMDD>-plan.txt):
    ask user: "Plan exists. (a) amend & re-render, (b) skip, (c) overwrite?"
```

Default behavior: **prompt, never silently overwrite**. Plans capture
intent — silently rewriting them defeats the point.

No `.closed`-style sentinel needed. Plans are open all day.

## Sync workflow (use the bin script — don't reimplement)

```
chronicle-day-plan/bin/plan.sh < plan-content.txt
```

Internals (see `bin/plan.sh`):

```
1. cd ~/Daily
2. git pull --rebase --autostash      (no-op if no remote)
3. resolve target date = today
4. write to <date>/<YYMMDD>-plan.txt   (atomic via tmp + mv)
5. run txt-to-canvas.py <txt> --out <date>/<YYMMDD>-plan.excalidraw
6. git add + commit -m "plan(<date>): <one-bet slug>"
7. git push (retry once on rejection)
```

If `<YYMMDD>-plan.txt` already exists, the script refuses unless
`--force` is passed (the conversational layer is responsible for the
amend/skip/overwrite prompt).

## How Claude actually authors the plan

1. **Phase 1**: silently read yesterday's txts, query MS365 for last 24h,
   run `git status` / `gh pr list`. Don't surface raw output to user.
2. **Phase 2**: walk the three buckets with sharp Socratic prompts.
   One bucket per turn — wait for the user's answer before moving on.
3. **Phase 3**: synthesize into ≤5 my-tasks + exactly one "today's bet".
4. **Phase 4**: draft the `.txt` as a fenced block in chat, get ✅,
   then pipe to `bin/plan.sh`.

## What this skill does NOT do

- ❌ Track AI-handled work (auto-runs, scheduled jobs, ARIS loops)
- ❌ Manage a multi-day backlog — today is today; carryover is one section, max
- ❌ Edit prior days' plans — write-once, like sessions
- ❌ Replace `chronicle-session` (that's the per-session log) or
  `chronicle-daily` (evening rollup)

## Sister skills

- `chronicle-session` — per-session log writer (during the day)
- `chronicle-daily` — evening rollup of session canvases (end of day)
- `chronicle-email` — monthly email index (Phase 1 fallback source)
- Underlying renderer: `diagram-ascii-canvas/bin/txt-to-canvas.py`
