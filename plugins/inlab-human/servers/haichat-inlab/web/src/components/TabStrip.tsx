/* TabStrip — one editor group's open views, VSCode-style.
 *
 * The rail OPENS a view; the strip is what is open in THIS group. Tabs coexist:
 * switching between them does not tear the previous one down (Console keeps every
 * open view mounted and hides the inactive ones).
 *
 * Side-by-side: ⫿ splits the active tab into a second group, and a tab can be
 * DRAGGED onto another group to move it there. Close with ✕ or a middle-click.
 */
import {useState} from 'react';

import type {ConsoleView} from '../types';
import {VIEW_META} from '../views';

interface Props {
    tabs: ConsoleView[];
    active: ConsoleView | null;
    focused: boolean;
    canSplit: boolean;
    /** tabs HaiChat opened — badged 🤖 until the clinician clicks one, so a tab that
     *  appeared under their hands is never mistaken for one they opened themselves */
    agentOpened: ConsoleView[];
    onSelect: (v: ConsoleView) => void;
    onClose: (v: ConsoleView) => void;
    onCloseOthers: (v: ConsoleView) => void;
    onSplit: (v: ConsoleView) => void;
    /** a tab was dropped on this group (it may come from the other group) */
    onDropTab: (v: ConsoleView) => void;
}

export default function TabStrip(props: Props) {
    const {tabs, active, focused, canSplit, agentOpened,
        onSelect, onClose, onCloseOthers, onSplit, onDropTab} = props;
    const [dragOver, setDragOver] = useState(false);

    return (
        <div
            className={'tabstrip' + (focused ? ' focused' : '') + (dragOver ? ' dragover' : '')}
            onDragOver={(e) => {
                e.preventDefault();
                setDragOver(true);
            }}
            onDragLeave={() => setDragOver(false)}
            onDrop={(e) => {
                e.preventDefault();
                setDragOver(false);
                const v = e.dataTransfer.getData('text/view') as ConsoleView;
                if (v) {
                    onDropTab(v);
                }
            }}
        >
            {tabs.map((v) => {
                const m = VIEW_META[v];
                const byAgent = agentOpened.includes(v);
                return (
                    <div
                        key={v}
                        className={'tab' + (v === active ? ' active' : '') + (byAgent ? ' by-agent' : '')}
                        draggable={true}
                        onDragStart={(e) => e.dataTransfer.setData('text/view', v)}
                        onClick={() => onSelect(v)}
                        onAuxClick={(e) => {
                            if (e.button === 1) {
                                e.preventDefault();
                                onClose(v);
                            }
                        }}
                        onDoubleClick={() => onCloseOthers(v)}
                        title={byAgent
                            ? 'HaiChat opened this'
                            : m.group + ' · ' + m.label + '  (drag to the other side · middle-click to close)'}
                    >
                        {byAgent && <span className='tab-bot'>{'🤖'}</span>}
                        <span className='tab-icon'>{m.icon}</span>
                        <span className='tab-label'>{m.label}</span>
                        <button
                            className='tab-close'
                            title='Close'
                            onClick={(e) => {
                                e.stopPropagation();
                                onClose(v);
                            }}
                        >
                            {'✕'}
                        </button>
                    </div>
                );
            })}

            <span className='tabstrip-space'/>

            {canSplit && (
                <button
                    className='tab-action'
                    title={active
                        ? 'Split — put “' + VIEW_META[active].label + '” in a pane beside this one'
                        : 'Split — open a second pane'}
                    onClick={() => active && onSplit(active)}
                >
                    {'◫ Split'}
                </button>
            )}
        </div>
    );
}
