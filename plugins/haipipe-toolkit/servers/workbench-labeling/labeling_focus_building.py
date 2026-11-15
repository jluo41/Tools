"""An older labeling building Task's page: its views, its Runs and its rail."""
from __future__ import annotations

from live import decision_report_view as DR, focus_page as F, frame, labeling_theme as T
from live import task_labeling as TL

from live.labeling_focus_read import ASSETS, BUILD_VIEWS, NEXT_WORDS, OLD_BUILD
from live.labeling_focus_frame import task_frame


def is_building(folder) -> bool:
    """A building Task: its face says `task-type: labeling-building` (one type, not today's labeling Page)."""
    return frame.level_of(folder) == "Task" and T.types_of(folder) == ("building",)


def building_runs(folder, root) -> str:
    """Runs: the Task's Runs, newest first, each its type, its state and its record; no Run's output."""
    rows = []
    for row in reversed(frame.runs_of(folder)):
        p = row["path"]
        if not F.inside(p, root):
            continue
        card = p / "run.yaml" if p.is_dir() else p
        state = TL._status(p) if p.is_dir() else row["status"]
        rows.append(f'<div class="dec-run"><span class="n">{frame.esc(row["run"])}</span>'
                    f'<span class="d">{frame.esc(row["type"])}</span><span class="w">{frame.esc(state)}</span>'
                    + (frame.pop(frame._file_url(card, root), row["run"], "Open").replace("<a ", '<a class="dec-btn" ', 1)
                       if card.is_file() and F.inside(card, root) else "") + "</div>")
    return DR.section(1, BUILD_VIEWS[-1][3], "".join(rows) or DR.line("No Runs yet."),
                      word=f"{len(rows)} Run{'' if len(rows) == 1 else 's'}" if rows else "nothing yet")


def building_view(folder, root, section, key) -> str:
    """One view of a building Task: Decide (decision_report_view), Runs, or a step not built yet, said so; in Work
    the step after it last (Report is read only, its Results only)."""
    _, name, caption, first, after = next(v for v in BUILD_VIEWS if v[0] == key)
    report = section == "report"
    if key == "decide":
        # one Report holds the step now: the form while a report waits for the person, its answers read only after
        body = DR.decide_view(folder, root, read_only=report or not DR.waiting_report(folder))
    elif key == "runs":
        body = DR.wrap(building_runs(folder, root))
    else:                                         # honest: what the view will show, no number made up
        body = DR.wrap(DR.section(1, first, DR.big("Nothing to show yet") + DR.line(f"This view will show {caption}."),
                                    word="not built yet"))
    if after:                                     # Work retired (JL 261111): the next step on the one Report view, no caption
        body += DR.wrap(DR.next_link(F.page_url(folder, root, "report", after), NEXT_WORDS[after]))
    return body


def building_page(theme, root, folder, section="", group=""):
    """A building Task's focus page: Frame · Decide · Changes · Staging · Release · Runs · Delivery on the shared
    frame (building_view)."""
    views = {key: name for key, name, *_ in BUILD_VIEWS}
    return task_frame(theme, root, folder, section, group, views,
                      lambda: "decide" if DR.waiting_report(folder) else "frame",
                      lambda view: building_view(folder, root, "work", view), old=OLD_BUILD,
                      head_extra="<style>" + (ASSETS / "decision_report.css").read_text(encoding="utf-8") + "</style>",
                      tail_extra="<script>" + (ASSETS / "decision_report.js").read_text(encoding="utf-8") + "</script>")
