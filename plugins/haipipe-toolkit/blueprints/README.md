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

- `end-to-end-sandwich-run.md` - one narrative, one probe, two discoveries,
  and three tasks from start to finish.
- `minimal-dry-run/` - a tiny completed run fixture with project log,
  status snapshots, local sites, one discovery, and two task results.
