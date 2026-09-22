/* Types mirroring the endpoint-predict engine's tool schemas.
 * Keep in sync with Tools/plugins/inlab-human/mcp-servers/endpoint-predict/server.py
 *
 * Console-only: nothing here knows about chat, agents, or WebSockets.
 */

export interface PatientSummary {
    birth_date: string | null;
    sex: string | null;
    race: string | null;
    table_counts: Record<string, number>;
    /** the cohort a store may name explicitly (the CGM store does) */
    cohort?: string;
    /** full-precision prediction trigger (index_date is truncated to the day) */
    anchor?: string | null;
    /** set when NO endpoint can score this patient — say so instead of offering ▶ Run */
    not_scoreable_reason?: string | null;
}

export interface PatientListItem {
    patient_id: string;
    summary: PatientSummary;
    seen_by: string[];
}

export interface PatientDetail {
    patient_id: string;
    summary: PatientSummary;
    /** the prediction trigger date — the chart is rendered AS OF this moment */
    index_date: string | null;
    /** age at index_date, NOT today */
    age_at_index: number | null;
    /** rows dated after index_date that were withheld (they are the future) */
    post_index_rows_hidden: number;
    row_cap: number;
    source_tables: Record<string, Record<string, unknown>[]>;
}

export interface ModelInfo {
    package: string;
    endpoint_name: string | null;
    endpoint_version: string | null;
    models_field: string | null;
    required_tables: string[];
    endpoint_url: string | null;
    live: boolean;
}

/** The model card — assembled from the package's own files (see /api/models/{pkg}/card). */
export interface ModelCardData {
    package: string;
    endpoint_name: string;
    endpoint_version: string;
    endpoint_url: string | null;
    created_at?: string;
    deployment?: Record<string, unknown>;
    prediction: {
        type?: string;
        unit?: string;
        /** 'forecast' = autoregressive rollout; anything else = teacher-forced eval path */
        mode?: string;
        horizon_steps?: number;
        context_steps?: number;
        interval_minutes?: number;
    };
    training: {
        modelinstance?: string;
        aidata?: string;
        tuner?: string;
        base_model?: string;
        max_seq_length?: number;
        value_range?: number[];
        learning_rate?: number;
        architecture?: Record<string, unknown>;
    };
    case: {
        casefns?: string[];
        obs_dt_index?: number;
        trigger?: string;
        min_segment_length?: number;
        max_consecutive_missing?: number;
        stride?: number;
        patient_registry?: string;
    };
    payload: {
        style?: string;
        models_field?: string;
        required_tables?: string[];
        optional_tables?: string[];
        input_schema?: unknown;
    };
    inference_functions: Record<string, string>;
}

export interface Gaps {
    missing_tables: string[];
    empty_tables: string[];
    unused_patient_tables: string[];
}

export interface PredictResult {
    patient_id: string;
    model: ModelInfo;
    endpoint_url: string;
    trigger: {record: Record<string, unknown>; source: string};
    gaps: Gaps;
    response: {
        models: {
            name: string;
            version: string;
            date: string;
            predictions: Record<string, unknown>[];
        }[];
        status?: {code: number; message: string};
    };
}

/** A CGM endpoint answers with a trajectory, not a score: models[0].forecast is a
 *  list of mg/dL values on a 5-minute grid. In forecast mode it also returns the
 *  context it was given and the values that were actually observed over the same
 *  horizon — a forecast is only readable next to what happened.
 *  Returns null for classifier endpoints. */
