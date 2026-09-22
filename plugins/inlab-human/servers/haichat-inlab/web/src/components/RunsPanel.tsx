/* RunsPanel — the Model insight view.
 *
 *   ┌────────────────┬──────────────────────────────────────────┐
 *   │ 🧠 MODELS      │  📇 Card | ▶ Run                          │
 *   │  · lts   ●     │  ─────────────────────────────────────── │
 *   │  · forecast ○  │  what it predicts / what it was trained  │
 *   │  · patchtst ○  │  on / how it builds a case / the payload │
 *   │                │  ─────────────────────────────────────── │
 *   │  (sidebar:     │  ▶ Run  →  runs history  →  forecast     │
 *   │   pick one)    │            chart vs the observed truth   │
 *   └────────────────┴──────────────────────────────────────────┘
 *
 * The ▶ Run button is the DETERMINISTIC path: a plain HTTP POST to the endpoint, no LLM.
 * A score (or a forecast) is an insight — from group to individual — so this lives under
 * INSIGHT, not ACTION.
 */
import {extractForecast, type ModelInfo, type RunRecord} from '../types';

import ForecastChart from './ForecastChart';
import PipelineBar from './PipelineBar';
import ModelCard from './ModelCard';

/* CONTROLLED — the sub-tab and the opened run live in useConsole, so HaiChat can say
 * "here is the card for this model" or "look at run #2" and actually show it. */
interface Props {
    /** whose message this is — MessagePanel needs it to load the patient */
    patientId: string | null;
    models: ModelInfo[];
    selected: string | null;
    tab: 'card' | 'run' | 'message';
    openRun: number | null;
    onTab: (t: 'card' | 'run' | 'message') => void;
    onOpenRun: (id: number) => void;
    onSelect: (pkg: string) => void;
    onRun: () => void;
    canRun: boolean;
    running: boolean;
    runs: RunRecord[];
    error: string | null;
    /** why this patient cannot be scored at all (endpoint patient-registry scope) */
    notScoreable?: string | null;
}

