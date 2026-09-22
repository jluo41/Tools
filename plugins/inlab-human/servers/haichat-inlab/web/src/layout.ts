/* layout — a recursive dock tree, and the pure operations on it.
 *
 * Two panes side by side was too rigid. This is the VSCode / Golden-Layout model:
 *
 *   split(row)
 *   ├── group A            drag a tab onto the LEFT / RIGHT / TOP / BOTTOM edge of any
 *   └── split(col)         pane and it docks there, splitting that pane in that
 *       ├── group B        direction; drop it in the CENTRE and it joins that pane's
 *       └── group C        tabs. Panes nest arbitrarily, in both directions.
 *
 * Everything here is a PURE function over the tree: the console holds one `LayoutNode`
 * in state and swaps it for the result. Empty groups are pruned and single-child splits
 * collapse, so the tree can never rot into invisible junk.
 */
import type {ConsoleView} from './types';

export interface GroupNode {
    kind: 'group';
    id: string;
    tabs: ConsoleView[];
    active: ConsoleView | null;
}

export interface SplitNode {
    kind: 'split';
    dir: 'row' | 'col';       // row = side by side, col = stacked
    sizes: number[];          // percentages, one per child, summing to 100
    children: LayoutNode[];
}

export type LayoutNode = GroupNode | SplitNode;

/** where a dragged tab lands relative to the pane it is dropped on */
export type Dock = 'center' | 'left' | 'right' | 'top' | 'bottom';

let seq = 0;
export const newGroupId = () => `g${++seq}`;

export const group = (tabs: ConsoleView[], active?: ConsoleView | null): GroupNode => ({
    kind: 'group',
    id: newGroupId(),
    tabs,
    active: active ?? tabs[tabs.length - 1] ?? null,
});

/* ── reads ────────────────────────────────────────────────────────────────── */

export function groups(node: LayoutNode): GroupNode[] {
    return node.kind === 'group' ? [node] : node.children.flatMap(groups);
}

export function allTabs(node: LayoutNode): ConsoleView[] {
    return groups(node).flatMap((g) => g.tabs);
}

export function groupOfView(node: LayoutNode, v: ConsoleView): GroupNode | null {
    return groups(node).find((g) => g.tabs.includes(v)) ?? null;
}

/* ── writes (all pure) ────────────────────────────────────────────────────── */

function mapGroups(node: LayoutNode, f: (g: GroupNode) => GroupNode): LayoutNode {
    if (node.kind === 'group') {
        return f(node);
    }
    return {...node, children: node.children.map((c) => mapGroups(c, f))};
}

/** drop empty groups; collapse a split that has one child left; flatten same-dir nesting */
export function prune(node: LayoutNode): LayoutNode | null {
    if (node.kind === 'group') {
        return node.tabs.length ? node : null;
    }
    const kept: LayoutNode[] = [];
    const sizes: number[] = [];
    node.children.forEach((c, i) => {
        const p = prune(c);
        if (p) {
            kept.push(p);
            sizes.push(node.sizes[i] ?? 100 / node.children.length);
        }
    });
    if (kept.length === 0) {
        return null;
    }
    if (kept.length === 1) {
        return kept[0];                      // a split with one child is just that child
    }
    const total = sizes.reduce((a, b) => a + b, 0) || 1;
    return {...node, children: kept, sizes: sizes.map((s) => (100 * s) / total)};
}

/** remove a view from wherever it lives (used before re-docking it) */
export function removeView(node: LayoutNode, v: ConsoleView): LayoutNode | null {
    return prune(mapGroups(node, (g) => {
        if (!g.tabs.includes(v)) {
            return g;
        }
        const tabs = g.tabs.filter((x) => x !== v);
        const i = g.tabs.indexOf(v);
        return {...g, tabs, active: g.active === v ? (tabs[Math.max(0, i - 1)] ?? null) : g.active};
    }));
}

/** add a view to a group's tab list and focus it */
export function addToGroup(node: LayoutNode, groupId: string, v: ConsoleView): LayoutNode {
    return mapGroups(node, (g) =>
        (g.id === groupId ? {...g, tabs: [...g.tabs, v], active: v} : g));
}

/** replace the group `groupId` with a split holding it and a NEW group carrying `v` */
function splitAt(node: LayoutNode, groupId: string, v: ConsoleView, dock: Dock): LayoutNode {
    const dir: 'row' | 'col' = dock === 'left' || dock === 'right' ? 'row' : 'col';
    const before = dock === 'left' || dock === 'top';

    const replace = (n: LayoutNode): LayoutNode => {
        if (n.kind === 'group') {
            if (n.id !== groupId) {
                return n;
            }
            const fresh = group([v]);
            return {
                kind: 'split',
                dir,
                sizes: [50, 50],
                children: before ? [fresh, n] : [n, fresh],
            };
        }
        return {...n, children: n.children.map(replace)};
    };
    return replace(node);
}

/** the one entry point the UI needs: dock `v` onto `groupId` at `dock` */
export function dock(root: LayoutNode, groupId: string, v: ConsoleView, where: Dock): LayoutNode {
    const target = groups(root).find((g) => g.id === groupId);
    // dropping a lone tab back onto its own pane is a no-op, not a self-destruct
    if (target && target.tabs.length === 1 && target.tabs[0] === v && where !== 'center') {
        return root;
    }
    const without = removeView(root, v);
    if (!without) {
        return group([v]);                    // it was the only view anywhere
    }
    // the target may have been pruned away when v left it
    const stillThere = groups(without).some((g) => g.id === groupId);
    const anchor = stillThere ? groupId : groups(without)[0].id;
    return where === 'center'
        ? addToGroup(without, anchor, v)
        : splitAt(without, anchor, v, where);
}

/** focus a view where it already is, or open it in `groupId` */
export function focusOrOpen(root: LayoutNode, groupId: string, v: ConsoleView): LayoutNode {
    const at = groupOfView(root, v);
    if (at) {
        return mapGroups(root, (g) => (g.id === at.id ? {...g, active: v} : g));
    }
    return addToGroup(root, groupId, v);
}

export function activate(root: LayoutNode, groupId: string, v: ConsoleView): LayoutNode {
    return mapGroups(root, (g) => (g.id === groupId ? {...g, active: v} : g));
}

export function closeTab(root: LayoutNode, groupId: string, v: ConsoleView): LayoutNode {
    const next = prune(mapGroups(root, (g) => {
        if (g.id !== groupId) {
            return g;
        }
        const tabs = g.tabs.filter((x) => x !== v);
        const i = g.tabs.indexOf(v);
        return {...g, tabs, active: g.active === v ? (tabs[Math.max(0, i - 1)] ?? null) : g.active};
    }));
    return next ?? group([]);                 // last tab closed -> one empty pane
}

/** resize: nudge the boundary between children i and i+1 of the split at `path` */
export function resize(root: LayoutNode, path: number[], i: number, deltaPct: number): LayoutNode {
    const walk = (n: LayoutNode, p: number[]): LayoutNode => {
        if (n.kind !== 'split') {
            return n;
        }
        if (p.length === 0) {
            const sizes = [...n.sizes];
            const a = sizes[i] + deltaPct;
            const b = sizes[i + 1] - deltaPct;
            if (a < 10 || b < 10) {
                return n;                     // never let a pane collapse to nothing
            }
            sizes[i] = a;
            sizes[i + 1] = b;
            return {...n, sizes};
        }
        const [head, ...rest] = p;
        return {...n, children: n.children.map((c, j) => (j === head ? walk(c, rest) : c))};
    };
    return walk(root, path);
}
