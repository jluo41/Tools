/* useConsole — all the console's state and REST calls, in one hook.
 *
 * Held here (not in a page) so any shell can drive the console: the standalone
 * page in this service, the REACH D01 demo, or a future Mattermost plugin RHS.
 *
 * Everything HaiChat is allowed to touch lives here or in the dock tree, and both
 * drivers reach it through Console.tsx's `dispatch` (see actions.ts). Three things
 * are held here specifically because a dock re-parent REMOUNTS a view and would
 * otherwise throw them away: the generated checklist, the run history, and the
 * panels' navigation state.
 */
import {useCallback, useEffect, useRef, useState} from 'react';

import {
    extractForecast,
    extractScore,
    NAV0,
    type Checklist,
    type ConsoleEvent,
    type ConsoleView,
    type Highlight,
    type ModelInfo,
    type Nav,
    type NavView,
    type Origin,
    type PatientDetail,
    type PatientListItem,
    type PredictResult,
    type RunRecord,
} from './types';

/** `api` lets an embedder point at a different origin (e.g. the console service
 *  running on :8091 while the host page is served elsewhere). Default = same origin. */
export interface DatasetInfo {
    name: string;
    n_patients: number;
    cohort: string | null;
}

export function useConsole(api = '') {
    const [datasets, setDatasets] = useState<DatasetInfo[]>([]);
    /** which data type is active — scopes the roster, the chart, and the cases.
     *  Persisted so the Individual⇄Group route switch (which remounts) keeps it;
     *  the two scopes are separate logics but should look at the same data type. */
    const [dataset, setDatasetState] = useState<string | null>(
        () => sessionStorage.getItem('inlab.dataset'),
    );
    const [patients, setPatients] = useState<PatientListItem[]>([]);
    const [models, setModels] = useState<ModelInfo[]>([]);
    const [patientId, setPatientId] = useState<string | null>(null);
    const [chart, setChart] = useState<PatientDetail | null>(null);
    const [chartLoading, setChartLoading] = useState(false);
    const [modelPkg, setModelPkg] = useState<string | null>(null);
    const [result, setResult] = useState<PredictResult | null>(null);
    const [runs, setRuns] = useState<RunRecord[]>([]);
    const [running, setRunning] = useState(false);
    const [error, setError] = useState<string | null>(null);
    /* Checklist state lives HERE, not in ChecklistView: a view that is dragged into
     * the other split group is re-parented (React remounts it), and a generated
     * checklist is too expensive to lose to a layout change. */
    const [checklist, setChecklist] = useState<Checklist | null>(null);
    const [checklistDone, setChecklistDone] = useState<Set<number>>(new Set());
    const [checklistBusy, setChecklistBusy] = useState(false);

    /* Panel navigation — lifted out of the panels so HaiChat can reach it. Only
     * WHERE the reader is looking; the rows themselves stay inside each panel. */
    const [nav, setNavState] = useState<Nav>(NAV0);
    const [highlight, setHighlight] = useState<Highlight | null>(null);

    /* Who did what. The agent reads only the `user` half of this (it must never be
     * told its own tab-opens back as if the clinician had done them), and it is
     * DRAINED when read, so each turn sees each event exactly once. */
    const [events, setEvents] = useState<ConsoleEvent[]>([]);
    const note = useCallback((origin: Origin, what: string) => {
        setEvents((es) => [...es.slice(-40), {at: Date.now(), origin, what}]);
    }, []);
    const drainUserEvents = useCallback((): ConsoleEvent[] => {
        let taken: ConsoleEvent[] = [];
        setEvents((es) => {
            taken = es.filter((e) => e.origin === 'user');
            return [];
        });
        return taken;
    }, []);

    /* Runs are appended from async callbacks; a ref keeps the id monotonic without
     * making `run` depend on the list (which would re-create it on every run). */
    const seq = useRef(0);

    /* data types available, and the default one. Models are endpoint-store, not
     * patient-store, so they load once and don't move with the dataset. */
    useEffect(() => {
        fetch(`${api}/api/datasets`)
            .then((r) => r.json())
            .then((d) => {
                setDatasets(d.datasets ?? []);
                setDatasetState((cur) => {
                    const names = (d.datasets ?? []).map((x: DatasetInfo) => x.name);
                    // keep a persisted choice only if it still exists in this store
                    return cur && names.includes(cur) ? cur : (d.default ?? names[0] ?? null);
                });
            })
            .catch(() => undefined);
        fetch(`${api}/api/models`)
            .then((r) => r.json())
            .then((d) => setModels(d.models ?? []))
            .catch(() => undefined);
    }, [api]);

    /* the roster follows the active data type */
    useEffect(() => {
        const qs = dataset ? `?dataset=${encodeURIComponent(dataset)}` : '';
        fetch(`${api}/api/patients${qs}`)
            .then((r) => r.json())
            .then((d) => setPatients(d.patients ?? []))
            .catch(() => setError('cannot reach the console API'));
    }, [api, dataset]);

    /** switch data type — the roster reloads and the current human is cleared,
     *  since a patient belongs to exactly one dataset. */
    const setDataset = useCallback((name: string) => {
        sessionStorage.setItem('inlab.dataset', name);
        setDatasetState(name);
        setPatientId(null);
        setChart(null);
        setResult(null);
        setError(null);
        setNavState(NAV0);
        setHighlight(null);
    }, []);

    const selectPatient = useCallback((id: string) => {
        setPatientId(id);
        setResult(null);
        setError(null);
        setChecklist(null);          // a checklist belongs to one patient
        setChecklistDone(new Set());
        setNavState(NAV0);           // so does a table selection
        setHighlight(null);
        setChartLoading(true);
        const qs = dataset ? `?dataset=${encodeURIComponent(dataset)}` : '';
        return fetch(`${api}/api/patients/${id}${qs}`)
            .then((r) => r.json())
            .then((d) => {
                setChart(d);
                return d as PatientDetail;
            })
            .catch(() => {
                setError('cannot load chart');
                return null;
            })
            .finally(() => setChartLoading(false));
    }, [api, dataset]);

    const setNav = useCallback((view: NavView, patch: Partial<Nav[NavView]>) => {
        setNavState((n) => ({...n, [view]: {...n[view], ...patch}}));
    }, []);

    /** Press ▶ Run — whoever is pressing it.
     *
     *  Returns the RunRecord so the AGENT can read the score it just produced
     *  instead of inventing one, and so its run lands in the same visible history
     *  as the clinician's. Explicit args exist so an agent call can name the
     *  patient and model it BELIEVES it is scoring; the caller (Console.dispatch)
     *  rejects a mismatch rather than silently scoring something else. */
    const run = useCallback((origin: Origin = 'user', pkgOverride?: string): Promise<RunRecord> => {
        const pid = patientId;
        /* An agent run names its model explicitly — the same one printed on the Allow
         * card the clinician approved. Reading it back out of `modelPkg` would be a
         * race (select-then-run in one turn reads the PREVIOUS selection), and a race
         * here means scoring a different model than the one that was consented to. */
        const pkg = pkgOverride ?? modelPkg;
        if (!pid || !pkg) {
            return Promise.reject(new Error('select a patient and a model first'));
        }
        if (pkgOverride && pkgOverride !== modelPkg) {
            setModelPkg(pkgOverride);   // keep the UI honest about what just ran
        }
        const model = models.find((m) => m.package === pkg);
        const label = model
            ? (model.endpoint_name ?? model.package) + ' ' + (model.endpoint_version ?? '?')
            : pkg;

        const record = (partial: Partial<RunRecord>): RunRecord => {
            const rec: RunRecord = {
                id: ++seq.current,
                at: new Date().toLocaleTimeString(),
                patient_id: pid,
                model_pkg: pkg,
                model_label: label,
                status: 'error',
                score: null,
                band: null,
                result: null,
                error: null,
                origin,
                ...partial,
            };
            setRuns((rs) => [rec, ...rs]);
            return rec;
        };

        setRunning(true);
        setError(null);
        setResult(null);
        return fetch(`${api}/api/predict`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({patient_id: pid, model: pkg, dataset}),
        })
            .then((r) => r.json())
            .then((d) => {
                if (d.error) {
                    setError(d.error);
                    const rec = record({status: 'error', error: d.error});
                    note(origin, 'ran ' + label + ' — failed: ' + d.error);
                    return rec;
                }
                setResult(d);
                const {score, band} = extractScore(d);
                const rec = record({status: 'ok', score, band, result: d});
                const fc = extractForecast(d);
                note(origin, 'ran ' + label + (fc
                    ? ' → ' + (fc.values.length * fc.stepMin) / 60 + 'h forecast' +
                      (fc.metrics?.mae !== undefined ? ', MAE ' + fc.metrics.mae + ' ' + fc.unit : '')
                    : score !== null ? ' → ' + score.toFixed(4) + (band ? ' (' + band + ')' : '') : ''));
                return rec;
            })
            .catch(() => {
                setError('prediction failed');
                const rec = record({status: 'error', error: 'prediction failed'});
                note(origin, 'ran ' + label + ' — failed');
                return rec;
            })
            .finally(() => setRunning(false));
    }, [api, patientId, modelPkg, models, note, dataset]);

    /** Generate the checklist. Lifted out of ChecklistView so the agent can ask for
     *  it through the same path the ✨ button uses — one generator, one prompt, one
     *  set of guardrails. */
    const generateChecklist = useCallback((origin: Origin = 'user'): Promise<Checklist> => {
        if (!patientId) {
            return Promise.reject(new Error('select a patient first'));
        }
        const lastRun = runs.find((r) => r.patient_id === patientId) ?? null;
        setChecklistBusy(true);
        setChecklist(null);
        setChecklistDone(new Set());
        return fetch(`${api}/api/checklist`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                patient_id: patientId,
                run: lastRun && lastRun.status === 'ok' ? {
                    model: lastRun.model_label,
                    score: lastRun.score,
                    band: lastRun.band,
                    gaps: lastRun.result?.gaps,
                } : null,
            }),
        })
            .then((r) => r.json())
            .then((d) => {
                if (d.error) {
                    throw new Error(d.error);
                }
                setChecklist(d);
                note(origin, 'generated a checklist (' + (d.items?.length ?? 0) + ' items)');
                return d as Checklist;
            })
            .finally(() => setChecklistBusy(false));
    }, [api, patientId, runs, note]);

    const toggleChecklistItem = useCallback((i: number) => {
        setChecklistDone((s) => {
            const next = new Set(s);
            if (next.has(i)) {
                next.delete(i);
            } else {
                next.add(i);
            }
            return next;
        });
    }, []);

    const selectedModel = models.find((m) => m.package === modelPkg) ?? null;

    /** run history for the currently selected patient (newest first) */
    const patientRuns = runs.filter((r) => r.patient_id === patientId);

    return {
        datasets, dataset, setDataset,
        patients, models, patientId, chart, chartLoading, modelPkg,
        result, runs, patientRuns, running, error, selectedModel,
        checklist, checklistDone, checklistBusy,
        nav, highlight, events,
        selectPatient, setModelPkg, run, generateChecklist,
        setChecklist, toggleChecklistItem, setNav, setHighlight,
        note, drainUserEvents,
    };
}

