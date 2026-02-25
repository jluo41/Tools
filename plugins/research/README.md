# Research Skills

[Agent Skills](https://agentskills.io/specification) for academic research workflows. Provides Claude with structured approaches for code review, evaluation visualization, notebook pipelines, and paper writing in LaTeX.

## Skills

| Skill | Description |
|-------|-------------|
| [coding-by-logging](skills/coding-by-logging/SKILL.md) | Structured code review and iterative improvement through documented discussions |
| [evaluation-display-skill](skills/evaluation-display-skill/SKILL.md) | Generate evaluation scripts for creating paper tables and figures from model results |
| [notebook-cell-python](skills/notebook-cell-python/SKILL.md) | Manage the pipeline from Python scripts to notebooks to markdown documentation |
| [paper-incubator](skills/paper-incubator/SKILL.md) | Create and interactively refine LaTeX working documents for paper incubation |

## Installation

### Claude Code (via marketplace)

```
/plugin marketplace add research-skills
/plugin install research@research-skills
```

### Claude Code (manual)

Copy the `skills/` directory and `.claude-plugin/` to your project's `.claude/` folder, or to `~/.claude/` for global access.

## License

MIT
