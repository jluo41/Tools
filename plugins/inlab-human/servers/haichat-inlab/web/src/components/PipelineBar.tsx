/* PipelineBar — the whole per-patient pipeline as ONE row of buttons.
 *
 *   [▶ Run endpoint_… ] │ [🔍 Interpret] [✉️ Message] [⚖️ Judge] [🩺 Feedback]
 *    deterministic·no LLM         └──────── LLM ────────┘        └─ human ─┘
 *
 * Left of the divider is the endpoint's own number, produced without an LLM.
 * Everything right of it is downstream of that number and each step is gated on
 * the one before, so the bar reads as the flow it is.
 *
 * ①→② and ②→③ cross a wall: the composer and the judge are handed the forecast
 * with `observed` stripped server-side (message_api._blind). A message written
 * with hindsight is not the message a patient would have received.
 *
 * Interpret and Message are the SAME engine with a different persona — care
 * provider vs patient — because the two audiences want opposite registers from
 * the identical forecast.
 */
import {useEffect, useState} from 'react';

import type {RunRecord} from '../types';

interface PersonaInfo {
    name: string;
    audience?: string | null;
    tone?: string | null;
    dimensions?: string[];
    safety_rules?: string[];
}

interface Composed {
    slot: string;
    persona: string;
    nl: string;
    report: Record<string, unknown>;
    prompt: string;
    error?: string;
}

interface Judged {
    rubric: string;
    dimensions: string[];
    judgment: Record<string, unknown>;
    raw?: string | null;
    error?: string;
}

interface Props {
    patientId: string | null;
    run: RunRecord | null;
    onRun: () => void;
    canRun: boolean;
    running: boolean;
    runLabel: string;
    disabledReason?: string | null;
}

/** Judge schemas nest as {…: {dimension: [{name, score, reasoning}]}} — dig for the
 *  first `dimension` array rather than trusting a shape an LLM authored. */
function dimensionsOf(j: Record<string, unknown> | null) {
    if (!j) {
        return [];
    }
    const stack: unknown[] = [j];
    while (stack.length) {
        const cur = stack.pop();
        if (!cur || typeof cur !== 'object') {
            continue;
        }
        const rec = cur as Record<string, unknown>;
        const d = rec.dimension;
        if (Array.isArray(d)) {
            return d.map((x) => {
                const r = (x ?? {}) as Record<string, unknown>;
                return {
                    name: String(r.name ?? '—'),
                    score: String(r.score ?? '—'),
                    reasoning: String(r.reasoning ?? ''),
                };
            });
        }
        for (const v of Object.values(rec)) {
            stack.push(v);
        }
    }
    return [];
}

function scoreClass(s: string): string {
    const n = Number(s);
    return !Number.isFinite(n) ? '' : n >= 4 ? ' good' : n >= 3 ? ' fair' : ' poor';
}

