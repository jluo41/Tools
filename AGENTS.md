# Repository guidance

## Layout and scope

- `plugins/` contains the first-party packages. Top-level package metadata lives in each package's `.claude-plugin/plugin.json`.
- `references/` contains upstream projects and reference material; many directories are Git submodules. `references/sources.yaml` records origins and license notes.
- The installers discover skills recursively under `plugins/**/skills/`. They do not install skills from `references/`.
- Root install behavior is implemented by `install.sh` and `install.ps1`; both read the shared sound-hook table in `install-hooks.json`.
- `export/` writes one part of this repository (a profile, such as `insight-design`) into a separate target repository, from a commit; `export/README.md`. A profile is named for what it holds; who a target is for lives only in the target's own files.

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
- A page carries no check tally (JL 261113): no "6 to fix", "41 of 70 keys verified" or "🙋 6 printed numbers to fix: …" pill, banner or count line. A check's result is shown where it lands (the number, the sentence, the citation), or not at all. A checker's counts stay in its own report or receipt, never on a workbench page. The same holds for progress tallies ("3 of 7 written", "N of M done", "⚙️ 12 Runs · ✅ 10"): each item shows its own state word where it sits. A count stays only where it is itself the answer ("2 wait for you") or is a report's own finding on that report's page.
- A page never says what state a thing is in ("Status: running", "the status is done", "State · not signed", "this plan is not signed yet"). The layout and the marks show it: an emoji mark beside the item (✅ ⬜ 🏃 ❗ 🙋), its group (Main, Appendix, Not printed), a closed or open fold, a faded or struck row, a button that appears only when the item waits on the reader. Words are kept only for what a mark cannot carry: a required action ("Sign the narrative") or the reason something failed.
- What waits on the reader pops out where it lives, as on a Draft Lab sentence: a mark beside the item (📝 N edit cards, 🙋 N a decision, ✓ handled), its cards opening under it on a click. A section bar carries only a mark from `ui_parts.word_span`: an orange 🙋 N when something inside waits, a quiet ✓ when done, nothing otherwise; never a state word ("nothing yet", "answered", "3 of 5 done"). Every orange mark and waiting question on a page is gathered in the 🙋 N tray beside its title (`focus.js`, a native popover). A section with nothing in it is not shown, Interaction included. Any item can carry these marks and cards: its address, card files and the one writer are in `plugins/haipipe-toolkit/servers/workbench/ref/cards.md`.
- A page never shows who asked for a design or when: no "JL 261113", "(JL 261020: …)", dated rule tags or quoted requests in a label, tooltip, button, banner or note. That provenance belongs in code comments, commit messages and docs only. Content the reader wrote (a timeline entry, a note, a commit message shown as data) stays as written.
- A Studio topic's drawing is a drawing: the idea drawn as a pattern (cycle, timeline, tree, fan-in), never the face's lines listed as text. The method is `references/workflow-diagrams/excalidraw-diagram-skill`; the kit is `haipipe-studio/scripts/quick_draw.py`.

- Each rule JL's feedback made is an article in the owning skill's `CONSTITUTION.md` (page rules: `plugins/haipipe-toolkit/skills/1_base/workbench/haipipe-ui/CONSTITUTION.md`; a theme's pages: its `workbench-<theme>/CONSTITUTION.md`). Read the owner's file before changing a page or a skill; it wins over the skill and the code. `haipipe-ui/scripts/page_words.py --running` scans what every running workbench shows, and `/haistack sweep` reruns every article's check.

## Keep files short

- A file a person reads (code, tests, skills, docs) stays under 700 lines, so one sitting reads it whole. Aim for 600 or less.
- Split by responsibility, never by line count: one module per part of a page, one ref file per topic, each named for what it holds. The old module keeps thin re-exports only while callers move.
- A new file starts under the limit. A change that would push a file past it splits the file first, then makes the change.
- A file already over the limit never grows: the part you change moves out into its own file in the same change, and the rest follows as it is touched.
- Out of scope: `references/`, generated output (built pages, rendered drawings, receipts), data, lock files, and `CHANGELOG.md` files.
- Several sessions edit the big shared files at once. Split one only when no other session is editing it, and say so to them first.

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

## Report

A Report is a message a session working in a Block of some SPACE sends, by SendMessage, to the session that owns a theme's workbench and skills here, `Workbench-<Theme>-UI` (for example `Workbench-Insight-UI`). It lists topics. A topic is one thing worth keeping: a problem, a missing step, a rule that was unclear, or a way of working that proved right, with what happened and the cause by file and line. The owning session collects the reports, recognizes the topics (the same topic often arrives from several Blocks), documents each in the skill or reference that owns it under `plugins/haipipe-toolkit/skills/`, updates the skill, and replies with what changed and what the sender must rerun or restart. The reporting session changes no file here itself. Reports are routed by topic, not by sender: a session takes only the topics its theme owns and passes any other on to the session that owns it.

### If you are a `Workbench-<Theme>-UI` session

You own your theme's topics. A topic comes from a Report or from the user's own message; a message that names a problem is a topic even when it does not say "Report". For every topic:

1. **Name it.** Ask what the topic is: the one thing behind the message, not the single case it showed up in.
2. **Write it down** in your theme's workbench skill, `ref/topics.md` (for example `skills/2_theme/insight/workbench-insight/ref/topics.md`): the topic's name, the user's message word for word (or the Report's text and its sender), the questions it raises, and the date.
3. **Work it.** Answer each question by reading the code and driving the real page or command, not from memory.
4. **Check that it is fixed.** Repeat the case that raised it and look at the output. Mark the topic `fixed` only when that case now passes and something keeps it passing: a test, a check script, or a rule written into the skill.
5. **Say what is still owed.** If the case passes today but nothing guarantees it, mark it `open` and write the extra work that would guarantee it. A fix with no guard is not finished.

Reply to the sender with the state of each topic (`fixed` or `open`), what changed, and what they must rerun or restart.

UI design
=========

Avoid unnecessary secondary labels and descriptions. Let the layout do the explaining.

Do not add unnecessary UI text. Let grouping, spacing, controls, and content explain themselves. Omit routine hints such as "available", "nothing yet", "one per kind", and instructions that repeat visible controls. Keep text when it communicates a meaningful state, a required action, or an otherwise unclear empty state.
