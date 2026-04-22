fn-review: Structural Code Review for haipipe-data Pipeline Functions
======================================================================

**Purpose**: Read a haipipe-data file (generated Fn, builder script, or YAML
config) and check it against the haipipe-data structural contract. Reports
PASS / WARN / FAIL per criterion. Read-only: does NOT modify any files.

**Scope**: Generated Fns in code/haifn/, builder scripts in code-dev/1-PIPELINE/,
and YAML pipeline configs.

---

Step R0: Determine Mode
-----------------------

Read what follows "review" in the user's command.

  Mode A (targeted)  -- user provided a file path
                        e.g. "/haipipe-data review code/haifn/fn_case/case_casefn/CGMValueBf24h.py"

  Mode B (discovery) -- nothing follows "review" (or only whitespace)

  Go to Step R1-A or Step R1-B accordingly.

---

Step R1-A: Targeted -- detect file type from path
--------------------------------------------------

Map the given path to a Fn type using the table below.
If the path does not match any pattern, go to Step R1-B and ask the user
to clarify which type it is.

  Path pattern                               Fn type
  -----------------------------------------  -------------------
  code/haifn/fn_source/*.py                  SourceFn
  code/haifn/fn_record/human/*.py            HumanFn
  code/haifn/fn_record/record/*.py           RecordFn
  code/haifn/fn_case/fn_trigger/*.py         TriggerFn
  code/haifn/fn_case/case_casefn/*.py        CaseFn
  code/haifn/fn_aidata/entryinput/*.py       InputTfmFn
  code/haifn/fn_aidata/entryoutput/*.py      OutputTfmFn
  code/haifn/fn_aidata/split/*.py            SplitFn
  code-dev/1-PIPELINE/1-Source-WorkSpace/*.py  SourceFn builder
  code-dev/1-PIPELINE/2-Record-WorkSpace/h*.py HumanFn builder
  code-dev/1-PIPELINE/2-Record-WorkSpace/r*.py RecordFn builder
  code-dev/1-PIPELINE/3-Case-WorkSpace/a*.py   TriggerFn builder
  code-dev/1-PIPELINE/3-Case-WorkSpace/c*.py   CaseFn builder
  code-dev/1-PIPELINE/4-AIData-WorkSpace/c*.py TfmFn builder
  code-dev/1-PIPELINE/4-AIData-WorkSpace/s*.py SplitFn builder
  config/**/*.yaml                              YAML config (stage auto-detected)

  For YAML configs: inspect the top-level keys to determine stage:
    Has SourceArgs        -> Source config
    Has HumanRecords      -> Record config
    Has CaseArgs          -> Case config
    Has InputArgs         -> AIData config

  Once the type is known, go to Step R2.

---

Step R1-B: Discovery -- ask for file path
-----------------------------------------

IMPORTANT: Do NOT start reviewing immediately.
Ask the user to provide the file they want reviewed.

Present this message:

  ---------------------------------------------------------------
  Please provide the file path you want me to review. I can check:

  Generated Fns (code/haifn/)
    SourceFn       code/haifn/fn_source/<SourceFnName>.py
    HumanFn        code/haifn/fn_record/human/<HumanFnName>.py
    RecordFn       code/haifn/fn_record/record/<RecordFnName>.py
    TriggerFn      code/haifn/fn_case/fn_trigger/<TriggerFnName>.py
    CaseFn         code/haifn/fn_case/case_casefn/<CaseFnName>.py
    InputTfmFn     code/haifn/fn_aidata/entryinput/<TfmFnName>.py
    OutputTfmFn    code/haifn/fn_aidata/entryoutput/<TfmFnName>.py
    SplitFn        code/haifn/fn_aidata/split/<SplitFnName>.py

  Builder scripts (code-dev/1-PIPELINE/)
    Any builder:   code-dev/1-PIPELINE/<N>-*-WorkSpace/<builder>.py

  Pipeline configs (config/)
    Any config:    config/<path>/<name>.yaml
  ---------------------------------------------------------------

Wait for the user to provide a path, then go to Step R2.

---

Step R2: Read the file
-----------------------

Read the file at the given path.
State: "Reviewing: <path> | Detected type: <FnType>"

If the file does not exist, report:
  ERROR: File not found at <path>. Please check the path and try again.
  Discover available files:
    ls code/haifn/fn_source/
    ls code/haifn/fn_record/human/
    ... (relevant ls for the intended type)

---

Step R3: Apply the Type Checklist
-----------------------------------

Run the checklist for the detected Fn type (see Checklists section below).

For each criterion:
  PASS  -- criterion satisfied (evidence: show the matching line/value)
  WARN  -- criterion partially met or ambiguous (explain why)
  FAIL  -- criterion violated (show the offending line/value)
  N/A   -- criterion does not apply to this specific Fn