export default function PipelineBar(props: Props) {
    const {patientId, run, onRun, canRun, running, runLabel, disabledReason} = props;

    const [personas, setPersonas] = useState<{message: PersonaInfo[]; judge: PersonaInfo[]} | null>(null);
    const [interp, setInterp] = useState<Composed | null>(null);
    const [msg, setMsg] = useState<Composed | null>(null);
    const [judged, setJudged] = useState<Judged | null>(null);
    const [busy, setBusy] = useState('');
    const [err, setErr] = useState<string | null>(null);
    const [open, setOpen] = useState<string | null>(null);
    const [note, setNote] = useState('');
    const [saved, setSaved] = useState<string | null>(null);
    const [rubric, setRubric] = useState('patient-comprehension');

    useEffect(() => {
        fetch('/api/personas').then((r) => r.json()).then(setPersonas).catch(() => undefined);
    }, []);

    /* a new run invalidates everything downstream — they describe the previous one */
    useEffect(() => {
        setInterp(null);
        setMsg(null);
        setJudged(null);
        setSaved(null);
        setErr(null);
        setOpen(null);
    }, [run?.id, patientId]);

    const runRef = run && patientId ? `${patientId}-run${run.id}` : null;
    const havePrediction = Boolean(run?.result?.response && runRef);

    /** pick the first persona whose audience matches, else the named fallback */
    function personaFor(audience: string, fallback: string): string {
        const hit = (personas?.message ?? []).find((p) =>
            (p.audience ?? '').toLowerCase().startsWith(audience));
        return hit?.name ?? fallback;
    }

    async function compose(slot: 'interpretation' | 'message') {
        if (!havePrediction) {
            return;
        }
        const persona = slot === 'interpretation'
            ? personaFor('care', 'clinician-brief')
            : personaFor('patient', 'patient-friendly');
        setBusy(slot);
        setErr(null);
        try {
            const r = await fetch('/api/message', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    patient_id: patientId, persona, slot, run_ref: runRef,
                    anchor: run?.result?.trigger?.record?.ObsDT ?? null,
                    response: run?.result?.response,
                }),
            });
            const d = await r.json();
            if (d.error) {
                setErr(d.error);
            } else if (slot === 'interpretation') {
                setInterp(d);
                setOpen('interpretation');
            } else {
                setMsg(d);
                setJudged(null);
                setOpen('message');
            }
        } catch {
            setErr(slot + ' request failed');
        } finally {
            setBusy('');
        }
    }

    async function judge() {
        if (!msg) {
            return;
        }
        setBusy('judge');
        setErr(null);
        try {
            const r = await fetch('/api/judge', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({run_ref: runRef, rubric, message: msg,
                    response: run?.result?.response}),
            });
            const d = await r.json();
            if (d.error) {
                setErr(d.error);
            } else {
                setJudged(d);
                setOpen('judge');
            }
        } catch {
            setErr('judge request failed');
        } finally {
            setBusy('');
        }
    }

    async function feedback(verdict: string) {
        if (!runRef) {
            return;
        }
        setBusy('feedback');
        try {
            const r = await fetch('/api/feedback', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({run_ref: runRef, verdict, note,
                    agrees_with_judge: judged ? verdict === 'agree' : null}),
            });
            const d = await r.json();
            setSaved(d.error ?? `saved · ${d.n} on file`);
            if (!d.error) {
                setNote('');
            }
        } catch {
            setSaved('feedback request failed');
        } finally {
            setBusy('');
        }
    }

    const dims = dimensionsOf(judged?.judgment ?? null);
    const step = (k: string) => (open === k ? ' open' : '');

    return (
        <div className='pipe'>
            <div className='pipe-bar'>
                <div className='pipe-left'>
                    <button
                        className='pipe-run'
                        disabled={!canRun || running || Boolean(disabledReason)}
                        onClick={onRun}
                        title={disabledReason ?? ''}
                    >
                        {running ? '⏳ Predicting…' : '▶ ' + runLabel}
                    </button>
                    <div className='pipe-cap'>{'deterministic · no LLM'}</div>
                </div>

                <div className='pipe-arrow'>{'▸'}</div>

                <div className='pipe-right'>
                    <div className='pipe-steps'>
                        <button
                            className={'pipe-step' + step('interpretation') + (interp ? ' done' : '')}
                            disabled={!havePrediction || busy !== ''}
                            onClick={() => (interp ? setOpen(open === 'interpretation' ? null : 'interpretation') : compose('interpretation'))}
                            title='a care-provider reading of this forecast'
                        >
                            {busy === 'interpretation' ? '⏳' : '🔍'}
                            {' Interpret'}
                            {interp && <span className='tick'>{'✓'}</span>}
                        </button>
                        <button
                            className={'pipe-step' + step('message') + (msg ? ' done' : '')}
                            disabled={!havePrediction || busy !== ''}
                            onClick={() => (msg ? setOpen(open === 'message' ? null : 'message') : compose('message'))}
                            title='the patient-facing message'
                        >
                            {busy === 'message' ? '⏳' : '✉️'}
                            {' Message'}
                            {msg && <span className='tick'>{'✓'}</span>}
                        </button>
                        <button
                            className={'pipe-step' + step('judge') + (judged ? ' done' : '')}
                            disabled={!msg || busy !== ''}
                            onClick={() => (judged ? setOpen(open === 'judge' ? null : 'judge') : judge())}
                            title='score the message against a rubric'
                        >
                            {busy === 'judge' ? '⏳' : '⚖️'}
                            {' Judge'}
                            {judged && <span className='tick'>{'✓'}</span>}
                        </button>
                        <button
                            className={'pipe-step' + step('feedback')}
                            disabled={!msg || busy !== ''}
                            onClick={() => setOpen(open === 'feedback' ? null : 'feedback')}
                            title='record the clinician verdict'
                        >
                            {'🩺 Feedback'}
                        </button>
                    </div>
                    <div className='pipe-cap'>
                        {'LLM · blind to ground truth'}
                        <span className='pipe-cap-human'>{' · human'}</span>
                    </div>
                </div>
            </div>

            {err && <div className='alert error'>{err}</div>}

            {open === 'interpretation' && interp && (
                <Panel
                    title={'🔍 For the care provider'}
                    sub={interp.persona}
                    nl={interp.nl}
                    prompt={interp.prompt}
                />
            )}

            {open === 'message' && msg && (
                <Panel
                    title={'✉️ For the patient'}
                    sub={msg.persona}
                    nl={msg.nl}
                    prompt={msg.prompt}
                />
            )}

            {open === 'judge' && judged && (
                <div className='pipe-panel'>
                    <div className='pipe-panel-head'>
                        <strong>{'⚖️ LLM-as-judge'}</strong>
                        <select className='msg-select' value={rubric}
                            onChange={(e) => setRubric(e.target.value)}>
                            {(personas?.judge ?? []).map((p) => (
                                <option key={p.name} value={p.name}>{p.name}</option>
                            ))}
                        </select>
                        <button className='btn tiny' onClick={judge} disabled={busy !== ''}>
                            {'re-score'}
                        </button>
                    </div>
                    {dims.length > 0 ? (
                        <table className='msg-scores'>
                            <tbody>
                                {dims.map((d) => (
                                    <tr key={d.name}>
                                        <td className='msg-dim'>{d.name}</td>
                                        <td className={'msg-score' + scoreClass(d.score)}>{d.score}</td>
                                        <td className='msg-why'>{d.reasoning}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    ) : (
                        <pre className='msg-prompt'>
                            {judged.raw || JSON.stringify(judged.judgment, null, 2)}
                        </pre>
                    )}
                </div>
            )}

            {open === 'feedback' && (
                <div className='pipe-panel'>
                    <div className='pipe-panel-head'>
                        <strong>{'🩺 Clinician feedback'}</strong>
                        <span className='roster-sub'>
                            {'append-only · this is the expert record the judge is measured against'}
                        </span>
                    </div>
                    <textarea
                        className='msg-note'
                        placeholder='what is wrong (or right) with this message?'
                        value={note}
                        onChange={(e) => setNote(e.target.value)}
                    />
                    <div className='msg-verdicts'>
                        <button className='btn ok' onClick={() => feedback('agree')} disabled={busy !== ''}>
                            {'👍 Agree'}
                        </button>
                        <button className='btn' onClick={() => feedback('disagree')} disabled={busy !== ''}>
                            {'👎 Disagree'}
                        </button>
                        <button className='btn danger' onClick={() => feedback('unsafe')} disabled={busy !== ''}>
                            {'⚠️ Unsafe'}
                        </button>
                        {saved && <span className='roster-sub'>{saved}</span>}
                    </div>
                </div>
            )}
        </div>
    );
}

function Panel({title, sub, nl, prompt}: {title: string; sub: string; nl: string; prompt: string}) {
    const [showPrompt, setShowPrompt] = useState(false);
    return (
        <div className='pipe-panel'>
            <div className='pipe-panel-head'>
                <strong>{title}</strong>
                <span className='chip'>{sub}</span>
            </div>
            <div className='msg-nl'>{nl || '(the model returned no text)'}</div>
            <button className='btn tiny' onClick={() => setShowPrompt(!showPrompt)}>
                {showPrompt ? 'hide the prompt' : 'show the exact prompt it saw'}
            </button>
            {showPrompt && <pre className='msg-prompt'>{prompt}</pre>}
        </div>
    );
}
