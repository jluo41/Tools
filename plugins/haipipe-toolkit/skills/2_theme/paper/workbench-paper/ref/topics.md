# Paper topics

The Paper theme's topics, one section each (the repository's AGENTS.md § Report). A topic is the one thing
behind a message or a Report, not the case it showed up in. `fixed` means the case that raised it passes and
something keeps it passing (the guard); `open` names the work still owed.

```text
T01  an older writing Job hides board.md's session prefix      open
T02  the lab opens windows with no terminals                    open
T03  the lab opens no pages when settings.env names no origin   open
T04  a resumed Section session never gets its first turn        open
```

P below is `skills/2_theme/paper/haipipe-paper`.

## T01 · An older writing Job hides board.md's session prefix · open

- **From**: Report, drfirst-space-2f, 261116, on `/lab examples-4-learning/Project-ExpLearn-SMSDesign/paper/
  Paper-TestToLearn-MS2026`: "`/lab <paper>` stopped with 'pass --prefix <Short>: …'. board.md already has
  `session-prefix: TestToLearn`, and no other paper uses it."
- **What happened**: `P/scripts/create_section_sessions.py` `board_prefix()` (line 77) takes the newest writing
  Job face's `session-prefix:`; with none there and more than one writing Job it returns "" and ignores board.md.
  The paper has j11 (v0429) and j12 (v1007), two versions of one manuscript, neither face naming a prefix. The same
  refusal text is in `open_writing_lab.py:271` and `create_section_sessions.py:481`.
- **Why the rule is there**: JL 261114, two writing Jobs in flight at once (a letter and a full proposal) must not
  share sessions. An older version of the same manuscript is not in flight, so the rule over-fires here.
- **Questions**: does board.md's prefix count when no other writing Job face already claims it (which keeps the
  261114 case safe)? Should the refusal name board.md's prefix as the value to pass?
- **Still owed**: the rule change in `board_prefix()`, `ref/writing-lab.md` § the session prefix, a test with two
  writing Jobs (one older, no face prefix) and one with two Jobs where the other face already holds board.md's.

## T02 · The lab opens windows with no terminals · open

- **From**: the same Report: "the lab opened both windows with no terminals and mentioned the missing extension
  only in the last lines of its output. Once `code --install-extension` ran, the windows that were already open
  loaded the extension … and started all 8 sessions right away, without being reopened."
- **What happened**: `P/scripts/open_writing_lab.py` `main()` checks `extension_installed()` (line 205) only after
  the workspaces and prompts are written, prints a notice and opens the windows anyway (line 333).
  `P/ref/writing-lab.md:85` says a newly installed version runs only in a window opened after the install, which
  holds for an upgrade but not a first install (`activationEvents: onStartupFinished`).
- **Questions**: should the plan (no `--apply`) name the missing extension? Should `--apply` stop before opening
  windows without it (the install is the person's step, never an agent's, `ref/writing-lab.md` § The extension)?
- **Passed on**: the Block lab prints the same late notice (`skills/1_base/workbench/lab/cli/lab.py:262`); that is
  the shared workbench's, not this theme's.
- **Still owed**: the check moved into the plan, the stop on `--apply`, the doc line split into first install and
  upgrade, a test that `--apply` opens nothing without the extension.

## T03 · The lab opens no pages when settings.env names no origin · open

- **From**: the same Report: "every unit's `url` in haipipeLab.terminals was None, so no page opened above any
  terminal, and the lab printed nothing about it. The SPACE's server was running at 127.0.0.1:5603."
- **What happened**: `P/scripts/open_writing_lab.py` `board_origin()` and `page_url()` (lines 138 to 159) read only
  `PUBLIC_URL` or `DOMAIN` from `.server_config/settings.env` and return None silently. `wb.py` writes only `PORT`
  there on first start and builds its own links from `http://127.0.0.1:<port>`
  (`skills/1_base/workbench/workbench/cli/wb.py:256`). The sender fixed their machine with `DOMAIN=127.0.0.1`.
- **Also found**: `board_origin()` strips a `JJLUO_` key prefix and its docstring names it, against the
  repository's AGENTS.md § Keep it general.
- **Questions**: may the lab fall back to the loopback origin, since the lab runs on the same machine as its
  reader (`skills/1_base/draft/haipipe-draft/fn/serve-host.md:133` allows a loopback DOMAIN for the person at this
  machine), or must it warn and stop? Should `wb.py` write `DOMAIN` beside `PORT`?
- **Passed on**: `wb.py` writing `DOMAIN` is the shared workbench's.
- **Still owed**: the decision above; the plan line naming a missing origin; the deployment prefix dropped; a test.

## T04 · A resumed Section session never gets its first turn · open

- **From**: the same Report: "all 7 Section sessions resumed and then sat idle. The first turn in their
  prompts/<unit>.txt (a read-only look, then the review round) was never sent."
- **What happened**: `P/scripts/lab_launch.py:45` runs `claude --resume <sid>` without the prompt, while
  `P/ref/writing-lab.md:54` says every unit's first turn includes the default review round, skipped only when the
  newest Draft was already reviewed at its version.
- **Questions**: should a resume send the prompt when the Section's newest Draft has not been reviewed at its
  version, or should the doc say a resumed session gets no turn? Can a resumed turn re-run a review a person
  already answered?
- **Still owed**: the decision, the change in `lab_launch.py` (or the doc), a test.
