fn-1-load: Load and inspect a built ExternalAsset
==================================================

Read-only inspection of one asset under the active (or pinned)
release. Prints shape, schema, vocabulary sizes, primary-key
uniqueness, and a sample row.

---

Step 1: Resolve the asset path
-------------------------------

```bash
source .venv/bin/activate && source env.sh
ASSET_DIR="_WorkSpace/ExternalStore/${EXTERNAL_VERSION}/{asset}"
ls "$ASSET_DIR"
```

If `--version @{tag}` was passed, override `EXTERNAL_VERSION` for
this load only:

```bash
ASSET_DIR="_WorkSpace/ExternalStore/{tag}/{asset}"
```

If the directory does not exist, surface a hint:

  "Asset {asset} not in release {version}. Available assets:
   $(ls _WorkSpace/ExternalStore/${version})
   To build: /haipipe-data-external cook {asset}"

---

Step 2: Read the README header
-------------------------------

```bash
head -40 "$ASSET_DIR/README.md"
```

The README exposes the documented schema, primary key, and source.
Surface the title, generated date, primary key, and stats block to
the user.

---

Step 3: Load the parquet + vocabulary
--------------------------------------

```python
import pandas as pd
import pickle
import os

ASSET_DIR = os.path.join(SPACE['LOCAL_EXTERNAL_STORE'], '{asset}')

# Default file naming: df_{asset}_id.parquet
parquet_path = os.path.join(ASSET_DIR, f'df_{asset}_id.parquet')
df = pd.read_parquet(parquet_path)

# Vocabulary uses '_li' suffix
pkl_path = os.path.join(ASSET_DIR, f'column_to_{asset}_li.pkl')
with open(pkl_path, 'rb') as f:
    vocabs = pickle.load(f)
```

Some assets ship multiple parquets (e.g. npi has demo + review +
zip5info). List them first with `ls "$ASSET_DIR"` and load each.

---

Step 4: Print the inspection block
-----------------------------------

```
{asset} ({family}, primary_key={PRIMARY_KEY}, release={version})
  rows:         {N:,}
  cols:         {C}
  vocab keys:   {V}
  sample row:
    {col}: {value}
    ...
  primary-key uniqueness: {unique}/{N}  ({pct}%)
  null rate per column (top 5):
    {col}:  {pct}%
    ...
```

Compute primary-key uniqueness on the `{PRIMARY_KEY}_original`
column, NOT the integer ID column.

---

Step 5: Return tail to the orchestrator
----------------------------------------

```
status:    ok
asset:     {asset}
release:   {version}
rows:      {N}
artifacts: [df_{asset}_id.parquet, column_to_{asset}_li.pkl, README.md]
next:      "/haipipe-data-external review {asset}   (schema + staleness)"
```

---

MUST NOT
---------

- Do NOT modify any file under `$ASSET_DIR`.
- Do NOT cache loaded data outside of this invocation.
- Do NOT run join / merge logic here -- that is `join`.
