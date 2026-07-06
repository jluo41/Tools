#!/usr/bin/env python3
"""
G2 Integrity Check — deterministic number-tracing for probe evidence.

Cross-references every number in evidence.md against the source CSV files
listed in probe.yaml's evidence_refs (plus sibling CSVs in the same results
directories). Zero model involvement.

Usage:
    python g2_integrity_check.py <probe_folder> [--verbose]
    python g2_integrity_check.py --batch <folder1> <folder2> ...
"""

import argparse
import os
import re
import sys
from pathlib import Path

import pandas as pd
import yaml


# ---------------------------------------------------------------------------
# 1. Number extraction from evidence.md
# ---------------------------------------------------------------------------

# Regex: captures scientific notation, percentages, comma-separated ints, decimals.
NUMBER_RE = re.compile(
    r"(?<![a-zA-Z_])"              # not preceded by letter or underscore
    r"("
    r"[+-]?\d+\.\d+[eE][+-]?\d+"   # scientific notation with decimal (9.67e-12)
    r"|"
    r"[+-]?\d+[eE][+-]?\d+"        # scientific notation int (1e-6)
    r"|"
    r"\d{1,3}(?:,\d{3})+"          # comma-separated integer (693,474)
    r"|"
    r"[+-]?\d+\.\d+"               # decimal (0.8148)
    r"|"
    r"[+-]?\d+"                     # plain integer
    r")"
    r"(%|[KMB](?![a-zA-Z]))?"      # optional trailing percent or K/M/B abbreviation
    r"(?![a-zA-Z_])"               # not followed by letter/underscore
)

# Lines that are file paths / artifact references — not data
ARTIFACT_LINE_RE = re.compile(
    r"results/run_|\.csv\b|\.png\b|\.pdf\b|^Artifact|^Task folder:|^Task:"
    r"|^Figures:|^Source artifact",
    re.IGNORECASE,
)
TABLE_SEP_RE = re.compile(r"^\s*\|[-:|\s]+\|$")
DATE_INLINE_RE = re.compile(r"\b20\d{2}[-/]\d{2}[-/]\d{2}\b|Date:\s*20\d{2}")
TASK_REF_LOCAL_RE = re.compile(r"B\d+/\d+")

# Threshold / parameter patterns — numbers here are settings, not results
THRESHOLD_CTX = re.compile(
    r"alpha\s*=\s*0\.05"
    r"|threshold\s*=\s*"
    r"|p\s*[<>]\s*0\.05"
    r"|p[<>]0\.05"
    r"|at\s+p\s*<"
    r"|at\s+alpha="
    r"|1\.000\s*\(ref\)"
    r"|rho\s*>=?\s*0\.5\b"
    r"|rho\s*<\s*0\.5\b",
    re.IGNORECASE,
)

# Context patterns for "derived / interpretive" numbers that are legitimately
# computed from CSV values but not stored as CSV values themselves.
DERIVED_PATTERNS = [
    # OR differences / coefficient changes
    (re.compile(r"OR\s+(shift|diff|change)|coefficient\s+change|absolute.*(shift|change)", re.I),
     "derived_diff"),
    # Percentage retained / removed
    (re.compile(r"retained|removed|reclassified|reduction|repeat", re.I),
     "derived_pct"),
    # Attenuation ratios
    (re.compile(r"attenuation|ratio.*logit.*probit|scaling", re.I),
     "derived_ratio"),
    # Combinatorial counts (66 pairs from 12 arms, 10 non-reference)
    (re.compile(r"pairs?\s+from|non-reference|comparisons.*from", re.I),
     "derived_combinatorial"),
    # Loss counts (4 comparisons lose significance)
    (re.compile(r"(lose|lost|gain)\s+significance", re.I),
     "derived_diff"),
    # Spread in pp
    (re.compile(r"\bspread\b.*pp|pp\s+spread|pp\s+(lift|below|above)", re.I),
     "derived_diff"),
]