export function extractForecast(r: PredictResult): {
    values: number[];
    observed: number[] | null;
    context: number[] | null;
    unit: string;
    stepMin: number;
    mode: string | null;
    metrics: {mae?: number; rmse?: number} | null;
} | null {
    const m = (r.response?.models?.[0] ?? {}) as Record<string, unknown>;
    const f = m.forecast;
    if (!Array.isArray(f) || f.length === 0 || typeof f[0] !== 'number') {
        return null;
    }
    const meta = (m.metadata ?? {}) as Record<string, unknown>;
    const num = (v: unknown) => (Array.isArray(v) && v.length ? (v as number[]) : null);
    return {
        values: f as number[],
        observed: num(m.observed),
        context: num(m.context),
        unit: (meta.unit as string) ?? 'mg/dL',
        stepMin: (meta.intervalMinutes as number) ?? 5,
        mode: (meta.inferenceMode as string) ?? null,
        metrics: (m.metrics as {mae?: number; rmse?: number}) ?? null,
    };
}

/** Pull the score + band out of an endpoint response, whatever the model names it. */
export function extractScore(r: PredictResult): {score: number | null; band: string | null} {
    const pred = r.response?.models?.[0]?.predictions?.[0];
    if (!pred) {
        return {score: null, band: null};
    }
    const key = Object.keys(pred).find((k) => k.toLowerCase().includes('score'));
    const score = key ? Number(pred[key]) : null;
    const band = (pred.risk_level as string) ?? null;
    return {score, band};
}

/** Which cohort a patient id belongs to — used for grouping in pickers/cards.
 *  A store may carry the cohort explicitly (the CGM store does); fall back to the
 *  id prefix, which is how the REACH store encodes it. */
export function cohortOf(patientId: string, summary?: Partial<PatientSummary>): string {
    const named = (summary as {cohort?: string} | undefined)?.cohort;
    if (named) {
        return named;
    }
    if (patientId.startsWith('reach-1')) {
        return 'ADHD';
    }
    if (patientId.startsWith('reach-2')) {
        return 'PD2D';
    }
    if (patientId.startsWith('ohio-')) {
        return 'OhioT1DM';
    }
    if (patientId.startsWith('CGMacros')) {
        return 'CGMacros';
    }
    return 'MIMIC';
}

/* ── console shell ────────────────────────────────────────────────────────── */

/** The views the nav rail switches between, grouped by the lab's paradigm:
 *  DATA (raw → source → record → case) → INSIGHT (internal / external / model)
 *  → ACTION (checklist, annotate).
 *
 *  The DATA views are the same dataset at successive stages of the pipeline, so a
 *  reader can watch it being transformed on its way to the model. Case is the last
 *  cut: one case = one annotation/prediction point sliced from one human's record. */
export type ConsoleView =
    | 'raw' | 'source' | 'record' | 'case'
    | 'internal' | 'external' | 'model' | 'tasks'
    | 'checklist' | 'annotate' | 'health';

/* ── data layers ──────────────────────────────────────────────────────────── */

/** 0-RawDataStore: the files exactly as they arrived. */
export interface RawFilesLayer {
    patient_id: string;
    layer: 'raw';
    available: true;
    files: {name: string; bytes: number; preview: string}[];
}

/** 2-RecStore: RecordFn output — cleaned, PID-keyed, binned to a 5-min grid. */
export interface RecordLayer {
    patient_id: string;
    layer: 'record';
    available: true;
    tables: Record<string, RawTable & {capped?: boolean}>;
}

export interface LayerUnavailable {
    patient_id: string;
    layer: string;
    available: false;
    reason: string;
}

/* ── checklist (ACTION) ───────────────────────────────────────────────────── */

/** One actionable item generated from the record + insights. Important AND doable:
 *  every item names a concrete next step, who does it, and the fact that prompted it. */
export interface ChecklistItem {
    title: string;
    why: string;
    priority: 'high' | 'medium' | 'low';
    category: 'data-gap' | 'verify' | 'monitor' | 'discuss' | 'follow-up';
    owner: 'clinician' | 'patient' | 'data-team';
    effort: string;
}

export interface Checklist {
    patient_id: string;
    generated_at: string;
    items: ChecklistItem[];
    caveats: string[];
    /** context the generator was given — so the reader can audit what it saw */
    basis: {index_date: string | null; model: string | null; score: number | null;
        band: string | null; empty_tables: string[]; missing_tables: string[]};
}

