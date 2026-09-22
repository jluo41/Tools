/* CaseView — the DATA layer's last cut: annotation points.
 *
 * A record is one human's whole timeline; a CASE is one point sliced from it —
 * a doctor↔patient dialogue, one review, one prediction window — the unit a
 * label or a score attaches to. Cases come from the SELECTED DATASET's record
 * (data-type driven): pick ACIBench and you get conversations, PhyReview and you
 * get reviews. Labeling history (sl gallery/batch) is joined on as an overlay
 * where a case id lines up.
 *
 * The case unit is data-type specific and is formalized by a CaseFn / 3-CaseStore;
 * until that exists we read it generically off the record streams (server side).
 */
import {useEffect, useMemo, useState} from 'react';

import {LAYER_BLURB} from '../views';

interface CaseAnnotation {
    gallery?: {label?: string; difficulty?: string; reasoning?: string; added_iteration?: number};
    batch?: {gold?: string; probe?: string; iter?: string};
}

interface CaseItem {
    id: string;
    text: string;
    human_id?: string;
    stream?: string;
    meta?: Record<string, string | number>;
    annotations: Record<string, CaseAnnotation>;
}

interface CasesResp {
    source: 'record' | 'corpus' | null;
    dataset?: string;
    dims?: string[];
    n_total: number;
    n_matched?: number;
    matched: boolean | null;
    scanned_humans?: number;
    human_id?: string | null;
    reason?: string;
    cases: CaseItem[];
    error?: string;
}

interface Props {
    patientId: string | null;
    dataset: string | null;
}

/** A dialogue transcript reads as turns, not a wall of text: split on [speaker]
 *  markers and render each turn on its own line. Returns null if it isn't one. */
function turnsOf(text: string): {who: string; said: string}[] | null {
    const re = /\[([a-z_ ]+)\]\s*([^[]*)/gi;
    const turns: {who: string; said: string}[] = [];
    let m: RegExpExecArray | null;
    while ((m = re.exec(text)) !== null) {
        const said = m[2].trim();
        if (said) {
            turns.push({who: m[1].trim(), said});
        }
    }
    return turns.length >= 2 ? turns : null;
}

function CaseText({text}: {text: string}) {
    const turns = useMemo(() => turnsOf(text), [text]);
    if (!turns) {
        return <div className='case-text'>{text}</div>;
    }
    return (
        <div className='case-text dialogue'>
            {turns.map((t, i) => (
                <div key={i} className={'turn turn-' + t.who.replace(/\s+/g, '-')}>
                    <span className='turn-who'>{t.who}</span>
                    <span className='turn-said'>{t.said}</span>
                </div>
            ))}
        </div>
    );
}

export default function CaseView({patientId, dataset}: Props) {
    const [data, setData] = useState<CasesResp | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [q, setQ] = useState('');
    const [query, setQuery] = useState('');

    useEffect(() => {
        setError(null);
        setData(null);
        const p = new URLSearchParams();
        if (dataset) {
            p.set('dataset', dataset);
        }
        if (patientId) {
            p.set('human_id', patientId);
        }
        if (query) {
            p.set('q', query);
        }
        fetch('/api/cases?' + p.toString())
            .then((r) => r.json())
            .then((d) => (d.error ? setError(d.error) : setData(d)))
            .catch(() => setError('failed to load cases'));
    }, [patientId, dataset, query]);

    const blurb = LAYER_BLURB.case;
    const banner = (
        <div className='layer-banner'>
            <span className='layer-step'>{'4 · CASE'}</span>
            <code>{blurb.store}</code>
            <span className='roster-sub'>{blurb.what}</span>
        </div>
    );

    if (error) {
        return <div className='view-scroll'>{banner}<div className='alert error'>{error}</div></div>;
    }
    if (!data) {
        return <div className='view-scroll'>{banner}<div className='muted pad'>{'Loading cases…'}</div></div>;
    }
    if (!data.source) {
        return (
            <div className='view-scroll'>
                {banner}
                <div className='stub-card'>
                    <div className='pane-header'>{'📌 no case source mounted'}</div>
                    <div className='roster-sub'>{data.reason}</div>
                </div>
            </div>
        );
    }

    const streams = Array.from(new Set(data.cases.map((c) => c.stream).filter(Boolean)));

    return (
        <div className='raw'>
            {banner}

            <div className='case-bar'>
                <input
                    className='case-search'
                    placeholder='search case text… (Enter)'
                    value={q}
                    onChange={(e) => setQ(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && setQuery(q)}
                />
                {data.dataset && <span className='chip'>{data.dataset}</span>}
                <span className='badge'>
                    {(data.n_matched ?? data.cases.length) +
                        (patientId ? ' cases for this human' : ' / ' + data.n_total + ' humans')}
                </span>
                {streams.map((s) => <span key={s} className='badge'>{s}</span>)}
                {data.dims && data.dims.map((d) => <span key={d} className='chip'>{d}</span>)}
            </div>

            {!patientId && data.source === 'record' && (
                <div className='hl-note'>
                    {'browsing cases across all humans in '}
                    <code>{data.dataset}</code>
                    {' — pick a human above to see just theirs'}
                </div>
            )}
            {patientId && data.cases.length === 0 && (
                <div className='hl-note'>
                    {'this human has no record cases in '}
                    <code>{data.dataset}</code>
                </div>
            )}

            <div className='view-scroll'>
                {data.cases.map((c) => (
                    <div key={c.id} className='case-card'>
                        <div className='case-head'>
                            <code className='case-id'>{c.id}</code>
                            {c.stream && <span className='chip'>{c.stream}</span>}
                            {Object.entries(c.meta ?? {}).slice(0, 5).map(([k, v]) => (
                                <span key={k} className='badge'>{k + ': ' + v}</span>
                            ))}
                            <span className='topbar-space'/>
                            {c.human_id && !patientId && <code className='roster-sub'>{c.human_id}</code>}
                        </div>
                        <CaseText text={c.text}/>
                        {Object.keys(c.annotations).length > 0 && (
                            <div className='case-anns'>
                                {Object.entries(c.annotations).map(([dim, a]) => (
                                    <span key={dim} className='case-ann'>
                                        <span className='chip'>{dim.replace(/^B\d+_dim_/, '')}</span>
                                        {a.gallery?.label && (
                                            <span className={'badge label-' + a.gallery.label.toLowerCase()}>
                                                {'🖼️ ' + a.gallery.label}
                                                {a.gallery.difficulty === 'boundary' ? ' · boundary' : ''}
                                            </span>
                                        )}
                                        {a.batch?.gold && (
                                            <span className='badge'>{'📥 ' + a.batch.iter + ' gold ' + a.batch.gold}</span>
                                        )}
                                    </span>
                                ))}
                            </div>
                        )}
                    </div>
                ))}
            </div>

            <div className='raw-foot roster-sub'>
                {data.source === 'record'
                    ? 'cases sliced from the ' + data.dataset + ' record — one annotation/prediction point each; ' +
                      'labels overlay where a labeling project shares the id'
                    : 'served from the labeling corpus until a 3-CaseStore is mounted'}
            </div>
        </div>
    );
}
