"""s01 · The console ladder: what the In-Lab Console is built from, the way the toolkit's s01 ladders are drawn.
Its ladder (Dataset → Human → Case → Score or Label), its scope axis (Individual · Group), and its rail groups as the
console's Spaces, each group's views read from web/src/views.ts; beside each, the toolkit workbench's counterpart.
A rebuild keeps whatever a person drew.

    python build_s01_console_ladder.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "_build"))
from console_draw import RED, VIEWS, Sheet, header, save  # noqa: E402

CHANGES = []                                          # (YYMMDD, what changed): a green note each
LADDER = [("🗃️ Dataset", "a data type: one patient store (one RecordSet cooked to per-human json)", "the topbar picker",
           "Block"),
          ("🧑 Human", "one patient or physician: the page binds to them (Individual)", "the patient picker",
           "Job"),
          ("📌 Case", "one point cut from that human's record: the unit a score or a label attaches to", "the Case view",
           "Task"),
          ("🧠 Score  or  ✏️ Label", "the endpoint's number (▶ Run), or a person's adjudicated label (Annotate)",
           "Model · Annotate", "Run")]
COUNTERPART = {"Data": "Description (what it is, from disk)", "Insight": "Audience Report (what it says)",
               "Action": "Runs (what acts, gated)", "Console": "the frame's own status"}


def main():
    s = Sheet()
    f = s.frame("1 · The console ladder", 0, 0, 1900, 100)
    y = header(s, f, "s01 · The console ladder: Dataset → Human → Case → Score or Label",
               "The In-Lab Console is inlab-human's workbench. Read against the toolkit's ladder (Block → Job → Task → Run),\n"
               "level by level, and its rail groups against the toolkit workbench's Spaces.", CHANGES)
    y = s.table(40, y, [("level", 260, 24), ("what it is", 700, 70), ("where on screen", 280, 28),
                        ("toolkit counterpart", 240, 24)], [list(r) for r in LADDER], f)
    y += 40
    s.text(40, y, "Scope axis: 👤 Individual (one human bound to the page) · 👥 Group (the dataset's whole cohort)", 20, f)
    y += 50
    groups = {}
    for key, icon, label, group in VIEWS:
        groups.setdefault(group, []).append(f"{icon} {label}")
    rows = [[g, "  ·  ".join(v), COUNTERPART.get(g, "")] for g, v in groups.items()]
    s.text(40, y, "The rail groups (web/src/views.ts), as the console's Spaces", 22, f)
    y = s.table(40, y + 40, [("group", 160, 16), ("views", 760, 80), ("toolkit counterpart", 560, 56)], rows, f)
    y += 30
    s.text(40, y, "? is a Case the console's Task, or its Run? one meaning would let both ladders share their screens (j02 Q04)",
           16, f, RED)
    save(s, f, y + 40, HERE / "s01-console-ladder.excalidraw", "build_s01_console_ladder.py")


if __name__ == "__main__":
    main()
