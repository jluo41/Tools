# References

This directory collects external skill and workflow references.

## Submodules

These entries are tracked as Git submodules so their upstream history stays separate from this repository:

- Research workflow suites: `academic-research-skills`, `aris`, `auto-research-skills`, `auto-empirical-research-skills`, `ai-scientist`.
- Writing, review, and venue skills: `ft50-empirical-writing`, `paperjury`, `awesome-journal-skills`, `aer-skills`, `paper2beamer-skills`.
- Patent, genealogy, and source-tracing skills: `paper-to-patent-*`, `research-genealogy`, `literature-source-tracing`.
- Figure, visualization, and methodology skills: `intelligrapher`, `happy-figure-skill`, `science-superpowers`, `superpower-socialscience-skills`.
- Math and writing-style skills: `mathmodel-skill`, `claude-code-math-skills`, `stop-slop`, `stop-slop-zh`, `llm-wiki-skill`.
- Tool libraries used as references: `tools/statsmodels`, `tools/dowhy`, `tools/causalml`, `tools/econml`, `tools/python-causality-handbook`, `tools/chatgpt-comparison-detection`.

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
