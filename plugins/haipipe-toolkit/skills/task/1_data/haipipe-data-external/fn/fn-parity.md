fn-parity: Frozen version vs live provider
==========================================

For an asset whose serving provider is live (feature store, third-party
API): the same keys through the frozen local version and the live provider
must return the same fields. This is what keeps training and serving from
drifting (`ref/asset-model.md` § Providers and environments).

Runs as a b51 Task: `j0N_asset_<asset>/t04_parity/`.

---

Step 1: Sample keys
-------------------

Draw a fixed-seed sample of keys from the frozen version (default 500),
plus a handful of keys known to be missing, to test the fallback.

---

Step 2: Look up both ways
-------------------------

- Frozen: `ExternalAsset(<asset>, version=<S date>, env='train')`.
- Live: the serving provider at the same time the snapshot represents, or
  immediately after a fresh freeze.

---

Step 3: Compare
---------------

Per field: exact-match rate, and for numeric fields the largest absolute
difference. Missing keys must return `_matched=False` with defaults on both
sides.

Report counts and rates only, never row values.

---

Step 4: Verdict
---------------

- pass: every field matches (or within a declared tolerance in asset.yaml).
- fail: list the fields that differ. A difference usually means the live
  provider moved on since the freeze; re-freeze and re-run before locking.