Apply ALL criteria in the checklist. Do NOT skip any criterion.
Show the evidence (quoted file content) for FAIL and WARN items.

---

Step R4: Report Findings
--------------------------

Print the review report in this format:

  Reviewing: <path>
  Detected type: <FnType>
  _________________________________________________________________________

   <icon>  <criterion short description>
           [evidence line if FAIL or WARN]
  ...
  _________________________________________________________________________
  Score: <PASS count> / <applicable count> -- <FAIL count> failures, <WARN count> warnings

  icon key:  PASS = [OK]   WARN = [WRN]   FAIL = [ERR]   N/A = [---]

Then print:

  Failures (if any):
  ------------------
  For each FAIL: state exactly what is wrong and what the correct value should be.

  Warnings (if any):
  ------------------
  For each WARN: explain the ambiguity and what to verify manually.

  Next steps:
  -----------
  If FAIL count > 0:
    "Fix the <N> failing items above. Re-run /haipipe-data review <path> to confirm."
  If FAIL count == 0 and WARN count > 0:
    "Investigate the <N> warnings above. File passes structural review."
  If FAIL count == 0 and WARN count == 0:
    "File passes structural review. Safe to register in config and test end-to-end."

---

Step R5: Offer Follow-Up
--------------------------

After the report, say:

  "Want me to review another file, or explain any of the failing criteria?"

If user says "explain <criterion>": go to fn-explain.md Step E1-A with that concept.
If user says "fix it": go to fn-design-chef.md (with the relevant stage ref loaded).
If user provides another path: restart from Step R1-A.

---

Checklists
==========

Each checklist criterion has:
  ID     -- short code for reference
  Check  -- what to look for in the file
  Rule   -- the haipipe-data contract rule being checked

