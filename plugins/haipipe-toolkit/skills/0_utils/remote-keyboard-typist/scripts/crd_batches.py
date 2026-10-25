#!/usr/bin/env python3
"""Turn a key_plan.py plan into click batches for claude-in-chrome.

Usage:
    crd_batches.py PLAN.json --tab TAB_ID [--iso] [--first-ref 5] [--lines A-B] [--max 300]

Prints one JSON list per batch: browser_batch actions, Enter before every line
but the first, then a 2 s wait. Lines are packed into batches of at most --max
keys.

The refs follow the CRD letter layout in screen order (verified 261025):
`1234567890-= at first-ref.., Backspace, Tab, qwertyuiop[]\\, asdfghjkl;',
Enter, Shift, zxcvbnm,./, Shift, then Space at first-ref + 56.

--js: print one key list for scripts/crd_type.js (the fast path) instead.

--iso: the layout that has one extra key (also a backslash) between the left Shift and z
(seen 261025 after a reconnect): z and every key after it move up by one, so
Space is at first-ref + 57. Tell the two apart in read_page: count the unnamed
buttons between the two "Shift" buttons, 10 = default, 11 = --iso.
"""

import argparse
import json


def ref_map(first, iso=False):
    r, i = {}, first
    for c in "`1234567890-=":
        r[c] = i
        i += 1
    r["Backspace"], r["Tab"] = i, i + 1
    i += 2
    for c in "qwertyuiop[]":
        r[c] = i
        i += 1
    r["Backslash"] = i
    i += 1
    for c in "asdfghjkl;'":
        r[c] = i
        i += 1
    r["Enter"], r["Shift"] = i, i + 1
    i += 2
    if iso:
        i += 1
    for c in "zxcvbnm,./":
        r[c] = i
        i += 1
    r["Space"] = first + 56 + (1 if iso else 0)
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("--tab", type=int, required=True)
    ap.add_argument("--first-ref", type=int, default=5)
    ap.add_argument("--iso", action="store_true")
    ap.add_argument("--js", action="store_true", help="print one JSON key list for crd_type.js instead of click batches")
    ap.add_argument("--probe", action="store_true", help="with --js: print the probe key list Aa$\\({\"; z/ and its 11 Backspaces")
    ap.add_argument("--lines")
    ap.add_argument("--max", type=int, default=300)
    a = ap.parse_args()

    refs = ref_map(a.first_ref, a.iso)
    if a.js and a.probe:
        probe = ["Shift", "a", "a", "Shift", "4", "Backslash", "Shift", "9", "Shift", "[", "Shift", "'", ";", "Space", "z", "/"]
        print(json.dumps(probe, separators=(",", ":")))
        print(json.dumps(["Backspace"] * 11, separators=(",", ":")))
        return
    if a.js:
        keys = []
        for p in json.load(open(a.plan))["lines"]:
            if p["n"] > 1:
                keys.append("Enter")
            keys += p["keys"]
        print(f"# {len(keys)} keys")
        print(json.dumps(keys, separators=(",", ":")))
        return
    lines = json.load(open(a.plan))["lines"]
    if a.lines:
        lo, hi = (int(x) for x in a.lines.split("-"))
        lines = [p for p in lines if lo <= p["n"] <= hi]

    def click(k):
        return {"name": "computer", "input": {"action": "left_click", "ref": f"ref_{refs[k]}", "tabId": a.tab, "action_summary": "Key"}}

    def actions(keys):
        return [click(k) for k in keys]

    batches, cur, span, n = [], [], [], 0
    for p in lines:
        keys = (["Enter"] if p["n"] > 1 else []) + p["keys"]
        if cur and n + len(keys) > a.max:
            batches.append((span, cur))
            cur, span, n = [], [], 0
        cur += actions(keys)
        n += len(keys)
        span.append(p["n"])
    if cur:
        batches.append((span, cur))

    wait = {"name": "computer", "input": {"action": "wait", "duration": 2, "tabId": a.tab}}
    for span, acts in batches:
        print(f"# lines {span[0]}-{span[-1]}, {len(acts)} clicks")
        print(json.dumps(acts + [wait], separators=(",", ":")))


if __name__ == "__main__":
    main()
