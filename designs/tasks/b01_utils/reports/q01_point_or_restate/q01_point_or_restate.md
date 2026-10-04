# Point to a skill or restate it
state: 🟡 DRAFT · written from the skill's change history; CHECK pending
content: draft v0.1 · adopted 261002 2350
answers: Q01
answer-status: answered
results-read: 2026-10-02T23:50:55-04:00

## Opening

Point to it. An instruction file names the skill and its path and keeps none of its rules, because a restated copy goes stale each time the skill changes: response-format changed 8 times on 2026-10-02 alone.

**Where this Page sits:** [Q01 · Should an instruction file such as AGENTS.md restate a skill’s rules, or only point to the skill?](../../board.md).

**Why it matters:** Every instruction file that copies a skill's rules becomes a second, drifting version of that skill.

## Content

### 1 · Answer

An instruction file should point to the skill and not restate its rules; the SPACE's AGENTS.md rule 5 is now the one line "Chat replies: load `/response-format` and follow it", with the skill's path. <!-- realizes: C1.P1.B1 -->
A restated copy goes stale whenever the skill changes, and response-format changed 8 times on 2026-10-02 alone, out of 21 recorded versions. <!-- realizes: C1.P1.B2 -->
The pointer still names the skill's folder, so a session that cannot run a slash command can open the file directly. <!-- realizes: C1.P1.B3 -->

### 2 · Evidence

The format itself lives only in the skill ([response-format SKILL.md](../../../../../plugins/haipipe-toolkit/skills/0_utils/response-format/SKILL.md)). <!-- realizes: C2.P2.B1 -->
Its version history, with 8 versions dated 2026-10-02, is in [response-format CHANGELOG.md](../../../../../plugins/haipipe-toolkit/skills/0_utils/response-format/CHANGELOG.md). <!-- realizes: C2.P2.B2 -->

### 3 · Limits

A pointer works only if the session actually loads the skill; nothing checks that it did. <!-- realizes: C3.P3.B1 -->

### 4 · Next

Apply the same rule to every instruction file that names a skill (AGENTS.md, CLAUDE.md, project instructions): name the skill and its path, and keep its rules in the skill. <!-- realizes: C4.P4.B1 -->
