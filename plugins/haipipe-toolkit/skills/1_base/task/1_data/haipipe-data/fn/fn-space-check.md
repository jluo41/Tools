fn-space-check: Is this SPACE up to date?
==========================================

Read-only check of one SPACE against the haipipe-data migration notes
(`ref/migration.md`). It says, item by item, whether the SPACE is up to date,
behind, or at risk, with the evidence and the exact next step. It never pulls,
cherry-picks, writes, builds or cooks. The person makes the change by
following the note, then runs the check again.

---

When
====

- A SPACE pulled a new Tools (skills changed; is its `code/` still right?).
- Before setting `fn_version:` in any Run config.
- Something loads the "wrong" Fn, or an endpoint behaves unlike local.
- The cross-stage dashboard runs the brief form automatically.

---

Run
===

From the SPACE root (the folder holding `code/` and `examples*/`). Resolve
`<skill>` to this skill's directory (the folder of the loaded SKILL.md,
following symlinks).

```bash
python3 <skill>/cli/space_check.py            # full report
python3 <skill>/cli/space_check.py --brief    # one line, for the dashboard
python3 <skill>/cli/space_check.py --root /path/to/OTHER-SPACE
```

Stdlib only, no network. The Tools line reads what the last `git fetch` saw;
suggest `git -C Tools fetch` when the person wants it current.

---

What it checks
==============

```
item                       RISK / BEHIND when
-------------------------  ------------------------------------------------------------
Tools                      the checkout is behind its remote (last fetch)
code: fn_dir               code/ has no haipipe.base.fn_dir (predates Fn versions)
code: loaders              a Source/Record/Case loader does not call fn_dir (partial update)
trap: fn_version ignored   a Run config sets fn_version: but code/ cannot honour it (RISK:
                           it silently loads the flat Fns)
haifn: <version>           a version folder is missing from fn_source, fn_record or fn_case
config -> version          a Run config names a version that is not built
dataset <project> j5N      the b01-b03 Runs of one dataset Job disagree on fn_version
code: external bundle      external_base cannot load pre-keyed versions (key_normalized)
aidata Block               BEHIND: a Project still has a b04_*aidata* Block (AIData is b10)
code: checkout             INFO: checked-out code/ differs from the commit the SPACE pins,
                           or has uncommitted edits
```

Status words: `OK` up to date, `BEHIND` an update is available, `RISK`
something runs wrong today, `INFO` worth knowing, `N/A` does not apply.
`overall` is the worst of RISK > BEHIND > OK.

---

Report
======

1. Run the full report and show it as printed (it has no data values: only
   paths, commit ids, version names and counts).
2. Lead with the RISK items, then BEHIND. For each, name the section of
   `ref/migration.md` that explains it and quote its `next:` step.
3. Never run a `next:` step yourself as part of the check. Offer it; apply it
   only when the person asks, as a separate action (a `code/` update may
   conflict on a SPACE's own branch: stop and show the conflict).
4. After the person has made a change, run the check again and confirm.

Specialist tail:

```
status:    ok
summary:   SPACE <name>: overall <OK|BEHIND|RISK>; <n> RISK, <n> BEHIND items
artifacts: []
next:      the first RISK item's next step, else the first BEHIND's, else "-"
```

---

Adding a check for a new note
=============================

A change another SPACE must follow gets, in the same Tools commit:

1. a dated note in `ref/migration.md` (what changed, does anything break,
   steps), with a `Check:` line naming the space-check items that detect it;
2. those items in `cli/space_check.py`, detected from the SPACE itself
   (files, configs, git), never from a recorded state file;
3. a line in this doc's table.
