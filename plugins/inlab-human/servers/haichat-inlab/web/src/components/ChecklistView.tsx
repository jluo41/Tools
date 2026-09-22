/* ChecklistView — the ACTION group's working surface.
 *
 * After reading the record (DATA) and the signals (INSIGHT), this turns them into
 * next steps: important AND doable. Each item names one concrete step, its owner,
 * the effort, and the fact from the record that prompted it — so a reader can
 * check it off, or reject it, without re-deriving why it is there.
 *
 * The score is never re-estimated here. Generation is context-fed (POST
 * /api/checklist assembles the chart with the same engine the ▶ Run button uses),
 * so the model gets no tools and there is nothing to approve.
 */
import {useState} from 'react';

import type {Checklist, ChecklistItem, RunRecord} from '../types';

/* Fully CONTROLLED. The checklist, its ticks, AND its generation all live in
 * useConsole — the view only renders. Two reasons: dragging this tab into the other
 * split group remounts it (a generated checklist is too expensive to lose to a layout
 * change), and HaiChat can ask for a checklist through the same `checklist/generate`
 * action the ✨ button dispatches — one generator, one prompt, one set of guardrails. */
interface Props {
    patientId: string | null;
    lastRun: RunRecord | null;
    checklist: Checklist | null;
    done: Set<number>;
    busy: boolean;
    onGenerate: () => void;
    onToggle: (i: number) => void;
}

const PRIO_ORDER = {high: 0, medium: 1, low: 2} as const;

function toMarkdown(cl: Checklist, done: Set<number>): string {
    const lines = [`# Checklist — ${cl.patient_id}`, `_as of ${cl.basis.index_date ?? '—'}_`, ''];
    cl.items.forEach((it, i) => {
        lines.push(`- [${done.has(i) ? 'x' : ' '}] **${it.title}** _(${it.priority} · ${it.owner} · ${it.effort})_`);
        lines.push(`      ${it.why}`);
    });
    if (cl.caveats.length) {
        lines.push('', '## Caveats', ...cl.caveats.map((c) => `- ${c}`));
    }
    return lines.join('\n');
}

export default function ChecklistView(props: Props) {
    const {patientId, lastRun, checklist: cl, done, busy, onGenerate, onToggle} = props;
    const [copied, setCopied] = useState(false);

    function copy() {
        if (!cl) {
            return;
        }
        navigator.clipboard?.writeText(toMarkdown(cl, done)).then(() => {
            setCopied(true);
            setTimeout(() => setCopied(false), 1500);
        });
    }

    if (!patientId) {
        return (
            <div className='view-scroll muted'>
                {'Select a patient — a checklist is written for one patient at a time.'}
            </div>
        );
    }

    const items: (ChecklistItem & {i: number})[] = (cl?.items ?? [])
        .map((it, i) => ({...it, i}))
        .sort((a, b) => (PRIO_ORDER[a.priority] ?? 3) - (PRIO_ORDER[b.priority] ?? 3));

    return (
        <div className='view-scroll'>
            <div className='cl-bar'>
                <div>
                    <div className='pane-header'>{'✅ Checklist'}</div>
                    <div className='roster-sub'>
                        {'Written from this patient’s record'}
                        {lastRun && lastRun.status === 'ok'
                            ? ' + the ' + lastRun.model_label + ' run (' +
                              (lastRun.score?.toFixed(4) ?? '—') + ' ' + (lastRun.band ?? '') + ')'
                            : ' — run a model first to fold the score and its data gaps in'}
                    </div>
                </div>
                <div className='cl-bar-btns'>
                    {cl && (
                        <button className='run-btn ghost cl-btn' onClick={copy}>
                            {copied ? '✓ copied' : '⧉ copy'}
                        </button>
                    )}
                    <button className='run-btn cl-btn' disabled={busy} onClick={onGenerate}>
                        {busy ? '⏳ Writing…' : cl ? '↻ Regenerate' : '✨ Generate checklist'}
                    </button>
                </div>
            </div>

            {!cl && !busy && (
                <div className='stub-card'>
                    <div className='roster-sub'>
                        {'Generates 3–7 items that are important and doable: each one names a '}
                        {'concrete step, who does it, and the fact in the record that prompted it. '}
                        {'Data gaps that could distort a score come first.'}
                    </div>
                    <div className='roster-sub'>
                        {'De-identified research data — review / verify / monitor steps only, '}
                        {'never treatment.'}
                    </div>
                </div>
            )}

            {cl && (
                <>
                    <div className='cl-list'>
                        {items.map((it) => (
                            <label
                                key={it.i}
                                className={'cl-item' + (done.has(it.i) ? ' done' : '')}
                            >
                                <input
                                    type='checkbox'
                                    checked={done.has(it.i)}
                                    onChange={() => onToggle(it.i)}
                                />
                                <div className='cl-body'>
                                    <div className='cl-title'>
                                        {it.title}
                                        <span className={'cl-prio ' + it.priority}>{it.priority}</span>
                                        <span className='badge'>{it.category}</span>
                                    </div>
                                    <div className='roster-sub'>{it.why}</div>
                                    <div className='cl-meta'>
                                        {'👤 ' + it.owner + ' · ⏱ ' + it.effort}
                                    </div>
                                </div>
                            </label>
                        ))}
                    </div>

                    <div className='cl-foot'>
                        <span className='roster-sub'>
                            {done.size + ' / ' + cl.items.length + ' done'}
                        </span>
                        {cl.basis.empty_tables.length > 0 && (
                            <span className='roster-sub'>
                                {'· empty at run: ' + cl.basis.empty_tables.join(', ')}
                            </span>
                        )}
                    </div>

                    {cl.caveats.length > 0 && (
                        <div className='alert warn'>
                            <strong>{'⚠️ Caveats'}</strong>
                            {cl.caveats.map((c, i) => <div key={i}>{'· ' + c}</div>)}
                        </div>
                    )}
                </>
            )}
        </div>
    );
}
