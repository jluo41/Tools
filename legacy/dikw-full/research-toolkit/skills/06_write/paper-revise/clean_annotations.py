"""
Strip annotation cruft from annotated .tex files, keeping:
  - Section header blocks (between % ==== lines)
  - \\section{} lines
  - Paragraph markers:  %% ---- PXX: ... ----
  - Sentence markers:   %% ---- PXX.SY [...] ----
  - Bare % separators
  - Active (proposed) text
  - Empty lines

Removing:
  - Old commented-out text (% old sentence...)
  - %% Proposed: %%
  - %% Changes: / %%   (1)... / %% Reason: / %% Author: / %% Comments:
"""

import os
import re
import sys


def clean_annotated_tex(input_path, output_path=None):
    with open(input_path, "r") as f:
        lines = f.readlines()

    output_lines = []
    in_header_block = False  # between % ===== lines

    for line in lines:
        stripped = line.rstrip("\n")

        # --- Section header block (between % ===== lines) → keep everything inside ---
        if stripped.startswith("% ===="):
            in_header_block = not in_header_block
            output_lines.append(line)
            continue
        if in_header_block:
            output_lines.append(line)
            continue

        # --- \section{} → keep ---
        if stripped.startswith("\\section{"):
            output_lines.append(line)
            continue

        # --- (1) Index markers: %% ---- P... ---- → keep ---
        # Only paragraph/sentence markers starting with P (e.g. P1.S2, P6: RQ1).
        # Excludes pure-dash separators and OLD-* deletion markers.
        if re.match(r"^%%\s*----\s+P", stripped):
            output_lines.append(line)
            continue

        # --- (2) Review dialogue: %% Comments: \ra{...} or \jl{...} → keep ---
        if stripped.startswith("%% Comments:"):
            output_lines.append(line)
            continue

        # --- Bare % separator → keep ---
        if stripped == "%":
            output_lines.append(line)
            continue

        # --- (3) Any other %% line → remove ---
        if stripped.startswith("%%"):
            continue

        # --- Old commented-out text → remove ---
        # (lines starting with "% " that are NOT inside the header block)
        if stripped.startswith("% "):
            continue

        # --- Empty lines → keep ---
        if stripped == "":
            output_lines.append(line)
            continue

        # --- Active text (non-comment) → keep ---
        output_lines.append(line)

    # Collapse runs of 3+ consecutive blank-ish lines (bare % or empty) to 2
    final = []
    blank_run = 0
    for line in output_lines:
        if line.rstrip("\n") in ("", "%"):
            blank_run += 1
            if blank_run <= 2:
                final.append(line)
        else:
            blank_run = 0
            final.append(line)

    out = output_path or input_path
    with open(out, "w") as f:
        f.writelines(final)
    print(f"Cleaned: {input_path} → {out}  ({len(lines)} → {len(final)} lines)")


def rebuild_sections_to_copy(src_dir="0-sections", dst_dir="0-sections-to-copy"):
    """Delete dst_dir, copy all .tex from src_dir, clean each one."""
    import glob
    import shutil

    script_dir = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(script_dir, src_dir)
    dst = os.path.join(script_dir, dst_dir)

    # Always start fresh
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.makedirs(dst)

    tex_files = sorted(glob.glob(os.path.join(src, "*.tex")))
    for f in tex_files:
        basename = os.path.basename(f)
        dst_file = os.path.join(dst, basename)
        shutil.copy2(f, dst_file)
        clean_annotated_tex(dst_file)

    print(f"\nDone: {len(tex_files)} files → {dst_dir}/")


if __name__ == "__main__":
    # No args = rebuild 0-sections-to-copy/ from 0-sections/
    # With args = clean a single file
    if len(sys.argv) < 2:
        rebuild_sections_to_copy()
    else:
        inp = sys.argv[1]
        out = sys.argv[2] if len(sys.argv) > 2 else None
        clean_annotated_tex(inp, out)
