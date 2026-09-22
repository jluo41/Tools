/* Console — the standalone page served by the haichat-inlab service.
 *
 * Databricks-grammar shell carrying the lab's Data → Insight → Action paradigm, over a
 * DOCK LAYOUT: the rail opens views, tab strips hold them open, and any tab can be
 * dragged onto any edge of any pane to split it (see layout.ts).
 *
 *   ┌──────┬───────────────────────┬─────────────────────┬──────────┐
 *   │ DATA │ 🗂️ Raw │ 🧠 Model ◫    │ ✅ Checklist ✕   ◫  │ HaiChat  │
 *   │ Raw  ├───────────────────────┼─────────────────────┤ drawer   │
 *   │INSIGHT   active view         │  active view        │ (standa- │
 *   │ ...  ├───────────────────────┤  (drag a tab to any │  lone    │
 *   │ACTION│ 🌐 External           │   EDGE to re-dock)   │  only)   │
 *   └──────┴───────────────────────┴─────────────────────┴──────────┘
 *
 * TWO DRIVERS, ONE REDUCER. The clinician's hands and HaiChat both move this console,
 * and they move it the same way: every gesture below — rail click, tab click, close,
 * split, Run — is a `ConsoleAction` handed to `dispatch`, and the agent's tools produce
 * exactly the same actions over the WebSocket (useHaiChat.ts). There is no second path
 * into the UI to audit, and no second way to produce a score.
 *
 * Every open view stays mounted (hidden, not unmounted) so a sort or a run history
 * survives a tab switch. Docking re-parents a view, which remounts it — so anything
 * expensive (the checklist, the run history, the panels' navigation) is owned by
 * useConsole, not by the views.
 *
 * One selected patient = one workspace. Embedded in HAI-Chat (iframe beside a thread)
 * the drawer is hidden — the Mattermost thread IS HaiChat there.
 */
import {useCallback, useEffect, useRef, useState} from 'react';

import {describe, type ActionResult, type ConsoleAction} from './actions';
import AnnotateView from './components/AnnotateView';
import CaseView from './components/CaseView';
import ChecklistView from './components/ChecklistView';
import ScopeStub from './components/ScopeStub';
import DockLayout from './components/DockLayout';
import ExternalView from './components/ExternalView';
import HaiChatDrawer from './components/HaiChatDrawer';
import HealthView from './components/HealthView';
import InternalView from './components/InternalView';
import NavRail from './components/NavRail';
import PatientCard from './components/PatientCard';
import PatientCombobox from './components/PatientCombobox';
import RawDataPanel from './components/RawDataPanel';
import RawFilesPanel from './components/RawFilesPanel';
import RecordPanel from './components/RecordPanel';
import RunsPanel from './components/RunsPanel';
import Splitter from './components/Splitter';
import TasksView from './components/TasksView';
import * as L from './layout';
import type {ConsoleView, Origin} from './types';
import {snapshotOf, useConsole, type Console as ConsoleState} from './useConsole';
import {useHaiChat} from './useHaiChat';

const clamp = (v: number, lo: number, hi: number) => Math.min(hi, Math.max(lo, v));

/** The two separated logics. Which one this Console instance IS comes from the URL
 *  route (main.tsx); switching remounts, so individual and group never share state. */
export type Scope = 'individual' | 'group';

/** Embedded beside a Mattermost thread, the thread is the conversation — no drawer,
 *  and no agent driving a console nobody can watch it drive. */
const embedded = window.self !== window.top;