___________________________________________________________________________
CHECKLIST: SourceFn   (code/haifn/fn_source/*.py)
___________________________________________________________________________

  ID     Check                                           Rule
  ------+-----------------------------------------------+---------------------
  SF-1   SourceFile_SuffixList defined at module level   required attribute
  SF-2   ProcName_List defined, non-empty list           required attribute
  SF-3   ProcName_to_columns defined, one key per        required attribute;
         ProcName in ProcName_List                       schema completeness
  SF-4   MetaDict defined at module level                required attribute
  SF-5   process_Source_to_Processed function exists     required function
  SF-6   process_Source_to_Processed takes 3 params:     function signature
         (SourceFile_List, get_ProcName_from_SourceFile,
          SPACE=None)
  SF-7   get_ProcName_from_SourceFile function exists    required function
  SF-8   CGM domain: Medication columns = 11             schema consistency
         (PatientID, MedAdministrationID, AdministrationDate,
          EntryDateTime, UserAdministrationDate,
          AdministrationTimeZoneOffset, AdministrationTimeZone,
          MedicationID, Dose, medication, external_metadata)
  SF-9   CGM domain: Exercise columns = 13               schema consistency
  SF-10  CGM domain: Diet columns = 15                   schema consistency

  NOTE SF-8/9/10: Only check if the SourceFn handles CGM/diabetes data.
  For other domains, check that ProcName_to_columns is consistent within the domain.

___________________________________________________________________________
CHECKLIST: HumanFn   (code/haifn/fn_record/human/*.py)
___________________________________________________________________________

  ID     Check                                           Rule
  ------+-----------------------------------------------+---------------------
  HF-1   OneHuman_Args defined with all 4 keys:         required attribute
         HumanName, HumanID, RawHumanID, HumanIDLength
  HF-2   HumanIDLength is an integer (not a string)     correct type
  HF-3   Excluded_RawNameList defined, is a list        required attribute
  HF-4   get_RawHumanID_from_dfRawColumns defined       required function
  HF-5   get_RawHumanID_from_dfRawColumns takes 1 param function signature
  HF-6   Function body includes a None return path      entity ID detection;
         for tables that don't contain the entity ID    missing = pipeline crash

___________________________________________________________________________
CHECKLIST: RecordFn   (code/haifn/fn_record/record/*.py)
___________________________________________________________________________

  ID     Check                                           Rule
  ------+-----------------------------------------------+---------------------
  RF-1   OneRecord_Args defined at module level          required attribute
  RF-2   RawName_to_RawConfig defined (dict)             required attribute
  RF-3   attr_cols defined, is a list                    required attribute
  RF-4   get_RawRecProc_for_HumanGroup defined           required function
  RF-5   Function has 3 params:                          CRITICAL: wrong signature
         (df_RawRec_for_HumanGroup, OneRecord_Args,       breaks all pipelines
          df_Human)
  RF-6   EMPTY_COLS defined inside function body         processing invariant 1
  RF-7   pd.DataFrame(columns=EMPTY_COLS) returned at   processing invariant 1
         every early-exit filter point
  RF-8   pd.to_datetime called with format='mixed'       processing invariant 2
         and errors='coerce'
  RF-9   assert len(df) == N (or similar) present        processing invariant 4
         after a pd.merge with df_Human                  prevents silent row inflation
  RF-10  DT_s column built and rounded                   processing invariant 6
  RF-11  DT_r column built and rounded                   processing invariant 6
  RF-12  DT_tz column built with fallback chain:         processing invariant 5
         explicit offset -> user_tz -> default 0
  RF-13  timezone filter present (abs < threshold)       processing invariant 1
  RF-14  value range filter present for numeric col      processing invariant 3

___________________________________________________________________________
CHECKLIST: TriggerFn   (code/haifn/fn_case/fn_trigger/*.py)
___________________________________________________________________________

  ID     Check                                           Rule
  ------+-----------------------------------------------+---------------------
  TF-1   Trigger attribute defined (string)              required attribute
  TF-2   Trigger_Args defined (dict)                     required attribute
  TF-3   Function named get_CaseTrigger_from_RecordBase  CRITICAL: wrong name
         (NOT fn_TriggerFn or any other name)             breaks loader
  TF-4   Function takes 3 params:                        function signature
         (record_set, Trigger_Args, df_case_raw=None)
  TF-5   Function returns a dict (not a DataFrame)       return contract
  TF-6   Return dict contains 'df_case' key              required output key

___________________________________________________________________________
CHECKLIST: CaseFn   (code/haifn/fn_case/case_casefn/*.py)
___________________________________________________________________________

  ID     Check                                           Rule
  ------+-----------------------------------------------+---------------------
  CF-1   CaseFnName defined; value matches filename      required attribute;
         (without .py extension)                         naming convention
  CF-2   RO_to_ROName defined (dict)                     required attribute
  CF-3   All ROName values use 3-part format:            ROName contract
         h<HumanFn>.r<RecordFn>.c<Ckpd>
         (2 dots, h/r/c prefixes)
  CF-4   Ckpd_to_CkpdObsConfig defined (dict)           required attribute
  CF-5   All CkpdNames in RO_to_ROName values appear     contract consistency
         in Ckpd_to_CkpdObsConfig keys
  CF-6   ROName_to_RONameInfo defined (dict)             required attribute
  CF-7   HumanRecords defined (dict)                     required attribute
  CF-8   COVocab defined (dict)                          required attribute
  CF-9   MetaDict defined with exactly 7 keys:           CRITICAL: builder needs
         CaseFnName, RO_to_ROName,                        all 7 keys
         Ckpd_to_CkpdObsConfig, ROName_to_RONameInfo,
         HumanRecords, COVocab, fn_CaseFn
  CF-10  fn_CaseFn defined with 6 params:               function signature
         (case_example, ROName_list, ROName_to_ROData,
          ROName_to_ROInfo, COVocab, context)
  CF-11  fn_CaseFn returns dict with SUFFIX-ONLY keys    CRITICAL: prefixed
         (--tid, --wgt, --val, --str, or no suffix)       keys break pipeline
         Does NOT return keys containing CaseFnName

___________________________________________________________________________
CHECKLIST: InputTfmFn   (code/haifn/fn_aidata/entryinput/*.py)
___________________________________________________________________________

  ID     Check                                           Rule
  ------+-----------------------------------------------+---------------------
  IT-1   build_vocab_fn defined                          required function
  IT-2   build_vocab_fn takes exactly 2 params:          CRITICAL: wrong count
         (InputArgs, CF_to_CFVocab)                       breaks vocab build
  IT-3   tfm_fn defined                                  required function
  IT-4   tfm_fn takes exactly 4 params:                  CRITICAL: wrong count
         (case_features, InputArgs, CF_to_CFvocab,        breaks transform
          feat_vocab=None)
  IT-5   Does NOT contain a 2-param tfm_fn               would indicate OutputTfmFn
         (that signature belongs to OutputTfmFn)          pattern in wrong file

___________________________________________________________________________
CHECKLIST: OutputTfmFn   (code/haifn/fn_aidata/entryoutput/*.py)
___________________________________________________________________________

  ID     Check                                           Rule
  ------+-----------------------------------------------+---------------------
  OT-1   tfm_fn defined                                  required function
  OT-2   tfm_fn takes exactly 2 params:                  CRITICAL: wrong count
         (case, OutputArgs)                               breaks label extraction
  OT-3   Does NOT take 4 params                          4-param = InputTfmFn;
         (that is InputTfmFn's signature)                 wrong type in file

___________________________________________________________________________
CHECKLIST: SplitFn   (code/haifn/fn_aidata/split/*.py)
___________________________________________________________________________

  ID     Check                                           Rule
  ------+-----------------------------------------------+---------------------
  SP-1   dataset_split_tagging_fn defined                required function
  SP-2   Function takes exactly 2 params:                function signature
         (df_tag, SplitArgs)
  SP-3   Function adds 'split_ai' column to df_tag       return contract
  SP-4   split_ai values are 'train', 'validation',      CRITICAL: 'val'/'test'
         'test-id', 'test-od'                             are wrong values
         (NOT 'val', NOT 'test')
  SP-5   Function returns the modified df_tag            return contract
         (NOT a dict of split DataFrames)

___________________________________________________________________________
CHECKLIST: Builder script   (code-dev/1-PIPELINE/**/*.py)
___________________________________________________________________________

  ID     Check                                           Rule
  ------+-----------------------------------------------+---------------------
  BS-1   RUN_TEST = True (or similar flag) present       builder pattern
  BS-2   [BOILERPLATE] comment tag present               builder pattern
  BS-3   [CUSTOMIZE] comment tag present                 builder pattern
  BS-4   OUTPUT_DIR or output directory defined          required for generation
  BS-5   Fn name constant defined (SOURCE_FN_NAME,       required for generation
         CASEFN_NAME, etc.)
  BS-6   Builder does NOT hardcode production paths      safety: generated code
         (no _WorkSpace/ absolute paths)                  should be portable

