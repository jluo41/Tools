Store Map
==========

Maps store name <-> env var <-> typical asset-name pattern. Used by
verbs that need to translate "1-SourceStore" into a path or identify
which asset name format to expect.

---

Stores
======

```
store name              local env var                 remote env var                  typical asset-name pattern
----------------------  ----------------------------- ------------------------------- --------------------------------------------
0-RawDataStore              LOCAL_RAW_STORE               REMOTE_RAWDATA_STORE            {YYYYMMDD}_{CohortLabel}/
1-SourceStore           LOCAL_SOURCE_STORE            REMOTE_SOURCE_STORE             {CohortName}/@{SourceFnName}/
2-RecStore              LOCAL_RECORD_STORE            REMOTE_RECORD_STORE             {CohortName}_v{N}RecSet/
3-CaseStore             LOCAL_CASE_STORE              REMOTE_CASE_STORE               {RecSetName}/@v{N}CaseSet-{TriggerFolder}/
4-AIDataStore           LOCAL_AIDATA_STORE            REMOTE_AIDATA_STORE             {ParentSetName}/@v{N}AIData-{aidata_name}/
5-ModelInstanceStore    LOCAL_MODELINSTANCE_STORE     REMOTE_MODELINSTANCE_STORE      {model_name}/
6-EndpointStore         LOCAL_ENDPOINT_STORE          REMOTE_ENDPOINT_STORE           {endpoint_name}/
7-AgentWorkspace ⚙opt   LOCAL_AGENTWORKSPACE_STORE    REMOTE_AGENTWORKSPACE_STORE     (varies)
ExternalStore           LOCAL_EXTERNAL_STORE          REMOTE_EXTERNAL_STORE           @{version}/{asset}/
ExternalStore/@inference ⚙opt LOCAL_REFERENCE_STORE   REMOTE_REFERENCE_STORE          {payload_*.json}
```

⚙opt = OPTIONAL store: listed for addressing, but not exported by every
workspace's env.sh and often absent on disk. `status` probes only the
stores whose env vars are actually exported — do not report an un-exported
optional store as "missing". Also on disk but DELIBERATELY NOT SYNCED
(no store-map row, no env pair): `_WorkSpace/LearnStore/`,
`_WorkSpace/0-REACH-RAW-Store/`.

`LOCAL_RAW_STORE` resolves to `_WorkSpace/0-RawDataStore`, but
hai-remote-sync's `--rawdata` flag uses `REMOTE_RAWDATA_STORE` --
note the name asymmetry (RAW vs RAWDATA).

---

Resolving a User Path
======================

```
User typed                            Resolves to
------------------------------------- -----------------------------------------
1-SourceStore/WellDoc2025CVS          --path 1-SourceStore/WellDoc2025CVS
SourceStore/WellDoc2025CVS            same (case/prefix forgiving)
source/WellDoc2025CVS                 same
WellDoc2025CVS (no store)             ASK which store -- do not guess
```

When the user gives a bare cohort name without a store, ask rather
than guess. If the same cohort name appears in multiple stores, list
them and ask.

---

hai-remote-sync Store Flags
============================

For named-store mode, the matching CLI flag:

```
store                          flag
------------------------------ ------------
0-RawDataStore                     --rawdata
1-SourceStore                  --source
2-RecStore                     --record
3-CaseStore                    --case
4-AIDataStore                  --aidata
5-ModelInstanceStore           --model
6-EndpointStore                --endpoint
ExternalStore                  --external
7-AgentWorkspace               (path mode only)
ExternalStore/@inference       (path mode only)
```

For stores without a flag, use `--path` form.

---

Discovery
==========

To see what stores exist on a given system, the source of truth is
env.sh. Read it directly:

```bash
grep -E "^export (LOCAL|REMOTE)_" env.sh
```

This catches the case where env.sh has been customized or extended
with stores not listed in this map.
