# Project-Packages

Plan the three code packages Tools ships (haipipe-toolkit, haipipe-utils, inlab-human): what each one is for and what to build next.

One of the three Projects of `Tools/blueprints/` (JL 261028: blueprints holds Projects, as `examples-*/` does in a SPACE; each Project keeps its Blocks in `work/`). Block numbers are unique across all of Tools.

## Blocks

- `work/b01_haipipe-toolkit`: Shared toolkit foundations: utilities, base skills, skill layout, and chat; one Job per area. The shared ladder and workbench belong to b10_project_workbench. Theme design belongs to the peer b11–b17 Blocks.
- `work/b02_haipipe-utils`: The blueprint of the `plugins/haipipe-utils` package: the normalizers that turn free text in a cohort's own dialect into typed, referenced numbers, and the API that serves them.
- `work/b03_inlab-human`: The blueprint of the `plugins/inlab-human` package: in-lab human evaluation of deployed prediction endpoints, in two modes (a reader study and a clinician console), over one endpoint tool.
