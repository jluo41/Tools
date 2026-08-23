"""
Fetch the 2024 Adult Compendium from its PUBLISHER, and diff it against the
mirror this skill has been running on.

WHY THIS EXISTS
================================================================================
`retrieve.py` hard-codes `CONF_CAP = OK`, so no result may ever be stamped GOOD.
The reason is in its docstring: the bank on this machine is a third-party mirror
(1,111 of the 1,114 activities) and not the publisher's file, and a note would
not have survived the next person's confidence, so the cap is code.

That docstring also says pacompendium.com returns 403 to non-browser clients. It
does not -- it returns 403 to curl's DEFAULT User-Agent. With a browser UA it
serves 200, and the site publishes one HTML table per major heading with exactly
the three columns the bank needs. Checked 260822.

WHAT IT WRITES, AND WHAT IT DOES NOT DECIDE
================================================================================
A CSV beside the mirror, plus a diff report. It does NOT raise CONF_CAP. Whether
this bank has earned GOOD is a judgement about provenance, and a person makes it
after reading the diff -- a script that fetched a file and then promoted its own
confidence would be marking its own homework.

    source .venv/bin/activate && source env.sh
    python build_compendium_bank.py            # fetch + diff
    python build_compendium_bank.py --diff     # diff what is already fetched
"""
import argparse
import html
import json
import pathlib
import re
import time
import urllib.request

import pandas as pd

ROOT = pathlib.Path("/home/jluo41/WellDoc-SPACE")
OUT = ROOT / "_WorkSpace/ExternalStore/pa_compendium"
MIRROR = OUT / "compendium_2024.csv"
FETCHED = OUT / "compendium_2024_publisher.csv"

BASE = "https://pacompendium.com"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/126.0 Safari/537.36")

# The 22 major headings, each its own page. Taken from the site's own nav rather
# than from the mirror, so a heading the mirror lost would still be fetched.
HEADINGS = [
    "bicycling", "conditioning-exercise", "dancing", "fishing-hunting",
    "home-activities", "home-repair", "inactivity", "lawn-garden",
    "miscellaneous", "music-playing", "occupation", "religious-activities",
    "running", "self-care", "sexual-activity", "sports", "transportation",
    "video-games", "volunteer-activities", "walking", "water-activities",
    "winter-activities",
]

_TR = re.compile(r"<tr[^>]*>(.*?)</tr>", re.S)
_TD = re.compile(r"<t[dh][^>]*>(.*?)</t[dh]>", re.S)
_TAG = re.compile(r"<[^>]+>")
_CODE = re.compile(r"^\d{5}$")


def _text(c: str) -> str:
    # \xa0 is all over these tables and is not a space to anyone comparing
    # strings later.
    return html.unescape(_TAG.sub("", c)).replace("\xa0", " ").strip()


def fetch_page(slug: str) -> list:
    req = urllib.request.Request(f"{BASE}/{slug}", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        body = r.read().decode("utf-8", "replace")
    rows = []
    for tr in _TR.findall(body):
        cells = [_text(c) for c in _TD.findall(tr)]
        if len(cells) < 3 or not _CODE.match(cells[0]):
            continue                       # the header row, and any stray tr
        try:
            met = float(cells[1])
        except ValueError:
            continue
        rows.append(dict(activity_code=cells[0], met_value=met,
                         activity_description=re.sub(r"\s+", " ", cells[2]),
                         major_heading=slug))
    return rows


def fetch_all() -> pd.DataFrame:
    out = []
    for h in HEADINGS:
        rows = fetch_page(h)
        print(f"  {h:24s} {len(rows):>5d}")
        out += rows
        time.sleep(0.5)                    # a courtesy, not a workaround
    d = pd.DataFrame(out)
    dup = int(d.activity_code.duplicated().sum())
    if dup:
        print(f"  NOTE {dup} codes appear on more than one page; keeping first")
        d = d.drop_duplicates("activity_code", keep="first")
    return d.sort_values("activity_code").reset_index(drop=True)


def diff(pub: pd.DataFrame, mir: pd.DataFrame) -> dict:
    pk, mk = set(pub.activity_code), set(mir.activity_code)
    m = pub.merge(mir, on="activity_code", suffixes=("_pub", "_mir"))
    moved = m[(m.met_value_pub - m.met_value_mir).abs() > 1e-9]
    desc = ("activity_description_pub" if "activity_description_pub" in m.columns
            else "activity_description")
    return {
        "publisher_codes": len(pk), "mirror_codes": len(mk),
        "n_only_in_publisher": len(pk - mk),
        "only_in_publisher": sorted(pk - mk)[:50],
        "n_only_in_mirror": len(mk - pk),
        "only_in_mirror": sorted(mk - pk)[:50],
        "shared": len(m),
        "met_disagreements": len(moved),
        "met_disagreement_examples": [
            {"code": r.activity_code, "publisher": float(r.met_value_pub),
             "mirror": float(r.met_value_mir), "desc": str(getattr(r, desc))[:70]}
            for r in moved.head(15).itertuples(index=False)],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--diff", action="store_true",
                    help="diff the already-fetched file, do not refetch")
    a = ap.parse_args()

    if a.diff:
        pub = pd.read_csv(FETCHED, dtype={"activity_code": str})
    else:
        print("fetching the publisher's tables, one per major heading")
        pub = fetch_all()
        OUT.mkdir(parents=True, exist_ok=True)
        pub.to_csv(FETCHED, index=False)
        print(f"\n  {len(pub):,} activities -> {FETCHED}")

    mir = pd.read_csv(MIRROR, dtype=str)
    print(f"  mirror columns: {list(mir.columns)}")
    if "activity_code" not in mir.columns or "met_value" not in mir.columns:
        print("  cannot diff: mirror does not use the expected column names")
        return
    mir["met_value"] = pd.to_numeric(mir.met_value, errors="coerce")

    d = diff(pub, mir)
    (OUT / "publisher_diff.json").write_text(json.dumps(d, indent=1))
    print(f"\n  publisher {d['publisher_codes']:,}  ·  mirror {d['mirror_codes']:,}"
          f"  ·  shared {d['shared']:,}")
    print(f"  only in publisher {d['n_only_in_publisher']}"
          f"  ·  only in mirror {d['n_only_in_mirror']}"
          f"  ·  MET disagreements {d['met_disagreements']}")
    for e in d["met_disagreement_examples"][:10]:
        print(f"    {e['code']}  publisher {e['publisher']:>5}  "
              f"mirror {e['mirror']:>5}   {e['desc']}")
    print(f"\n  wrote {OUT}/publisher_diff.json")
    print("  CONF_CAP is NOT changed by this script. A person reads the diff.")


if __name__ == "__main__":
    main()
