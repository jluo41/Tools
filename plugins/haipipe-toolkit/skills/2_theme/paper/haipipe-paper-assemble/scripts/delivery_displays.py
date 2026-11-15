"""delivery_displays.py: a Page's display units and the paper's display register (page_display_units, display_register).
build_delivery.py runs this file inside its own namespace (_load_part), so ROOT, HERE, CFG and the LaTeX room come from there."""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path


def _yaml_scalar(value: str) -> str:
    """Read the simple scalar fields used by Page Result envelopes."""
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value.split("#", 1)[0].strip()


def _result_field(text: str, key: str) -> str:
    match = re.search(rf"(?m)^{re.escape(key)}:[ \t]*(.*?)\s*$", text)
    return _yaml_scalar(match.group(1)) if match else ""


def _result_text(text: str) -> str:
    """0.8.2: a result.yaml written in JSON form (valid YAML) is read like the YAML form.
    The field readers below match `key: value` lines, so a JSON Result was invisible:
    its unit was never placed and its page-relative \\input broke the master (Paper-Example-Misq 260928)."""
    s = text.lstrip()
    if not s.startswith("{"):
        return text
    try:
        d = json.loads(s)
    except ValueError:
        return text
    lines = [f"{k}: {d[k]}" for k in ("item", "type", "status", "run") if isinstance(d.get(k), str)]
    payload = d.get("payload") if isinstance(d.get("payload"), dict) else {}
    if isinstance(payload.get("unit"), str):
        lines += ["payload:", f"  unit: {payload['unit']}"]
    return "\n".join(lines) + "\n"


def _page_result_display_unit(page_dir: Path, manifest: Path, text: str):
    """Resolve a typed Page DISPLAY Result's payload.unit within results/."""
    item = _result_field(text, "item")
    kind = _result_field(text, "type").upper()
    if kind != "DISPLAY" and not re.search(r"-DISPLAY-", item, re.I):
        return None

    payload = re.search(
        r"(?ms)^payload:[ \t]*\n((?:^[ \t]+[^\n]*(?:\n|$))*)", text
    )
    if not payload:
        return None
    unit_match = re.search(r"(?m)^[ \t]{2}unit:[ \t]*(.*?)\s*$", payload.group(1))
    if not unit_match:
        return None
    raw = _yaml_scalar(unit_match.group(1))
    if not raw:
        return None

    result_root = page_dir / "results"
    raw_path = Path(raw)
    candidates = []
    placeholder = "<resolved-result>/"
    if raw.startswith(placeholder):
        candidates.append(manifest.parent / raw[len(placeholder):])
    if raw_path.is_absolute():
        candidates.append(raw_path)
    else:
        candidates.extend((page_dir / raw_path, manifest.parent / raw_path))
        if raw_path.parts and raw_path.parts[0] not in ("results", "payload"):
            candidates.append(manifest.parent / "payload" / raw_path)

    try:
        resolved_root = result_root.resolve()
    except OSError:
        return None
    for candidate in candidates:
        if candidate.is_symlink():
            continue
        try:
            resolved = candidate.resolve(strict=True)
            resolved.relative_to(resolved_root)
        except (OSError, ValueError):
            continue
        if resolved.is_dir():
            return resolved
    return None


def page_display_units(page_dir: Path):
    """Return current Result units; read the retired Outline lane only during migration."""
    result_root = page_dir / "results"
    current = {}
    saw_display_result = False
    if result_root.is_dir() and not result_root.is_symlink():
        for manifest in sorted(result_root.rglob("result.yaml")):
            if manifest.is_symlink():
                continue
            try:
                manifest.resolve().relative_to(result_root.resolve())
                text = manifest.read_text(encoding="utf-8", errors="replace")
                text = _result_text(text)
            except (OSError, ValueError):
                continue
            item = _result_field(text, "item")
            kind = _result_field(text, "type").upper()
            if kind != "DISPLAY" and not re.search(r"-DISPLAY-", item, re.I):
                continue
            saw_display_result = True
            # Sorted Result paths mirror the Page Evidence reader: a later
            # attempt for the same stable Evidence Item replaces the older one.
            key = item or manifest.parent.name
            current[key] = (
                _page_result_display_unit(page_dir, manifest, text),
                manifest,
            )
    if saw_display_result:
        unresolved = [
            (item, manifest)
            for item, (unit, manifest) in current.items()
            if unit is None
        ]
        if unresolved:
            details = "; ".join(
                f"{item} ({manifest.relative_to(page_dir)})"
                for item, manifest in unresolved
            )
            raise RuntimeError(
                "Could not resolve payload.unit for current Page DISPLAY Result(s): "
                f"{details}. Expected a unit directory contained under results/. "
                "Refusing to omit these displays from the assembled paper."
            )
        return sorted(
            {unit for unit, _manifest in current.values()},
            key=lambda p: p.as_posix(),
        )

    # Current draft Tasks own display/ beside draft/ and evidence/. Typed
    # Result bindings above remain authoritative when a Page uses them.
    direct = page_dir / "display"
    if direct.is_dir():
        return sorted((p for p in direct.iterdir()
                       if p.is_dir() and not p.name.startswith(("_", "."))),
                      key=lambda p: p.name)
    legacy = plan_home(page_dir) / "evidence" / "display"
    return sorted((p for p in legacy.glob("*/") if p.is_dir()), key=lambda p: p.name) if legacy.is_dir() else []


