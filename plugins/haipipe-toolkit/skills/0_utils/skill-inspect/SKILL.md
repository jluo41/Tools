---
name: skill-inspect
description: >-
  Inspect one skill family (or one skill), two modes. INVENTORY (default):
  the skills it holds, the folder tree its contracts declare, and against a
  target folder what exists, is missing, or is extra. SCORE (--score): the
  five-class quality tables (DOOR, MACHINE, CONTRACT, LIBRARY, CRAFT), each
  class on its own columns, static score beside dynamic field record, a row
  with no field record provisional — absorbed from skill-set-status 260831.
  Read-only; the report is the deliverable; field-test stays the sibling that
  proves a rewrite RUNS cold. Trigger: skill inspect, inspect the skill set,
  expected structure, family inventory, skillset status, family status,
  score the contracts, contract audit, review this skill, /skill-inspect.
argument-hint: "<family-folder | skill-name> [--target <folder to diff against>]"
allowed-tools: Bash, Read, Grep, Glob, Skill
metadata:
  version: "0.2.0"
  last_updated: "2026-08-31"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /skill-inspect · what this family is, and what it would put on disk

Two modes, two questions, one skill (JL 260831 merged skill-set-status in):
INVENTORY asks WHAT IS HERE and WHAT WOULD APPEAR — the four-section report
below; SCORE asks HOW GOOD each member is — the five-class tables in
`ref/score-classes.md` (classify by what a skill OWNS; static score beside
dynamic field record; no field record ⇒ `(provisional)`; read every file in
full, never score from memory; the result lands in the family's README under
`Family status`, dated, with the regenerating command). `field-test` stays
the sibling that proves a rewrite RUNS cold.

## ⚡ Brief

```text
Q        which skills does this family hold, what folder tree do their
         contracts declare, and how far along is <target> against it?
READS    every SKILL.md frontmatter in the family folder · the family's
         structure authority (see the table below) · the target folder
WRITES   nothing; the report is the reply (save it only where the caller
         names a path)
OUTPUT   the four-section outline below, always in that order, real names
         only, one line per fact
```

## 🧾 The report · four sections, fixed order

```text
## ① The skills
- <name> · <version> · <class> — <one line from its own description>
     class ∈ DOOR · MACHINE · CONTRACT · LIBRARY · CRAFT (skill-set-status §🗂;
     classify by what the skill OWNS, not where it sits)

## ② The expected structure
one fenced tree: every folder and file the family's contracts DECLARE a
consumer would create, each line ending with the skill that declares it.
Read declarations from the structure authority, never inferred from examples.

## ③ Status against <target>          (only when --target is given)
- ✅ <path> — exists, matches the declaration
- ⬜ <path> — declared, absent (normal when the lane is unused: say which)
- 🎈 <path> — on disk, no contract declares it
- one closing line: versions read · last CHANGELOG date · instance count
  (how many real folders of this shape exist under the repo)

## ④ Gaps
- declared-unshipped: a contract names a folder/skill nothing ships
- shipped-undeclared: a skill or folder present with no declaring row
```

## 📚 Where each family's structure truth lives

```text
family        the declaration to read                       never read instead
──────────────────────────────────────────────────────────────────────────────
board page    haipipe-plugin/ref/roster.md (the lane table) a live page's folder
              + haipipe-page §📁 + plugin-outline ref/record-shape.md
page types    cli/pagetypes.py output (owner · key · engine) the folder names alone
task          haipipe-task ref/task-structure.md +           one job's habit
              ref/hierarchy.md (b/j/t/r grammar)
paper·app     the family door skill + its page-types/        sibling papers
0_utils       each SKILL.md's own Files section              (no shared tree)
```

A structure read off a live example instead of a declaration inherits that
example's drift; the diff in ③ is exactly where declaration and example are
allowed to meet.

## 🔒 Rules

- **Writes nothing, fixes nothing.** A gap found here is reported with the
  file that should change; the fix runs under that file's own skill.
- **Real names only**: the skill's `name:`, the folder's literal path, the
  version string as printed. A coined word for a class of thing is defined
  inline the first time (`/claude-response-format` owns the reply shape).
- **A missing lane is not a finding by itself**: page lanes are created only
  when used (haipipe-page §📁); ⬜ rows say "unused" unless a contract makes
  the folder mandatory (outline/ on any worked page; workflow/ in a job).
- **Version + date come from frontmatter and CHANGELOG**, never from git
  blame; an instance count comes from one glob stated in the report.

## 📏 SCORE mode · --score

Load `ref/score-classes.md` and follow it whole: enumerate, classify into the
five classes, read each SKILL.md in full this session, gather every mechanical
fact by command (versions, routes, `pagetypes.py` inventory through the
population law, instances from REAL boards only, gates fired from Log rows,
sizes as `<SKILL.md chars>/<desc chars>`), emit the class tables plus the top
two knife points, and stamp the result into the family README. A single-skill
call scores that one row on its class's columns.

## 📂 Files

```text
skill-inspect/
├── SKILL.md               this method
├── ref/score-classes.md   the five classes, columns, size and population laws
└── CHANGELOG.md           version history
```

Owns no scripts yet; when the walk is mechanized it becomes one `cli/` script
here, proven to fail first on a family with a known gap. Sibling: `0_utils/field-test`; the reply shape is `0_utils/claude-response-format`.
`skill-set-status` merged in 260831 and rests in `0_utils/_old/`.
