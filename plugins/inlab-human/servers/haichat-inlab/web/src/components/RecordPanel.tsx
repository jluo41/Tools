/* RecordPanel — the DATA layer's third stage: RecordFn output.
 *
 * What the pipeline actually reads. Compared with Source, this is where the cleaning
 * shows: sensor rows filtered, a PID assigned, timestamps binned onto a 5-minute grid,
 * duplicates aggregated. Put this beside Source (drag the tab) and the transformation
 * is visible row for row — which is the point.
 */
import {useCallback, useEffect, useMemo, useRef, useState} from 'react';

import type {Highlight, LayerUnavailable, RecordLayer} from '../types';
import {LAYER_BLURB} from '../views';

import {wideColumns} from './grid';
import {rowsInWindow, useScrollToHighlight} from './highlight';
import RecordChart from './RecordChart';

/* CONTROLLED — see RawDataPanel: the table selection is owned by useConsole so that
 * HaiChat can open a table and ring a row through the same dispatch a click goes
 * through. The fetch stays local. */
interface Props {
    patientId: string | null;
    dataset: string | null;
    table: string | null;
    highlight: Highlight | null;
    /** the prediction trigger, drawn on the chart as the anchor line */
    anchor?: string | null;
    onTable: (t: string) => void;
}

function cell(v: unknown): string {
    if (v === null || v === undefined || v === 'NaT' || v === '') {
        return '—';
    }
    return String(v);
}

export default function RecordPanel({patientId, dataset, table, highlight, anchor, onTable}: Props) {
    const [data, setData] = useState<RecordLayer | LayerUnavailable | null>(null);
    const [error, setError] = useState<string | null>(null);
    const picked = useRef<string | null>(null);
    /* a point clicked on the chart: which row to ring, in which table. Separate from
     * `highlight` — that channel belongs to HaiChat; this one is the user's mouse. */
    const [fromChart, setFromChart] = useState<{table: string; row: number} | null>(null);
    const chartRow = useRef<HTMLTableRowElement>(null);

    useEffect(() => {
        if (!patientId) {
            setData(null);
            return;
        }
        setError(null);
        setData(null);
        picked.current = null;
        const qs = dataset ? `?dataset=${encodeURIComponent(dataset)}` : '';
        fetch(`/api/patients/${patientId}/layer/record${qs}`)
            .then((r) => r.json())
            .then((d) => (d.error ? setError(d.error) : setData(d)))
            .catch(() => setError('failed to load the record layer'));
    }, [patientId, dataset]);

    useEffect(() => {
        if (!data || !data.available || table || picked.current === patientId) {
            return;
        }
        picked.current = patientId;
        const first = Object.entries((data as RecordLayer).tables)
            .sort((a, b) => b[1].n_rows - a[1].n_rows)[0];
        if (first) {
            onTable(first[0]);
        }
    }, [data, table, patientId, onTable]);

    const active = useMemo(
        () => (data && data.available && table ? (data as RecordLayer).tables[table] : null),
        [data, table],
    );

    const ringed = useMemo(
        () => rowsInWindow(active?.rows ?? [], active?.columns ?? [], highlight),
        [active, highlight],
    );
    const firstRing = useScrollToHighlight(highlight);

    /* clicking a point on the chart opens that stream's table and scrolls to the row */
    const onPick = useCallback((t: string, row: number) => {
        setFromChart({table: t, row});
        onTable(t);
    }, [onTable]);

    useEffect(() => {
        if (fromChart && table === fromChart.table) {
            chartRow.current?.scrollIntoView({block: 'center', behavior: 'smooth'});
        }
    }, [fromChart, table]);

    /* long-text columns (notes, dialogue) wrap; ids / splits stay one line */
    const wide = useMemo(
        () => wideColumns(active?.rows ?? [], active?.columns ?? []),
        [active],
    );

    if (!patientId) {
        return <div className='view-scroll muted'>{'Select a patient.'}</div>;
    }
    if (error) {
        return <div className='view-scroll'><div className='alert error'>{error}</div></div>;
    }
    if (!data) {
        return <div className='view-scroll muted'>{'Loading records…'}</div>;
    }

    const blurb = LAYER_BLURB.record;

    if (!data.available) {
        return (
            <div className='view-scroll'>
                <div className='layer-banner'>
                    <span className='layer-step'>{'3 · RECORD'}</span>
                    <code>{blurb.store}</code>
                    <span className='roster-sub'>{blurb.what}</span>
                </div>
                <div className='stub-card'>
                    <div className='roster-sub'>{(data as LayerUnavailable).reason}</div>
                </div>
            </div>
        );
    }

    const entries = Object.entries((data as RecordLayer).tables);

    return (
        <div className='raw'>
            <div className='layer-banner'>
                <span className='layer-step'>{'3 · RECORD'}</span>
                <code>{blurb.store}</code>
                <span className='roster-sub'>{blurb.what}</span>
            </div>

            {highlight?.note && ringed.size > 0 && (
                <div className='hl-note'>
                    {'🤖 '}
                    {highlight.note}
                    <span className='roster-sub'>{' · ' + ringed.size + ' rows ringed'}</span>
                </div>
            )}

            <RecordChart data={data as RecordLayer} anchor={anchor} onPick={onPick} />

            <div className='raw-tabs'>
                {entries.map(([name, t]) => (
                    <button
                        key={name}
                        className={'raw-tab' + (name === table ? ' active' : '') +
                            (t.n_rows === 0 ? ' empty' : '')}
                        onClick={() => onTable(name)}
                    >
                        {name}
                        <span className='badge'>{t.n_rows}</span>
                    </button>
                ))}
            </div>

            <div className='raw-grid-wrap'>
                {!active || active.n_rows === 0 ? (
                    <div className='muted pad'>{'no records in this table'}</div>
                ) : (
                    <table className='raw-grid'>
                        <thead>
                            <tr>
                                <th>{'#'}</th>
                                {active.columns.map((c) => (
                                    <th key={c} className={wide.has(c) ? 'wrap' : undefined}>{c}</th>
                                ))}
                            </tr>
                        </thead>
                        <tbody>
                            {active.rows.map((r, i) => {
                                const ring = ringed.has(i);
                                const fromMouse = fromChart?.table === table && fromChart.row === i;
                                return (
                                    <tr
                                        key={i}
                                        ref={fromMouse
                                            ? chartRow
                                            : ring && i === Math.min(...ringed) ? firstRing : undefined}
                                        className={[ring ? 'ringed' : '', fromMouse ? 'picked' : '']
                                            .filter(Boolean).join(' ') || undefined}
                                    >
                                        <td className='rownum'>{i + 1}</td>
                                        {active.columns.map((c) => (
                                            <td key={c} className={wide.has(c) ? 'wrap' : undefined}>{cell(r[c])}</td>
                                        ))}
                                    </tr>
                                );
                            })}
                        </tbody>
                    </table>
                )}
            </div>

            <div className='raw-foot roster-sub'>
                {active?.capped
                    ? 'showing the first ' + active.rows.length + ' of ' + active.n_rows +
                      ' records — the pipeline reads all of them'
                    : 'RecordFn output, as the trigger and case pipeline see it'}
            </div>
        </div>
    );
}
