fn-help: Intent Routing + Guided Suggestions
=============================================

Interprets the user's natural-language request, maps it to the best-matching
subskill and specific step, and suggests an exact call they can make.

Output format (one suggestion per resolved intent):

  Please call `/haipipe-project {subskill}` specifying {step or portion}
  and ask "{rephrased question that fits the skill's language}"

If the intent is ambiguous, ask ONE clarifying question before suggesting.
Never ask more than one clarifying question at a time.

---

Step 0: Parse the User's Request
==================================

Read the user's request. Identify:

  TOPIC      — what domain the request is about
               (files, structure, progress, code sync, organization, creation, summary)

  ACTION     — what they want to do or know
               (see, check, fix, create, organize, verify, summarize, understand)

  SCOPE      — how broad is the request
               (specific file, specific stage, whole project, cross-project)

Then look up TOPIC + ACTION in the Intent Map below.

---

Intent Map
===========

Each row maps a class of user requests to a subskill + the specific step or
portion to target, plus guidance on how to rephrase the request.

-----------------------------------------------------------------------
INFORMATION — user wants to READ or UNDERSTAND something
-----------------------------------------------------------------------

  What files are in this project / show me all project files
    -> subskill:  organize
       portion:   Phase 1 (File Inventory)
       rephrase:  "Generate the file inventory for {PROJECT_ID}, listing all
                  files in the project folder and related external files."

  What pipeline stages does this project use / what YAMLs are configured
    -> subskill:  review
       portion:   Step 4 (config/ review) + Step 4c (data-map)
       rephrase:  "Review the config/ folder for {PROJECT_ID} and generate
                  docs/data-map.md showing which stages are declared and their
                  FnClass names."

  What Fns or models does this project depend on / what external code does it use
    -> subskill:  review
       portion:   Step 7 (Code Sync Check) + Step 4d (dependency-report)
       rephrase:  "Run the code sync check for {PROJECT_ID} and generate
                  docs/dependency-report.md listing all Fns and models used."

  What other projects share the same Fn or model as this one
    -> subskill:  review
       portion:   Step 7a / 7b (cross-project reuse reporting)
       rephrase:  "Check which other projects share the Fns and models used by
                  {PROJECT_ID} via the code sync check."

  What scripts are in this project / what is the script index
    -> subskill:  review
       portion:   Step 5b (scripts/INDEX.md sync)
       rephrase:  "Generate or update scripts/INDEX.md for {PROJECT_ID} and
                  show me all scripts with their data, functionality, and status."

  What results do we have / what metrics were recorded
    -> subskill:  summarize
       portion:   Step 1d (results/ scan) + Step 2 (Key Results table)
       rephrase:  "Summarize the results for {PROJECT_ID}, extracting key metrics
                  from results/*/metrics.json and the top findings from reports."

  Show me the data flow / how does data move through this project
    -> subskill:  summarize
       portion:   Step 2 (Flow Chart section)
       rephrase:  "Generate the ASCII pipeline flow chart for {PROJECT_ID}
                  showing all active stages from data source through to results."

  What is in cc-archive / what sessions have been recorded
    -> subskill:  review
       portion:   Step 3 (cc-archive/ review)
       rephrase:  "Review the cc-archive/ folder for {PROJECT_ID} — list session
                  files and flag any naming or content issues."

  What is the structure of this project / does the folder layout look right
    -> subskill:  review
       portion:   Step 2 (four-part structure check)
       rephrase:  "Check whether {PROJECT_ID} has all five mandatory folders
                  (cc-archive, config, scripts, results, docs) and flag any deviations."

-----------------------------------------------------------------------
PROGRESS / STATUS — user wants to know how far along the project is
-----------------------------------------------------------------------

  What is the current progress / how far along is this project
    -> subskill:  review
       portion:   Step 4b (TODO.md sync) + Step 4 (declared stages)
       rephrase:  "Update docs/TODO.md for {PROJECT_ID} and report which pipeline
                  stages are done, which are in progress, and which are missing."

  Which pipeline stages are implemented / what is done vs. todo
    -> subskill:  review
       portion:   Step 4 (config check) + Step 7 (code sync) + Step 4b (TODO.md)
       rephrase:  "Review config/ and code sync for {PROJECT_ID} to determine
                  which stages are fully implemented (YAML + FnClass found) and
                  update the Pipeline Progress table in docs/TODO.md."

  Are all scripts done / which scripts still have missing results
    -> subskill:  review
       portion:   Step 5 (scripts/results alignment) + Step 5b (INDEX.md sync)
       rephrase:  "Check script-result alignment for {PROJECT_ID} — flag any
                  scripts without a matching results/ folder and update INDEX.md status."

  What is missing from this project / full gap report
    -> subskill:  review
       portion:   (full review — all steps)
       rephrase:  "Run a full gap analysis on {PROJECT_ID} and produce the complete
                  gap report covering structure, docs, config, scripts, results,
                  and code sync."

  Is the implementation complete / are all Fns and models implemented
    -> subskill:  review
       portion:   Step 7 (full code sync: 7a + 7b + 7c + 7d)
       rephrase:  "Run the full code sync check for {PROJECT_ID}: verify all
                  FnClasses in config/ resolve to real classes, all builders have
                  generated output, and all script imports are valid."

  Are there any broken imports or missing classes in the scripts
    -> subskill:  review
       portion:   Step 7d (scripts/ import resolution)
       rephrase:  "Scan all scripts in {PROJECT_ID}/scripts/ and verify every
                  imported class exists in code/haifn/ or code/hainn/."

  What should I do next / what is the next step for this project
    -> subskill:  review
       portion:   Step 4b (TODO.md sync) — reads current Pipeline Progress table
       rephrase:  "Update docs/TODO.md for {PROJECT_ID} and tell me the first
                  incomplete item across Required Files, Track A Stubs, and
                  Pipeline Progress tables."

  Regenerate just the data-map / show the pipeline flow without a full review
    -> subskill:  review
       portion:   Step 4 (read config/ for DECLARED_STAGES) + Step 4c (data-map only)
       rephrase:  "Read config/ for {PROJECT_ID} to identify declared stages, then
                  regenerate docs/data-map.md only — skip all other review steps."

-----------------------------------------------------------------------
ORGANIZATION / CLEANUP — user wants to tidy or restructure files
-----------------------------------------------------------------------

  Clean up or reorganize the project / files are in the wrong place
    -> subskill:  organize
       portion:   Phase 1 (inventory) + Phase 2 (proposed moves)
       rephrase:  "Inventory all files in {PROJECT_ID}, then propose a reorganization
                  to bring the project to the standard five-part layout."

  Rename scripts to follow naming convention
    -> subskill:  organize
       portion:   Phase 2 (script naming issues)
       rephrase:  "Propose renames for scripts in {PROJECT_ID}/scripts/ that do not
                  follow the {seq}_{YYMMDD}_{desc}.{ext} convention."

  Check if imports and paths still work after moving files
    -> subskill:  organize
       portion:   Phase 3 / organize verify
       rephrase:  "Verify that all imports and path references in {PROJECT_ID}/scripts/
                  are still valid after the recent reorganization."

  Just show me what files exist without proposing changes
    -> subskill:  organize
       portion:   Phase 1 only (stop after inventory, do not proceed to Phase 2)
       rephrase:  "Generate the file inventory for {PROJECT_ID} (Phase 1 only) —
                  list all project files and related external files, and stop
                  before proposing any reorganization."

-----------------------------------------------------------------------
CREATION / SCAFFOLDING — user wants to set up something new
-----------------------------------------------------------------------

  Start a new project / create a new experiment folder
    -> subskill:  new
       portion:   (full flow — both Track A and Track B)
       rephrase:  "Create a new haipipe project, walking me through the project
                  naming, pipeline stages, dataset, and whether new Fns or models
                  are needed."

  Add a new pipeline function stub for a new dataset
    -> subskill:  new
       portion:   Track A A1 (Step 3, pipeline Fn stubs)
       rephrase:  "Add Track A pipeline Fn stubs for a new dataset to an existing
                  project, and auto-generate the paired example scripts."

  Add a new ML model stub
    -> subskill:  new
       portion:   Track A A2 (Step 3, ML model stubs)
       rephrase:  "Add Track A ML model stubs (algorithm, tuner, instance) to an
                  existing project, and auto-generate the paired example script."

-----------------------------------------------------------------------
DOCUMENTATION — user wants to generate or update docs
-----------------------------------------------------------------------

  Generate a project summary / write a summary for this project
    -> subskill:  summarize
       portion:   (full flow — Step 1 + Step 2 + Step 3)
       rephrase:  "Generate docs/project-summary.md for {PROJECT_ID} with the
                  pipeline stages used, key metrics from results/, and an ASCII
                  flow chart."

  Update TODO.md / refresh the planning tracker
    -> subskill:  review
       portion:   Step 4b (docs/ generation — TODO.md update)
       rephrase:  "Update docs/TODO.md for {PROJECT_ID}: sync Pipeline Progress
                  rows against current config/ YAML presence and mark completed stages."

  Generate the data-map / show the pipeline flow in a diagram
    -> subskill:  review
       portion:   Step 4c (data-map generation)
       rephrase:  "Generate docs/data-map.md for {PROJECT_ID} showing the full
                  pipeline flow from raw data through to results, derived from
                  config/ YAML files."

  Generate the dependency report / what Fns and models does this project need
    -> subskill:  review
       portion:   Step 4d (dependency-report generation)
       rephrase:  "Generate docs/dependency-report.md for {PROJECT_ID} listing
                  all pipeline Fn and model dependencies, their implementation status,
                  and any cross-project reuse."

-----------------------------------------------------------------------
AMBIGUOUS — multiple intents possible
-----------------------------------------------------------------------

  If TOPIC = "check" or "look at" with no clear ACTION:
    Ask: "Are you looking to (a) check the project for structural gaps and missing
          files, (b) check implementation status (imports, code sync), or
          (c) check what files exist and whether they're organized correctly?"

    (a) -> review (full gap analysis)
    (b) -> review Step 7 (code sync)
    (c) -> organize Phase 1 + 2

  If TOPIC = "status" with no project specified:
    Ask: "Which project would you like to check the status of? I can auto-detect
          from recent changes, or you can give me a path."
    Then route to: review Step 4b + Step 5b

  If TOPIC = "everything" or "full check":
    Ask: "Should I run a full gap analysis (review) or generate a human-readable
          summary (summarize) — or both?"
    Both -> run review first, then summarize

---

Step 1: Compose the Suggestion
================================

Once the intent is resolved, output ONE suggestion per distinct intent using
this exact format:

  Please call `/haipipe-project {subskill}` specifying {step or portion (if not full flow)}
  and ask "{rephrased question}"

Guidelines for the rephrased question:
  - Use the skill's vocabulary (PROJECT_ID, FnClass, Track A/B, declared stages, etc.)
  - Be specific enough that the skill can start without further questions
  - Confirm the user's intention so they can correct any misunderstanding
  - If a project path was mentioned, include it in the rephrase

Examples of well-formed suggestions:

  Please call `/haipipe-project review` specifying Step 7 (code sync check)
  and ask "Run the full code sync check for ProjC-Model-2-GlucoseTransformer:
  verify all FnClasses in config/ resolve to real classes and all script imports
  are valid."

  Please call `/haipipe-project organize` specifying Phase 1 only (file inventory,
  no reorganization) and ask "Generate the file inventory for ProjB-Bench-1-FairGlucose,
  listing all project files and related external Fn/model files."

  Please call `/haipipe-project summarize`
  and ask "Generate docs/project-summary.md for ProjC-Model-2-GlucoseTransformer
  with the pipeline stages used, key metrics from results/, and an ASCII flow chart."

---

Step 2: Multiple Intents
=========================

If the user's request maps to more than one intent (e.g., "check progress and
see if files are organized"), output one suggestion per intent, numbered:

  Your request covers two things:

  1. Please call `/haipipe-project review` specifying Step 4b + Step 5b
     and ask "..."

  2. Please call `/haipipe-project organize` specifying Phase 1 + Phase 2
     and ask "..."

  You can run these in sequence. Start with 1.

---

Step 3: Out-of-Scope Requests
===============================

If the user's request is outside what haipipe-project covers (e.g., asking
to implement a model, run a pipeline, write a script):

  Print:
    "That task is outside haipipe-project's scope. Here is where to go instead:

     {one of the following as applicable}

     Implement a pipeline Fn (Stage 1-4):
       Use /haipipe-data design-chef {stage}

     Implement an ML model (Stage 5):
       Use /haipipe-nn

     Deploy an endpoint (Stage 6):
       Use /haipipe-end

     Record this CC session:
       Use /cc-session-summary -> cc-archive/"

---

MUST NOT
---------

- Do NOT execute any subskill — only suggest which one to call and how.
- Do NOT read project files during help — the suggestion should be based on
  the user's description alone, unless the project path is needed to fill in
  PROJECT_ID in the rephrase (in which case, only read the folder name).
- Do NOT ask more than one clarifying question before making a suggestion.
- Do NOT produce suggestions for tasks outside the five subskills
  (new / review / summarize / organize / help).
