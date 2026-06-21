---
name: haipipe-paper-enter
description: "Enter a paper repo in status-aware mode. Use for `/haipipe-paper enter <paper-path>`, `/haipipe-paper status [paper-path]`, or when starting work in an existing paper folder. Reads STATUS.md, 0-lifecycle, 0-displays, 0-sections, 1-feedback, and git state; outputs a dashboard with current layer, stable assets, open gates, loopback diagnosis, and next commands. Does not edit files."
argument-hint: "[paper-path]"
allowed-tools: Bash, Read, Grep, Glob
metadata:
  version: "1.0.0"
  last_updated: "2026-06-21"
  summary: "Status-aware paper session loader."
---

# haipipe-paper-enter

Enter a concrete paper folder in aware mode. This skill is a preflight/status
loader. It does not write, revise, compile, or create files.

The awareness is explicit, not hidden. The skill loads paper state into the
current conversation by reading files and emitting a dashboard. Follow-up paper
actions in the same session must treat that dashboard, especially
`current_layer`, `next_layer`, and open gates, as the working context. A fresh
Claude/Codex session should run `enter` again.

## Input

Accept either:

```text
<paper-root>
```

or any path inside a paper root. If no path is supplied, use the current
directory.

## Resolve Paper Root

Look upward from the supplied path until one of these signatures is found:

- `STATUS.md`
- `0-lifecycle/`
- `0-*.tex` and `0-sections/`
- `1-compile.sh` and `0-sections/`

If no paper root is found, report `status: blocked` and suggest:

```text
/haipipe-paper prospectus "<paper-path>"
/haipipe-paper-structure folder "<paper-path>"
```

## Read Order

Read only files that exist, in this order:

1. `STATUS.md`
2. `0-lifecycle/README.md`
3. Stage TeX files:
   - `0-lifecycle/0-seed/0-seed.tex`
   - `0-lifecycle/1-pitch/1-pitch.tex`
   - `0-lifecycle/2-claims/2-claims.tex`
   - `0-lifecycle/3-narrative/3-narrative.tex`
   - `0-lifecycle/4-figures-tables/4-figures-tables.tex`
   - `0-lifecycle/5-minimap/5-minimap.tex`
4. `0-displays/README.md`
5. `0-displays/*/README.md`
6. `0-sections/README.md`
7. `0-sections/*.tex` names and short headers/comments only; do not read full
   long sections unless needed to diagnose minimap drift.
8. `1-feedback/<branch>/latest.md`, then the referenced round README,
   `decisions.md`, `todo.md`, and `applied.md` if they exist.
9. Git state:
   - `git status --short --branch`
   - `git log --oneline --max-count=3`

## Diagnosis Rules

Infer the current layer from `STATUS.md` first. If missing or stale, infer from
available artifacts:

| Evidence | Current layer |
|---|---|
| only `README.md` / prospectus lifecycle | `0-seed` or `1-pitch` |
| `1-pitch.tex` exists but claims are absent/thin | `1-pitch -> 2-claims` |
| claims exist but narrative is absent/thin | `2-claims -> 3-narrative` |
| narrative exists but display units are missing | `3-narrative -> 4-figures-tables` |
| display plan exists but display units/canonical PDFs are missing | `4-figures-tables` |
| display units exist but paragraph placement is missing | `5-minimap` |
| minimap exists and displays are placed | ready for section edit/build/review |

Loopback diagnosis follows the paper lifecycle:

| Symptom | Return to |
|---|---|
| wording, citation, format, stale number | edit cycle |
| paragraph has no job | `5-minimap` |
| figure/table unclear or lacks source/caption/preview | `4-figures-tables` |
| unsupported or too-strong claim | `2-claims` / `3-narrative` |
| story not compelling or abstract/intro disagree | `1-pitch` |
| paper no longer viable | `0-seed` |

## Output Format

Always answer with emoji-headed sections:

```markdown
## 📄 Paper Session

| Field | Value |
|---|---|
| Paper | ... |
| Path | ... |
| Branch | ... |
| Current layer | ... |
| Next layer | ... |
| Maturity | ... |

## ✅ Stable

- ...

## ⚠️ Open Gates

- ...

## 🔁 Loopback Diagnosis

- ...

## 🎯 Recommended Next

1. `/haipipe-paper-structure ...`
2. ...

## 📦 Artifacts Read

- ...
```

Keep the dashboard concise. The goal is to orient the session, not to rewrite
the paper.

## Return Contract

End with a machine-readable tail:

```text
status: ok|blocked
paper_root: <path or none>
current_layer: <layer or unknown>
next: <single recommended command>
```