# Dataset-level constants: sample sizes that are known properties of the
# dataset, not per-row CSV values. Recognized via N= or (n=...) context.
N_CONTEXT_RE = re.compile(
    r"\bN\s*=\s*[\d,]+"
    r"|\(N\s*=\s*[\d,]+\)"
    r"|\bn\s*=\s*[\d,]+"
    r"|\(n\s*=?\s*[\d,]+\)"
    r"|\bN\s*~\s*[\d,]+"
)


def classify_number(value, raw, pct, line, m_start, m_end, line_num):
    """Classify a number for the G2 check.

    Returns (category, reason):
      'check'            — verify against CSV
      'skip_param'       — known threshold/parameter
      'skip_artifact'    — in a file-path/artifact line
      'skip_date'        — date component
      'skip_trivial'     — structurally trivial (0-3 in prose)
      'skip_context'     — temporal or label reference
      'derived'          — legitimately computed from CSV values but not stored
      'dataset_constant' — sample size / dataset property
    """
    stripped = line.strip()

    # --- hard skips --------------------------------------------------------

    # Artifact / path lines (unless they contain table pipes with data)
    if ARTIFACT_LINE_RE.search(stripped) and "|" not in stripped:
        return "skip_artifact", "artifact/path line"

    # Table separator
    if TABLE_SEP_RE.match(stripped):
        return "skip_trivial", "table separator"

    # Date inline
    if DATE_INLINE_RE.search(line):
        ctx = line[max(0, m_start - 15):m_end + 15]
        if re.search(r"20\d{2}[-/]\d{2}[-/]\d{2}", ctx):
            return "skip_date", "date component"

    # Task reference (B00/06)
    if TASK_REF_LOCAL_RE.search(line[max(0, m_start - 5):m_end + 5]):
        return "skip_artifact", "task reference"

    # Threshold values
    if THRESHOLD_CTX.search(stripped):
        if value == 0.05 and not pct:
            return "skip_param", "significance threshold"
        if value == 0.5 and "rho" in stripped.lower():
            return "skip_param", "falsification threshold"

    # Explicit "threshold" or "min cell" cutoffs
    prefix_thresh = line[max(0, m_start - 15):m_start].lower()
    suffix_thresh = line[m_end:m_end + 15].lower()
    if "threshold" in suffix_thresh or "< " + raw in line[max(0, m_start - 5):m_end + 15]:
        if re.search(r"<\s*$", prefix_thresh):
            return "skip_param", "threshold cutoff"

    # Temporal reference ("15 days", "30d", "15-day")
    suffix = line[m_end:m_end + 10].lstrip()
    if re.match(r"(days?|d\b|-day)", suffix, re.IGNORECASE):
        return "skip_context", "temporal reference"

    # Range notation: "2-3", "10-28", "56-64%", "59-61%"
    # Part 1: negative value right after digit (the second element) -> range dash
    if raw.startswith("-") and value < 0:
        prefix_1 = line[max(0, m_start - 1):m_start]
        if prefix_1 and prefix_1[-1].isdigit():
            return "derived", "range_dash"
    # Part 2: positive value followed by "-\d" (the first element in a range)
    if value >= 0:
        suffix_range = line[m_end:m_end + 8]
        if re.match(r"-\d+%?(\s|$|\))", suffix_range):
            return "derived", "range_start"

    # Year
    if 2020 <= value <= 2030 and not pct and value == int(value):
        return "skip_date", "year"

    # Very small structural integers (0-3) in prose (not in tables/data context)
    if value in (0, 1, 2, 3) and not pct and value == int(value):
        if "|" in stripped:
            return "check", None
        pre = line[max(0, m_start - 25):m_start].lower()
        if any(kw in pre for kw in ["n=", "chi2", "wald", "rho", "or=", "df=",
                                     "count", "rate", "coef"]):
            return "check", None
        return "skip_trivial", "small structural integer"

    # Probe/section identifiers: PP06, E1, E5, Phase 1, P.0623a
    prefix_id = line[max(0, m_start - 6):m_start]
    if re.search(r"(PP\d*|E\d?|Phase\s|P\.\d*)$", prefix_id, re.I):
        return "skip_trivial", "section/probe identifier"

    # Note: K/M/B abbreviation (379K, 2.9M) handled before classify_number

    # "X of Y pairs/comparisons" — the total count Y is structural
    if value == int(value) and value >= 4:
        suffix_of = line[m_end:m_end + 30]
        if re.match(r"\s+of\s+\d+\s+(pair|comparison|term)", suffix_of, re.I):
            pass  # keep the first number (X) as checkable
        prefix_of = line[max(0, m_start - 6):m_start]
        if re.search(r"(of|for)\s+$", prefix_of, re.I):
            suffix_count = line[m_end:m_end + 20]
            if re.match(r"\s+(pair|comparison|term|arm|test)", suffix_count, re.I):
                return "derived", "total_count"

    # --- derived / interpretive numbers ------------------------------------

    # N= sample sizes that won't be in per-row CSVs
    if value == int(value) and value >= 100:
        prefix_20 = line[max(0, m_start - 20):m_start]
        # Explicit N=, n=, (n=...) context
        if re.search(r"[Nn]\s*[=~]\s*$", prefix_20) or re.search(r"\(n\s*=?\s*$", prefix_20, re.I):
            return "dataset_constant", "sample size (N=)"
        # Dataset header line: "(NNN,NNN rows/messages/patients/prescribers)"
        if re.search(r"Dataset:|Data:|Sample:", stripped, re.I):
            suffix_20 = line[m_end:m_end + 25]
            if re.search(r"\s*(rows|messages|patients|prescribers|arms|obs)", suffix_20, re.I):
                return "dataset_constant", "dataset header"

    # Counts in dataset metadata lines: "12 arms", "102,484 prescribers", "673,989 patients"
    if value == int(value) and value >= 4:
        suffix_25 = line[m_end:m_end + 35].lstrip()
        if re.match(r"(arms?\b|prescribers|patients|messages|obs\b|subgroups|dimensions|"
                     r"hippo-eligible|hippo_eligible|behavioral|rows|samples|"
                     r"in\s+top|drug\s+class|pairs|[-]arm)",
                     suffix_25, re.I):
            return "dataset_constant", "dataset count"

    # Wald chi2 / LR chi2 / test statistics (often computed in-script, not saved)
    if re.search(r"(Wald|LR|chi2|chi-?square)\s*(=|chi2\s*=)\s*", stripped, re.I):
        prefix_ctx = line[max(0, m_start - 15):m_start]
        if re.search(r"chi2\s*=\s*$|chi2=\s*$", prefix_ctx, re.I):
            return "derived", "test_statistic"
        # df= in same line as chi2
        if re.search(r"df\s*=", stripped) and value == int(value):
            prefix_ctx2 = line[max(0, m_start - 5):m_start]
            if re.search(r"df\s*=\s*$", prefix_ctx2, re.I):
                return "derived", "degrees_of_freedom"

    # Model-level summary statistics: pseudo-R2, AIC, BIC, log-likelihood
    if re.search(r"pseudo-?R2|AIC|BIC|log.?lik", stripped, re.I):
        prefix_ctx = line[max(0, m_start - 20):m_start]
        if re.search(r"(pseudo-?R2|AIC|BIC|log.?lik)\s*[=:]\s*$", prefix_ctx, re.I):
            return "derived", "model_summary_stat"
        # Also handle "pseudo-R2: ~0.003-0.006" range context
        if re.search(r"pseudo-?R2|AIC|BIC", stripped, re.I):
            return "derived", "model_summary_stat"

    # Derived calculations (OR diffs, percentages, ratios, combinatorial counts)
    for pat, reason in DERIVED_PATTERNS:
        if pat.search(stripped):
            return "derived", reason

    # Percentages that describe proportions-of-sample (97.2% retained, 0.2% of clicks)
    if pct and re.search(r"of\s+(sample|total|all|clicks|messages|patients)", stripped, re.I):
        return "derived", "proportion_of_sample"

    # Parenthetical percentage summarizing a fraction: "6/12 ... (50%)"
    if pct:
        prefix_paren = line[max(0, m_start - 2):m_start]
        if "(" in prefix_paren:
            # Check if there's a fraction earlier in the line
            if re.search(r"\d+/\d+", line[:m_start]):
                return "derived", "fraction_percentage"

    # Ranges described as "+X to +Y" for coefficient ranges
    if re.search(r"from\s+[+-]|to\s+[+-]|ranging\s+from", stripped, re.I):
        if raw.startswith("+") or raw.startswith("-"):
            if "ranging" in stripped.lower() or "from" in stripped.lower():
                return "derived", "range_endpoint"

    # Fraction denominators: "59/66", "23/44" — the denominator is a structural
    # count (total comparisons, total terms) that may not be stored in CSV
    if value == int(value) and value >= 4:
        # Check if preceded by digits + "/" (i.e., this is the denominator of X/Y)
        prefix_frac = line[max(0, m_start - 6):m_start]
        if re.search(r"\d+/\s*$", prefix_frac):
            return "derived", "fraction_denominator"
        # Check if followed by "/" + digits (i.e., this is the numerator of X/Y)
        # — numerators are usually result values, so keep them as "check"

    return "check", None


