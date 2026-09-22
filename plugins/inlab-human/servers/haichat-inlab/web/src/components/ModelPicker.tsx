/* ModelPicker — available prediction models + live status + the RUN button.
 * Source of truth lives here, in HAI-Chat. The REACH D01 demo imports it from
 * this folder rather than keeping a copy — one component, no fork.
 *
 * The "Run" button is the DETERMINISTIC path: straight to the endpoint, no LLM.
 */
import {extractScore, type ModelInfo, type PredictResult} from '../types';

interface Props {
    models: ModelInfo[];
    selected: string | null;
    onSelect: (pkg: string) => void;
    onRun: () => void;
    canRun: boolean;
    running: boolean;
    result: PredictResult | null;
    error: string | null;
}

export default function ModelPicker(props: Props) {
    const {models, selected, onSelect, onRun, canRun, running, result, error} = props;
    const {score, band} = result ? extractScore(result) : {score: null, band: null};
    const gaps = result?.gaps;
    const missing = gaps?.missing_tables ?? [];
    const empty = gaps?.empty_tables ?? [];

    return (
        <div className='pane-section'>
            <div className='pane-header'>{'🧠 Models'}</div>
            <ul className='roster'>
                {models.map((m) => (
                    <li
                        key={m.package}
                        className={
                            'roster-item' +
                            (m.package === selected ? ' selected' : '') +
                            (m.live ? '' : ' dead')
                        }
                        onClick={() => m.live && onSelect(m.package)}
                        title={m.live ? m.endpoint_url ?? '' : 'endpoint not running'}
                    >
                        <div className='roster-main'>
                            {/* version in the title line: several packages can share an
                                endpoint_name (v0002 vs v0003) and must be distinguishable */}
                            <span className='roster-id'>
                                {(m.endpoint_name ?? m.package) + ' ' + (m.endpoint_version ?? '?')}
                            </span>
                            <span className={'dot ' + (m.live ? 'live' : 'down')} />
                        </div>
                        <div className='roster-sub'>
                            {(m.live ? m.required_tables.length + ' tables' : 'endpoint not running')}
                        </div>
                    </li>
                ))}
            </ul>

            <button
                className='run-btn'
                disabled={!canRun || running}
                onClick={onRun}
            >
                {running ? '⏳ Predicting…' : '▶ Run prediction'}
            </button>
            <div className='roster-sub center'>{'deterministic · no LLM'}</div>

            {error && <div className='alert error'>{error}</div>}

            {result && score !== null && (
                <div className='score-card'>
                    <div className='score-value'>{score.toFixed(4)}</div>
                    <div className={'score-band band-' + (band ?? '').toLowerCase()}>
                        {band ?? '—'}
                    </div>
                    <div className='roster-sub center'>{'verbatim from the endpoint'}</div>

                    {(missing.length > 0 || empty.length > 0) && (
                        <div className='alert warn'>
                            <strong>{'⚠️ Data gaps'}</strong>
                            {missing.length > 0 && (
                                <div>{'missing: ' + missing.join(', ')}</div>
                            )}
                            {empty.length > 0 && <div>{'empty: ' + empty.join(', ')}</div>}
                            <div className='roster-sub'>
                                {'the model still scored — treat as partial data'}
                            </div>
                        </div>
                    )}
                    {result.trigger && (
                        <div className='roster-sub'>
                            {'as-of: ' + String(result.trigger.record.ObsDT ?? '—')}
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
