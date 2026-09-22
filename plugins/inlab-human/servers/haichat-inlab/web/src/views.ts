/* views — the single registry of what a view IS.
 *
 * The rail (where you open views from) and the tab strip (what you have open)
 * must agree on every icon and label, so both read this and neither owns it.
 * Groups are the paradigm: DATA → INSIGHT → ACTION, plus the console's own Health.
 */
import type {ConsoleView} from './types';

export interface ViewMeta {
    icon: string;
    label: string;
    group: 'Data' | 'Insight' | 'Action' | 'Console';
}

export const VIEW_META: Record<ConsoleView, ViewMeta> = {
    // DATA — the same dataset at successive stages of the pipeline
    raw: {icon: '📄', label: 'Raw', group: 'Data'},
    source: {icon: '🗂️', label: 'Source', group: 'Data'},
    record: {icon: '🧾', label: 'Record', group: 'Data'},
    case: {icon: '📌', label: 'Case', group: 'Data'},

    internal: {icon: '🧬', label: 'Internal', group: 'Insight'},
    external: {icon: '🌐', label: 'External', group: 'Insight'},
    model: {icon: '🧠', label: 'Model', group: 'Insight'},
    tasks: {icon: '📋', label: 'Tasks', group: 'Insight'},
    checklist: {icon: '✅', label: 'Checklist', group: 'Action'},
    annotate: {icon: '✏️', label: 'Annotate', group: 'Action'},
    health: {icon: '❤️', label: 'Health', group: 'Console'},
};

/** what each DATA view is, in one line — shown as the view's own banner */
export const LAYER_BLURB: Record<'raw' | 'source' | 'record' | 'case', {store: string; what: string}> = {
    raw: {
        store: '0-RawDataStore',
        what: 'the files exactly as they arrived — nothing parsed yet',
    },
    source: {
        store: '1-SourceStore',
        what: 'SourceFn → ProcName_to_ProcDf: the raw files parsed into tables. This is the layer a payload is built from.',
    },
    record: {
        store: '2-RecStore',
        what: 'RecordFn → cleaned, PID-keyed, binned to a 5-min grid. This is what the trigger and the case pipeline read.',
    },
    case: {
        store: '3-CaseStore',
        what: 'one case = one annotation/prediction point cut from one human\'s record — the unit a label or a score attaches to.',
    },
};

/** rail order — Health is rendered separately, in the rail's footer */
export const RAIL_GROUPS: {title: ViewMeta['group']; items: ConsoleView[]}[] = [
    {title: 'Data', items: ['raw', 'source', 'record', 'case']},
    {title: 'Insight', items: ['internal', 'external', 'model', 'tasks']},
    {title: 'Action', items: ['checklist', 'annotate']},
];