def extract_numbers(evidence_path):
    """Extract all numbers from evidence.md with classification."""
    with open(evidence_path) as f:
        lines = f.readlines()

    results = []
    for line_num, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped:
            continue

        for m in NUMBER_RE.finditer(line):
            raw = m.group(1)
            suffix = m.group(2) or ""
            pct = suffix == "%"
            abbrev = suffix in ("K", "M", "B")
            clean = raw.replace(",", "")
            try:
                value = float(clean)
            except ValueError:
                continue

            # Abbreviated numbers (379K, 2.9M) are dataset constants
            if abbrev:
                category, reason = "dataset_constant", "abbreviated count"
            else:
                category, reason = classify_number(
                    value, raw, pct, line, m.start(), m.end(), line_num
                )

            display_raw = raw + suffix
            results.append({
                "value": value,
                "raw": display_raw,
                "pct": pct,
                "line_num": line_num,
                "context": stripped,
                "category": category,
                "skip_reason": reason,
            })

    return results


# ---------------------------------------------------------------------------
# 2. Parse probe.yaml for evidence_refs
# ---------------------------------------------------------------------------

def resolve_evidence_refs(probe_yaml_path, project_root):
    """Parse probe.yaml evidence_refs, returning absolute CSV paths.

    Also auto-discovers sibling CSVs in the same results directories.
    """
    with open(probe_yaml_path) as f:
        probe = yaml.safe_load(f)

    refs = probe.get("evidence_refs", [])
    csv_paths = set()
    results_dirs = set()

    for ref in refs:
        # Format 1: artifact as direct path
        artifact = ref.get("artifact", "")
        if artifact:
            full = project_root / artifact
            if artifact.endswith(".csv") and full.exists():
                csv_paths.add(full)
                results_dirs.add(full.parent)
            elif full.parent.exists():
                results_dirs.add(full.parent)
            if artifact.endswith("/") and full.exists():
                results_dirs.add(full)

        # Format 2: path + artifacts list
        base_path = ref.get("path", "")
        artifacts_list = ref.get("artifacts", [])
        if base_path and artifacts_list:
            base = project_root / base_path
            for art in artifacts_list:
                if art.endswith(".csv"):
                    full = base / art
                    if full.exists():
                        csv_paths.add(full)
            if base.exists():
                results_dirs.add(base)

        # Format 3: supplementary list
        supplementary = ref.get("supplementary", [])
        for sup in supplementary:
            if not sup.endswith(".csv"):
                continue
            # Try resolving relative to the task folder implied by artifact
            resolved = False
            if artifact:
                # Walk up from artifact to find where supplementary paths root
                task_dir = (project_root / artifact).parent
                while task_dir != project_root and not resolved:
                    candidate = task_dir / sup
                    if candidate.exists():
                        csv_paths.add(candidate)
                        results_dirs.add(candidate.parent)
                        resolved = True
                    task_dir = task_dir.parent
            if not resolved:
                full = project_root / sup
                if full.exists():
                    csv_paths.add(full)
                    results_dirs.add(full.parent)

    # Auto-discover sibling CSVs
    for d in list(results_dirs):
        if d.is_dir():
            for f in d.glob("*.csv"):
                csv_paths.add(f)

    return sorted(csv_paths)


