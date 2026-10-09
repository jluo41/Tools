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

## Adopt an existing Project folder

When the Project folder already exists in the workspace (a `workspace`
Project becoming its own repo, first done for Project-Samsung on 2026-10-04),
adopt it in place; never recreate or copy it:

1. Scan what will be pushed: keys, passwords, participant data, files over
   5 MB. A note holding a credential stays out through the Project's `.gitignore`.
2. Copy the workspace root `.gitignore` rules that matter inside the Project
   (for example `_old/`) into the Project's own `.gitignore`; workspace rules
   stop applying once the Project is its own repo.
3. Set `git_mode: submodule`, `git init -b main`, re-add nested code repos
   with `git submodule add <url> <path>` (git adds the existing repo), commit.
4. Create the repository (private unless confirmed), add `origin`, push.
5. In the workspace, drop the nested repos' index entries with
   `git update-index --force-remove <path>` (files untouched) and their
   `.gitmodules` blocks, then `git submodule add <url> <project-path>`.
   Commit only these paths; other sessions' staged work stays staged.
6. Move the git data to the absorbed layout every Project uses: the
   Project's into `.git/modules/<project-path>/`, nested repos' into
   `.git/modules/<project-path>/modules/<sub-path>/`, each `.git` a pointer
   file. Set each `core.worktree` by editing its `config` file: `git config`
   refuses while the old worktree path is broken. Back up the git data first.

## Nested Paper repositories

A Paper may be a submodule inside `paper/`. Its pointer is owned by the
Project repository, then the Project pointer is owned by the workspace:

```text
paper commit → Project pointer commit → workspace pointer commit
```

A nested Paper under an older `papers/` moves to `paper/` only with the Project's Theme rename
(`scripts/rename_themes.py`, which moves submodules with `git mv`), never in routine setup.

## Verify and return

Run the root audit after materialization. Return repository URL, Project path,
profile, Git mode, both pointer states, and the first-content command.
