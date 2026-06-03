"""
Status Reporter for End-to-End Roadmaps.

Ask Claude to analyze a roadmap markdown file and report:
  - Current phase (which stage)
  - Progress % (how many stages done)
  - Next action
  - Blockers (if marked)

Usage:
  python statusline_reporter.py status _WorkSpace/project-name/roadmap.md
"""
import argparse
import os
import sys
from pathlib import Path

try:
    import anthropic
except ImportError:
    print("❌ anthropic SDK required. Install: pip install anthropic")
    sys.exit(1)


def analyze_roadmap(roadmap_path: Path) -> str:
    """Ask Claude to analyze a roadmap markdown and report status.

    Args:
        roadmap_path: Path to roadmap.md

    Returns:
        Claude's analysis (formatted string)
    """
    if not roadmap_path.exists():
        print(f"❌ Roadmap not found: {roadmap_path}")
        return ""

    roadmap_content = roadmap_path.read_text()

    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    prompt = f"""Analyze this E2E project roadmap and report status:

<roadmap>
{roadmap_content}
</roadmap>

Report:
1. **Current Phase** — Which stage are we in right now?
2. **Progress** — How many stages done/running/pending? % complete?
3. **Next Action** — What should happen next?
4. **Blockers** — Any impediments or risks marked?
5. **Timeline** — When might we finish based on what's done?

Format as:

📊 **Roadmap Status Report**

**Current Phase:** [stage X of Y]
**Progress:** [X done, Y running, Z pending] (A% complete)
**Next Action:** [what to do next]
**Blockers:** [none / list any]
**Timeline:** [estimated completion]

---

[Brief narrative (2-3 sentences) on overall progress]
"""

    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.content[0].text


def main():
    parser = argparse.ArgumentParser(
        description="Status Reporter for E2E Roadmaps"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command")

    status_parser = subparsers.add_parser("status", help="Analyze roadmap status")
    status_parser.add_argument("roadmap", type=Path, help="Path to roadmap.md")

    args = parser.parse_args()

    if args.command == "status":
        if not os.environ.get("ANTHROPIC_API_KEY"):
            print("❌ ANTHROPIC_API_KEY not set")
            sys.exit(1)

        print("🔍 Analyzing roadmap...")
        report = analyze_roadmap(args.roadmap)
        print(report)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