export default function Console({scope, navigate}: {scope: Scope; navigate: (s: Scope) => void}) {
    const c = useConsole();
    // Source is the default: it is the layer the payload is built from, and the one a
    // reader wants first. Raw (files) and Record are one rail click away.
    const [root, setRoot] = useState<L.LayoutNode>(() => L.group(['source']));
    const [focusedId, setFocusedId] = useState<string | null>(null);
    const [railCollapsed, setRailCollapsed] = useState(embedded);
    const [chatOpen, setChatOpen] = useState(false);
    const [chatW, setChatW] = useState(340);
    /** tabs HaiChat opened, until the clinician adopts one by clicking it */
    const [agentOpened, setAgentOpened] = useState<ConsoleView[]>([]);

    /* Scope is a MODE, and a mode should be visible without reading a label: the
     * accent tokens are swapped on :root so the whole console — nav, tabs, buttons,
     * charts — shifts colour when you switch. See [data-scope] in console.css. */
    useEffect(() => {
        document.documentElement.dataset.scope = scope;
    }, [scope]);

    const panes = L.groups(root);
    const focused = panes.find((g) => g.id === focusedId) ?? panes[0];
    const activeView = focused?.active ?? null;

    /* setRoot's updater must not read `focusedId` from the render it was created in —
     * a concurrent agent action and a human drag would then race. A ref keeps the
     * anchor honest. */
    const focusedRef = useRef<string | null>(null);
    focusedRef.current = focused?.id ?? null;
    const anchorOf = (r: L.LayoutNode) =>
        (L.groups(r).find((g) => g.id === focusedRef.current) ?? L.groups(r)[0]).id;

    const adopt = useCallback((v: ConsoleView) =>
        setAgentOpened((xs) => xs.filter((x) => x !== v)), []);

    /* Mark a view as the agent's ONLY if the agent actually opened it. A tab the
     * clinician already had open stays theirs even when HaiChat focuses it or rings a
     * row inside it — stamping 🤖 on a tab they opened themselves is a lie, and it
     * would slowly badge the whole console. */
    const claimIfNew = useCallback((v: ConsoleView, wasOpen: boolean) => {
        if (!wasOpen) {
            setAgentOpened((xs) => (xs.includes(v) ? xs : [...xs, v]));
        }
    }, []);

    /* ── THE REDUCER ─────────────────────────────────────────────────────────────
     *
     * One entry point. The clinician's gestures call it with origin 'user'; HaiChat's
     * tool calls arrive over the socket and call it with origin 'agent'. Same actions,
     * same effects, same run history — the only difference is the badge and, for the
     * consequential actions, the Allow/Deny card the server already made the agent
     * pass through before this is ever reached.
     */
    const dispatch = useCallback(async (
        a: ConsoleAction, origin: Origin,
    ): Promise<ActionResult> => {
        const said = () => c.note(origin, describe(a));

        switch (a.type) {
        case 'state/read':
            // a pure read: the caller gets the snapshot every ui_result carries anyway,
            // and the console is not disturbed by being looked at
            return {ok: true};

        case 'view/open': {
            const wasOpen = L.allTabs(root).includes(a.view);
            setRoot((r) => (a.where === 'side'
                ? L.dock(r, anchorOf(r), a.view, 'right')
                : L.focusOrOpen(r, anchorOf(r), a.view)));
            if (origin === 'agent') {
                claimIfNew(a.view, wasOpen);
            } else {
                adopt(a.view);
            }
            said();
            return {ok: true};
        }

        case 'view/focus': {
            const at = L.groupOfView(root, a.view);
            if (!at) {
                return dispatch({type: 'view/open', view: a.view}, origin);
            }
            setFocusedId(at.id);
            setRoot((r) => L.activate(r, at.id, a.view));
            if (origin === 'user') {
                adopt(a.view);     // the clinician looked at it — it is theirs now
            }
            said();
            return {ok: true};
        }

        case 'view/close': {
            const at = L.groupOfView(root, a.view);
            if (!at) {
                return {ok: false, error: a.view + ' is not open'};
            }
            setRoot((r) => L.closeTab(r, at.id, a.view));
            adopt(a.view);
            said();
            return {ok: true};
        }

        case 'panel/set': {
            const patch: Record<string, unknown> = {};
            for (const k of ['table', 'sort', 'file', 'tab', 'openRun'] as const) {
                if (a[k] !== undefined) {
                    patch[k] = a[k];
                }
            }
            c.setNav(a.view, patch as never);
            said();
            return {ok: true};
        }

        case 'highlight/set': {
            const wasOpen = L.allTabs(root).includes(a.view);
            c.setHighlight({
                view: a.view, table: a.table ?? null, row: a.row ?? null,
                from: a.from ?? null, to: a.to ?? null, note: a.note ?? null,
                at: Date.now(),
            });
            /* Ringing a row in a table nobody has open is pointing at nothing — so a
             * highlight opens (or focuses) its view. If it also names a table, open that
             * table too, or the ring lands on a grid the clinician cannot see. */
            if (a.table && (a.view === 'source' || a.view === 'record')) {
                c.setNav(a.view, {table: a.table});
            }
            setRoot((r) => L.focusOrOpen(r, anchorOf(r), a.view));
            if (origin === 'agent') {
                claimIfNew(a.view, wasOpen);
            }
            said();
            return {ok: true};
        }

        case 'highlight/clear':
            c.setHighlight(null);
            return {ok: true};

        case 'patient/select':
            if (!c.patients.some((p) => p.patient_id === a.patient_id)) {
                return {ok: false, error: 'no such patient in this store: ' + a.patient_id};
            }
            said();
            await c.selectPatient(a.patient_id);
            return {ok: true};

        case 'model/select':
            if (!c.models.some((m) => m.package === a.package)) {
                return {ok: false, error: 'no such model: ' + a.package};
            }
            c.setModelPkg(a.package);
            said();
            return {ok: true};

        case 'run/start': {
            /* The agent names the patient and model it BELIEVES it is scoring, and the
             * clinician approved a card showing exactly those. If the console has moved
             * since, refuse — never silently score something else. */
            if (a.patient_id && a.patient_id !== c.patientId) {
                return {ok: false, error: 'the console is on ' + (c.patientId ?? 'no patient') +
                    ', not ' + a.patient_id + ' — switch the patient first'};
            }
            const pkg = a.package ?? c.modelPkg;
            if (!pkg) {
                return {ok: false, error: 'no model selected'};
            }
            if (!c.models.some((m) => m.package === pkg)) {
                return {ok: false, error: 'no such model: ' + pkg};
            }
            if (c.chart?.summary?.not_scoreable_reason) {
                return {ok: false, error: c.chart.summary.not_scoreable_reason};
            }
            try {
                const rec = await c.run(origin, pkg);
                return rec.status === 'ok'
                    ? {ok: true, run: rec.result}
                    : {ok: false, error: rec.error ?? 'the prediction failed'};
            } catch (e) {
                return {ok: false, error: String(e)};
            }
        }

        case 'checklist/generate':
            try {
                const cl = await c.generateChecklist(origin);
                return {ok: true, checklist: cl};
            } catch (e) {
                return {ok: false, error: String(e)};
            }

        case 'checklist/toggle':
            c.toggleChecklistItem(a.index);
            said();
            return {ok: true};

        default:
            return {ok: false, error: 'unknown action'};
        }
        // `root` is read to LOCATE a view (view/focus, view/close, was-it-already-open);
        // every WRITE uses the functional setRoot form, so a concurrent human drag and an
        // agent action cannot clobber each other.
    }, [c, root, adopt, claimIfNew]);

    const snapshot = useCallback(
        () => snapshotOf(c, L.allTabs(root), activeView, agentOpened, scope),
        [c, root, activeView, agentOpened, scope],
    );

    const hai = useHaiChat({
        enabled: !embedded,
        patientId: c.patientId,
        dispatch,
        snapshot,
        drainUserEvents: c.drainUserEvents,
        pulse: c.events.length,
    });

    /* thin wrappers so every gesture below is an ACTION, not a bespoke setState */
    const act = (a: ConsoleAction) => void dispatch(a, 'user');

    /* The labeling forge's ▶ steps (and any "run this via the agent" affordance) go
     * through HaiChat: open the drawer and hand it the command. The agent narrates and
     * its writes still hit the Allow gate — a button in a view never writes the store. */
    const runInChat = useCallback((prompt: string) => {
        if (embedded) {
            return;    // embedded beside a Mattermost thread: the thread IS HaiChat
        }
        setChatOpen(true);
        hai.send(prompt);
    }, [hai]);

    return (
        <div className='app'>
            <header className='topbar'>
                <span className='logo'>
                    <span className='brand-dot'/>
                    {'🩺 In-Lab Console'}
                </span>
                <div className='level-toggle' role='group' aria-label='scope'>
                    <button
                        className={scope === 'individual' ? 'active' : ''}
                        onClick={() => navigate('individual')}
                        title='one patient — everything on this page is about them'
                    >{'👤 Individual'}</button>
                    <button
                        className={scope === 'group' ? 'active' : ''}
                        onClick={() => navigate('group')}
                        title='a cohort — the same views, scoped to a group of people'
                    >{'👥 Group'}</button>
                </div>
                {c.datasets.length > 0 && (
                    <label className='ds-picker' title='data type — which RecordSet is active'>
                        {'🗃️'}
                        <select
                            className='ds-select'
                            value={c.dataset ?? ''}
                            onChange={(e) => c.setDataset(e.target.value)}
                        >
                            {c.datasets.map((d) => (
                                <option key={d.name} value={d.name}>
                                    {d.name + (d.cohort ? ' · ' + d.cohort : '') + ' (' + d.n_patients + ')'}
                                </option>
                            ))}
                        </select>
                    </label>
                )}
                {scope === 'individual' ? (
                    <PatientCombobox
                        patients={c.patients}
                        selected={c.patientId}
                        onSelect={(id) => act({type: 'patient/select', patient_id: id})}
                    />
                ) : (
                    <span className='group-indicator' title='the group these views are scoped to'>
                        {'👥 ' + (c.dataset ?? 'cohort') + ' · ' +
                            ((c.datasets.find((d) => d.name === c.dataset)?.n_patients) ?? c.patients.length) +
                            ' patients'}
                    </span>
                )}
                {c.chart?.index_date && (
                    <span className='as-of'>{'🕒 as-of ' + c.chart.index_date}</span>
                )}
                <span className='topbar-space'/>
                <span className='roster-sub'>
                    {'de-identified data · research · not for clinical use'}
                </span>
                {!embedded && (
                    <button
                        className={'chat-toggle' + (chatOpen ? ' active' : '')}
                        onClick={() => setChatOpen((o) => !o)}
                        title='HaiChat — ask about this patient (Agent SDK)'
                    >
                        {'💬 HaiChat'}
                        <span className={'dot ' + (hai.status === 'offline' ? 'down'
                            : hai.status === 'busy' ? 'busy' : 'live')}/>
                    </button>
                )}
            </header>

            <div className='layout-shell'>
                <NavRail
                    active={activeView}
                    open={L.allTabs(root)}
                    agentOpened={agentOpened}
                    onOpen={(v) => act({type: 'view/open', view: v})}
                    onOpenToSide={(v) => act({type: 'view/open', view: v, where: 'side'})}
                    collapsed={railCollapsed}
                    onToggle={() => setRailCollapsed((x) => !x)}
                />

                <main className='center'>
                    <PatientCard patient={c.chart} loading={c.chartLoading}/>

                    <DockLayout
                        node={root}
                        path={[]}
                        focusedId={focused?.id ?? null}
                        agentOpened={agentOpened}
                        render={(v) => viewFor(v, c, dispatch, scope, runInChat)}
                        onFocus={setFocusedId}
                        onActivate={(gid, v) => {
                            setFocusedId(gid);
                            act({type: 'view/focus', view: v});
                        }}
                        onClose={(gid, v) => {
                            setFocusedId(gid);
                            act({type: 'view/close', view: v});
                        }}
                        onCloseOthers={(gid, v) => setRoot((r) => {
                            const g = L.groups(r).find((x) => x.id === gid);
                            return g
                                ? g.tabs.filter((t) => t !== v).reduce((acc, t) => L.closeTab(acc, gid, t), r)
                                : r;
                        })}
                        onSplit={(gid, v) => setRoot((r) => L.dock(r, gid, v, 'right'))}
                        onDock={(gid, v, where) => setRoot((r) => L.dock(r, gid, v, where))}
                        onResize={(path, i, pct) => setRoot((r) => L.resize(r, path, i, pct))}
                    />
                </main>

                {/* mounted for the life of the console, hidden when closed: the agent
                    session must not die because the clinician collapsed the drawer */}
                {!embedded && (
                    <>
                        {chatOpen && (
                            <Splitter
                                orientation='vertical'
                                onDrag={(d) => setChatW((w) => clamp(w - d, 260, 560))}
                                onDoubleClick={() => setChatW(340)}
                            />
                        )}
                        <div
                            className={'drawer-slot' + (chatOpen ? '' : ' hidden')}
                            style={{width: chatOpen ? chatW : 0}}
                        >
                            <HaiChatDrawer
                                patientId={c.patientId}
                                items={hai.items}
                                status={hai.status}
                                follow={hai.follow}
                                onFollow={hai.setFollow}
                                onSend={hai.send}
                                onAnswer={hai.answer}
                                onInterrupt={hai.interrupt}
                                onClose={() => setChatOpen(false)}
                            />
                        </div>
                    </>
                )}
            </div>
        </div>
    );
}

