/* AnnotateView — the GROUP orientation's labeling FORGE.
 *
 * Orientation matters: in group mode the CORPUS is fixed and the GUIDELINE is the
 * variable — you are forging a labeling instrument against the corpus, not reading
 * one person's label off a finished rubric (that is the individual READOUT). So this
 * view is not a report card; it is a development bench with STATE, VERSIONS, and a
 * CONVERGENCE criterion:
 *
 *   seed (init) → iterate (probe→panel→analyze→conflicts) → validate (κ) → scale
 *
 * The researcher is the PI/adjudicator, not a bulk labeler. Each ▶ step is HANDED TO
 * HaiChat (onRunStep) — the agent runs the matching /sl-* skill in lab mode, narrates,
 * and its writes pass the Allow gate. The ONLY write from this view itself is the PI's
 * decision on a surfaced conflict (human_decisions.jsonl). Everything else here —
 * guideline, gallery, κ trajectory — is the artifact the loop produces, read back.
 */
import {useCallback, useEffect, useState} from 'react';

interface DimSummary {
    dim: string;
    topic?: string;
    status: string;
    iteration?: number;
    guideline_version?: number;
    gallery_size?: number;
    labels: string[];
    kappa?: number;
    next?: string;
}

interface GalleryItem {
    id: string;
    text: string;
    label: string;
    reasoning?: string;
    difficulty?: string;
    provenance?: string;
    added_iteration?: number;
    platform?: string;
}

interface InboxItem {
    kind: 'residual' | 'next-step';
    case_ref: string;
    ask: string;
    resolved: boolean;
}

interface Decision {
    at: string;
    origin: string;
    case_ref: string;
    ask: string;
    decision: string;
    note?: string;
}

interface TrajectoryRow {
    version?: string;
    kappa?: number;
    acc?: number;
    kappa_majority_vs_gold?: number;
    acc_majority_vs_gold?: number;
    panel_kappa_claude_vs_codex?: number;
}

interface DimDetail extends DimSummary {
    state: Record<string, unknown> & {
        last_validation?: {verdict?: string; dataset?: string; agent_vs_human_kappa?: number};
    };
    guideline: {current: string | null; versions: string[]; text: string};
    changelog: string;
    trajectory: TrajectoryRow[];
    gallery: {items?: GalleryItem[]};
    inbox: InboxItem[];
    decisions: Decision[];
    error?: string;
}

interface Props {
    dataset: string | null;
    nHumans: number;
    onRunStep: (prompt: string) => void;
    embedded: boolean;
}

/** The sl loop as the forge's stage bar. Order == the development pipeline. */
const STAGES = [
    {key: 'init', label: 'seed', icon: '🌱', cmd: '/sl-init',
        hint: 'cold-start — recommend a dimension, elicit intent, seed guideline V0 (~60 anchors)'},
    {key: 'iterate', label: 'iterate', icon: '🔁', cmd: '/sl-iterate',
        hint: 'one round — probe → panel labels → analyze → surface conflicts → refine the guideline'},
    {key: 'validate', label: 'validate', icon: '📐', cmd: '/sl-validate',
        hint: 'benchmark the gallery against a public dataset — κ vs human consensus'},
    {key: 'scale', label: 'scale', icon: '📤', cmd: '/sl-scale',
        hint: 'batch-label the whole corpus with the converged gallery'},
] as const;

