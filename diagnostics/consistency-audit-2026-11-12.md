# Repository consistency audit — 2026-11-12

Two batches cover root installation, first-party package catalogs, discovery rules,
basic skill metadata, package documentation, shared-host configuration, and selected
host tests. It is not a full application or security audit.
The checkout already contained extensive blueprint and plugin edits and dirty
reference submodules. Those changes were preserved; references were not modified.

## Confirmed issues fixed

Line numbers below refer to the reviewed working tree after the fixes.

| Issue | Location | Evidence and impact | Change |
|---|---|---|---|
| Marketplace registration could delete local work | `install.sh:99`, `install.ps1:549` | Shell registration recursively deleted an existing non-link marketplace directory. An isolated fixture reproduced the loss. | Both installers stop and preserve real files or directories; existing links can still be replaced. |
| Paths containing apostrophes broke shell installation | `install.sh:108`, `:143`, `:491`, `:573` | Checkout and workspace paths were interpolated into Python source, producing `SyntaxError`. | Pass paths as arguments instead. |
| Agent discovery differed between platforms | `install.ps1:156` | A fixture at `agents/nested/nested-agent.md` installed under Bash but was omitted under PowerShell. | Accept nested agent folders on both platforms. |
| PowerShell deleted valid relative agent links | `install.ps1:259` | Cleanup resolved targets against the process working directory; a valid user link disappeared. | Resolve targets relative to the link's directory. |
| PowerShell verification accepted stale managed copies | `install.ps1:432` | An outdated installer-owned agent still produced verification exit status 0. | Compare managed copies with sources; outdated or retired copies fail verification. |
| Catalog versions disagreed with manifests | `.claude-plugin/marketplace.json:19`, `plugins/haipipe-toolkit/.claude-plugin/marketplace.json:12` | Utilities catalog said `0.1.0`, manifest `0.2.0`; toolkit-local catalog said `0.2.0`, manifest `0.4.0`. | Align catalog versions with manifests. |
| Shell skill discovery was broader than documented | `install.sh:186` | Its pattern accepted `plugins/<package>/examples/skills/.../SKILL.md`; PowerShell rejected that layout. | Require the direct package `skills/` tree. |
| Unknown shell flags were silently ignored | `install.sh:65` | `--unknown` proceeded; an argument-less `--project` failed without a useful diagnostic. | Reject invalid arguments before installation, with exit status 2. |
| Failed shell verification skipped cleanup | `install.sh:285`, `:304` | `set -e` exited on an audit failure before deleting temporary inventory files. | Capture failure, clean up, and return the failure status. |
| Shell hooks assumed the settings directory existed | `install.sh:611`, `:659` | Opening `settings.json` required an existing parent, unlike PowerShell. | Create the parent and use the configured settings path. |
| Verification documentation overstated exit-status coverage | `README.md:166` | Missing MCP registrations and unknown links were printed without causing failure. | Document them as informational; preserve existing verification behavior. |

## Second batch: confirmed fixes and peer reconciliation

