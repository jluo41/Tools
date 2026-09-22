/* NavRail — the left rail, Databricks-style, whose groups ARE the paradigm:
 *
 *   DATA     raw                    the record itself
 *   INSIGHT  internal/external/     signals inferred from data — none of them act
 *            model                  on the patient (a model score is an insight,
 *                                   "from group to individual")
 *   ACTION   checklist, annotate    things that act on the world and create new data
 *
 * Health sits in the footer: it is about the console, not the patient.
 *
 * Clicking an item OPENS it as a tab (VSCode-style) rather than replacing what is
 * there — open views are marked with a dot, the active one is highlighted.
 * Collapsible: expanded shows group headers + labels; collapsed keeps icons with
 * group dividers (the default inside a narrow HAI-Chat iframe embed).
 */
import type {ConsoleView} from '../types';
import {RAIL_GROUPS, VIEW_META} from '../views';

interface Props {
    active: ConsoleView | null;
    open: ConsoleView[];
    /** views HaiChat opened and the clinician has not looked at yet */
    agentOpened: ConsoleView[];
    onOpen: (v: ConsoleView) => void;
    /** alt/ctrl-click — open this view in a pane BESIDE the current one */
    onOpenToSide: (v: ConsoleView) => void;
    collapsed: boolean;
    onToggle: () => void;
}

export default function NavRail(props: Props) {
    const {active, open, agentOpened, onOpen, onOpenToSide, collapsed, onToggle} = props;

    const item = (v: ConsoleView, group: string) => {
        const m = VIEW_META[v];
        const byAgent = agentOpened.includes(v);
        return (
            <button
                key={v}
                className={
                    'nr-item' +
                    (v === active ? ' active' : '') +
                    (open.includes(v) ? ' open' : '') +
                    (byAgent ? ' by-agent' : '')
                }
                onClick={(e) => (e.altKey || e.ctrlKey || e.metaKey ? onOpenToSide(v) : onOpen(v))}
                title={byAgent
                    ? 'HaiChat opened this — click to read it'
                    : group + ' · ' + m.label + '   (alt-click: open at the side)'}
            >
                <span className='nr-icon'>{m.icon}</span>
                {!collapsed && <span className='nr-label'>{m.label}</span>}
                {byAgent && <span className='nr-bot'>{'🤖'}</span>}
                {open.includes(v) && v !== active && !byAgent && <span className='nr-dot'/>}
            </button>
        );
    };

    return (
        <nav className={'navrail' + (collapsed ? ' collapsed' : '')}>
            {RAIL_GROUPS.map((g) => (
                <div className='nr-group' key={g.title}>
                    {collapsed ? <div className='nr-divider'/> : <div className='nr-title'>{g.title}</div>}
                    {g.items.map((v) => item(v, g.title))}
                </div>
            ))}

            <div className='nr-foot'>
                {item('health', 'Console')}
                <button
                    className='nr-item'
                    onClick={onToggle}
                    title={collapsed ? 'Expand rail' : 'Collapse rail'}
                >
                    <span className='nr-icon'>{collapsed ? '⏵' : '⏴'}</span>
                    {!collapsed && <span className='nr-label'>{'Collapse'}</span>}
                </button>
            </div>
        </nav>
    );
}
