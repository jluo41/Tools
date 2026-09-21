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

## Keep repository metadata aligned

- The top-level package inventory is the set of direct child directories in `plugins/`. When adding or retiring a package, keep its plugin manifest, `.claude-plugin/marketplace.json`, and the README package table aligned. Every marketplace `source` must resolve to an existing package directory.
- Do not assume a nested `.claude-plugin/plugin.json` is a top-level package. Decide deliberately whether it should be listed separately in the root marketplace and documentation.
- Both installers scan skill files recursively under package `skills/` trees. Keep reference trees out of those trees unless they are intentionally part of the installed skills.
- Keep `install.sh` and `install.ps1` behavior aligned when changing discovery, exclusions, duplicate handling, or target installation. Their current skill exclusions differ for `_old/`; check the implementations rather than assuming exact parity.
- Keep sound-hook event data in `install-hooks.json`, not duplicated between the installers. Update README instructions when installer behavior or flags change.

## Validation

- There is no single root build or test command. Read the relevant package guide and use checks appropriate to the files changed.
- For skill changes, follow the fresh-context validation process in the root README.
- For installer or marketplace changes, inspect both platform installers and verify package source paths and metadata. Report platform-specific checks that could not be run.
