/* actions — the one vocabulary the console understands.
 *
 * The console has TWO drivers now: the clinician's hands and HaiChat. The whole
 * safety story rests on them not having two code paths:
 *
 *      rail click ─┐                            ┌─ mcp__console__open_view
 *                  ├──► ConsoleAction ──► dispatch(action, origin) ──► state
 *   HaiChat tool ──┘                            └─ (layout.ts pure ops, useConsole)
 *
 * A rail click and an agent tool call produce the SAME action object and land in
 * the SAME reducer. There is no agent-only mutation to audit, no second way to
 * open a tab, and — critically — no second way to produce a score: `run/start`
 * is the ▶ Run button, whoever pressed it.
 *
 * Every action carries an `origin`, which is how the UI can badge what the agent
 * did (🤖) and how the agent is stopped from reading its own tab-opens back as if
 * the clinician had done them.
 */
import type {ConsoleView, NavView, Origin, SortDir} from './types';
import {VIEW_META} from './views';

export type ConsoleAction =
    /* a pure read — the agent asking "what does she have on screen?". Changes nothing;
     * the reply carries the snapshot every ui_result carries anyway. */
    | {type: 'state/read'}

    /* layout — free for the agent (reversible, read-only, cosmetic) */
    | {type: 'view/open'; view: ConsoleView; where?: 'here' | 'side'}
    | {type: 'view/focus'; view: ConsoleView}
    | {type: 'view/close'; view: ConsoleView}

    /* panel navigation — which table, which sort, which sub-tab */
    | {type: 'panel/set'; view: NavView; table?: string; sort?: {col: string; dir: SortDir} | null;
        file?: string; tab?: 'card' | 'run' | 'message'; openRun?: number | null}

    /* pointing — "look at this row / this window" */
    | {type: 'highlight/set'; view: ConsoleView; table?: string | null; row?: number | null;
        from?: string | null; to?: string | null; note?: string | null}
    | {type: 'highlight/clear'}

    /* consequential — each of these raises an Allow/Deny card when the agent asks */
    | {type: 'patient/select'; patient_id: string}
    | {type: 'model/select'; package: string}
    | {type: 'run/start'; patient_id?: string; package?: string}
    | {type: 'checklist/generate'}
    | {type: 'checklist/toggle'; index: number};

/** What an action DID, in the clinician's words — for the transcript, the 🤖 chip,
 *  and the awareness feed the agent reads. One sentence, no jargon, no ids. */
export function describe(a: ConsoleAction): string {
    const label = (v: ConsoleView) => VIEW_META[v]?.label ?? v;
    switch (a.type) {
    case 'state/read':
        return 'looked at the console';
    case 'view/open':
        return 'opened ' + label(a.view) + (a.where === 'side' ? ' beside it' : '');
    case 'view/focus':
        return 'switched to ' + label(a.view);
    case 'view/close':
        return 'closed ' + label(a.view);
    case 'panel/set':
        if (a.table) {
            return 'opened the ' + a.table + ' table in ' + label(a.view as ConsoleView);
        }
        if (a.file) {
            return 'opened the file ' + a.file;
        }
        if (a.tab) {
            return 'switched the Model tab to ' + (a.tab === 'card' ? 'the model card' : 'Run');
        }
        if (a.sort) {
            return 'sorted by ' + a.sort.col + ' (' + a.sort.dir + ')';
        }
        if (a.openRun !== undefined && a.openRun !== null) {
            return 'opened run #' + a.openRun;
        }
        return 'changed the ' + label(a.view as ConsoleView) + ' panel';
    case 'highlight/set':
        return 'pointed at ' + (a.row ? 'row ' + a.row : a.from ? a.from + '…' + (a.to ?? '') : 'something') +
            ' in ' + label(a.view);
    case 'highlight/clear':
        return 'cleared the highlight';
    case 'patient/select':
        return 'switched to patient ' + a.patient_id;
    case 'model/select':
        return 'selected the model ' + a.package;
    case 'run/start':
        return 'ran a prediction';
    case 'checklist/generate':
        return 'generated the checklist';
    case 'checklist/toggle':
        return 'ticked checklist item ' + (a.index + 1);
    default:
        return 'changed the console';
    }
}

/** Actions HaiChat may take WITHOUT an Allow/Deny card.
 *
 * The line is not "harmless" — it is: **read-only, instantly reversible, and with
 * no consequence outside this browser tab**. Opening a tab moves nobody's care;
 * running a model hits a real endpoint and produces a clinical number.
 *
 * `model/select` is deliberately NOT here: a silent swap means the clinician then
 * presses ▶ Run and scores a different model than the one they believe they chose.
 * `view/close` is not here either — it destroys a pane the clinician may be reading.
 *
 * The server enforces this list too (haichat_api.ALLOWED_UI_AUTO); this copy exists
 * so the UI can label an action as agent-driven before the server answers. If the
 * two ever disagree, the SERVER wins — it is the one holding the gate. */
export const AGENT_AUTO: ConsoleAction['type'][] = [
    'state/read', 'view/open', 'view/focus', 'panel/set', 'highlight/set', 'highlight/clear',
];

export const isAutoAllowed = (a: ConsoleAction): boolean =>
    AGENT_AUTO.includes(a.type);

/** The result of applying an action — what the agent gets back, and what the
 *  transcript shows. `ok:false` is a normal outcome (a denied run, a patient with
 *  no scoreable endpoint), not an exception. */
export interface ActionResult {
    ok: boolean;
    error?: string;
    /** run/start returns the run it produced, verbatim from the endpoint */
    run?: unknown;
    checklist?: unknown;
}

export type Dispatch = (a: ConsoleAction, origin: Origin) => Promise<ActionResult>;
