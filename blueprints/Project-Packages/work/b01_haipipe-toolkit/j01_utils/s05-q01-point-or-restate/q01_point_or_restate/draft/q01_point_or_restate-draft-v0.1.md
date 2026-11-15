# q01_point_or_restate · draft v0.1
draft-version: v0.1
supersedes: none
date: 261002
approved: ⬜
status: working · written from the skill's change history in run-section
arc: A skill changes too often for a restated copy to stay true, so instruction files only point to it.

## 1 · Structure · Bullet Point Table

### Structure Overview

- C1 · Answer
- C1.P1 · Point, do not restate
- C2 · Evidence
- C2.P2 · The skill and its history
- C3 · Limits
- C3.P3 · What a pointer cannot do
- C4 · Next
- C4.P4 · The rule going forward

### C1.P1 · Point, do not restate
- B1 · [Answer] Instruction files point to a skill, never restate it.
  Note: Settled when AGENTS.md rule 5 became one line.
  Evidence: none · reads the files linked under Evidence
- B2 · [Reason] A copy drifts every time the skill changes.
  Note: response-format version count on one day.
  Evidence: none · reads the files linked under Evidence
- B3 · [Detail] The pointer keeps the path for path-only sessions.
  Note: Sessions that cannot run a slash command.
  Evidence: none · a scope statement, no new value

### C2.P2 · The skill and its history
- B1 · [Evidence] The skill is the one source of the format.
  Note: SKILL.md.
  Evidence: none · the sentence links its file
- B2 · [Evidence] Its change history shows the pace of change.
  Note: CHANGELOG.md.
  Evidence: none · the sentence links its file

### C3.P3 · What a pointer cannot do
- B1 · [Limit] A pointer relies on the session loading the skill.
  Note: Not enforced by any check.
  Evidence: none · a scope statement, no new value

### C4.P4 · The rule going forward
- B1 · [Next] Apply the same rule to other instruction files.
  Note: AGENTS.md, CLAUDE.md, project instructions.
  Evidence: none · a scope statement, no new value

## 2 · Scratch · What to write here

### C1.P1 · Point, do not restate

### C2.P2 · The skill and its history

### C3.P3 · What a pointer cannot do

### C4.P4 · The rule going forward

## 3 · Draft · Reading and Revise

### C1.P1 · Point, do not restate
- B1 · An instruction file should point to the skill and not restate its rules; the SPACE's AGENTS.md rule 5 is now the one line "Chat replies: load `/response-format` and follow it", with the skill's path.
- B2 · A restated copy goes stale whenever the skill changes, and response-format changed 8 times on 2026-10-02 alone, out of 21 recorded versions.
- B3 · The pointer still names the skill's folder, so a session that cannot run a slash command can open the file directly.

### C2.P2 · The skill and its history
- B1 · The format itself lives only in the skill ([response-format SKILL.md](../../../../../plugins/haipipe-toolkit/skills/0_utils/response-format/SKILL.md)).
- B2 · Its version history, with 8 versions dated 2026-10-02, is in [response-format CHANGELOG.md](../../../../../plugins/haipipe-toolkit/skills/0_utils/response-format/CHANGELOG.md).

### C3.P3 · What a pointer cannot do
- B1 · A pointer works only if the session actually loads the skill; nothing checks that it did.

### C4.P4 · The rule going forward
- B1 · Apply the same rule to every instruction file that names a skill (AGENTS.md, CLAUDE.md, project instructions): name the skill and its path, and keep its rules in the skill.
