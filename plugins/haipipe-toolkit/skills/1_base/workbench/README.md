# workbench · the family map

The shared screen manuals, in one folder (JL 261016, s21-D05); moved out of `../draft/` on 2026-10-16. The screens'
code is in `servers/` (`servers/workbench/`, `servers/_host/`); these skills say what each screen shows, what it
stores and who writes it. A theme's own screen manual (`2_theme/<theme>/workbench-<theme>`) stays with its theme, and
the Studio screen is `../project/haipipe-studio/ref/screen.md`.

```
workbench/             🔌 the /wb door and the WORKBENCH contract: open a place by path or words, ref/roster.md (the folder roster)
workbench-task-draft/  📃 the Page Task's screen (code: servers/workbench/workbench-task-draft/): Draft, Evidence, Delivery, Run Space, Folder; its ref/ material contracts
haipipe-ui/            👁 the rules every page passes (five-second test, one verb per section) and the blind page review
haipipe-interaction/   📝 request and record the input a page's work needs: question forms, answers pasted back; one Interaction button on the workbench rows (scripts/collect.py)
```

Start at `workbench/SKILL.md` (`/wb`). The Page agents (`haipipe-draft-*-agent`) live in `../draft/haipipe-draft/agents/`.