# ---------------------------------------------------------------------------
# 3. CSV value index
# ---------------------------------------------------------------------------

class CSVIndex:
    """Searchable index of all numeric values in source CSVs."""

    def __init__(self, csv_paths, verbose=False):
        self.values = []       # (float_val, file_name, col, row_idx)
        self.row_counts = {}   # file_name -> row count
        self.col_counts = {}   # (file_name, col) -> count-of-True
        self.verbose = verbose

        for path in csv_paths:
            try:
                df = pd.read_csv(path)
            except Exception as e:
                if verbose:
                    print(f"  WARN: cannot read {path.name}: {e}")
                continue

            fname = path.name
            self.row_counts[fname] = len(df)

            for col in df.columns:
                true_count = 0
                for row_idx, val in enumerate(df[col]):
                    if pd.isna(val):
                        continue

                    # Numeric
                    try:
                        num = float(val)
                        self.values.append((num, fname, col, row_idx))
                    except (ValueError, TypeError):
                        pass

                    # Boolean True
                    if val is True or str(val).strip().lower() == "true":
                        true_count += 1

                    # Fraction strings ("11/11")
                    frac = re.match(r"^(\d+)/(\d+)$", str(val).strip())
                    if frac:
                        self.values.append(
                            (int(frac.group(1)), fname, f"{col}:numer", row_idx))
                        self.values.append(
                            (int(frac.group(2)), fname, f"{col}:denom", row_idx))

                if true_count > 0:
                    self.col_counts[(fname, col)] = true_count

    def search(self, target, is_pct=False, rtol=0.006, atol=1e-6):
        """Search for target. Returns list of match dicts or []."""
        candidates = [target]
        if is_pct:
            candidates.append(target / 100.0)

        matches = []
        seen = set()

        for cand in candidates:
            # Direct value match
            for val, fname, col, row_idx in self.values:
                if _match(cand, val, rtol, atol):
                    key = (fname, col, row_idx)
                    if key not in seen:
                        seen.add(key)
                        matches.append({
                            "csv_value": val, "file": fname,
                            "column": col, "row": row_idx,
                            "match_type": "direct",
                        })

            # Derived count match (count of True in boolean columns)
            if cand == int(cand) and cand > 0:
                for (fname, col), count in self.col_counts.items():
                    if count == int(cand):
                        key = (fname, col, "count")
                        if key not in seen:
                            seen.add(key)
                            matches.append({
                                "csv_value": count, "file": fname,
                                "column": f"{col} (count_true)",
                                "row": -1, "match_type": "count_true",
                            })

            # Row count match (large N values)
            if cand == int(cand) and cand > 100:
                for fname, count in self.row_counts.items():
                    if count == int(cand):
                        key = (fname, "(rows)")
                        if key not in seen:
                            seen.add(key)
                            matches.append({
                                "csv_value": count, "file": fname,
                                "column": "(row_count)",
                                "row": -1, "match_type": "row_count",
                            })

        return matches


