"""The family's Workbench Table: its rows, the HTML table, and the Guide Space's Runs panel."""

from live.guide_core import REPOSITORY, VIEWS, esc

TABLE_COLUMNS = ("Space", "View", "Run type", "Agent", "Skill")
TABLE_HEAD = ("Space", "View", "Run type", "Agent · Skill")


def table_rows(profile):
    """The family's Workbench Table rows, or [] when it declares none or the file has none."""
    if not profile.get("table"):
        return []
    import importlib.util
    reader = REPOSITORY / "plugins/haipipe-toolkit/skills/0_utils/table-workbench/ref/render_workbench_table.py"
    try:
        spec = importlib.util.spec_from_file_location("render_workbench_table", reader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.read_table(REPOSITORY / profile["table"])
    except (OSError, SystemExit):
        return []


def workbench_table(profile):
    """The family's Workbench Table (skills/0_utils/table-workbench) as one HTML table: Space ·
    View · Run type · Agent · Skill (one column: the agent, the skill under it), and Folder when the
    table has it (where the run writes); a repeated Space or View cell is merged into the first.
    Empty when the family declares no `table` or the file has no Workbench Table."""
    rows = table_rows(profile)
    if not rows:
        return ""

    def cell(value):
        planned = value.endswith(" (new)")
        name = value.removesuffix(" (new)")
        if name in ("", "none"):
            return '<span class="wg-none">—</span>'
        return f'<code>{esc(name)}</code>' + (' <span class="wg-planned">planned</span>' if planned else '')

    def span(i, key):
        n = 1
        while i + n < len(rows) and all(rows[i + n][k] == rows[i][k] for k in TABLE_COLUMNS[:TABLE_COLUMNS.index(key) + 1]):
            n += 1
        return n

    folder = bool(rows) and "Folder" in rows[0]
    body = []
    for i, row in enumerate(rows):
        tds = []
        for key in ("Space", "View"):
            first = i == 0 or any(rows[i - 1][k] != row[k] for k in TABLE_COLUMNS[:TABLE_COLUMNS.index(key) + 1])
            if first:
                tds.append(f'<th scope="rowgroup" rowspan="{span(i, key)}">{esc(row[key])}</th>')
        run = row["Run type"]
        tds.append(f'<td>{esc(run) if run != "none" else "<span class=wg-none>—</span>"}</td>')
        pair = (f'<span class="wg-agent">{cell(row["Agent"])}</span><span class="wg-skill">{cell(row["Skill"])}</span>'
                if row["Agent"] != "none" or row["Skill"] != "none" else cell("none"))
        tds.append(f'<td>{pair}</td>')
        if folder:
            tds.append(f'<td>{cell(row["Folder"])}</td>')
        body.append("<tr>" + "".join(tds) + "</tr>")
    head = "".join(f"<th>{c}</th>" for c in TABLE_HEAD + (("Folder",) if folder else ()))
    # a closed card like the drawings beside it, its name only (JL 261003: "make it into this
    # style", "remove this, we don't need this")
    return ('<details class="wg-drawing" data-drawing="workbench-table"><summary><span><strong>Workbench Table</strong>'
            '</span></summary><div class="wg-drawing-body">'
            f'<div class="wg-table"><table><thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table></div></div></details>')


def guide_runs(profile, view):
    """Guide's Runs panel: the family's Workbench Table rows on the Guide Space, those of the
    open View first (JL 261003: "always put the run in the right panel"). Each run type gives
    its agent, skill and a prompt to copy; Guide keeps no run records, so none are listed."""
    rows = [r for r in table_rows(profile) if r["Space"] == "Guide" and r["Run type"] not in ("", "none")]
    if not rows:
        return ""
    from live.runs_panel import PANEL_CSS, PANEL_JS, SPLIT_CSS, panel_markup
    label = dict((key, name) for key, name, _ in VIEWS)[view]
    rows = [r for r in rows if r["View"] == label] or rows
    plain = lambda value: value.replace(" (new)", " (planned)")
    kinds = [{"label": r["Run type"], "pattern": "", "views": "",
              "skills": [r["Skill"].replace(" (new)", "")] if r["Skill"] not in ("", "none") else [],
              "prompt": (f'Run with {plain(r["Agent"])}. {r["Run type"]} for the {profile["label"]} workbench, '
                         f'Guide › {r["View"]}, following {plain(r["Skill"])}.'
                         + (f' The person signs {r["Person signs"]}.' if r.get("Person signs") not in ("", "none", None) else ""))}
             for r in rows]
    panel = panel_markup("guide", kinds, [[] for _ in kinds], base=REPOSITORY, fill=lambda row: {},
                         whole=f'the {profile["label"]} Guide')
    css = (".wg-split{--line:var(--wg-rule);--card:var(--wg-bg);--acc:var(--wg-blue);--fg:var(--wg-ink);--mut:var(--wg-muted)}"
           + PANEL_CSS + SPLIT_CSS)
    return f'<style>{css}</style>{panel}<script>{PANEL_JS}</script>'
