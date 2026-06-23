"""CLI: show patient context for one individual.

    python show_ctx_cli.py --individual Subject-18
    python show_ctx_cli.py --individual UserGroup-WellDoc2022CGM/Subject-26
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from load_patient import load_patient_ctx, summarize_ctx  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--individual", required=True)
    ap.add_argument("--cgm-tail", type=int, default=None)
    args = ap.parse_args()

    ctx = load_patient_ctx(args.individual, cgm_tail=args.cgm_tail)
    print(json.dumps(summarize_ctx(ctx), indent=2, default=str))


if __name__ == "__main__":
    main()
