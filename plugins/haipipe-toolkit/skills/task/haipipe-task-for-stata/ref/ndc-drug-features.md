# NDC drug-type feature pattern

Reference for case-pipeline feat builders that merge NDC crosswalks to generate
per-drug-class features (opioidrx, diabetesrx, etc.).

## Pattern: per-class binary flags + n_distinct

When a PDE feat builder (bfaf-{bt,nt,bnt}-pde-*rx.do) merges an NDC crosswalk,
it can produce two tiers of drug-type features:

### Tier 1: potency/class flags (always reliable)

Computed from structured NDC metadata, not name matching.
Coverage = 100% of crosswalk NDCs.

```
Opioid:   is_strong_opioid (from MME threshold + DEA schedule)
Diabetes: drug class membership (one NDC file per class: metformin, insulin, glp1, sglt2, dpp4, sulf)
```

### Tier 2: named-drug flags (partial coverage)

Computed via `strpos(lower(generic_name), "<drug>")`. Coverage depends on
FDA NDC Directory match rate (~28% for opioid crosswalk as of 2026-06).
Unmatched NDCs get all named-drug flags = 0.

```
Opioid:   has_fentanyl, has_oxycodone, has_hydrocodone, has_morphine,
          has_codeine, has_tramadol, has_methadone, has_buprenorphine
```

### Tier 3: diversity count

Post-collapse sum of tier-2 flags: `n_distinct_opioid`.
Max = number of tier-2 drug categories. Useful as polypharmacy proxy.


## Opioid crosswalk coverage (NDC_opioid_named.dta)

```
Total NDCs:          2,891
With generic_name:     813 (28%)  -- FDA NDC Directory match
Without:             2,078 (72%)  -- all is_strong=0

Drug         NDCs   strong?   Avg MME/unit
----------   -----  -------   ------------
oxycodone      230  yes       18.2
hydrocodone    197  yes       10.9
tramadol        91  no        12.1
codeine         76  no         4.2
fentanyl        51  yes       354.9
morphine         3  yes       10.0
methadone        0  --        --       <-- MAT drug, not in analgesic table
buprenorphine    0  --        --       <-- MAT drug, not in analgesic table
```

**Implications:**
- `has_strong` / `has_weak` -- fully reliable (tier 1)
- `has_oxycodone/hydrocodone/tramadol/codeine/fentanyl` -- good (top 5 Medicare opioids)
- `has_morphine` -- low (3 NDCs); detectable but rare in outpatient
- `has_methadone` / `has_buprenorphine` -- always 0 with current crosswalk
  (NY State DOH table = analgesic opioids only, not MAT)
- `n_distinct_opioid` -- practical max ~5 (top 5 drugs)


## Diabetes crosswalk coverage (per-class NDC files)

Each drug class has its own NDC file in 0-External-Store/Diabetes/ndc/<class>/.
Coverage is per-class (tier 1 pattern -- no name matching needed).

```
Class           File                  Var token   Literature name
-----------     --------------------  ---------   ---------------
Metformin       NDC_metformin.dta     metformin   1st-line oral
Insulin         NDC_insulin.dta       insulin     Injectable baseline
GLP-1 RA        NDC_glp1.dta          glp1        Ozempic, Trulicity, etc.
SGLT2i          NDC_sglt2.dta         sglt2       Jardiance, Farxiga, etc.
DPP-4i          NDC_dpp4.dta          dpp4        Januvia, Tradjenta, etc.
Sulfonylurea    NDC_sulfonylurea.dta  sulf        Glipizide, Glyburide, etc.
```

Config driver: `global diabetes_drug_classes "metformin insulin glp1 sglt2 dpp4 sulf"`
Each class produces: `{level}_{win}_{class}_rx_num`, `_days_suply`, `_qty`, `_has_rx`


## Infection/antibiotic crosswalk (NDC_antibiotic_oral.dta)

```
Total NDCs:       2,432  (all have substance_name -- 100% classifiable)
Class token:      'abx'  (short; Stata 32-char var limit)
Filename tag:     'AntibioticOral'

Abbrev    Full name           NDCs   Example drugs
------    ---------           -----  -------------
has_pcn   penicillin            516  amoxicillin, amox/clav, ampicillin
has_ceph  cephalosporin         389  cephalexin, cefdinir, cefuroxime
has_fq    fluoroquinolone       537  ciprofloxacin, levofloxacin (FDA black box)
has_macro macrolide             306  azithromycin (Z-pack), clarithromycin
has_tetra tetracycline          367  doxycycline, minocycline
has_sulfa sulfonamide           169  TMP-SMX (Bactrim)
has_metro nitroimidazole        119  metronidazole (Flagyl)
has_nitro nitrofurantoin        140  nitrofurantoin (UTI-specific)
```

Matching uses `substance_name` (not `generic_name`), giving ~100% coverage.
No dead flags -- all 8 categories have substantial NDC counts.


## Stata 32-character variable name limit

Long class tokens (e.g., `antibiotic_oral` = 15 chars) combined with window
prefix + flag name can exceed 32 chars. Use short class tokens in the config:

```
Stata var pattern:  {prefix}_{window}_{class}_{flag}
Max allowed:        bene_bf90d_XXXXX_YYYYYYYYYY = 32
                    ^^^^           ^^^^^  ^^^^^^^^^^
                    5+1+5=11       class   flag+underscore
Available:          32 - 12 = 20 chars for class + flag
```

Config example: `global infection_drug_classes "abx"` (not "antibiotic_oral").
The `filename_{class}` tag stays human-readable for .dta output names.


## Implementation checklist (for new drug domains)

1. Build NDC crosswalk file(s) in 0-External-Store/{Group}/ndc/{class}/
2. Add `global ndc_{class}_file` paths in cohort config
3. **Check var name length**: `{prefix}_{window}_{class}_{longest_flag}` must be <= 32
4. Write bfaf-{bt,nt,bnt}-pde-{domain}rx.do feat builders
5. Add `global run_topic_pde_{domain}rx 1` flag in config
6. Add dispatcher branches + orchestrator topic block
7. For tier-2 (named drugs): check match rate; document which flags are dead
