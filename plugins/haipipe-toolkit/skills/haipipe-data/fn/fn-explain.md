Explain Function
================

Purpose: educational mode. Explains haipipe-data concepts with concrete
codebase examples. Two modes depending on whether the user supplied a topic.

---

Step E0: Determine mode
-----------------------

  Read what follows "explain" in the user's command.

  Mode A (targeted)  -- user wrote a concept, question, or comparison
                        e.g. "explain CaseFn"
                             "explain dashboard vs cook"
                             "explain what ROName means"

  Mode B (discovery) -- nothing follows "explain" (or only whitespace)
                        e.g. "/haipipe-data explain"

  Go to Step E1-A or Step E1-B accordingly.

---

Step E1-A: Targeted mode -- map to concept pool
------------------------------------------------

  Scan the user's text for keywords listed in the Concept Pool at the
  bottom of this file.

  If you find a match, note the concept ID(s) and go to Step E2.

  If no keyword matches clearly, ask one clarifying question:
    "Did you mean [best guess]? Or pick from the list below: ..."
  Then show the concept menu (same as Step E1-B) and wait.

---

Step E1-B: Discovery mode -- ask first, then explain
-----------------------------------------------------

  IMPORTANT: Do NOT start explaining immediately.
             Show the menu and wait for the user's answer.

  Present this message:

  ---------------------------------------------------------------
  I can explain any haipipe-data concept. Pick one or more from
  the list below, or say "surprise me" and I'll pick for you.

  Architecture
    1.  Cooking metaphor (Kitchen / Chef / Recipe / Dish / Academy)
    2.  4-stage pipeline flow  (Source -> Record -> Case -> AIData)
    3.  _WorkSpace layout  (what each Store folder holds)
    4.  Builder pattern  (code-dev/ generates code/haifn/)
    5.  YAML @ reference system

  Stage 1 — Source
    6.  SourceFn  (what it does, ProcName_List)
    7.  SourceSet  (the Stage 1 output Dish)
    8.  Schema consistency rule  (why all SourceFns share the same columns)

  Stage 2 — Record
    9.  HumanFn vs RecordFn  (two chef types, two roles)
   10.  RecordSet flat layout  (parquet files per RecordName)
   11.  ROName format  (hHumanName.rRecordName.cWindow)
   12.  5-minute temporal alignment  (why everything snaps to 5-min grid)

  Stage 3 — Case
   13.  TriggerFn  (what fires a case and why)
   14.  CaseFn  (feature extraction at the trigger point)
   15.  Window naming  (Bf24h, Af2h, Bf14d -- what the suffixes mean)
   16.  ROName inside a CaseFn  (how a CaseFn requests a data slice)

  Stage 4 — AIData
   17.  TfmFn  (transforming case features into model-ready format)
   18.  SplitFn  (how train/val/test splitting works)
   19.  feat_vocab vs cf_to_cfvocab  (two vocab files, two purposes)
   20.  HuggingFace Arrow format  (why AIDataStore uses .arrow not .parquet)

  Comparisons
   21.  dashboard vs cook
   22.  dashboard vs load
   23.  design-chef vs design-kitchen
   24.  SourceFn vs RecordFn vs CaseFn  (the three main chef types)
   25.  CaseSet vs AIDataSet  (stage 3 dish vs stage 4 dish)
  ---------------------------------------------------------------

  If user says "surprise me": pick 2 concepts at random from different
  categories, announce which you picked, then go to Step E2.

  Otherwise wait for the user's selection, then go to Step E2.

---