CITE_CMD = re.compile(r"\\cite[a-zA-Z]*\{([^}]*)\}")


def display_register(main, appx, extra_findings=()):
    units, counters, rows = label_to_unit(), {"figure": 0, "table": 0}, []
    cited = set()
    # Count from the FINAL master in \\input order, not from the fragments. Counting
    # fragments measured what a page CONTAINS, never what the document PRINTS, so it
    # stayed blind to a float the master \\input a second time -- the exact bug this
    # register exists to catch (proved by removing the dedupe and re-running).
    owner = {f"sections/{q['id']}": q["id"] for q, _ in main}
    owner.update({f"appendices/{q['id']}": q["id"] for q, _ in appx})
    for m in re.finditer(r"\\input\{([^}]+)\}", MASTER.read_text(encoding="utf-8", errors="replace")):
        target = LATEX / (m.group(1) + ".tex")
        if not target.exists(): continue
        target_text = target.read_text(encoding="utf-8", errors="replace")
        for group in CITE_CMD.findall(target_text):
            cited.update(k.strip() for k in group.split(",") if k.strip())
        for kind, body in FLOAT_ENV.findall(target_text):
            counters[kind] += 1
            hit = LABEL_CMD.search(body)
            lab = hit.group(1) if hit else ""
            unit = units.get(lab, "")
            rows.append({"printed": f"{kind.title()} {counters[kind]}", "kind": kind,
                         "label": lab, "unit": unit,
                         "page": owner.get(m.group(1), m.group(1)),
                         "declared": declared_number(unit) if unit else None})
    # sections: what LaTeX NUMBERS is every unstarred \section{...} in \input order; a page whose
    # fragment (or stub) prints only \section*{...} (Key Points, an abstract) gets no number.
    # 0.7.5: the declared value is the H1's §N / Appendix L; the page id carries the same index.
    def _numbered_count(p_, rel):
        """how many sections LaTeX will NUMBER for this page: every unstarred \\section{ in its placed
        file; a not-included page is a stub in master.tex with exactly one. 0.7.6: counting, not a
        flag, because a fragment whose inner divisions use \\section (md2tex mapped ### that way)
        shifts every later section number, and the register must print what the reader sees."""
        if not p_.get("included", p_["ready"]): return 1
        f = LATEX / (rel + ".tex")
        return len(re.findall(r"\\section\{", f.read_text(encoding="utf-8", errors="replace"))) if f.exists() else 0
    secs, n, letter, overnumbered = [], 0, 0, []
    for p_, _ in main:
        dec, title = page_heading(p_)
        k = _numbered_count(p_, f"sections/{p_['id']}")
        printed = f"§{n + 1}" if k else None
        if k > 1: overnumbered.append((p_["id"], k))
        n += k
        secs.append({"printed": printed, "declared": f"§{dec}" if dec and dec.isdigit() else None,
                     "index": page_index(p_["id"]), "title": title, "page": p_["id"], "ready": p_["ready"]})
    for p_, _ in appx:
        dec, title = page_heading(p_)
        k = _numbered_count(p_, f"appendices/{p_['id']}")
        printed = f"Appendix {chr(64 + letter + 1)}" if k else None
        if k > 1: overnumbered.append((p_["id"], k))
        letter += k
        secs.append({"printed": printed, "declared": f"Appendix {dec}" if dec and dec.isalpha() else None,
                     "index": page_index(p_["id"]), "title": title, "page": p_["id"], "ready": p_["ready"]})
    findings, seen_label, claimed = [], {}, {}
    for pid_, k in overnumbered:
        findings.append(f"{pid_}: its fragment prints {k} numbered sections; inner divisions should be \\subsection so the page is one §")
    for r in secs:
        if r["declared"] and r["printed"] and r["declared"] != r["printed"]:
            findings.append(f"{r['page']}: page H1 says {r['declared']}, prints {r['printed']}")
    for r in rows:
        if r["declared"] and r["declared"] != r["printed"]:
            findings.append(f"{r['unit'] or r['label']}: claims {r['declared']}, prints {r['printed']}")
        if r["unit"] and not r["declared"]:
            findings.append(f"{r['unit']}: prints {r['printed']} but its README declares no number")
        if r["label"] and r["label"] in seen_label:
            findings.append(f"label {r['label']} printed twice: {seen_label[r['label']]} and {r['printed']}")
        seen_label.setdefault(r["label"], r["printed"])
    # Check units on disk, including Pages not yet ready. Page IDs are stable
    # identities; legacy embedded indices never determine current reading order.
    ladder = [VERSION.relative_to(ROOT).as_posix() + "/"] if VERSION != ROOT else []   # 0.10.0: the version's Sections
    for page_dir in sorted(q for pat in ["B*-*-Main/*/"] + ladder for q in ROOT.glob(pat)
                           if q.is_dir() and not q.name.startswith(("_", "."))) + \
                    sorted(q for q in ROOT.glob("B*-*-Appendix/*/") if q.is_dir() and not q.name.startswith(("_", "."))):
        page = page_dir.name
        if not (page.startswith("S-") or re.match(r"^t[0-2]\d_", page)): continue
        disp = plan_home(page_dir) / "evidence" / "display"
        for unit_dir in sorted(u for u in disp.glob("*/") if u.is_dir()) if disp.exists() else []:
            unit = unit_dir.name; key = f"{page}/{unit}"
            if not re.fullmatch(r"Display\d+-[A-Za-z0-9][A-Za-z0-9-]*", unit):
                findings.append(f"legacy unit name {key}: rename to Display<n>-<slug> (the Page owns the unit independently of printed order)")
            if not (unit_dir / "README.md").exists():
                findings.append(f"{key} has no README.md, so it can declare no number")
                continue
            d = declared_number(key)
            if d: claimed.setdefault(d, []).append(key)
    for number, owners in sorted(claimed.items()):
        if len(owners) > 1:
            findings.append(f"{number} claimed by {len(owners)} units: {', '.join(owners)}")
    # 0.7.7 tooth: one work under two keys. Both cited = the reference list PRINTS it twice
    # (a finding). Only one cited = the spare entry is still staged and the next author can
    # pick the wrong key, so it is a warning rather than a finding.
    dup_both, dup_staged = duplicate_bib_works(cited)
    for keys in dup_both:
        findings.append(f"one work cited under {len(keys)} keys, so the reference list prints it twice: {', '.join(keys)}")
    for keys in dup_staged:
        BUILD_WARNINGS.append(f"bib: one work staged under {len(keys)} keys ({', '.join(keys)}); only one is cited, drop the spare before someone cites it")
    lines = [f"# Display register · GENERATED by {ENGINE_TAG}, never hand-edited", "",
             f"Built {datetime.now().strftime('%Y-%m-%d %H:%M')} · "
             f"{counters['figure']} figure(s) + {counters['table']} table(s) printed.",
             "A number here is provisional while any page is NOT READY: a page that starts",
             "compiling inserts its floats and renumbers everything after it.", "", "```text"]
    lines.append(f"{'PRINTED':<10} {'DECLARED':<10} {'LABEL':<34} {'UNIT (page/Display<n>-slug)':<64} PAGE")
    for r in rows:
        flag = "" if (r["declared"] or "") in ("", r["printed"]) else "  ⛔"
        lines.append(f"{r['printed']:<10} {(r['declared'] or '—'):<10} {r['label']:<34} {r['unit'] or '—':<64} {r['page']}{flag}")
    lines += ["```", "", "## Sections", "", "```text"]
    lines.append(f"{'PRINTED':<12} {'DECLARED':<12} {'READY':<6} {'TITLE':<44} PAGE")
    for r in secs:
        flag = "" if (r["declared"] or r["printed"] or "") == (r["printed"] or r["declared"] or "") else "  ⛔"
        lines.append(f"{(r['printed'] or '(unnumbered)'):<12} {(r['declared'] or '—'):<12} "
                     f"{('yes' if r['ready'] else 'no'):<6} {r['title'][:44]:<44} {r['page']}{flag}")
    lines += ["```", ""]
    findings.extend(extra_findings)
    # Computed HERE, not by the caller: build() used to assemble these two and pass
    # them in, so every other entry point (the test harness included) silently ran
    # without them (found 260908 when both new teeth reported nothing under pytest).
    all_pages = [q for q, _ in main] + [q for q, _ in appx]
    page_title, cfg_title = declared_title(all_pages), CFG["paper"].get("title")
    if page_title and cfg_title and page_title != cfg_title:
        findings.append(f"title drift: the Abstract page says {page_title!r}, paper-build.toml says "
                        f"{cfg_title!r}; the page is printed")
    findings.extend(venue_findings(all_pages))
    lines.append("## Findings")
    lines += [f"- {f}" for f in findings] if findings else ["- none"]
    (HERE / "display-register.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"figures": counters["figure"], "tables": counters["table"],
            "rows": rows, "sections": secs, "findings": findings}
