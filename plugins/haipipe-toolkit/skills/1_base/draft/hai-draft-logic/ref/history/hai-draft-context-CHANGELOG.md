## 0.4.1 · 2026-09-29 · outline/ to draft/ in current-layout prose (JL 260929)

- Paths that describe the current Page layout say `draft/`: the plan `draft/<stem>-draft-v<G>.<S>[.<E>].md`, records `draft/records/`, `draft/previous/`, `draft/skill/`, the Evidence Markdown `draft/<stem>-evidence-items.md`, `draft/evidence/bibex/` and `draft/evidence/materials/` (JL 260929: "it should be draft"). Mentions of legacy Pages, retired `outline/evidence/` lanes and the migration keep `outline/`, as do the OUTLINE stage, the Outline table and the `outline:` grammar key.

## 0.4.0 · 2026-09-28 · No content hashes (JL 260928)

- A Context source's freshness fact is its own version number and date, or its saved time (file
  time or last `git` commit); never a SHA-256. `ref/context-record.md` Sources read
  `version/date`. Stale means the source changed after the record (newer file time or `git diff`).

## 0.3.0 · 2026-09-22

- Moved to `skills/page/workflow-runs/`; the description leads with the Run (`Page.context`) and
  keeps the old 00 CONTEXT label as an alias.

## 0.2.1 · 2026-09-20

- Keep Context collection outside the Workflow Run list unless separately commissioned.

## 0.2.0 · 2026-09-15

- Treat CONTEXT as a compatibility dispatch adapter that freezes planning
  inputs for later Run Specs without minting a Level-4 Run.

## 0.1.3 · 2026-09-04

- Resolve an exact Page Face owner—workflow phase, canonical family, or legacy
  Page Type—and load it once when it is also the Folder owner.

## 0.1.2 · 2026-09-04

- Route stale Narrative authority to the paper journey but stale Venue
  authority to the QBv bank Page Type, because Venue is a library.

## 0.1.1 · 2026-09-04

- Follow the canonical Page dependency order.
- Define the upstream repair handoff: HOLD with source path, owning skill,
  required change, and resume at CONTEXT instead of editing stale policy here.

## 0.1.0 · 2026-09-04

- Add the distinct `00 CONTEXT` Page phase and its `PREPARE` cycle.
- Define Collect, Resolve, and Freeze as internal movements, not Level-4 Runs.
- Add the generated `outline/<stem>-context.md` projection and make the shared
  Outline workbench's Context Workspace its presentation surface.
- Merge policy, requirements, related information, feedback, decisions, files,
  log, and ranked Skills into one workspace without merging their source files.