def _match(a, b, rtol=0.006, atol=1e-6):
    """Numeric match with tolerance.

    rtol=0.6% handles typical rounding (0.81 vs 0.8148).
    For small values (|a| < 0.05), widens tolerance to handle
    aggressive p-value rounding (0.003 vs 0.00343 = 14%).
    """
    if a == b:
        return True
    diff = abs(a - b)
    if diff <= atol:
        return True
    denom = max(abs(a), abs(b))
    if denom == 0:
        return False

    rel = diff / denom

    # Standard tolerance
    if rel <= rtol:
        return True

    # Wider tolerance for small values (p-values, small rates):
    # evidence.md often rounds to 1 sig fig (0.003 for 0.00343)
    if denom < 0.1 and rel <= 0.15:
        return True

    return False


# ---------------------------------------------------------------------------
# 4. Run the check
# ---------------------------------------------------------------------------

def run_check(probe_folder, verbose=False):
    """Run G2 integrity check. Returns result dict."""
    probe_folder = Path(probe_folder).resolve()
    evidence_path = probe_folder / "evidence.md"
    yaml_path = probe_folder / "probe.yaml"

    if not evidence_path.exists():
        return {"error": f"evidence.md not found in {probe_folder}"}
    if not yaml_path.exists():
        return {"error": f"probe.yaml not found in {probe_folder}"}

    project_root = _find_project_root(probe_folder)
    if not project_root:
        return {"error": f"Cannot find project root from {probe_folder}"}

    # 1) Extract
    numbers = extract_numbers(evidence_path)
    checkable = [n for n in numbers if n["category"] == "check"]
    derived = [n for n in numbers if n["category"] == "derived"]
    dataset_const = [n for n in numbers if n["category"] == "dataset_constant"]
    skipped = [n for n in numbers if n["category"].startswith("skip")]

    # 2) Resolve CSVs
    csv_paths = resolve_evidence_refs(yaml_path, project_root)
    if verbose:
        print(f"  CSVs: {len(csv_paths)}")
        for p in csv_paths:
            print(f"    {p.relative_to(project_root)}")

    # 3) Build index
    index = CSVIndex(csv_paths, verbose=verbose)
    if verbose:
        print(f"  Index: {len(index.values)} vals, "
              f"{len(index.col_counts)} bool cols")

    # 4) Verify checkable numbers against CSV index
    verified = []
    unverified = []
    for num in checkable:
        ms = index.search(num["value"], is_pct=num["pct"])
        if ms:
            num["matches"] = ms
            verified.append(num)
        else:
            unverified.append(num)

    # 5) Also try to verify derived/dataset_constant numbers (bonus credit)
    derived_verified = []
    derived_unverified = []
    for num in derived + dataset_const:
        ms = index.search(num["value"], is_pct=num["pct"])
        if ms:
            num["matches"] = ms
            derived_verified.append(num)
        else:
            derived_unverified.append(num)

    # 6) Verdict based on checkable numbers only
    n_check = len(checkable)
    n_ver = len(verified)
    n_unver = len(unverified)
    pct_ver = (n_ver / n_check * 100) if n_check > 0 else 100.0

    if pct_ver >= 95:
        verdict = "PASS"
    elif pct_ver >= 80:
        verdict = "WARN"
    else:
        verdict = "FAIL"

    return {
        "probe_folder": str(probe_folder),
        "probe_name": probe_folder.name,
        "total_numbers": len(numbers),
        "skipped": len(skipped),
        "derived": len(derived),
        "dataset_const": len(dataset_const),
        "checkable": n_check,
        "verified": n_ver,
        "unverified": n_unver,
        "pct_verified": pct_ver,
        "verdict": verdict,
        "verified_list": verified,
        "unverified_list": unverified,
        "derived_verified": derived_verified,
        "derived_unverified": derived_unverified,
        "skipped_list": skipped,
        "csv_files": [str(p) for p in csv_paths],
    }


