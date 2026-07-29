#!/usr/bin/env python3
"""Regenerate a section's icons as ONE clean grid via Codex native image-gen,
then you slice it with slice_grid.py. See lesson/13, lesson/14.

Drives the codex-image2 bridge directly (its MCP tools may not be registered in
a given session). Requires the `codex` CLI on PATH + the codex-image2 bridge from
the haipipe-toolkit plugin. Point CODEX_IMAGE2_SERVER at server.py, or rely on the
default sibling-plugin path below.

Usage:
    gen_icon_grid.py <workspace_cwd> <reference.png> <out_name.png> <prompt.txt> [timeout=300]

The grid lands in <workspace_cwd>/figures/ai_generated/<out_name.png> (the bridge
hard-locks output under figures/ai_generated/). Prompt should ask for a 3x3 grid
by DEFAULT (2x2 for human-figure-heavy sections; never 4x4), ~60% cell fill with
large margins, pure white background, no text.
"""
import importlib.util, os, sys
from pathlib import Path

# The bridge lives at <haipipe-toolkit>/mcp-servers/codex-image2/server.py. This skill has moved
# between plugin layouts more than once (own plugin, nested under haipipe-display-diagram, now a
# sibling skill inside haipipe-toolkit), so resolve by SEARCHING upward instead of counting
# parents: walk the ancestors and take the first hit, either inside an ancestor itself or inside
# an ancestor's haipipe-toolkit/ child. Override with CODEX_IMAGE2_SERVER when it lives elsewhere.
REL = Path("mcp-servers") / "codex-image2" / "server.py"


def find_bridge():
    for anc in Path(__file__).resolve().parents:
        for cand in (anc / REL, anc / "haipipe-toolkit" / REL):
            if cand.is_file():
                return str(cand)
    return ""


BRIDGE = os.environ.get("CODEX_IMAGE2_SERVER") or find_bridge()

if not Path(BRIDGE).is_file():
    sys.exit(
        f"ERROR: codex-image2 bridge not found (searched every ancestor of this script for "
        f"{REL} and haipipe-toolkit/{REL}; got {BRIDGE!r}).\n"
        "This is a hard prerequisite of the pipeline. Install the haipipe-toolkit plugin, or set "
        "CODEX_IMAGE2_SERVER to its mcp-servers/codex-image2/server.py, then rerun.")

spec = importlib.util.spec_from_file_location("codex_image2_server", BRIDGE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
sys.stdout = sys.__stdout__   # bridge swaps stdout to binary on import; restore it

cwd = Path(sys.argv[1]).resolve()
ref = Path(sys.argv[2]).resolve()
out = (cwd / "figures" / "ai_generated" / sys.argv[3]).resolve()
prompt = Path(sys.argv[4]).read_text(encoding="utf-8")
timeout = int(sys.argv[5]) if len(sys.argv) > 5 else 300

payload, error = mod.run_codex_image(
    prompt, cwd=cwd, output_path=out,
    system="High-resolution icon sheet. Match the reference icons' style and colours. No text labels.",
    reference_image_paths=[str(ref)], timeout_sec=timeout,
    run_log_path=out.with_suffix(".log"),
)
if error:
    print("ERROR:", error); sys.exit(1)
print("OK ->", payload.get("outputPath"))
