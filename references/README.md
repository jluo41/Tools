# References

This directory collects external skill, workflow, and tool references.

## Remote Workspaces

- [How dsh-remote works in Tools-SPACE](dsh-remote-guide.md): where commands run, where files are saved, and when to sync the local mirror.
- [dsh-remote upstream source](dsh-remote): Git submodule pinned to `v1.4.1`, matching the version used for the guide.

## Generative UI

- [dsh-a2ui](dsh-a2ui): answer-first, self-contained A2UI snapshots.
- [dsh-genui-a2ui](dsh-genui-a2ui): reactive A2UI Express surfaces, live docks, and structured forms.
- [Comparison and learning path](dsh-a2ui-comparison.md): what to borrow for Tools-SPACE without replacing the file-backed workbench.

## Submodules

These entries are tracked as Git submodules so their upstream history stays separate from this repository:

- Research workflow suites: `academic-research-skills`, `aris`, `auto-research-skills`, `auto-empirical-research-skills`, `ai-scientist`.
- Writing, review, and venue skills: `nature-paper-skills`, `paperspine`, `ft50-empirical-writing`, `paperjury`, `awesome-journal-skills`, `aer-skills`, `paper2beamer-skills`, `ieee-latex-writer`, `grant-writer-skills`.
- Paper RAG, citation, statistics, reproduction, and survey skills: `paper-rag-skill`, `cite-guard`, `research-agent-skills`, `reprorun`, `research-co-pilot`.
- Patent, genealogy, and source-tracing skills: `paper-to-patent-*`, `research-genealogy`, `literature-source-tracing`.
- Figure, visualization, and methodology skills: `scipilot-figure-skill`, `intelligrapher`, `happy-figure-skill`, `science-superpowers`, `superpower-socialscience-skills`.
- Math skills: `mathmodel-skill`, `claude-code-math-skills`.
- Deck and slide skills: `presentation-agent` (a transcript-to-deck agent with an HTML deck kit; no upstream license, read only); `baoyu-skills` (MIT; `skills/baoyu-slide-deck`: content into slide pictures by image generation, 17 style presets, merged to PPTX and PDF; haipipe-studio's idea slides follow its base prompt and `sketch-notes` style); `ian-handdrawn-ppt` (MIT, attribution to Ian kept: refined ink-and-pastel teaching-note pages, made for Chinese text; tried 261029, too quiet for a Studio slide).
- Agent governance and writing-style skills: `writing-dna-skill`, `sepia`, `stop-that-shit`, `stop-slop`, `stop-slop-zh`, `llm-wiki-skill`.
- Anti-AI writing comparison shelf: [`anti-ai-writing-skills.md`](anti-ai-writing-skills.md); it records the ten screenshot items and the exact `SKILL.md` path for each source.
- HAI integration: `haipipe-draft-review/ref/anti-slop-adapter.md` and its
  read-only `cli/anti_slop.py` adapter consume one selected reference after
  paragraph drafting; the references here remain independently updateable.
- Tool libraries used as references: `tools/statsmodels`, `tools/dowhy`, `tools/causalml`, `tools/econml`, `tools/python-causality-handbook`, `tools/chatgpt-comparison-detection`.
- Visual feedback tools: [`edithere`](edithere) (PolyForm Noncommercial 1.0.0, source-available; commercial use requires separate authorization). [Review and workbench mapping](edithere-review.md).

Use this after cloning the parent repository:

```sh
git submodule update --init --recursive
```

To refresh references from upstream:

```sh
git submodule update --remote --merge --recursive
```

## Workflow Diagrams

`workflow-diagrams/` entries are also submodules. The copied local diagram snapshots were moved to `/tmp/workflow-diagrams-backup-20260620` before these paths were replaced with upstream repositories.

## Comparative Reports

- `haipipe-paper-comparison-reports/`: one report per external paper/research skill library, each compared against `Tools/plugins/haipipe-toolkit/skills/paper`.