def _find_project_root(probe_folder):
    """Walk up to find directory containing tasks/."""
    cur = probe_folder
    for _ in range(10):
        if (cur / "tasks").is_dir():
            return cur
        cur = cur.parent
    return None


# ---------------------------------------------------------------------------
# 5. Report formatting
# ---------------------------------------------------------------------------

def format_report(result, verbose=False):
    """Format G2 report as plain text."""
    if "error" in result:
        return f"ERROR: {result['error']}\n"

    lines = []
    name = result["probe_name"]
    lines.append(f"G2 Integrity Report: {name}")
    lines.append("=" * (22 + len(name)))
    lines.append("")
    lines.append(f"Verdict: {result['verdict']}")
    lines.append("")
    lines.append("Numbers")
    lines.append("-------")
    lines.append(f"  Total extracted:     {result['total_numbers']}")
    lines.append(f"  Skipped (non-data):  {result['skipped']}")
    lines.append(f"  Derived/computed:    {result['derived']}")
    lines.append(f"  Dataset constants:   {result['dataset_const']}")
    lines.append(f"  Checkable:           {result['checkable']}")
    lines.append(f"  Verified in CSV:     {result['verified']}  ({result['pct_verified']:.1f}%)")
    lines.append(f"  NOT found in CSV:    {result['unverified']}")
    lines.append("")
    lines.append(f"Source CSVs: {len(result['csv_files'])}")
    for p in result["csv_files"]:
        pp = Path(p)
        # Show parent dir if there are duplicates
        label = f"{pp.parent.name}/{pp.name}" if pp.parent.name != "run_default" else pp.name
        lines.append(f"  {label}")
    lines.append("")

    if result["unverified_list"]:
        lines.append("Unverified Numbers (potential phantoms)")
        lines.append("---------------------------------------")
        for num in result["unverified_list"]:
            ctx = num["context"][:100]
            lines.append(f"  L{num['line_num']:3d} | {num['raw']:>14s} | {ctx}")
        lines.append("")

    if result["derived_unverified"]:
        lines.append("Derived/Constant (not in CSV, expected)")
        lines.append("----------------------------------------")
        for num in result["derived_unverified"]:
            ctx = num["context"][:100]
            tag = num["skip_reason"] or num["category"]
            lines.append(f"  L{num['line_num']:3d} | {num['raw']:>14s} | [{tag}] {ctx}")
        lines.append("")

    if verbose:
        if result["verified_list"]:
            lines.append("Verified Numbers (sample)")
            lines.append("-------------------------")
            for num in result["verified_list"][:30]:
                m = num["matches"][0]
                lines.append(
                    f"  L{num['line_num']:3d} | {num['raw']:>14s} -> "
                    f"{m['file']}:{m['column']} [{m['match_type']}]"
                )
            rem = len(result["verified_list"]) - 30
            if rem > 0:
                lines.append(f"  ... and {rem} more")
            lines.append("")

    return "\n".join(lines)


