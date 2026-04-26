ExternalStore Asset Catalog
============================

Lightweight index of the externally-built assets. Schemas live in each
asset's auto-generated README; this file carries only what the skill
needs to dispatch (slug, family, primary key, builder).

Always discover the active release at runtime:

```bash
ls _WorkSpace/ExternalStore/                    # all releases
echo $EXTERNAL_VERSION                           # active release (from env.sh)
ls _WorkSpace/ExternalStore/$EXTERNAL_VERSION/   # assets in active release
```

For full schema of an asset, read its README:

```bash
cat _WorkSpace/ExternalStore/$EXTERNAL_VERSION/{asset}/README.md
```

---

Current Builders (code-dev/0-EXTERNAL/)
========================================

Discovered via `ls code-dev/0-EXTERNAL/e*.py`. The 11 entries below are
the snapshot at the time of this skill's first draft; rerun ls for the
current list.

```
slug                  family       primary_key   builder
--------------------- -----------  ------------  --------------------------------------
ndc                   dimension    ndc           e1_build_external_ndc.py
npi                   dimension    NPI           e2_build_external_npi.py
ncpdp                 dimension    ncpdp         e3_build_external_ncpdp.py
zip3                  dimension    zip3          e4_build_external_zip3.py
zip5                  dimension    zip5          e5_build_external_zip5.py
zip3_engagement       engagement   zip3          e6_build_external_zip3_engagement.py
zip5_engagement       engagement   zip5          e7_build_external_zip5_engagement.py
ncpdp_engagement      engagement   ncpdp         e8_build_external_ncpdp_engagement.py
npi_engagement        engagement   NPI           e9_build_external_npi_engagement.py
ndc_engagement        engagement   ndc           e10_build_external_ndc_engagement.py
patient_engagement    engagement   patient_id    e11_build_external_patient_engagement.py
```

Primary keys are case-sensitive in the data: `NPI` is uppercase as
NPPES uses it; `ndc` / `ncpdp` / `zip3` / `zip5` / `patient_id` are
lowercase. Match the case in any join.

---

Family rules (recap from concepts.md)
======================================

  dimension   -- vendor-sourced; refresh on vendor cadence
  engagement  -- cohort-aggregated; refresh on cohort change

The skill's `review` and `refresh` verbs treat them differently:
dimension staleness compares `@raw/<vendor file>` mtime vs the asset's
mtime; engagement staleness compares the source cohort SourceSet mtime
vs the asset's mtime.

---

Common cohort columns that join to each primary key
====================================================

When previewing a join (`/haipipe-data-external join <asset> --to <set>`),
look for these source-side columns. The right-side join key is always
`{PRIMARY_KEY}_original` in the external's `df_{asset}_id.parquet`.

```
asset slug          cohort columns commonly used as left-side join key
------------------  -----------------------------------------------------
ndc                 ndc, drug_ndc
npi                 prescriber_npi, npi (provider), provider_npi
ncpdp               pharmacy_ncpdp_id, ncpdp_provider_id, pharmacy_id
zip3                patient_zip3, zipcode3, zip3
zip5                patient_zip5, patient_zipcode, zipcode5, zip5, npi_zip5
patient_id          patient_id, patient_id_encoded
```

The engagement variants share the same join columns as their
dimension counterparts (npi_engagement joins on the same NPI key as
npi).

---

How to add a new asset to this catalog
=======================================

When `design-chef` produces a new `e{N}_build_external_*.py`:

  1. Run the builder once to materialize the asset.
  2. Add a row to the table above with slug, family, primary_key, builder.
  3. Add a row to "Common cohort columns" if the asset introduces a
     new join key.
  4. The asset's auto-generated README handles the schema -- do NOT
     duplicate column lists here.
