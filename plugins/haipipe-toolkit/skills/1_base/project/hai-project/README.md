# hai-project

Project-root setup, audit, and safe reconciliation for `examples/`.

## Commands

```text
/hai-project new <id> [--profile research|software|hybrid]
/hai-project repo <id> --org <owner> [--profile ...]
/hai-project audit [<project>|--all]
/hai-project update [<project>|--all]
```

Every active Project has `project.md` and `project.yaml` (`README.md` is optional). Content worlds are
lazy: `work/`, `discovery/`, `cowork/`, `paper/`, `insight/`,
`design/`, `external/` and (software/hybrid) `platforms/` appear when first
used. `diagram/` and `applications/` are retired.

`profile` and `git_mode` are independent manifest fields; names never choose
repository topology. Routine updates record unsafe moves as migration debt
instead of relocating submodules, generated Results, or large code trees.

## Files

```text
SKILL.md                   entrypoint and routing
ref/project-structure.md   schema and Project-root authority
ref/code-structure.md      profile-specific root-code boundary
fn/project.md              workspace-backed creation
fn/repo-project.md         submodule-backed creation/adoption
fn/audit.md                read-only compliance
fn/update.md               safe reconciliation
scripts/audit_projects.py  deterministic root audit
```
