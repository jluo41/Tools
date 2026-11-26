# The buttons

Part of haipipe-studio's topic contract (`ref/topic-contract.md`).


| What it does | where | how |
|---|---|---|
| add a topic | `sNN-<topic>/` | `new_topic.py topic <level> --slug … --title … --band …` |
| redraw a topic | the topic's drawing | rerun its `build_*.py` (or draw by hand), then the preview |
| save this session or meeting | a round, `passes/pNN-<MMDD>/` | `new_topic.py session <level> sNN --title … [--kind meeting]` |
