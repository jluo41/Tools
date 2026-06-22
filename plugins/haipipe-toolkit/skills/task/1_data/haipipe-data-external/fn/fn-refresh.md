fn-refresh: Rebuild stale external assets
==========================================

Composite verb: runs `review` to detect staleness, then `cook` for each
stale asset. Always confirms before rebuilding.

---

Step 1: Resolve scope
----------------------

  - `refresh`              -> consider every asset in active release
  - `refresh {asset...}`   -> consider just those listed

---

Step 2: Run staleness audit
----------------------------

Delegate to `fn-review.md` Step 4 for each in-scope asset. Collect:

```
stale     = [assets where raw or cohort newer than output]
fresh     = [assets where output newer than inputs]
unknown   = [assets where input not present locally]
```

If `stale` is empty, print "All in-scope assets fresh." and return.

---

Step 3: Confirm with the user
------------------------------

Print:

```
Stale assets (will be rebuilt):
  {asset}  raw=2025-09-01  asset=2025-08-15  (raw 17d newer)
  ...

Unknown (raw missing -- skip):
  {asset}  ...

Total to rebuild: {N}
Estimated runtime: based on prior cook timings, ~{seconds}s

Proceed? (yes / dry-run / cancel)
```

  yes      -> Step 4
  dry-run  -> exit, no rebuild
  cancel   -> exit, no rebuild

---

Step 4: Rebuild each stale asset
---------------------------------

For each: delegate to `fn-2-cook.md`. Stream output. Capture status
per asset.

If a cook fails, pause and ask whether to:

  - abort entirely
  - skip this asset and continue with the rest

Do NOT silently continue past a failure.

---

Step 5: Return tail
--------------------

```
status:    ok | partial | failed
rebuilt:   [list of assets, with new mtimes]
skipped:   [unknown / cancelled / failed]
failed:    [{asset}: {error}]
next:      "/haipipe-data-external review   (verify all fresh now)"
```

---

MUST NOT
---------

- Do NOT skip Step 3's confirmation prompt.
- Do NOT publish to a different release than EXTERNAL_VERSION without
  asking.
- Do NOT continue past a cook failure without the user's call.