___________________________________________________________________________
CHECKLIST: Source YAML config   (config/**/*.yaml with SourceArgs)
___________________________________________________________________________

  ID     Check                                           Rule
  ------+-----------------------------------------------+---------------------
  YS-1   SourceArgs present at top level                 required section
  YS-2   SourceArgs.raw_data_name present and non-empty  required key
  YS-3   SourceArgs.SourceFnName present and non-empty   required key

___________________________________________________________________________
CHECKLIST: Record YAML config   (config/**/*.yaml with HumanRecords)
___________________________________________________________________________

  ID     Check                                           Rule
  ------+-----------------------------------------------+---------------------
  YR-1   source_set_name present (top-level or nested    CRITICAL: required input
         under RecordArgs)
  YR-2   source_set_name uses format '<Name>/@<Fn>'      naming convention
  YR-3   HumanRecords present (top-level or nested       required key
         under RecordArgs)
  YR-4   HumanRecords values are lists                   format requirement

___________________________________________________________________________
CHECKLIST: Case YAML config   (config/**/*.yaml with CaseArgs)
___________________________________________________________________________

  ID     Check                                           Rule
  ------+-----------------------------------------------+---------------------
  YC-1   record_set_name present and non-empty           required key
  YC-2   CaseArgs present                                required section
  YC-3   CaseArgs.Case_Args is a list                    required structure
  YC-4   Each Case_Args entry has TriggerName            required key
  YC-5   Each Case_Args entry has CaseFnList (a list)    required key

___________________________________________________________________________
CHECKLIST: AIData YAML config   (config/**/*.yaml with InputArgs)
___________________________________________________________________________

  ID     Check                                           Rule
  ------+-----------------------------------------------+---------------------
  YA-1   InputArgs present                               required section
  YA-2   InputArgs.input_method present and non-empty    required key
  YA-3   InputArgs.input_casefn_list present (list)      required key
  YA-4   If SplitArgs present: uses SplitMethod          CRITICAL: split_method
         (capital M), NOT split_method                    (lowercase) is wrong
  YA-5   If SplitArgs present: uses Split_to_Selection,  CRITICAL: split_ratio
         NOT split_ratio                                  does not exist
  YA-6   If SplitArgs.Split_to_Selection present:        correct split labels
         split keys are 'train', 'validation', 'test-id',
         'test-od' -- NOT 'val' or 'test'
  YA-7   If OutputArgs present: uses output_method,      CRITICAL: output_format
         NOT output_format                                does not exist

---

Quick Reference: Checklist by Type
====================================

  File type          Checklist IDs to apply
  -----------------  ----------------------------------------
  SourceFn           SF-1 through SF-10 (SF-8/9/10 = CGM only)
  HumanFn            HF-1 through HF-6
  RecordFn           RF-1 through RF-14
  TriggerFn          TF-1 through TF-6
  CaseFn             CF-1 through CF-11
  InputTfmFn         IT-1 through IT-5
  OutputTfmFn        OT-1 through OT-3
  SplitFn            SP-1 through SP-5
  Builder script     BS-1 through BS-6
  Source YAML        YS-1 through YS-3
  Record YAML        YR-1 through YR-4
  Case YAML          YC-1 through YC-5
  AIData YAML        YA-1 through YA-7