/** One ▶ Run, kept client-side so the Model view shows a Databricks-Jobs-style
 *  run history instead of a single transient score.
 *
 *  `origin` is not decoration: HaiChat can press Run itself, and a score whose
 *  author the reader cannot see is exactly what this console exists to prevent. */
export interface RunRecord {
    id: number;
    at: string; // locale time string, display-only
    patient_id: string;
    model_pkg: string;
    model_label: string;
    status: 'ok' | 'error';
    score: number | null;
    band: string | null;
    result: PredictResult | null;
    error: string | null;
    origin: Origin;
}

/* ── two drivers ──────────────────────────────────────────────────────────────
 *
 * The clinician and HaiChat drive the SAME console. Every state change is tagged
 * with who caused it, so (a) the UI can badge what the agent did, and (b) the
 * agent is never told its own actions back as if the clinician had done them.
 */

export type Origin = 'user' | 'agent';

export type SortDir = 'asc' | 'desc';

/** Panel-level navigation: the part of a panel a SECOND driver needs to reach.
 *
 *  Only "where the reader is looking" is lifted out of the panels — which table
 *  is open, how it is sorted, which sub-tab. The data itself (rows, loading,
 *  errors) stays local to each panel, because the agent has no business owning a
 *  fetch. */
export interface Nav {
    raw: {file: string | null};
    source: {table: string | null; sort: {col: string; dir: SortDir} | null};
    record: {table: string | null};
    model: {tab: 'card' | 'run' | 'message'; openRun: number | null};
}

export type NavView = keyof Nav;

export const NAV0: Nav = {
    raw: {file: null},
    source: {table: null, sort: null},
    record: {table: null},
    model: {tab: 'card', openRun: null},
};

/** A pointer — "look HERE". Rings a row (or a time range) and scrolls it in.
 *
 *  This is the agent's cheapest and least invasive move: pointing at a row in a
 *  tab the clinician already has open beats opening another tab. The ring fades
 *  on its own so the console never accumulates stale agent marks. */
export interface Highlight {
    view: ConsoleView;
    table: string | null;
    /** 1-based, as the grid displays it */
    row: number | null;
    /** a time window, matched against the table's first datetime-ish column */
    from: string | null;
    to: string | null;
    note: string | null;
    /** Date.now() when it landed — the ring fades after HIGHLIGHT_TTL_MS */
    at: number;
}

export const HIGHLIGHT_TTL_MS = 12000;

/** One thing that happened in the console, for the agent's awareness feed. */
export interface ConsoleEvent {
    at: number;
    origin: Origin;
    what: string;   // already human-readable: "opened Record", "ran LTS v0001 → MAE 34.0"
}

/** What HaiChat is told the clinician has on screen. Compact and PHI-light: it
 *  carries the SHAPE of the session (tabs, selections, run outcomes), never chart
 *  rows — those the agent must fetch through a gated tool, on the record. */
export interface ConsoleSnapshot {
    patient_id: string | null;
    cohort: string | null;
    index_date: string | null;
    not_scoreable_reason: string | null;
    tabs: ConsoleView[];
    focused_view: ConsoleView | null;
    agent_opened: ConsoleView[];
    model: string | null;
    model_live: boolean;
    nav: Nav;
    runs: {
        id: number; model: string; status: string; origin: Origin;
        score: number | null; band: string | null;
        forecast_mae: number | null; forecast_last: number | null;
    }[];
    checklist: {items: number; done: number} | null;
}

/* ── raw explorer ─────────────────────────────────────────────────────────── */

export interface RawTable {
    columns: string[];
    n_rows: number;
    rows: Record<string, unknown>[];
}

export interface RawPatient {
    patient_id: string;
    index_date: string | null;
    tables: Record<string, RawTable>;
}