Step E2: Explain each selected concept
---------------------------------------

  For EACH concept the user selected, write a block in this format:

  _______________________________________________________________
  <Concept Name>
  _______________________________________________________________

  What it is
  ----------
  1-2 plain-language sentences. No jargon on first mention.

  Where it lives
  --------------
  Codebase path or _WorkSpace path.

  How it works
  ------------
  Key mechanism, data flow, or role.
  Use a concrete example from the real codebase.

  Real example
  ------------
  Show an actual name (e.g., CGMValueBf24h, OhioT1DMxmlv250302,
  hHmPtt.rCGM5Min.cBf24h) and walk through what it means step by step.

  Common gotcha
  -------------
  One thing people often confuse or misunderstand.

  How it connects
  ---------------
  Link to the concept immediately upstream and downstream in the pipeline.

  Target depth: 150-300 words per concept.
  Tone: clear, practical, conversational. Like explaining to a new team member.
  Code snippets: only when they directly illustrate the concept (keep short).
  Do NOT re-describe the whole architecture for every concept.
  Focus on what is UNIQUE and SPECIFIC about this concept.

---

Step E3: Offer follow-up
-------------------------

  After all explanations, say:

    "Want me to go deeper on any of these, or explain another concept?"

  If the user says "go deeper" or "more detail":
    - Show a worked example tracing a single data row through the concept
    - Or compare with a closely related concept side by side
    - Or show the actual Python signature / module structure

  If the user names a new concept:
    - Go back to Step E1-A.

---

Concept Pool (internal keyword map for Step E1-A)
--------------------------------------------------

  "cooking" / "metaphor" / "kitchen" / "chef" / "recipe" / "dish" / "academy"
    -> Concept 1

  "pipeline" / "flow" / "stages" / "4 stages" / "sequence" / "4-stage"
    -> Concept 2

  "workspace" / "_workspace" / "store" / "sourcestore" / "recstore" / "casestore" / "aidatastore"
    -> Concept 3

  "builder" / "code-dev" / "generated" / "haifn" / "builder pattern" / "generate code"
    -> Concept 4

  "yaml" / "@ reference" / "@meta" / "resolve" / "@ prefix"
    -> Concept 5

  "sourcefn" / "source fn" / "procname" / "procname_list" / "source function"
    -> Concept 6

  "sourceset" / "source set"
    -> Concept 7

  "schema" / "schema consistency" / "same columns" / "column mismatch"
    -> Concept 8

  "humanfn" / "human fn" / "recordfn" / "record fn" / "humanfn vs recordfn"
    -> Concept 9

  "recordset" / "flat layout" / "record set" / "parquet"
    -> Concept 10

  "roname" / "ro name" / "h." / "r." / "c." / "hhmPtt" / "hhmptt" / "record object"
    -> Concept 11

  "5 min" / "5-min" / "5 minute" / "temporal alignment" / "alignment" / "grid" / "dt_s"
    -> Concept 12

  "triggerfn" / "trigger fn" / "trigger" / "case trigger" / "trigger function"
    -> Concept 13

  "casefn" / "case fn" / "case function" / "feature extraction" / "fn_casefn"
    -> Concept 14

  "bf24h" / "af24h" / "window" / "window suffix" / "bf14d" / "af2h" / "window naming" / "ckpd"
    -> Concept 15

  "roname casefn" / "how casefn requests" / "roname_to_rownameinfo"
    -> Concept 16

  "tfmfn" / "tfm fn" / "transform" / "inputtetoken" / "inputmulticf" / "tfm function"
    -> Concept 17

  "splitfn" / "split fn" / "train val test" / "splitting" / "split function"
    -> Concept 18

  "feat_vocab" / "cf_to_cfvocab" / "vocab" / "vocabulary"
    -> Concept 19

  "arrow" / "huggingface" / "hf" / ".arrow" / "datasets" / "load_from_disk"
    -> Concept 20

  "dashboard vs cook" / "dashboard cook" / "observe run"
    -> Concept 21

  "dashboard vs load" / "dashboard load"
    -> Concept 22

  "design-chef vs design-kitchen" / "chef kitchen" / "chef vs kitchen"
    -> Concept 23

  "sourcefn vs recordfn" / "three chef types" / "fn types" / "which fn"
    -> Concept 24

  "caseset vs aidata" / "caseset aidata" / "stage 3 vs stage 4" / "case vs ai"
    -> Concept 25
