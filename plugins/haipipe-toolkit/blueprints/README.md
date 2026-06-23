HAI-Pipe Run Blueprints
=======================

This folder shows what the Narrative / Probe / Discovery / Task stack should
look like when it runs inside a real project.

These files are plugin-level documentation, not skills and not example
projects. They exist to answer:

- What folders should appear?
- What does the single project log contain?
- What does each local `status.yaml` or `site.md` summarize?
- How do Narrative, Probe, Discovery, and Task point to one another without
  containing one another?

Start here:

- `hai-pipe-stack-concept.png` - visual concept map for Narrative, Probe,
  Discovery, Task, Insight, and sibling folder references.
- `hai-pipe-one-slide-workflow.md` - one-slide figure brief for explaining
  HAI-Pipe as both an evidence-to-delivery workflow and a persisted ML asset
  pipeline.
- `end-to-end-sandwich-run.md` - one narrative, one probe, two discoveries,
  and three tasks from start to finish.
- `minimal-dry-run/` - a tiny completed run fixture with project log,
  status snapshots, local sites, one discovery, and two task results.