def write_report(result, probe_folder):
    """Write g2_integrity_report.md to probe folder."""
    path = Path(probe_folder) / "g2_integrity_report.md"
    with open(path, "w") as f:
        f.write(format_report(result, verbose=True))
    return path


# ---------------------------------------------------------------------------
# 6. CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="G2 Integrity Check: deterministic number-tracing for probe evidence"
    )
    parser.add_argument("probe_folder", nargs="?",
                        help="Path to probe folder")
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--batch", nargs="*",
                        help="Run on multiple probe folders")
    args = parser.parse_args()

    folders = []
    if args.batch is not None:
        folders = [Path(p).resolve() for p in args.batch]
    elif args.probe_folder:
        folders = [Path(args.probe_folder).resolve()]
    else:
        parser.print_help()
        sys.exit(1)

    all_results = []
    for folder in folders:
        if not folder.is_dir():
            print(f"SKIP: {folder} not a directory", file=sys.stderr)
            continue

        print(f"\nG2 Integrity Check: {folder.name}")
        print("-" * 50)

        result = run_check(folder, verbose=args.verbose)
        all_results.append(result)

        if "error" in result:
            print(f"  ERROR: {result['error']}")
            continue

        print(format_report(result, verbose=args.verbose))
        rp = write_report(result, folder)
        print(f"Report written to: {rp}")

    # Batch summary
    if len(all_results) > 1:
        print("\n" + "=" * 75)
        print("BATCH SUMMARY")
        print("=" * 75)
        print(f"{'Probe':<42s} {'Check':>5s} {'OK':>4s} {'??':>4s} {'%':>6s}  Verdict")
        print("-" * 75)
        for r in all_results:
            if "error" in r:
                print(f"{r.get('probe_name','?'):<42s}  ERROR")
            else:
                print(
                    f"{r['probe_name']:<42s} "
                    f"{r['checkable']:>5d} "
                    f"{r['verified']:>4d} "
                    f"{r['unverified']:>4d} "
                    f"{r['pct_verified']:>5.1f}%  "
                    f"{r['verdict']}"
                )
        print("-" * 75)


if __name__ == "__main__":
    main()