| Issue | Location | Evidence and impact | Resolution |
|---|---|---|---|
| Sound setup erased custom hooks | `install.sh:644`, `install.ps1:627` | Claude reported it; Codex reproduced it in both installers. A fixture's `PreToolUse` guard disappeared and its custom `Stop` hook was replaced. | Add missing sound commands while preserving all custom entries. Repeated setup is idempotent. Old sounds are not guessed to be installer-owned or removed. |
| Quoted settings were truncated at a hash | `plugins/haipipe-toolkit/servers/_host/server_config.py:50` | `SPACE_NAME="Study # 2"` became `"Study`; an auth path containing ` #` was truncated too. JSON-valued settings were also vulnerable. | Recognize inline comments only outside quotes. Tests cover display names, auth paths, JSON, URL fragments, and ordinary comments. |
| Prefixed settings overrode explicit canonical values | `plugins/haipipe-toolkit/servers/_host/server_config.py:100` | `PORT=5599`, `NO_AUTH=0`, then `WEB_PORT=80`, `SKIP_NO_AUTH=1` changed the listener port and disabled login. Claude found it; Codex reproduced it. | Explicit bare canonical keys now win regardless of order. Prefix-only configurations remain supported; namespace ambiguity without canonical keys is a separate design question below. |
| Python 3.11 could not import design code | `plugins/haipipe-toolkit/servers/workbench-design/design.py:2409`, `design_canvas.py:116`, `:396` | Backslashes inside f-string expressions and reuse of an outer quote required Python 3.12 syntax, despite the host's advertised 3.10+ requirement. `serve.py --only labeling --help` failed before argument handling. | Move escaped expressions outside f-strings and use compatible quoting. All 239 scanned server Python files now parse under 3.11; shared-host entry tests pass. |
| Toolkit README described the old layout and retirement policy | `plugins/haipipe-toolkit/README.md:116`, `:123`, `:145` | Advertised `skills/task`, `skills/board`, `skills/run`, and `skills/STRUCTURE.md` do not exist. It also said folder names never identify skills and retirement requires deletion, conflicting with actual installers and root guidance. | Document the current three layers, folder-based installer links, current reader path, and exclusion of underscore-prefixed folders. |
| Utilities README said its shared contract had no code | `plugins/haipipe-utils/README.md:31`, `:65` | `skills/haipipe-norm/eventnorm/` now contains 50 Python files. The stated responsibility split hid this implementation. | Describe shared event processing and noun-specific resolvers accurately. |
| Fixture redirection could silently fail after installer formatting changes | `diagnostics/test_installers.py:47` | Claude identified that unchecked exact-text replacement could leave real configuration paths active in a future test run. | Assert exactly one matching configuration assignment before running any installer. The caller's home variables are not changed. |

## Remaining finding

The tracked `.agents/plugins/marketplace.json` refers to
`./codex-plugins/haipipe-toolkit`. That directory is absent both relative to the
repository root and relative to the catalog. The repository's Claude package
exists under `plugins/haipipe-toolkit`, but this audit has not established that it
is a valid replacement for the intended Codex package. The toolkit changelog's
2026-07-03 entry records removal of the old `codex-plugins/` mirror, corroborating
that the catalog was left behind. The catalog was therefore
left unchanged. Resolve whether the missing Codex adapter should be restored or
the catalog retired/replaced before using that entry.

The same catalog's lines 2 and 4 contain a deployment-specific name, violating
root `AGENTS.md`'s neutral-configuration rule. This is also confirmed. A catalog
migration or retirement should resolve both problems together, rather than
inventing a replacement package path.

## Suspicions requiring verification

- **Claude marketplace discovery of nested skills.** Claude flagged
  `plugins/haipipe-toolkit/.claude-plugin/plugin.json:1`: it has no explicit
  skill/agent path list, and the toolkit's 128 skills are nested deeper than
  `skills/<name>/SKILL.md`. The root installers demonstrably discover them, but
  neither audit tested native plugin loading in an isolated Claude session.
  Treat the claim that native plugin installation omits them as unverified.
  Verify the native discovery result before changing package metadata or removing
  the install instructions.

## Optional changes requiring a policy decision

- **Select one settings namespace explicitly.** `_known()` at
  `plugins/haipipe-toolkit/servers/_host/server_config.py:73` intentionally accepts
  arbitrary prefixes. Bare canonical keys are now protected, but a prefix-only
  file can still mix unrelated namespaces. Selecting one prefix would remove
  ambiguity but changes the documented configuration contract; define migration
  behavior before implementing it.
- **Limit stale-link cleanup to installer-owned links.** `install.sh:445`,
  `:531`, `:593` and `install.ps1:377` delete dangling links without establishing
  ownership. A user link to a disconnected drive can be lost. An ownership rule
  could prevent this, but must account for moved checkouts and intentionally
  retired skills. Current behavior is documented; no cleanup-policy change was
  made in this batch.

## Independent Claude Code review

The user explicitly requested the native peer through
`plugins/haipipe-toolkit/skills/0_utils/call-peer/SKILL.md`.

- Pair and Codex session name: `SPACE-CODE-Quality`.
- Caller: Codex `01a1d0e2-cb29-7c71-9271-2446fd4f6349`.
- Callee: `SPACE-CODE-Quality-Claude`, Claude session
  `414315fa-5a25-47dc-b0c9-32138cb2b5db`; completed successfully.