/** one view, wired to the console's state. Panels are CONTROLLED (nav + highlight come
 *  from useConsole) so that HaiChat can drive them through the same dispatch the
 *  clinician's clicks go through. */
function viewFor(
    v: ConsoleView,
    c: ConsoleState,
    dispatch: (a: ConsoleAction, o: Origin) => Promise<ActionResult>,
    scope: Scope,
    runInChat: (prompt: string) => void,
): JSX.Element {
    const act = (a: ConsoleAction) => void dispatch(a, 'user');
    const hl = c.highlight;
    const group = scope === 'group';
    const ds = c.dataset ?? 'this cohort';

    switch (v) {
    // DATA — one dataset, three stages of the pipeline
    case 'raw':
        return group ? (
            <ScopeStub icon='👥' title='Group · Raw' lines={[
                'Raw files for every human in ' + ds + ', not one person.',
                'Switch to Individual + a patient to browse one person’s raw files.']}/>
        ) : (
            <RawFilesPanel
                patientId={c.patientId}
                dataset={c.dataset}
                open={c.nav.raw.file}
                onOpen={(file) => act({type: 'panel/set', view: 'raw', file})}
            />
        );
    case 'source':
        return group ? (
            <ScopeStub icon='👥' title='Group · Source' lines={[
                'SourceFn tables across all of ' + ds + ' — every human’s rows in one table.',
                'The dataset-wide source browse is the next slice to land here.']}/>
        ) : (
            <RawDataPanel
                patientId={c.patientId}
                dataset={c.dataset}
                table={c.nav.source.table}
                sort={c.nav.source.sort}
                highlight={hl?.view === 'source' ? hl : null}
                onTable={(table) => act({type: 'panel/set', view: 'source', table})}
                onSort={(sort) => act({type: 'panel/set', view: 'source', sort})}
            />
        );
    case 'record':
        return group ? (
            <ScopeStub icon='👥' title='Group · Record' lines={[
                'RecordFn streams across all of ' + ds + ', not one timeline.',
                'The dataset-wide record browse is the next slice to land here.']}/>
        ) : (
            <RecordPanel
                patientId={c.patientId}
                dataset={c.dataset}
                table={c.nav.record.table}
                highlight={hl?.view === 'record' ? hl : null}
                anchor={c.chart?.summary?.anchor ?? c.chart?.index_date ?? null}
                onTable={(table) => act({type: 'panel/set', view: 'record', table})}
            />
        );
    case 'case':
        // group = the whole batch across the cohort; CaseView browses all humans
        // when no patient is passed, which is exactly the group case set.
        return <CaseView patientId={group ? null : c.patientId} dataset={c.dataset}/>;
    case 'internal':
        return group
            ? <ScopeStub icon='👥' title='Group · Insight' lines={[
                'Cohort-level insight over ' + ds + ' — distributions and aggregates, not one patient’s chart.']}/>
            : <InternalView patient={c.chart} loading={c.chartLoading}/>;
    case 'external':
        return group
            ? <ScopeStub icon='👥' title='Group · External' lines={[
                'External evidence for the cohort, not a single patient.']}/>
            : <ExternalView patient={c.chart}/>;
    case 'model':
        return group ? (
            <ScopeStub icon='👥' title='Group · Model' lines={[
                'Model performance across ' + ds + ' — batch scoring and metrics, not one ▶ Run.']}/>
        ) : (
            <RunsPanel
                patientId={c.patientId}
                models={c.models}
                selected={c.modelPkg}
                tab={c.nav.model.tab}
                openRun={c.nav.model.openRun}
                onTab={(tab) => act({type: 'panel/set', view: 'model', tab})}
                onOpenRun={(openRun) => act({type: 'panel/set', view: 'model', openRun})}
                onSelect={(pkg) => act({type: 'model/select', package: pkg})}
                onRun={() => act({type: 'run/start'})}
                canRun={Boolean(c.patientId && c.modelPkg)}
                running={c.running}
                runs={c.patientRuns}
                error={c.error}
                notScoreable={c.chart?.summary?.not_scoreable_reason ?? null}
            />
        );
    case 'checklist':
        return group ? (
            <ScopeStub icon='👥' title='Group · Checklist' lines={[
                'Actions over the whole cohort, not one patient.']}/>
        ) : (
            <ChecklistView
                patientId={c.patientId}
                lastRun={c.patientRuns[0] ?? null}
                checklist={c.checklist}
                done={c.checklistDone}
                busy={c.checklistBusy}
                onGenerate={() => act({type: 'checklist/generate'})}
                onToggle={(i) => act({type: 'checklist/toggle', index: i})}
            />
        );
    case 'tasks':
        // the work linked to this scope — group tasks vs per-individual tasks,
        // scanned from examples/Project-*/tasks and filtered by kind.
        return <TasksView scope={scope}/>;
    case 'annotate':
        // TWO ORIENTATIONS, ONE VERB. Group = the FORGE: develop the labeling
        // instrument over the whole corpus (the sl loop, driven through HaiChat).
        // Individual = the READOUT: apply a ready guideline to this one person.
        return group
            ? <AnnotateView
                dataset={c.dataset}
                nHumans={(c.datasets.find((d) => d.name === c.dataset)?.n_patients) ?? c.patients.length}
                onRunStep={runInChat}
                embedded={embedded}/>
            : <ScopeStub icon='✏️' title='Apply a guideline' lines={[
                'Pick a ready labeling guideline and Run it on this one patient — like the model’s ▶ Run, but it produces a label.',
                'Guideline DEVELOPMENT — the forge: gallery, κ trajectory, batch labeling — lives in Group mode.']}/>;
    case 'health':
        return <HealthView/>;
    default:
        return <div/>;
    }
}