export type Console = ReturnType<typeof useConsole>;

/** The compact picture of the session handed to HaiChat with every message.
 *  Shape, not chart rows: the agent must fetch data through a tool, on the record. */
export function snapshotOf(
    c: Console,
    tabs: ConsoleView[],
    focusedView: ConsoleView | null,
    agentOpened: ConsoleView[],
    scope: 'individual' | 'group' = 'individual',
) {
    const m = c.models.find((x) => x.package === c.modelPkg);
    return {
        // WHICH LOGIC is driving. In group mode the agent orients to the CORPUS
        // (dataset) it is developing labels over — not a patient (there is none).
        scope,
        dataset: c.dataset,
        n_humans: c.datasets.find((d) => d.name === c.dataset)?.n_patients ?? c.patients.length,
        patient_id: c.patientId,
        cohort: c.chart?.summary?.cohort ?? null,
        index_date: c.chart?.index_date ?? null,
        not_scoreable_reason: c.chart?.summary?.not_scoreable_reason ?? null,
        tabs,
        focused_view: focusedView,
        agent_opened: agentOpened,
        model: c.modelPkg,
        model_live: Boolean(m?.live),
        nav: c.nav,
        runs: c.patientRuns.slice(0, 5).map((r) => {
            const fc = r.result ? extractForecast(r.result) : null;
            return {
                id: r.id,
                model: r.model_label,
                status: r.status,
                origin: r.origin,
                score: r.score,
                band: r.band,
                forecast_mae: fc?.metrics?.mae ?? null,
                forecast_last: fc ? fc.values[fc.values.length - 1] : null,
            };
        }),
        checklist: c.checklist
            ? {items: c.checklist.items.length, done: c.checklistDone.size}
            : null,
    };
}