- Manifest: `~/.config/haipipe/pairs/space-code-quality--2415463f4442.json`.
- Independent report: [Claude audit](claude-consistency-audit-2026-11-12.md).
  It is a snapshot from before the second-batch fixes. Its hooks, canonical-key
  precedence, and fixture-redirection findings were reproduced or inspected and
  addressed above. Its plugin-discovery concern remains unverified. The peer
  changed no source files.

## Validation

- Regression suite: `python3 -m unittest discover -s diagnostics -p test_installers.py -v`.
  All 24 tests passed after the second batch. Fixtures isolate checkout, workspace, and configuration
  paths in temporary directories.
- Full-checkout installation and verification succeeded with Bash and PowerShell
  (`-Symlink`) on macOS. Both produced identical targets: 143 skill links
  (136 skills plus 7 aliases) in each of the three skill roots, and 32 agents.
- All 136 active skills had parseable YAML front matter and nonempty names and descriptions.
- All three top-level package directories matched the root Claude catalog;
  root and package-local Claude catalog source paths and versions were checked.
- Local Markdown links in the root README and the three package READMEs resolved.
- Bash syntax and whitespace checks passed for the changed files.
- 31 shared-host tests passed: configuration, skill/part lookup, authentication,
  private static paths, short workbench routes, and CLI entry. Run with Python
  3.11 and PyYAML available, adding `servers/_host` and `servers/_host/tests` to
  the import path, through `unittest`. This machine's existing pure-Python
  PyYAML installation was exposed via `PYTHONPATH`; no packages were installed.
- An AST parse of 239 server Python files passed under Python 3.11. This scan
  excludes underscore/hidden subtrees other than `_host` and `node_modules`.
  Syntax success does not establish runtime correctness.

PowerShell was exercised on macOS. Native Windows junctions, Windows PowerShell
5.1, Python 3.10 itself, and Linux-specific hook playback were not exercised.
The default `python3` is 3.9, below the host's declared requirement; its initial
collection failure was an environment mismatch, not counted as a code defect.
Browser UI flows, live external services, the utilities and in-lab server suites,
full theme suites, and the substantive correctness of all skill instructions
remain outside this pass. Existing user installations were not updated.

## Session reconciliation addendum

While preparing the session website, the independent theme agents' statements
were reviewed separately from the reproduced maintenance findings above.

- **Confirmed, open — Labeling entry task recognition.** At
  `plugins/haipipe-toolkit/skills/2_theme/labeling/haipipe-labeling/scripts/start.py:27`,
  `TYPES` recognizes building/scanning but not `labeling-meaning` or
  `labeling-expression`. Two temporary Task faces passed to `tasks()` returned
  empty type arrays and the fallback dot icon for both types. This corroborates
  `Workbench-Labeling-UI`, native Claude session
  `8a090711-118f-467f-aa4c-ffe26dc18a4b`, transcript line 1024. The entry command's
  building selection at line 99 cannot select those tasks. Aligning routing with
  the two-loop contract changes workflow behavior, so no speculative routing
  change was made. The full workflow was not executed.
- **Unverified — Labeling links and prose.** The same session reports that old
  Work links lead to the previous layout or removed tabs. The entry URL at
  `start.py:69,97` still omits `layout=focus` and requests `Work Details`.
  Live routing and all prose destinations were not rechecked in this pass.
- **Unverified — Insight terminology drift.** `Workbench-Insight-UI`, Claude
  session `42d6f896-1d57-4ce5-8464-c9b1dccd7e8d`, transcript line 5547, reports
  older terminology in the Codex design context than in its implementation.
  Reconcile `blueprints/Project-Ladder/work/b11_theme_insight` with current
  Insight contracts before further design edits; this is not yet a completed
  cross-file terminology audit.
- **Unverified — Discovery navigation drift.** `Discovery theme design`, Codex
  session `01a1bc86-bb69-7383-bf83-7a492cfb1891`, turn
  `01a1bc86-bc4e-7ab3-b5be-cd01f458a4a3`, reported older navigation in guides
  alongside newer views. Exact current passages and legacy route support still
  need checking.

The website in `sites/space-code-quality` distinguishes these attributed
statements from independently verified findings. It also records the current
pair registry rather than inferring pairing from similar display titles.
