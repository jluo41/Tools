fn-2-cook: Run an external builder script
==========================================

Executes one `e{N}_build_external_<asset>.py` to produce or refresh
the asset triplet under the active release.

---

Step 1: Locate the builder
---------------------------

```bash
ls code-dev/0-EXTERNAL/e*_build_external_{asset}.py
```

If multiple match (unlikely), ask the user which to run. If none match:

  "No builder for {asset}. Available builders:
   $(ls code-dev/0-EXTERNAL/e*_build_external_*.py)
   To scaffold one: /haipipe-data-external design-chef"

---

Step 2: Pre-flight checks
--------------------------

```bash
# Active release present?
ls -d _WorkSpace/ExternalStore/${EXTERNAL_VERSION} 2>/dev/null || \
    mkdir -p _WorkSpace/ExternalStore/${EXTERNAL_VERSION}

# If asset already exists in this release, warn before overwriting
if [ -d "_WorkSpace/ExternalStore/${EXTERNAL_VERSION}/{asset}" ]; then
    echo "Asset {asset} already exists in release ${EXTERNAL_VERSION}."
    echo "Cook will overwrite it. Continue?"
fi
```

NEVER overwrite without explicit user confirmation -- releases are
reproducibility anchors.

---

Step 3: Verify raw inputs are present
--------------------------------------

Read the builder header to find input files. Look for top-level path
constants:

```bash
grep -E '_PATH\s*=' code-dev/0-EXTERNAL/e*_build_external_{asset}.py
```

Confirm each exists:

```bash
ls _WorkSpace/ExternalStore/@raw/<file>
```

If a raw input is missing, surface the path and the install hint
embedded in the builder (builders typically print a download URL,
e.g. "Download NPPES from https://download.cms.gov/nppes/NPI_Files.html").

---

Step 4: Run the builder
------------------------

```bash
source .venv/bin/activate && source env.sh && \
    python code-dev/0-EXTERNAL/e{N}_build_external_{asset}.py
```

Stream output to the user. Builders print progress and a verification
block at the end; capture both.

---

Step 5: Verify the output triplet
----------------------------------

```bash
ls _WorkSpace/ExternalStore/${EXTERNAL_VERSION}/{asset}/
```

Expect at minimum:

  df_{asset}_id.parquet
  column_to_{asset}_li.pkl
  README.md

Engagement assets also produce `df_{asset}_raw.parquet`. Some assets
have additional auxiliary parquets (e.g. npi has df_npi_to_zip5info,
df_npi_review_id) -- read the builder's save section to see what's
expected.

---

Step 6: Return tail
--------------------

```
status:    ok | failed
asset:     {asset}
release:   {version}
artifacts: [list of files written]
runtime:   {seconds}
next:      "/haipipe-data-external review {asset}   (verify schema + coverage)"
```

---

MUST NOT
---------

- Do NOT skip the pre-flight raw-input check.
- Do NOT silently overwrite an existing asset within a release.
- Do NOT modify the builder script during cook -- use `design-chef`
  for changes.
