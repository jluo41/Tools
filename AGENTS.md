# Repository guidance

## Layout and scope

- `plugins/` contains the first-party packages. Top-level package metadata lives in each package's `.claude-plugin/plugin.json`.
- `references/` contains upstream projects and reference material; many directories are Git submodules. `references/sources.yaml` records origins and license notes.
- The installers discover skills recursively under `plugins/**/skills/`. They do not install skills from `references/`.
- Root install behavior is implemented by `install.sh` and `install.ps1`; both read the shared sound-hook table in `install-hooks.json`.

## Protect existing work

- Check `git status` before editing. Preserve pre-existing changes, untracked files, and dirty submodule worktrees. Do not reset, clean, or overwrite them.
- Treat `references/` as upstream content. Edit it only when the task targets that source. Before doing so, inspect the submodule status, read any scoped `AGENTS.md` and project guidance, and avoid broad formatting changes or unintended submodule pointer updates.
- The root `AGENTS.md` applies to this repository. Nested `AGENTS.md` files add instructions for their own directories.

## Keep it general

- Nothing in code, configuration keys, defaults, or documentation names one person, one lab, or one deployment. Settings keys are generic (`DOMAIN`, `BIND_HOST`, `PORT`, `AUTH_FILE`, `SPACE_NAME`, `NO_AUTH`), display defaults are neutral (`SPACE Home`), and examples use placeholders such as `<DOMAIN>` or `example.test`. A deployment-specific prefix belongs in that deployment's `settings.env`, not in the repository.
- Servers never bake an origin into a page, a redirect, or a printed link. `DOMAIN` is a variable: the same origin-relative link body (`/b/<board>/<page>`, `/w/<board>/<page>/<tab>`) is reached through `http://127.0.0.1:<port>`, a Tailscale IP, or a configured public origin.
- A plugin's `servers/` may depend on the shared host in `plugins/haipipe-toolkit/servers/_host`, but the dependency is declared in that plugin's `servers/README.md`, and the shared host must start when the other plugin is absent.

## Page words

- A label names a thing; it carries no count or other number that changes as work moves ("What a topic is", never "What a topic is · 3 topics"; "Runs", never "Runs · 12"). The reader sees how many by looking; a count is written only where the count is itself the answer, such as "2 questions waiting on you".
- A Studio topic's drawing is a drawing: the idea drawn as a pattern (cycle, timeline, tree, fan-in), never the face's lines listed as text. The method is `references/workflow-diagrams/excalidraw-diagram-skill`; the kit is `haipipe-studio/scripts/quick_draw.py`.

## Keep repository metadata aligned

- The top-level package inventory is the set of direct child directories in `plugins/`. When adding or retiring a package, keep its plugin manifest, `.claude-plugin/marketplace.json`, and the README package table aligned. Every marketplace `source` must resolve to an existing package directory.
- Do not assume a nested `.claude-plugin/plugin.json` is a top-level package. Decide deliberately whether it should be listed separately in the root marketplace and documentation.
- Both installers scan skill files recursively under package `skills/` trees. Keep reference trees out of those trees unless they are intentionally part of the installed skills.
- Keep `install.sh` and `install.ps1` behavior aligned when changing discovery, exclusions, duplicate handling, or target installation. Both skip any folder whose name starts with `_` and `node_modules/`, for skills and agents alike; keep that one rule in both rather than listing retired folders.
- Keep sound-hook event data in `install-hooks.json`, not duplicated between the installers. Update README instructions when installer behavior or flags change.

## Validation

- There is no single root build or test command. Read the relevant package guide and use checks appropriate to the files changed.
- For skill changes, follow the fresh-context validation process in the root README.
- For installer or marketplace changes, inspect both platform installers and verify package source paths and metadata. Report platform-specific checks that could not be run.

## Work tree replies

When the user asks about work (where it lives, how far it got, which Run counts), reply with the Block map: the Block on top, one line per Job, its Task and Run range in aligned columns, then the state emoji (✅ done, 🏃 running, ⬜ stopped or not yet, ❗ void, 🙋 your call) and what that Job builds or answers. Template and rules: the `response-format` skill, § Work tree.

```text
<bNN_block>
├─ <jNN_C_data_job>  ─▶ <tNN>  <rNN-rNN rNN>  <state> <what it builds>
├─ <jNN_D_reg_job>   ─▶ <tNN>  <rNN-rNN>      <state> <the question it answers>
└─ <jNN_D_reg_job>   ─▶ <tNN>  <rNN-rNN>      <state> <the question it answers>
```

UI design
=========

Avoid unnecessary secondary labels and descriptions. Let the layout do the explaining.

Do not add unnecessary UI text. Let grouping, spacing, controls, and content explain themselves. Omit routine hints such as "available", "nothing yet", "one per kind", and instructions that repeat visible controls. Keep text when it communicates a meaningful state, a required action, or an otherwise unclear empty state.
