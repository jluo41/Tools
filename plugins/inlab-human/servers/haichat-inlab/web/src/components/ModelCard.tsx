/* ModelCard — what this endpoint IS: what it predicts, what it eats, what it was
 * trained on, and how it turns a patient into a case.
 *
 * Every field is read from the package's own files (manifest / meta / model config /
 * prefn config) — nothing is hand-written per model, so a card cannot drift from the
 * artifact it describes.
 *
 * The card is deliberately blunt about the inference MODE: a rolled-out forecast and a
 * teacher-forced reconstruction look alike in a chart and are not remotely the same
 * claim.
 */
import {useEffect, useState} from 'react';

import type {ModelCardData} from '../types';

interface Props {
    pkg: string | null;
}

function Row({k, v}: {k: string; v: unknown}) {
    if (v === null || v === undefined || v === '' ||
        (Array.isArray(v) && v.length === 0)) {
        return null;
    }
    const text = Array.isArray(v)
        ? v.join(', ')
        : typeof v === 'object'
            ? Object.entries(v as object).map(([a, b]) => `${a}=${b}`).join(' · ')
            : String(v);
    return (
        <tr>
            <td className='mc-k'>{k}</td>
            <td className='mc-v'>{text}</td>
        </tr>
    );
}

export default function ModelCard({pkg}: Props) {
    const [card, setCard] = useState<ModelCardData | null>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (!pkg) {
            setCard(null);
            return;
        }
        setError(null);
        setCard(null);
        fetch(`/api/models/${pkg}/card`)
            .then((r) => r.json())
            .then((d) => (d.error ? setError(d.error) : setCard(d)))
            .catch(() => setError('failed to load the model card'));
    }, [pkg]);

    if (!pkg) {
        return <div className='muted pad'>{'← pick a model'}</div>;
    }
    if (error) {
        return <div className='alert error'>{error}</div>;
    }
    if (!card) {
        return <div className='muted pad'>{'Loading model card…'}</div>;
    }

    const p = card.prediction ?? {};
    const t = card.training ?? {};
    const cs = card.case ?? {};
    const pl = card.payload ?? {};
    const rolled = p.mode === 'forecast';

    return (
        <div className='mc'>
            <div className='mc-head'>
                <span className='mc-title'>{card.endpoint_name + ' ' + card.endpoint_version}</span>
                <span className={'dot ' + (card.endpoint_url ? 'live' : 'down')}/>
                <span className='roster-sub'>{card.endpoint_url ?? 'not served'}</span>
            </div>

            {/* the claim the number makes — the single most misreadable thing about a model */}
            <div className={'mc-mode ' + (rolled ? 'ok' : 'warn')}>
                {rolled ? (
                    <>
                        <strong>{'🔮 Autoregressive forecast'}</strong>
                        <div>
                            {'Sees ' + p.context_steps + ' bins (' +
                             ((p.context_steps ?? 0) * 5 / 60).toFixed(0) + 'h) of history, then rolls forward ' +
                             p.horizon_steps + ' steps (' +
                             ((p.horizon_steps ?? 0) * 5 / 60).toFixed(0) + 'h) feeding its OWN predictions back in. ' +
                             'It is never shown the values it predicts.'}
                        </div>
                    </>
                ) : (
                    <>
                        <strong>{'⚠️ Teacher-forced (eval path — not a forecast)'}</strong>
                        <div>
                            {'Predicts the next 5 minutes at every position from the TRUE values up to ' +
                             'that point. Reads beautifully in a chart; is not a forecast.'}
                        </div>
                    </>
                )}
            </div>

            <div className='pane-header'>{'🎯 Prediction'}</div>
            <table className='mc-table'>
                <tbody>
                    <Row k='type' v={p.type}/>
                    <Row k='unit' v={p.unit}/>
                    <Row k='horizon' v={p.horizon_steps ? `${p.horizon_steps} steps × ${p.interval_minutes} min = ${(p.horizon_steps * 5) / 60} h` : null}/>
                    <Row k='context' v={p.context_steps ? `${p.context_steps} bins = ${(p.context_steps * 5) / 60} h` : null}/>
                </tbody>
            </table>

            <div className='pane-header'>{'📚 Trained on'}</div>
            <table className='mc-table'>
                <tbody>
                    <Row k='AIData' v={t.aidata}/>
                    <Row k='ModelInstance' v={t.modelinstance}/>
                    <Row k='tuner' v={t.tuner}/>
                    <Row k='base model' v={t.base_model}/>
                    <Row k='architecture' v={t.architecture}/>
                    <Row k='seq length' v={t.max_seq_length}/>
                    <Row k='value range' v={t.value_range}/>
                </tbody>
            </table>

            <div className='pane-header'>{'🧩 Case construction'}</div>
            <table className='mc-table'>
                <tbody>
                    <Row k='CaseFns' v={cs.casefns}/>
                    <Row k='trigger' v={cs.trigger}/>
                    <Row k='anchor (obs_dt_index)' v={cs.obs_dt_index}/>
                    <Row k='min segment' v={cs.min_segment_length}/>
                    <Row k='max gap' v={cs.max_consecutive_missing}/>
                    <Row k='stride' v={cs.stride}/>
                    <Row k='patient registry' v={cs.patient_registry}/>
                </tbody>
            </table>

            <div className='pane-header'>{'📦 Payload'}</div>
            <table className='mc-table'>
                <tbody>
                    <Row k='style' v={pl.style}/>
                    <Row k='models field' v={pl.models_field}/>
                    <Row k='required tables' v={pl.required_tables}/>
                    <Row k='optional tables' v={pl.optional_tables}/>
                </tbody>
            </table>
            {pl.style === 'cgm_columnar' && (
                <pre className='mc-pre'>{`{
  "models": ["${pl.models_field}"],
  "CGM":  {"PatientID": [...], "ObservationDateTime": [...], "BGValue": [...], ...},
  "Ptt":  {"PatientID": [...], ...},
  "Diet": {...}, "Medication": {...}, "Exercise": {...}
}`}</pre>
            )}

            <div className='pane-header'>{'⚙️ Inference functions'}</div>
            <table className='mc-table'>
                <tbody>
                    {Object.entries(card.inference_functions ?? {}).map(([k, v]) => (
                        <Row key={k} k={k} v={v}/>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
