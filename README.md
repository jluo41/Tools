# Tools

A personal collection of research and workflow tools for Claude Code and
Codex. The repository contains first-party skill packages in `plugins/` and
upstream projects in `references/`.

## First-party packages

| Package | Focus | Guide |
|---|---|---|
| **haipipe** | Research and ML workflows across evidence, task Runs, first-class Insight and Design, papers, and the data → model → endpoint pipeline | [HAI-Pipe guide](plugins/haipipe-toolkit/README.md) |
| **haipipe-utils** | Normalization skills that turn cohort-specific food, exercise, medication and insulin text into typed measurements with provenance, plus the `servers/` API host that serves them | [Utilities guide](plugins/haipipe-utils/README.md) |
| **inlab-human** | Clinician studies of deployed prediction endpoints, including blind-then-assisted review | [In-Lab Human guide](plugins/inlab-human/README.md) |
| **subjective-label** | Human-grounded construct building and corpus labeling with calibration and audit workflows | [Subjective Label guide](plugins/subjective-label/README.md) |

This table covers the four package directories directly under `plugins/`. The HAI-Pipe display subtree also contains nested HTML-PPT package metadata; nested packages are not automatically top-level entries in the root marketplace.

## Repository map

| Path | Purpose |
|---|---|
| `plugins/` | First-party packages. The installers discover skills recursively under these package roots. |
| `references/` | Upstream projects, reference material, and Git submodules. The installers do not install skills from this tree. |
| `references/sources.yaml` | Source, origin, and license notes for the reference collection. |
| `.claude-plugin/marketplace.json` | Claude Code marketplace catalog for this repository. |
| `install.sh`, `install.ps1` | macOS/Linux and Windows installers for marketplace registration and skill links. |
| `install-hooks.json` | Shared per-OS sound-hook configuration read by both installers. |

For HAI-Pipe workflows, see its [package guide](plugins/haipipe-toolkit/README.md)
and [skill structure map](plugins/haipipe-toolkit/skills/STRUCTURE.md).

## Installation

Clone with submodules to populate the reference collection as well as the
first-party packages:

```bash
git clone --recurse-submodules git@github.com:jluo41/Tools.git
cd Tools
```

If the repository is already cloned, initialize its pinned submodules with:

```bash
git submodule update --init --recursive
```

Both installers discover skills recursively under first-party package
`skills/` trees. The retired `plugins/haipipe-toolkit/skills/display/_todo/`
tree is excluded on macOS/Linux and Windows, matching the Display package
guide; its skills remain in the repository for historical reference.

### macOS and Linux

To link the current skills into a specific workspace without registering the
marketplace:

```bash
./install.sh --no-marketplace --project /path/to/workspace
```

This creates `.claude/` and `.codex/` in the target workspace, links skills
into both tools' `skills/` directories, and links plugin agents into
`.claude/agents/`.

Other options:

```bash
./install.sh                  # register the marketplace; may detect the parent workspace
./install.sh --global         # link skills and agents into ~/.claude/
./install.sh --hooks          # configure Claude Code sound hooks
./install.sh --all            # marketplace + global links + hooks
```

The default shell installer registers this repository as the `jluo41-tools`
marketplace. It auto-detects a parent workspace when that directory contains
`.git` or `pyproject.toml`; use `--project` to select a target explicitly.
Marketplace commands use the package names listed in
`.claude-plugin/marketplace.json`.

### Windows

In PowerShell, create the target tool directories first, then link skills into
them:

```powershell
New-Item -ItemType Directory -Force -Path 'C:\workspace\.claude','C:\workspace\.codex'
.\install.ps1 -NoMarketplace -Project 'C:\workspace'
```

The Windows installer only installs into `.claude/` and `.codex/` directories
that already exist under the target. It creates directory junctions by default;
agents are copied and tracked so a later run can refresh installer-owned copies.
Use `-Symlink` to create symbolic links instead, which requires Administrator
privileges or Developer Mode.

Other options:

```powershell
.\install.ps1                         # register the marketplace and detect an existing parent workspace
.\install.ps1 -Global                 # link skills globally and copy agents
.\install.ps1 -Hooks                  # configure Claude Code sound hooks
.\install.ps1 -All                    # marketplace + global links + hooks
.\install.ps1 -NoMarketplace          # skip marketplace registration
```

Windows junctions use absolute paths. Re-run the installer after moving the
repository. The project auto-detection behavior differs between the shell and
PowerShell installers, so use an explicit project path when targeting a
workspace.

### Sound hooks

`--hooks` / `-Hooks` updates the `hooks` section in
`~/.claude/settings.json` using the shared event and sound table in
`install-hooks.json`. Other settings are preserved. A sound file that is not
present on the machine leaves that hook silent.

### Updating the checkout

```bash
git pull
git submodule update --init --recursive
```

## Skill development

When adding or changing a skill, validate it from a fresh context: ask a
subagent to invoke the skill on a realistic task, then confirm it selected the
skill, followed its instructions, and produced the intended result. Follow any
package-specific guidance as well.

## License

The root `LICENSE` applies to repository-owned material. Projects under `references/` retain their upstream licenses; check their license files and `references/sources.yaml` before reuse.
