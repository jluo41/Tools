---
name: haipipe-paper-project
description: "Project approved Paper Board S-page content into isolated, deterministic LaTeX candidates using 2-src/projection.yaml. Validates exact source/target coverage (G0), reads only explicitly GATED pages (G1), generates under a content-addressed 3-dist/tex run directory without touching submission files (G2), checks citation/question-marker non-regression (G3), optionally compiles in a disposable copy (G4), and promotes only with an explicit human token plus rollback backup (G5). Trigger: project paper, generate tex from S pages, projection manifest, candidate build, sync gated section to LaTeX, /haipipe-paper-project."
allowed-tools: Bash, Read, Grep, Glob
metadata:
  version: "0.1.3"
  last_updated: "2026-07-30"
  summary: "Manifest-driven S-page → isolated LaTeX candidate projection with six explicit gates and no implicit promotion."
---

# Haipipe Paper Project

Turn Board-owned manuscript sources into reviewable LaTeX candidates. This is a
projection boundary, not a second authoring system:

```text
0-lifecycle/**/S-*.md   SOURCE AUTHORITY
          │
          ▼
2-src/projection.yaml   WIRING ONLY
          │
          ▼
3-dist/tex/<run-id>/    IMMUTABLE CANDIDATE
          │  explicit human promotion only
          ▼
sections/ appendices/   SUBMISSION TREE
```

The skill does not edit S-page prose, infer missing mappings, approve Board
gates, or promote merely because generation/checking succeeded.

## Usage

From a paper root (nearest ancestor containing `0-lifecycle/`):

```bash
python <skill>/project.py validate --paper .
python <skill>/project.py generate --paper . --unit main-1
python <skill>/project.py check --paper . --candidate 3-dist/tex/<run-id>
python <skill>/project.py check --paper . --candidate 3-dist/tex/<run-id> --compile
python <skill>/project.py promote --paper . --candidate 3-dist/tex/<run-id> \
  --approve PROMOTE --actor "<human>" --reason "<why>"
```

Read [references/projection-manifest.md](references/projection-manifest.md)
before creating or changing a manifest.

## Six gates

| Gate | Runtime obligation | Failure behavior |
|---|---|---|
| G0 coverage | Manifest target paths are unique and safe; every `.tex` under each target root is declared as an output or as `unreachable` with a disposition/reason. | Stop before generation. |
| G1 source | Every selected source page exists; its declared gate id resolves to exactly one S page whose first `state:` is `✅ GATED …`. | Refuse the unit; never “helpfully” use open prose. |
| G2 isolation | Run id is a content hash. Write only a new partial directory under `candidate_root`, then rename it to `<run-id>`. Never overwrite submission files. The runtime contains no recursive workspace deletion. | Leave a forensic `.partial-*` directory on write failure. |
| G3 evidence | Candidate retains every citation key and every `[Q-…]` marker found in the selected manuscript prose; regenerating the same inputs is byte-identical. | Check fails. |
| G4 compile | With `--compile`, copy only the unnumbered deliverable into a system temp directory, overlay the candidate, and compile there. | Preserve the candidate and submission tree; report compiler output. |
| G5 promotion | Require the literal token `PROMOTE`, actor, reason, a passing candidate check, and an unchanged submission snapshot. Back up replaced files and atomically replace them; roll back on any error. | No partial accepted promotion. |

## Workflow

1. Resolve the paper root and `2-src/projection.yaml`.
2. Run `validate`. Fix the manifest, never infer an undeclared target.
3. Run `generate --unit …` only for the requested gated unit(s).
4. Run `check` on the exact returned candidate. Use `--compile` when the
   candidate should pass the isolated build gate.
5. Show the candidate diff to the human.
6. Stop. Run `promote` only when the user explicitly asks to accept that exact
   candidate and provides/authorizes an actor and reason.

Receipts are append-only JSON files in `2-src/projection-receipts/`. They record
the manifest hash, source hashes, candidate id, gate results, and—in promotion
receipts—the pre-promotion target hashes and backup paths.

## Safety invariants

- Resolve every manifest path against the paper root and reject absolute paths,
  `..`, symlink escapes, and targets outside declared roots.
- `candidate_root` must be under `3-dist/`.
- Generation uses exclusive file creation and never calls `rmtree` on a
  workspace path.
- Submission files are read-only in `validate`, `generate`, and `check`.
- `promote` accepts only a direct child of the declared candidate root.
- Promotion never changes the master, bibliography, venue shell, or a path not
  declared in the candidate manifest.
- A compiler verdict never changes a Board S-page state.

## Return contract

```text
status:    ok | blocked | failed
summary:   gate verdicts and candidate/promotion identity
artifacts: [manifest, candidate directory, receipts]
next:      inspect/check candidate, or explicit human promotion
```
