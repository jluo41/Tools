/* DockLayout — renders the dock tree, and owns the drag-to-dock gesture.
 *
 * Each leaf is a pane: a tab strip plus its views. While a tab is being dragged over
 * a pane, the pane shows WHERE it would land — a highlighted band on the edge you are
 * nearest (left/right/top/bottom = split that pane in that direction) or the whole
 * pane (centre = join its tabs). That preview is the whole point: you can see the
 * layout you are about to get before you let go.
 *
 * Splitters sit between siblings of a split node and resize by percentage, so the
 * layout keeps its proportions when the window changes.
 */
import {useState} from 'react';

import type {ConsoleView} from '../types';
import {type Dock, type GroupNode, type LayoutNode} from '../layout';

import Splitter from './Splitter';
import TabStrip from './TabStrip';

interface Props {
    node: LayoutNode;
    path: number[];                       // where this node sits in the tree
    focusedId: string | null;
    /** tabs HaiChat opened — passed straight through to the tab strips */
    agentOpened: ConsoleView[];
    render: (v: ConsoleView) => JSX.Element;
    onFocus: (groupId: string) => void;
    onActivate: (groupId: string, v: ConsoleView) => void;
    onClose: (groupId: string, v: ConsoleView) => void;
    onCloseOthers: (groupId: string, v: ConsoleView) => void;
    onSplit: (groupId: string, v: ConsoleView) => void;
    onDock: (groupId: string, v: ConsoleView, where: Dock) => void;
    onResize: (path: number[], i: number, deltaPct: number) => void;
}

/** which edge of the pane is the pointer nearest? (centre if it is well inside) */
function dockZone(e: React.DragEvent, el: HTMLElement): Dock {
    const r = el.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width;
    const y = (e.clientY - r.top) / r.height;
    const EDGE = 0.3;
    const d: [Dock, number][] = [
        ['left', x],
        ['right', 1 - x],
        ['top', y],
        ['bottom', 1 - y],
    ];
    const [where, dist] = d.sort((a, b) => a[1] - b[1])[0];
    return dist < EDGE ? where : 'center';
}

function Pane({g, ...p}: Props & {g: GroupNode}) {
    const [zone, setZone] = useState<Dock | null>(null);

    return (
        <div
            className={'group' + (p.focusedId === g.id ? ' focused' : '')}
            onMouseDown={() => p.onFocus(g.id)}
            onDragOver={(e) => {
                e.preventDefault();
                setZone(dockZone(e, e.currentTarget));
            }}
            onDragLeave={(e) => {
                if (!e.currentTarget.contains(e.relatedTarget as Node)) {
                    setZone(null);
                }
            }}
            onDrop={(e) => {
                e.preventDefault();
                const v = e.dataTransfer.getData('text/view') as ConsoleView;
                const where = zone ?? 'center';
                setZone(null);
                if (v) {
                    p.onDock(g.id, v, where);
                }
            }}
        >
            <TabStrip
                tabs={g.tabs}
                active={g.active}
                focused={p.focusedId === g.id}
                canSplit={g.tabs.length > 0}
                agentOpened={p.agentOpened}
                onSelect={(v) => p.onActivate(g.id, v)}
                onClose={(v) => p.onClose(g.id, v)}
                onCloseOthers={(v) => p.onCloseOthers(g.id, v)}
                onSplit={(v) => p.onSplit(g.id, v)}
                onDropTab={(v) => p.onDock(g.id, v, 'center')}
            />

            <div className='pane-body'>
                {g.tabs.length === 0 && (
                    <div className='view-scroll muted'>
                        {'Empty pane — pick a view from the rail, or drag a tab here.'}
                    </div>
                )}
                {/* every open view stays MOUNTED; only the active one shows */}
                {g.tabs.map((v) => (
                    <div key={v} className={'pane' + (v === g.active ? '' : ' hidden')}>
                        {p.render(v)}
                    </div>
                ))}

                {/* live preview of where the dragged tab would land */}
                {zone && <div className={'dockzone ' + zone}/>}
            </div>
        </div>
    );
}

export default function DockLayout(p: Props) {
    const {node, path} = p;

    if (node.kind === 'group') {
        return <Pane {...p} g={node}/>;
    }

    return (
        <div className={'split ' + node.dir}>
            {node.children.map((child, i) => (
                <div
                    key={child.kind === 'group' ? child.id : 'split' + i}
                    className='split-slot'
                    style={{flexBasis: node.sizes[i] + '%'}}
                >
                    <DockLayout {...p} node={child} path={[...path, i]}/>
                    {i < node.children.length - 1 && (
                        <Splitter
                            orientation={node.dir === 'row' ? 'vertical' : 'horizontal'}
                            onDrag={(px) => {
                                const span = node.dir === 'row'
                                    ? window.innerWidth
                                    : window.innerHeight;
                                p.onResize(path, i, (px / span) * 100);
                            }}
                        />
                    )}
                </div>
            ))}
        </div>
    );
}
