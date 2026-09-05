# `new` · create a workspace-backed Project

Create a Project root under `examples/` without fabricating empty worlds.

## Inputs

```text
/haipipe-project new <id> [--profile research|software|hybrid]
                         [--git-mode workspace]
                         [--mission "..."]
```

Default `profile` to `research` only when no root-owned software artifact was
requested. `git_mode` is `workspace` for this verb. If the id or mission is
missing, ask only for the missing value.

## Preflight

- Read `../ref/project-structure.md`.
- Confirm `examples/<id>` does not already exist. If it exists, route to
  `update`, never overwrite it.
- Confirm the id is readable and stable. Do not derive Git mode from its name.

## Create

```text
examples/<id>/
├── README.md
└── project.yaml
```

`README.md` states the mission in one short opening and lists only real entry
points. `project.yaml` uses schema `haipipe-project/v1`.

Do not create empty `tasks/`, `discoveries/`, `diagram/`, `papers/`,
`applications/`, or `external/`. When the user also requests first content,
route that content to its owning skill, which materializes the corresponding
world.

Do not create root Results, code stubs, seed Tasks, Boards, or diagrams unless
the user requested them separately.

## Verify and return

Run:

```text
python3 <haipipe-project>/scripts/audit_projects.py examples/<id>
```

Return created paths, profile, Git mode, compliance result, and the appropriate
first-content command.