export default function RunsPanel(props: Props) {
    const {patientId, models, selected, tab, openRun, onTab, onOpenRun, onSelect, onRun,
        canRun, running, runs, error, notScoreable} = props;

    const shown = openRun === null ? runs[0] : runs.find((r) => r.id === openRun);
    const forecast = shown?.result ? extractForecast(shown.result) : null;
    const gaps = shown?.result?.gaps;
    const missing = gaps?.missing_tables ?? [];
    const empty = gaps?.empty_tables ?? [];

    return (
        <div className='mv'>
            <aside className='mv-side'>
                <div className='pane-header'>
                    {'🧠 Models'}
                    <span className='badge'>{models.length}</span>
                </div>
                <ul className='roster'>
                    {models.map((m) => (
                        <li
                            key={m.package}
                            className={
                                'roster-item' +
                                (m.package === selected ? ' selected' : '') +
                                (m.live ? '' : ' offline')
                            }
                            onClick={() => onSelect(m.package)}
                            title={m.live ? m.endpoint_url ?? '' : 'endpoint not running — the card still reads'}
                        >
                            <div className='roster-main'>
                                <span className='roster-id'>
                                    {(m.endpoint_name ?? m.package) + ' ' + (m.endpoint_version ?? '?')}
                                </span>
                                <span className={'dot ' + (m.live ? 'live' : 'down')}/>
                            </div>
                            <div className='roster-sub'>
                                {m.live ? m.required_tables.join(' · ') : 'endpoint not running'}
                            </div>
                        </li>
                    ))}
                </ul>
            </aside>

            <div className='mv-main'>
                <div className='mv-tabs'>
                    <button
                        className={'mv-tab' + (tab === 'card' ? ' active' : '')}
                        onClick={() => onTab('card')}
                    >
                        {'📇 Card'}
                    </button>
                    <button
                        className={'mv-tab' + (tab === 'run' ? ' active' : '')}
                        onClick={() => onTab('run')}
                    >
                        {'▶ Run'}
                        {runs.length > 0 && <span className='badge'>{runs.length}</span>}
                    </button>
                </div>

                <div className='mv-body'>
                    {tab === 'card' && <ModelCard pkg={selected}/>}

                    {tab === 'run' && (
                        <div className='pane-section'>
                            {notScoreable && (
                                <div className='alert warn'>
                                    <strong>{'⚠️ No model can score this patient'}</strong>
                                    <div>{notScoreable}</div>
                                    <div className='roster-sub'>
                                        {'The record is still fully browsable — only ▶ Run is unavailable.'}
                                    </div>
                                </div>
                            )}

                            <PipelineBar
                                patientId={patientId}
                                run={shown ?? null}
                                onRun={onRun}
                                canRun={canRun}
                                running={running}
                                runLabel={selected ? 'Run ' + selected : 'Run prediction'}
                                disabledReason={notScoreable ?? null}
                            />
                            {error && <div className='alert error'>{error}</div>}

                            <div className='pane-header'>
                                {'🕒 Runs'}
                                <span className='badge'>{runs.length}</span>
                            </div>
                            {runs.length === 0 ? (
                                <div className='roster-sub'>
                                    {'no runs yet for this patient — pick a model and ▶ Run'}
                                </div>
                            ) : (
                                <table className='runs-table'>
                                    <thead>
                                        <tr>
                                            <th>{'#'}</th>
                                            <th>{'time'}</th>
                                            <th>{'by'}</th>
                                            <th>{'model'}</th>
                                            <th>{'status'}</th>
                                            <th>{'result'}</th>
                                            <th>{'kind'}</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {runs.map((r) => {
                                            const fc = r.result ? extractForecast(r.result) : null;
                                            return (
                                                <tr
                                                    key={r.id}
                                                    className={shown?.id === r.id ? 'selected' : undefined}
                                                    onClick={() => onOpenRun(r.id)}
                                                >
                                                    <td className='rownum'>{r.id}</td>
                                                    <td>{r.at}</td>
                                                    {/* who pressed Run — a score whose author
                                                        the reader cannot see is the thing this
                                                        console exists to prevent */}
                                                    <td title={r.origin === 'agent' ? 'HaiChat ran this' : 'you ran this'}>
                                                        {r.origin === 'agent' ? '🤖' : '🧑'}
                                                    </td>
                                                    <td className='roster-id'>{r.model_label}</td>
                                                    <td>
                                                        <span className={'dot ' + (r.status === 'ok' ? 'live' : 'down')}/>
                                                    </td>
                                                    <td className='roster-id'>
                                                        {fc
                                                            ? fc.values[fc.values.length - 1] + ' ' + fc.unit
                                                            : r.score === null ? '—' : r.score.toFixed(4)}
                                                    </td>
                                                    <td>
                                                        {fc
                                                            ? (fc.values.length * fc.stepMin) / 60 + 'h forecast'
                                                            : r.band ?? '—'}
                                                    </td>
                                                </tr>
                                            );
                                        })}
                                    </tbody>
                                </table>
                            )}

                            {shown && shown.status === 'ok' && shown.result && forecast && (
                                <ForecastChart
                                    values={forecast.values}
                                    observed={forecast.observed}
                                    context={forecast.context}
                                    unit={forecast.unit}
                                    stepMin={forecast.stepMin}
                                    mode={forecast.mode}
                                    metrics={forecast.metrics}
                                />
                            )}

                            {shown && shown.status === 'ok' && !forecast && shown.score !== null && (
                                <div className='score-card'>
                                    <div className='score-value'>{shown.score.toFixed(4)}</div>
                                    <div className={'score-band band-' + (shown.band ?? '').toLowerCase()}>
                                        {shown.band ?? '—'}
                                    </div>
                                    <div className='roster-sub center'>{'verbatim from the endpoint'}</div>
                                </div>
                            )}

                            {shown && shown.status === 'ok' && (missing.length > 0 || empty.length > 0) && (
                                <div className='alert warn'>
                                    <strong>{'⚠️ Data gaps'}</strong>
                                    {missing.length > 0 && <div>{'missing: ' + missing.join(', ')}</div>}
                                    {empty.length > 0 && <div>{'empty: ' + empty.join(', ')}</div>}
                                    <div className='roster-sub'>
                                        {'the model still ran — treat as partial data'}
                                    </div>
                                </div>
                            )}
                            {shown && shown.status === 'error' && (
                                <div className='alert error'>{shown.error ?? 'prediction failed'}</div>
                            )}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
