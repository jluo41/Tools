# `repo` · create or adopt a submodule-backed Project

This explicit verb creates or adopts a Project with its own Git repository and
records `git_mode: submodule`. Project spelling never selects this mode.

## Inputs

```text
/haipipe-project repo <id> --org <owner>
                           [--profile research|software|hybrid]
                           [--mission "..."] [--public]
```

Resolve the organization from the explicit flag or ask. Never assume one.
Private is the default visibility; confirm before creating a public repository.

## Preflight

```text
gh auth status
gh repo view <org>/<id>
git rev-parse --show-toplevel
```

- Existing remote repository → ADOPT mode; do not recreate or force-push.
- Existing local `examples/<id>` path → stop and route to `update` or a manual
  adoption plan. Never overwrite it.

## Create or adopt

In CREATE mode, create the requested repository. Then add it as:

```text
examples/<id>/    submodule → <org>/<id>
```

Inside the Project, create only:

```text
README.md
project.yaml       git_mode: submodule
.gitignore
```

Do not manufacture empty world directories. The first Task, Discovery, Board,
Paper, Application, or external dependency creates its own world through the
owning skill.

Commit and push inside the Project, then commit the workspace `.gitmodules`
entry and submodule pointer. Report both commits separately.

## Nested Paper repositories

A Paper may be a submodule inside `papers/`. Its pointer is owned by the
Project repository, then the Project pointer is owned by the workspace:

```text
paper commit → Project pointer commit → workspace pointer commit
```

Never move an existing nested Paper from legacy `paper/` during routine setup
or update; record that path as migration debt first.

## Verify and return

Run the root audit after materialization. Return repository URL, Project path,
profile, Git mode, both pointer states, and the first-content command.
