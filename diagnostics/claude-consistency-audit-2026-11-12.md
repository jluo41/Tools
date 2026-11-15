# Claude Code peer audit, 2026-11-12

This is an independent, read-only review that runs beside the Codex audit in
`consistency-audit-2026-11-12.md`. No source files were edited. Every check ran
in a temporary fixture and used a redirected `HOME`. No real installation or
settings file was touched.

## Findings (most severe first)

### 1. `--hooks` / `-Hooks` deletes every existing hook, not only sound hooks (confirmed)

- **Where**: `install.sh:645-651`, `install.ps1:642-643`, and the claim at `README.md:173-176`.
- **Trigger**: a fixture `settings.json` held a `PreToolUse` guard hook
  (`/usr/local/bin/guard.sh`) and a user `Stop` hook. After
  `HOME=<tmp> bash install.sh --no-marketplace --hooks`, `hooks` held only the 8
  sound events. The guard hook was gone (`guard present: False`). `model` was kept.
- **Impact**: the installer silently removes safety and permission hooks the user
  configured. The README says "Other settings are preserved", which a reader
  takes to include their own hooks.
- **Fix**: merge per event. Add or replace only the installer's own entries (for
  example, entries whose command starts with `afplay`, the `{player}` value, or
  `Media.SoundPlayer`), and keep the other matchers and events. Make the same
  change in both installers. Extend `test_hooks_create_settings_directory` so it
  asserts that a pre-existing `PreToolUse` hook survives.

### 2. Shared-host settings: any key ending in `_PORT`, `_NO_AUTH`, `_DOMAIN`, ... overrides the real key (confirmed)

- **Where**: `plugins/haipipe-toolkit/servers/_host/server_config.py:72-80`
  (`_known` suffix match). It is used at `serve.py:1009-1025`.
- **Trigger**: `settings.env` with
  `PORT=5599 / NO_AUTH=0 / REDIS_PORT=6379 / WEB_PORT=80 / SKIP_NO_AUTH=1`
  makes `load_server_config` return `{'PORT': '80', 'NO_AUTH': '1'}`.
- **Impact**: an unrelated variable in the SPACE's settings file can silently
  move the listener to another port or **turn authentication off**: `serve.py`
  sets `a.no_auth = True` when `NO_AUTH` is truthy. The documented intent
  ("a deployment may namespace every key with its own `<PREFIX>_`") is one prefix
  for the whole file, not a free suffix match per line.
- **Fix**: find the prefix once. Use the bare key if any canonical key is
  present; otherwise take the single prefix shared by the recognized keys. You
  could also accept `PREFIX_` only when the prefix has no further `_`. As a
  minimum, ignore a stripped key when the bare canonical key also appears.
  Add a regression test for `REDIS_PORT` and `X_NO_AUTH`. The existing 7 tests in
  `tests/test_server_config.py` pass and do not cover this case.

### 3. `/plugin install haipipe@jluo41-tools` most likely loads no HAI-Pipe skills (suspected, high)

- **Where**: `.claude-plugin/marketplace.json` (source `./plugins/haipipe-toolkit`),
  `plugins/haipipe-toolkit/.claude-plugin/plugin.json` (no `skills` field), and
  the hint at `install.sh:163-165`.
- **Evidence**: `plugins/haipipe-toolkit/skills/*/SKILL.md` matches 0 files. All 128
  skills sit 2-3 levels deeper (`0_utils/`, `1_base/<family>/`, `2_theme/<theme>/`).
  Claude Code plugin skill discovery is `skills/<name>/SKILL.md`, one level, unless
  `plugin.json` lists skill paths. 21 of the 32 agents live in skill-nested
  `agents/` folders, which a plugin install also would not load. Only the root
  installers' recursive symlink path gives the full set. `haipipe-utils` (7 at
  depth 1) and `inlab-human` (1) are not affected.
- **Untested**: I did not start a `claude --plugin-dir` session to confirm.
  That is the one-line check.
