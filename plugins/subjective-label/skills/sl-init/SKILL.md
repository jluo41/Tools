---
name: sl-init
description: "Initialize a subjective-labeling project. Creates the project directory, runs Moderator + Boundary Prober dialogue with the researcher to define topic, label schema, and initial boundaries. Use when starting a new labeling project or when the researcher says /sl-init."
---

Skill: sl-init
==============

One-shot initialization. Runs at project birth only.

Outputs:
  - {project_dir}/config.yaml         topic + label schema
  - {project_dir}/gallery/gallery.json   (empty shell)
  - {project_dir}/gallery/guideline.md   (draft from dialogue)
  - {project_dir}/.state.json         project state machine


Protocol
--------

Step 1. Load ref files.
  Read: ref/ref-architecture.md, ref/ref-assets.md, ref/ref-schema.md
  Confirm: "Loaded. Initializing subjective-label project."

Step 2. Ask researcher for project_dir.
  If arg provided, use it. Otherwise ask.
  Create directory scaffold.

Step 3. Invoke Moderator agent (Task tool, subagent_type: moderator).
  Pass:
    mode: "init"
    project_dir: <path>
  Moderator will:
    - Ask researcher: "What subjective dimension do you want to label?"
    - Ask: "What are the possible label values? (2-6 recommended)"
    - Call Boundary Prober to generate 5-8 probe questions
      (each probe = one edge-case the researcher must adjudicate)
    - Collect adjudications into draft guideline.md
    - Write config.yaml + draft guideline.md + empty gallery.json
    - Initialize .state.json with status="initialized", iteration=0

Step 4. Report to researcher.
  "Project initialized at {path}. Topic: {topic}. Labels: {values}.
   Next: /sl-iterate to run the first labeling iteration."
