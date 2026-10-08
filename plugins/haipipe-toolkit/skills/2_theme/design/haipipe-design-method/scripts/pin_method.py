"""run-setup-method-j<NN>: copy the Job's pinned method version from the registry into its inputs/method.md.

    python pin_method.py <block>/jNN_<goal>_<method>          reads the face's `method: M04 m2`
    python pin_method.py --list                                  the registered methods and their versions

The registry is this skill's methods/MNN-<slug>/m<k>.md. The copy is word for word; the face's `method-sha:` gets the
first 12 hex of the version file's sha256. An unknown method or version is refused. A Job already pinned to the same
version is left as it is; pinned to a different text, it is refused: a changed method is a new Job.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

import yaml

REGISTRY = Path(__file__).resolve().parent.parent / "methods"


def front(text: str) -> dict:
    m = re.match(r"(?s)^---\n(.*?)\n---\n", text)
    return (yaml.safe_load(m.group(1)) or {}) if m else {}


def registered(registry: Path = REGISTRY) -> dict:
    """{"M04": {"name": …, "type": …, "versions": {"m1": Path, "m2": Path}}}"""
    out = {}
    for d in sorted(registry.glob("M[0-9][0-9]-*")):
        card = front((d / "method.md").read_text(encoding="utf-8")) if (d / "method.md").is_file() else {}
        out[d.name[:3]] = {"name": card.get("name", ""), "type": card.get("type", ""), "path": d,
                           "versions": {p.stem: p for p in sorted(d.glob("m[0-9]*.md"))}}
    return out


def version_file(pin: str, registry: Path = REGISTRY) -> Path:
    m = re.match(r"^(M\d\d)\s+(m\d+)$", str(pin or "").strip())
    if not m:
        sys.exit(f"a method pin is 'MNN m<k>' (M04 m2): {pin!r}")
    reg = registered(registry)
    if m.group(1) not in reg:
        sys.exit(f"{m.group(1)} is not a registered method: {', '.join(reg) or 'none'}")
    v = reg[m.group(1)]["versions"].get(m.group(2))
    if v is None:
        sys.exit(f"{m.group(1)} has no version {m.group(2)}: {', '.join(reg[m.group(1)]['versions'])}")
    return v


def pin(jdir: Path, made: list, registry: Path = REGISTRY) -> None:
    face = jdir / f"{jdir.name}.md"
    if not face.is_file():
        sys.exit(f"no Job face {face.name}")
    text = face.read_text(encoding="utf-8")
    src = version_file(front(text).get("method"), registry)
    body = src.read_text(encoding="utf-8")
    sha = hashlib.sha256(body.encode("utf-8")).hexdigest()[:12]
    dest = jdir / "inputs" / "method.md"
    if dest.is_file():
        if dest.read_text(encoding="utf-8") != body:
            sys.exit(f"{jdir.name} is pinned to another method text: a changed method is a new Job")
    else:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(body, encoding="utf-8")
        made.append(dest)
    new = re.sub(r"(?m)^method-sha:.*$", f"method-sha: {sha}", text, count=1)
    if new == text and "method-sha:" not in text:
        new = re.sub(r"(?m)^(method:.*)$", rf"\1\nmethod-sha: {sha}", text, count=1)
    if new != text:
        face.write_text(new, encoding="utf-8")
        made.append(face)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("job", type=Path, nargs="?")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args(argv)
    if a.list:
        for mid, m in registered().items():
            print(f"{mid}  {m['name']:<22} {m['type']:<14} {' · '.join(m['versions'])}")
        return []
    if not a.job:
        ap.error("pin_method.py <job> or --list")
    made = []
    pin(a.job, made)
    for p in made:
        print("made", p)
    return made


if __name__ == "__main__":
    main()