- **Fix**: add an explicit `skills` path list (and `agents`) to the toolkit's
  `plugin.json`, generated from the same `_`-pruned walk. Otherwise, drop the
  `/plugin install haipipe@...` hint and say that the installers' links are the
  supported path.

### 4. `.agents/plugins/marketplace.json` breaks the "Keep it general" rule as well as pointing at a missing path (confirmed)

- **Where**: `.agents/plugins/marketplace.json:2,4,11` (tracked).
- **Evidence**: `"name": "drfirst-local"`, `"displayName": "DrFirst Local"` name one
  deployment. `AGENTS.md` § "Keep it general" forbids that in repository
  configuration. Codex reported only the missing `./codex-plugins/haipipe-toolkit`.
- **Impact**: any Codex client reading this catalog gets a dead entry with a
  deployment-specific name. No test covers this file (`CatalogTests` reads only
  `.claude-plugin/` catalogs).
- **Fix**: retire the file, or rename it to a neutral catalog and point it at an
  existing package. Either way, add it to `CatalogTests` so it cannot rot again.

### 5. The installer tests isolate the home folder through a silent `str.replace` (confirmed latent hazard)

- **Where**: `diagnostics/test_installers.py:24-30`.
- **Evidence**: the redirect replaces the exact text `CLAUDE_DIR="$HOME/.claude"`
  and `$ClaudeDir   = Join-Path $userHome ".claude"` (3 spaces). `str.replace`
  does nothing if the text is not found. If either line is reformatted,
  the suite runs against the **real** `~/.claude`. It does this with
  `test_marketplace_registration_with_quoted_checkout` (rewrites
  `known_marketplaces.json`) and the hooks test (would then wipe hooks, per
  finding 1).
- **Fix**: assert that each replacement changed the text. Also pass
  `env={**os.environ, "HOME": tmp, "USERPROFILE": tmp}` to `subprocess.run`
  as a second guard.

### 6. Stale-link cleanup removes any dangling link, including links Tools does not own (optional improvement)

- **Where**: `install.sh:445-451` (global `~/.claude/skills`), `install.sh:531-537`,
  `install.sh:593-599`, and the matching PowerShell cleanup around `install.ps1:373-380`.
- **Impact**: a user's own skill link to a drive that is not mounted right now is
  deleted when `--global` or `--project` runs. Low severity, but it contradicts
  the "real directories you own are left alone" stance.
- **Fix**: remove a dangling link only when its stored target (from `readlink`)
  points into `$SCRIPT_DIR/plugins`.

## Codex conclusions checked

- Agreed: the catalog versions now match the manifests (haipipe 0.4.0, haipipe-utils 0.2.0,
  inlab-human 0.2.2). The 136 skills split 128 + 7 + 1. There are 7 aliases and
  no alias collisions. All frontmatter `name:` values match the folder or file
  names for the 136 skills and 32 agents. No duplicate agent names were found.
- Agreed: the bash and PowerShell discovery rules give the same results for the
  current tree (`_*` and `node_modules` pruned; direct `<pkg>/skills/` only;
  agents in any `agents/` folder).
- Ran: `python3 -m unittest discover -s diagnostics -p test_installers.py` gave 22 OK (41 s).
- Challenged: "Documentation overstated verification" was fixed, but the
  README's hooks sentence (finding 1) is still inaccurate.

## Environment, not defects

- `~/.claude/plugins/installed_plugins.json` lists `research@jluo41-tools`. No
  plugin named `research` is in the current catalog, so that is a stale local
  install. Nothing in the repository needs to change.
- `timeout` is not installed on this macOS host. The shared-host tests ran via `uv`.

## Not inspected or untested

PowerShell was not run by me (Codex ran it). There was no live `claude` plugin
install (finding 3). Server suites beyond `test_server_config.py` were not run.
I did not check `haipipe-utils/servers/_host` or `inlab-human` servers in depth,
the substance of the skill instructions, or `references/`.