export default function AnnotateView({dataset, nHumans, onRunStep, embedded}: Props) {
    const [dims, setDims] = useState<DimSummary[] | null>(null);
    const [reason, setReason] = useState<string | null>(null);
    const [active, setActive] = useState<string | null>(null);
    const [detail, setDetail] = useState<DimDetail | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [notes, setNotes] = useState<Record<string, string>>({});
    const [posting, setPosting] = useState<string | null>(null);
    const [gVersion, setGVersion] = useState<string | null>(null);
    const [gText, setGText] = useState<string | null>(null);

    /** every labeling call is scoped to the active dataset — the labeling project
     *  follows the data type, so switching datasets swaps the dimensions. */
    const dsq = dataset ? '?dataset=' + encodeURIComponent(dataset) : '';
    const ds = dataset ?? 'this corpus';

    useEffect(() => {
        setDims(null);
        setActive(null);
        setDetail(null);
        setError(null);
        fetch('/api/labeling/dimensions' + dsq)
            .then((r) => r.json())
            .then((d) => {
                setDims(d.dimensions ?? []);
                setReason(d.reason ?? null);
                if (d.dimensions?.length) {
                    setActive(d.dimensions[0].dim);
                }
            })
            .catch(() => setError('failed to reach /api/labeling'));
    }, [dsq]);

    useEffect(() => {
        if (!active) {
            return;
        }
        setDetail(null);
        setGVersion(null);
        setGText(null);
        fetch('/api/labeling/' + active + dsq)
            .then((r) => r.json())
            .then((d) => (d.error ? setError(d.error) : setDetail(d)))
            .catch(() => setError('failed to load ' + active));
    }, [active, dsq]);

    /* older guideline versions on demand; the current one rides in the detail */
    const showVersion = useCallback((v: string) => {
        setGVersion(v);
        setGText(null);
        if (!detail) {
            return;
        }
        if (v === detail.guideline.current) {
            setGText(detail.guideline.text);
            return;
        }
        fetch('/api/labeling/' + detail.dim + '/guideline/' + v + dsq)
            .then((r) => r.json())
            .then((d) => setGText(d.text ?? d.error ?? ''))
            .catch(() => setGText('failed to load ' + v));
    }, [detail, dsq]);

    const decide = useCallback((item: InboxItem, decision: string) => {
        if (!detail) {
            return;
        }
        setPosting(item.case_ref);
        fetch('/api/labeling/' + detail.dim + '/decision', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                case_ref: item.case_ref,
                ask: item.ask,
                decision,
                note: notes[item.case_ref] ?? '',
                dataset,
            }),
        })
            .then((r) => r.json())
            .then((d) => {
                setPosting(null);
                if (d.error) {
                    setError(d.error);
                    return;
                }
                setDetail((old) => (old ? {
                    ...old,
                    inbox: old.inbox.map((x) =>
                        (x.case_ref === item.case_ref ? {...x, resolved: true} : x)),
                    decisions: [...old.decisions, d.decision],
                } : old));
            })
            .catch(() => setPosting(null));
    }, [detail, notes, dataset]);

    /* one line of project context, so the agent targets the right dimension folder */
    const ctx = useCallback((verb: string) =>
        `On the "${ds}" corpus (${nHumans} humans), subjective-labeling dimension ` +
        `"${detail?.dim ?? '?'}"` +
        (detail ? ` — status ${detail.status}, iter ${detail.iteration ?? 0}, ` +
            `guideline ${detail.guideline.current ?? 'none'}, κ ${detail.kappa ?? '—'}. ` : '. ') +
        verb, [ds, nHumans, detail]);

    const startProject = useCallback(() => onRunStep(
        `I want to start a subjective-labeling project on the "${ds}" corpus (${nHumans} humans). ` +
        `Run /sl-init: read this data, recommend a few subjective dimensions worth labeling, then ` +
        `help me pick one and cold-start it (elicit what I care about, seed ~60 anchors, draft ` +
        `guideline V0). Ask me before you label anything — I adjudicate, I don't bulk-label.`,
    ), [ds, nHumans, onRunStep]);

    if (error) {
        return <div className='view-scroll'><div className='alert error'>{error}</div></div>;
    }
    if (!dims) {
        return <div className='view-scroll muted'>{'Loading the labeling forge…'}</div>;
    }

    /* ── EMPTY STATE: no instrument yet for this corpus → START one ─────────────── */
    if (dims.length === 0) {
        return (
            <div className='view-scroll'>
                <div className='fg-start'>
                    <div className='fg-start-icon'>{'✏️'}</div>
                    <div className='fg-start-title'>{'The labeling forge'}</div>
                    <div className='fg-start-sub'>
                        {'No labeling instrument exists for '}<b>{ds}</b>{' yet. In group mode you ' +
                        'don’t read one person’s label — you FORGE a guideline against the whole ' +
                        'corpus: recommend a dimension, seed anchors, iterate on conflicts, validate ' +
                        'against public κ, then scale.'}
                    </div>
                    <button
                        className='run-btn fg-start-btn'
                        disabled={embedded}
                        onClick={startProject}
                    >
                        {'▶ Start labeling ' + ds}
                    </button>
                    <div className='roster-sub fg-start-foot'>
                        {embedded
                            ? 'Embedded beside a thread — start the loop from the HaiChat thread itself.'
                            : reason ?? 'HaiChat runs /sl-init in lab mode, then walks the loop with you.'}
                    </div>
                </div>
            </div>
        );
    }

    /* ── how far the instrument has progressed, from real artifacts ────────────── */
    const iterN = detail?.iteration ?? 0;
    const validated = Boolean(detail?.state?.last_validation?.verdict);
    const scaled = detail?.status === 'scaled';
    const reached = scaled ? 3 : validated ? 2 : iterN >= 1 ? 1 : detail?.guideline.current ? 0 : -1;
    const nextStr = (detail?.next ?? '').toLowerCase();
    const recommended =
        nextStr.includes('scale') ? 3
            : nextStr.includes('validat') ? 2
                : nextStr.includes('iterat') ? 1
                    : nextStr.includes('init') || nextStr.includes('seed') ? 0
                        : Math.min(reached + 1, 3);

    const gallery = detail?.gallery?.items ?? [];
    const sections: Record<string, GalleryItem[]> = {};
    for (const g of gallery) {
        (sections[g.label] ??= []).push(g);
    }
    const traj = (detail?.trajectory ?? []).map((t) => ({
        version: t.version ?? '—',
        kappa: t.kappa ?? t.kappa_majority_vs_gold,
        acc: t.acc ?? t.acc_majority_vs_gold,
        panel: t.panel_kappa_claude_vs_codex,
    }));
    const pending = (detail?.inbox ?? []).filter((i) => i.kind === 'residual');
    const version = gVersion ?? detail?.guideline.current ?? null;
    const versionText = gVersion ? gText : detail?.guideline.text;

    return (
        <div className='raw'>
            <div className='raw-tabs'>
                {dims.map((d) => (
                    <button
                        key={d.dim}
                        className={'raw-tab' + (d.dim === active ? ' active' : '')}
                        onClick={() => setActive(d.dim)}
                        title={d.topic}
                    >
                        {'✏️ ' + d.dim.replace(/^B\d+_dim_/, '')}
                        {d.kappa !== undefined && <span className='badge'>{'κ ' + d.kappa}</span>}
                    </button>
                ))}
                <button
                    className='raw-tab fg-new'
                    disabled={embedded}
                    onClick={startProject}
                    title='forge a new dimension on this corpus'
                >{'＋ new'}</button>
            </div>

            {!detail ? <div className='muted pad'>{'Loading ' + active + '…'}</div> : (
                <div className='view-scroll'>
                    {detail.topic && <div className='roster-sub lb-topic'>{detail.topic}</div>}

                    <div className='lb-strip'>
                        <span className='roster-sub'>{'👥 ' + ds + ' · ' + nHumans + ' humans'}</span>
                        <span className={'badge lb-status-' + detail.status}>{detail.status}</span>
                        {detail.iteration !== undefined && <span className='badge'>{'iter ' + detail.iteration}</span>}
                        {detail.guideline.current && <span className='badge'>{'guideline ' + detail.guideline.current}</span>}
                        <span className='badge'>{'gallery ' + (detail.gallery_size ?? gallery.length)}</span>
                        {detail.state.last_validation?.verdict && (
                            <span className='chip' title={'vs ' + detail.state.last_validation.dataset}>
                                {detail.state.last_validation.verdict}
                            </span>
                        )}
                    </div>

                    {/* ── THE LOOP (the figure) ──────────────────────────────── */}
                    <div className='pane-header lb-h'>{'🔨 the loop'}</div>
                    <div className='fg-stages'>
                        {STAGES.map((s, i) => {
                            const done = i <= reached;
                            const rec = i === recommended;
                            return (
                                <button
                                    key={s.key}
                                    className={'fg-stage' + (done ? ' done' : '') + (rec ? ' rec' : '')}
                                    disabled={embedded}
                                    title={s.hint + '  —  runs ' + s.cmd + ' through HaiChat'}
                                    onClick={() => onRunStep(ctx('Run ' + s.cmd + '.'))}
                                >
                                    <span className='fg-stage-icon'>{done ? '✓' : s.icon}</span>
                                    <span className='fg-stage-label'>{s.label}</span>
                                    {rec && <span className='fg-stage-next'>{'▶ next'}</span>}
                                </button>
                            );
                        })}
                        <button
                            className='fg-stage ghost'
                            disabled={embedded}
                            title='where does this project stand? — runs /sl-status'
                            onClick={() => onRunStep(ctx('Run /sl-status and summarize where this stands.'))}
                        >{'🔄 status'}</button>
                    </div>
                    <div className='roster-sub fg-loop-foot'>
                        {embedded
                            ? 'Embedded — drive the loop from the HaiChat thread.'
                            : detail.next
                                ? 'suggested next: ' + detail.next + ' — a step ▶ hands the skill to HaiChat; you adjudicate, it labels.'
                                : 'a step ▶ hands the matching /sl-* skill to HaiChat; you adjudicate, it labels.'}
                    </div>

                    {/* ── CONFLICTS NEEDING THE PI (human upstream of the instrument) ── */}
                    <div className='pane-header lb-h'>
                        {'⚖️ conflicts needing you (' + pending.filter((p) => !p.resolved).length + ')'}
                    </div>
                    <div className='cl-list lb-pad'>
                        {pending.length === 0 && (
                            <div className='roster-sub'>
                                {'nothing to adjudicate — the panel has no unresolved boundary cases. ' +
                                'Run 🔁 iterate to surface the next round.'}
                            </div>
                        )}
                        {pending.map((item) => (
                            <div key={item.case_ref} className={'cl-item' + (item.resolved ? ' done' : '')}>
                                <div className='cl-body'>
                                    <div className='cl-title'>{item.case_ref}</div>
                                    {!item.resolved && (
                                        <div className='lb-decide'>
                                            {(detail.labels.length ? detail.labels : ['agree', 'disagree']).map((lb) => (
                                                <button
                                                    key={lb}
                                                    className='run-btn ghost lb-label-btn'
                                                    disabled={posting === item.case_ref}
                                                    onClick={() => decide(item, lb)}
                                                >
                                                    {lb}
                                                </button>
                                            ))}
                                            <input
                                                className='case-search lb-note'
                                                placeholder='why (optional — lands in the audit log)'
                                                value={notes[item.case_ref] ?? ''}
                                                onChange={(e) => setNotes((n) => ({...n, [item.case_ref]: e.target.value}))}
                                            />
                                        </div>
                                    )}
                                    {item.resolved && (
                                        <div className='cl-meta'>
                                            {'decided: ' +
                                                (detail.decisions.filter((x) => x.case_ref === item.case_ref).slice(-1)[0]?.decision ?? '—')}
                                        </div>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>

                    {detail.decisions.length > 0 && (
                        <>
                            <div className='pane-header lb-h'>{'🧾 your rulings (audit)'}</div>
                            <div className='lb-pad'>
                                {detail.decisions.slice(-5).reverse().map((x, i) => (
                                    <div key={i} className='roster-sub'>
                                        <code>{x.at}</code>
                                        {' · ' + x.case_ref + ' → '}
                                        <b>{x.decision}</b>
                                        {x.note ? ' — ' + x.note : ''}
                                    </div>
                                ))}
                            </div>
                        </>
                    )}

                    {/* ── THE INSTRUMENT: guideline is the figure ─────────────── */}
                    <div className='pane-header lb-h'>{'📜 guideline — the instrument being forged'}</div>
                    <div className='raw-tabs lb-pad'>
                        {detail.guideline.versions.length === 0 && (
                            <span className='roster-sub'>{'no versions yet — run 🌱 seed to draft V0'}</span>
                        )}
                        {detail.guideline.versions.map((v) => (
                            <button
                                key={v}
                                className={'raw-tab' + (v === version ? ' active' : '')}
                                onClick={() => showVersion(v)}
                            >
                                {v}
                                {v === detail.guideline.current ? ' ●' : ''}
                            </button>
                        ))}
                    </div>
                    <div className='lb-pad'>
                        <pre className='lb-pre fg-guideline'>{versionText ?? 'loading…'}</pre>
                    </div>

                    {/* ── GALLERY as SECTIONS, not a table ────────────────────── */}
                    <div className='pane-header lb-h'>
                        {'🖼️ gallery — the ground truth, by label'}
                    </div>
                    {gallery.length === 0 && (
                        <div className='roster-sub lb-pad'>{'empty — the gallery fills as you iterate'}</div>
                    )}
                    {Object.entries(sections).map(([label, items]) => (
                        <div key={label} className='fg-section'>
                            <div className='fg-section-head'>
                                <span className={'badge label-' + label.toLowerCase()}>{label}</span>
                                <span className='roster-sub'>{items.length + ' anchors'}</span>
                            </div>
                            {items.slice(0, 8).map((g) => (
                                <div key={g.id} className='fg-card'>
                                    <div className='fg-card-head'>
                                        <code className='case-id'>{g.id}</code>
                                        {g.difficulty && <span className='chip'>{g.difficulty}</span>}
                                        {g.added_iteration !== undefined && (
                                            <span className='roster-sub'>{'iter ' + g.added_iteration}</span>
                                        )}
                                    </div>
                                    <div className='case-text'>{g.text}</div>
                                    {g.reasoning && <div className='cl-meta fg-why'>{g.reasoning}</div>}
                                </div>
                            ))}
                            {items.length > 8 && (
                                <div className='roster-sub fg-more'>{'+ ' + (items.length - 8) + ' more'}</div>
                            )}
                        </div>
                    ))}

                    {/* ── EVIDENCE: κ trajectory + what each step did ─────────── */}
                    {(traj.length > 0 || detail.changelog) && (
                        <div className='lb-cols'>
                            {traj.length > 0 && (
                                <div>
                                    <div className='pane-header lb-h'>{'📈 κ trajectory (evidence)'}</div>
                                    <table className='health-table lb-table'>
                                        <thead>
                                            <tr><th>{'version'}</th><th>{'κ vs gold'}</th><th>{'acc'}</th><th>{'panel κ'}</th></tr>
                                        </thead>
                                        <tbody>
                                            {traj.map((t, i) => (
                                                <tr key={i}>
                                                    <td>{t.version}</td>
                                                    <td>{t.kappa ?? '—'}</td>
                                                    <td>{t.acc ?? '—'}</td>
                                                    <td>{t.panel ?? '—'}</td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            )}
                            {detail.changelog && (
                                <div>
                                    <div className='pane-header lb-h'>{'🧾 report — what each step did'}</div>
                                    <pre className='lb-pre'>{detail.changelog}</pre>
                                </div>
                            )}
                        </div>
                    )}

                    <div className='raw-foot roster-sub'>
                        {'the panel labels, the PI adjudicates. Every ▶ step runs the matching /sl-* skill ' +
                        'through HaiChat (lab mode) — this view reads the project and records your rulings.'}
                    </div>
                </div>
            )}
        </div>
    );
}
