# haipipe-project

Project-root setup, audit, and safe reconciliation for `examples/`.

## Commands

```text
/haipipe-project new <id> [--profile research|software|hybrid]
/haipipe-project repo <id> --org <owner> [--profile ...]
/haipipe-project audit [<project>|--all]
/haipipe-project update [<project>|--all]
```

Every active Project has `README.md` and `project.yaml`. Content worlds are
lazy: `tasks/`, `discoveries/`, `diagram/`, `papers/`, `applications/`,
and `external/` appear when first used.

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
