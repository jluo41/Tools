# %% [markdown]
# Scan a repository for directories named `1-probes`; for each, record the
# owning folder (its parent) and every PP-numbered child entry.

# %%
import json
import os
import re
import sys
from datetime import datetime

import yaml

# %%
config_path = sys.argv[1] if len(sys.argv) > 1 else "configs/scan.yaml"
with open(config_path) as f:
    cfg = yaml.safe_load(f)

repo_root = cfg["repo_root"]
target = cfg["target_basename"]
entry_re = re.compile(cfg["entry_pattern"])
exclude = set(cfg["exclude_dirs"])

# %%
records = []
for dirpath, dirnames, _ in os.walk(repo_root):
    dirnames[:] = [d for d in dirnames if d not in exclude]
    if os.path.basename(dirpath) == target:
        entries = sorted(
            e for e in os.listdir(dirpath)
            if entry_re.match(e) and os.path.isdir(os.path.join(dirpath, e))
        )
        records.append({
            "probes_dir": os.path.relpath(dirpath, repo_root),
            "owner": os.path.relpath(os.path.dirname(dirpath), repo_root),
            "pp_count": len(entries),
            "pp_entries": entries,
        })

records.sort(key=lambda r: r["probes_dir"])

# %%
out = {
    "scanned_at": datetime.now().isoformat(timespec="minutes"),
    "repo_root": repo_root,
    "target_basename": target,
    "dirs_found": len(records),
    "records": records,
}
out_path = os.path.join(os.path.dirname(os.path.abspath(config_path)), "..", cfg["out"])
out_path = os.path.normpath(out_path)
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w") as f:
    json.dump(out, f, indent=2)

print(f"found {len(records)} `{target}` dir(s); wrote {out_path}")
for r in records:
    print(f"  {r['probes_dir']}  owner={r['owner']}  pp={r['pp_count']}")
