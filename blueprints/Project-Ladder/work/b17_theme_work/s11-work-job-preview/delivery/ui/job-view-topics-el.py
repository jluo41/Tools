"""Run: python3 job-view-topics-el.py <the Tools folder> > job-view-topics-el.js. The real page's element menu
(page/element_marks/element_info.py: its STYLE and SCRIPT, copied as they are) for the s11 preview; right-click a part
shows its kind and Info, Comment and Copy address. The kinds name the preview's own selectors; a static file keeps no
comment, so Comment opens the Info card."""
import json, re, sys
from pathlib import Path
src = (Path(sys.argv[1]) / "plugins/haipipe-toolkit/servers/workbench/page/element_marks/element_info.py").read_text()
style = re.search(r'STYLE = """(.*?)"""', src, re.S).group(1)
script = re.search(r'SCRIPT = """(.*?)"""', src, re.S).group(1).replace("\\\\", "\\")
kinds = [["title", "h1", "focus_shell.page_shell"],
         ["view-button-list", "#rows [data-row]", "focus_jobs.section / job_pane"],
         ["band", "#body h2", "focus_render.around_work / work_frame"],
         ["fold", "details.band-sec", "work_frame.section / focus_plan_results.numbered"],
         ["job-row", "details.job-row", "focus_plan_results.tasks_section"]]
data = {"kinds": kinds, "slots": {}, "empty": "", "page": "blueprints/Project-Ladder/work/b17_theme_work"}
# the real page resets every button in focus.css; the preview has no such reset, so its menu gets it here
style_css = re.sub(r"</?style>", "", style) + ".el-pop button{border:0;background:none;font:inherit;color:inherit;cursor:pointer}.el-menu button:hover{background:var(--soft)}"
script_js = re.sub(r"</?script>", "", script)
print("document.head.insertAdjacentHTML('beforeend', " + json.dumps("<style>" + style_css + "</style>") + ");")
print("window.__elInfo = " + json.dumps(data, ensure_ascii=False) + ";")
print("document.addEventListener('DOMContentLoaded', function(){" + script_js + "});")
