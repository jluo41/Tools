fn-3-design-chef: Scaffold a new external builder
==================================================

Creates a new `e{N+1}_build_external_<asset>.py` under
`code-dev/0-EXTERNAL/`. In Phase 1 (no helper extraction yet), this
copies the closest existing builder and customizes it.

---

Step 0: Read prerequisite refs
-------------------------------

  - This skill's `ref/concepts.md` (asset triplet contract)
  - This skill's `ref/asset-catalog.md` (slug + primary-key conventions)
  - `../haipipe-data-source/ref/concepts.md` (downstream cohort schema
    that the asset will join into)

---

Step 1: Collect inputs from the user
-------------------------------------

Ask in one block; wait for answers:

```
Q1. Asset slug?            (snake_case, e.g. payer, allergen, sig_text)
Q2. Family?                (dimension | engagement)
Q3. Primary key?           (e.g. NPI, ndc, ncpdp, zip5, custom)
Q4. Display name?          (human label, e.g. 'Payer')
Q5. Source?                dimension  -> path under @raw/
                           engagement -> cohort SourceSet path
Q6. Output columns?        (list of column names you intend to expose)
Q7. New e-script number?   (next free integer; check ls code-dev/0-EXTERNAL/)
```

Compose:

  builder filename = `e{N+1}_build_external_{slug}.py`
  asset folder     = `_WorkSpace/ExternalStore/${EXTERNAL_VERSION}/{slug}/`

Display the summary and require explicit YES.

---

Step 2: Pick the seed builder
------------------------------

Use the closest match by family AND primary-key family:

```
target                          seed builder
------------------------------- -----------------------------------------
dimension + zip-keyed           e5_build_external_zip5.py
dimension + provider-keyed      e2_build_external_npi.py
dimension + drug-keyed          e1_build_external_ndc.py
dimension + pharmacy-keyed      e3_build_external_ncpdp.py
engagement + zip3 / zip5        e6_build_external_zip3_engagement.py
                                e7_build_external_zip5_engagement.py
engagement + provider           e9_build_external_npi_engagement.py
engagement + drug               e10_build_external_ndc_engagement.py
engagement + pharmacy           e8_build_external_ncpdp_engagement.py
engagement + patient            e11_build_external_patient_engagement.py
```

If none fit, ask the user which to seed from.

---

Step 3: Copy and customize
---------------------------

```bash
cp code-dev/0-EXTERNAL/{seed}.py \
   code-dev/0-EXTERNAL/e{N+1}_build_external_{slug}.py
```

Edit the new file to change:

```python
OUTPUT_DIR_NAME = '{slug}'
DISPLAY_NAME    = '{Display Name}'
PRIMARY_KEY     = '{primary_key}'
```

Then update:

  - The data-loading section -- point at the new source(s)
  - The column-selection list -- match the user's Q6
  - The metadata dict that feeds `generate_readme()` -- title,
    description, source, columns, stats, usage_example

Do NOT extract or refactor the duplicated helpers
(`build_vocabulary`, `convert_to_ids`, `generate_readme`) -- Phase 1
keeps them inline. Note the duplication with a
`# TODO: extract helpers (Phase 2)` comment near each.

---

Step 4: Run the new builder once
---------------------------------

Delegate to `cook`:

  /haipipe-data-external cook {slug}

Verify the asset triplet appears in the active release.

---

Step 5: Update ref/asset-catalog.md
------------------------------------

Add a row for the new asset:

```
{slug}    {family}    {primary_key}    e{N+1}_build_external_{slug}.py
```

If the asset has new common cohort join keys, add them to the
"Common cohort columns" table.

---

Step 6: Return tail
--------------------

```
status:     ok
new asset:  {slug}
builder:    code-dev/0-EXTERNAL/e{N+1}_build_external_{slug}.py
artifacts:  [list of files written]
catalog:    updated
next:       "/haipipe-data-external review {slug}"
            "/haipipe-data-external join {slug} --to <set>   (preview a join)"
```

---

MUST NOT
---------

- Do NOT scaffold without confirming the user's Q1-Q7 answers.
- Do NOT skip Step 5 -- a new builder without a catalog entry is
  invisible to dashboard / review / refresh.
- Do NOT extract helpers in this step (Phase 2 deferred).
