"""s01 · The normalizer map: s01-norm-map.excalidraw, drawn by this builder from disk (haipipe-studio).

How `plugins/haipipe-utils` fits together, read left to right: the contract (haipipe-norm), each member with its
version and the banks it resolves against, the API lane that serves it, and the Job of b02 that owns it. A bank
the SPACE's ExternalStore does not hold is marked red ("? not here"). Arrow: describe-medication's DrugKey feeds
describe-insulin. A rebuild keeps whatever a person drew on the canvas.

    python build_s01_norm_map.py
"""
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BLOCK = HERE.parents[1]
sys.path.insert(0, str(BLOCK.parent / "_build"))
from mapdraw import GREEN, Sheet  # noqa: E402

TOOLS = BLOCK.parents[1]
PKG = TOOLS / "plugins" / "haipipe-utils"
SPACE = TOOLS.parent
STORE = SPACE / os.environ.get("LOCAL_EXTERNAL_STORE", "_WorkSpace/ExternalStore")
MEMBERS = [("describe-food", "foodnorm", "food", "j02_food"),
           ("describe-exercise", "exnorm", "exercise", "j03_exercise"),
           ("describe-medication", "mednorm", "medication", "j04_medication"),
           ("describe-insulin", "insnorm", "insulin", "j05_insulin")]
BANK = re.compile(r'"((?:ext_[a-z0-9_]+)|medbank|pa_compendium)"')
CHANGES = []                                          # (YYMMDD, what changed): a green note each


def version(skill: Path) -> str:
    m = re.search(r'^\s*version:\s*"?([\d.]+)', (skill / "SKILL.md").read_text(encoding="utf-8"), re.M)
    return m.group(1) if m else "?"


def banks(pkg: Path) -> list:
    found = set()
    for f in pkg.glob("*.py"):
        found |= set(BANK.findall(f.read_text(encoding="utf-8", errors="ignore")))
    return sorted(found)


def rows():
    out = [["haipipe-norm", "the contract: five rules, the door normalize(items), shared packages",
            version(PKG / "skills/haipipe-norm"), "", "", "j01_norm_contract"]]
    for skill, pkg, lane, job in MEMBERS:
        bs = banks(PKG / "skills" / skill / pkg)
        here = [b + ("" if (STORE / b).exists() else " (? not here)") for b in bs]
        api = f"/{lane}" if (PKG / "servers" / f"api-{lane}").is_dir() else "? no lane"
        out.append([skill, f"{pkg}/ · its own resolver", version(PKG / "skills" / skill), " · ".join(here) or "-",
                    api, job])
    return out


def main():
    s = Sheet()
    data = rows()
    cols = [("part", 200, 20), ("what", 360, 38), ("version", 90, 8), ("banks in ExternalStore", 440, 44),
            ("API lane", 120, 10), ("Job of b02", 180, 18)]
    width = sum(w for _, w, _ in cols)
    f = s.frame("1 · The normalizer map", 0, 0, width + 80, 100)
    s.text(40, 30, "s01 · The normalizer map: contract → members → banks → API", 30, f)
    s.text(40, 80, f"Read from disk on each rebuild; banks checked in {STORE.relative_to(SPACE)}/. "
                   "Red: a bank this SPACE does not hold. All lanes sit on one host, servers/_host (:8070) → j06_api.",
           16, f)
    for i, (date, what) in enumerate(CHANGES):
        s.text(40, 112 + i * 26, f"✎ {date} {what}", 16, f, GREEN)
    y = s.table(40, 150 + len(CHANGES) * 26, cols, data, f, red=lambda r: "?" in " ".join(map(str, r)))
    s.text(40, y + 24, "describe-medication ──DrugKey──▶ describe-insulin   (insulin reads medication's output)", 18, f)
    s.text(40, y + 56, "the banks: where they live and how a SPACE gets them → j07_banks", 18, f)
    f["height"] = y + 110
    s.save(HERE / "s01-norm-map.excalidraw", "build_s01_norm_map.py")


if __name__ == "__main__":
    main()
