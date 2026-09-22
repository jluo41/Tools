/* RawDataPanel — "show me exactly what raw data this patient has".
 *
 * Every source table, every column, every row. Nothing curated, nothing hidden.
 * Rows dated AFTER the prediction are FLAGGED (not withheld) — in the raw view
 * the whole point is to see the record as it is, including what postdates the
 * score.
 *
 * Source of truth lives here, in HAI-Chat. The REACH D01 demo imports it from
 * this folder rather than keeping a copy — one component, no fork.
 */
import {useEffect, useMemo, useRef, useState} from 'react';

import type {Highlight, RawPatient, SortDir} from '../types';
import {LAYER_BLURB} from '../views';

import {wideColumns} from './grid';
import {rowsInWindow, useScrollToHighlight} from './highlight';

/* CONTROLLED: which table is open and how it is sorted live in useConsole, not here,
 * because HaiChat can drive them too ("open the CGM table and sort by time"). The
 * DATA — rows, loading, errors — stays local: a second driver has no business owning
 * a fetch. */
interface Props {
    patientId: string | null;
    dataset: string | null;
    table: string | null;
    sort: {col: string; dir: SortDir} | null;
    highlight: Highlight | null;
    onTable: (t: string) => void;
    onSort: (s: {col: string; dir: SortDir} | null) => void;
}

function cell(v: unknown): string {
    if (v === null || v === undefined || v === 'NaT' || v === '') {
        return '—';
    }
    return String(v);
}

/** Compare that keeps numbers numeric and dates chronological, and always sinks
 *  blanks to the bottom — a lexicographic sort would put "10" before "9" and
 *  scatter empty cells through the middle. */
function compare(a: unknown, b: unknown): number {
    const blank = (v: unknown) =>
        v === null || v === undefined || v === '' || v === 'NaT';
    if (blank(a) && blank(b)) {
        return 0;
    }
    if (blank(a)) {
        return 1;
    }
    if (blank(b)) {
        return -1;
    }
    const na = Number(a);
    const nb = Number(b);
    if (!isNaN(na) && !isNaN(nb)) {
        return na - nb;
    }
    return String(a).localeCompare(String(b));
}

export default function RawDataPanel(props: Props) {
    const {patientId, dataset, table, sort, highlight, onTable, onSort} = props;
    const [data, setData] = useState<RawPatient | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const picked = useRef<string | null>(null);

    useEffect(() => {
        if (!patientId) {
            setData(null);
            return;
        }
        setLoading(true);
        setError(null);
        setData(null);
        picked.current = null;
        const qs = dataset ? `?dataset=${encodeURIComponent(dataset)}` : '';
        fetch(`/api/patients/${patientId}/raw${qs}`)
            .then((r) => r.json())
            .then((d) => {
                if (d.error) {
                    setError(d.error);
                    return;
                }
                setData(d);
            })
            .catch(() => setError('failed to load raw data'))
            .finally(() => setLoading(false));
    }, [patientId, dataset]);

    /* The default table is chosen once the data lands — but the SELECTION is owned by
     * useConsole, so an agent that pre-selected a table before the fetch finished is
     * not overruled by this default. */
    useEffect(() => {
        if (!data || table || picked.current === patientId) {
            return;
        }
        picked.current = patientId;
        const first = Object.entries(data.tables)
            .filter(([, t]) => t.n_rows > 0)
            .sort((a, b) => b[1].n_rows - a[1].n_rows)[0];
        if (first) {
            onTable(first[0]);
        }
    }, [data, table, patientId, onTable]);

    const active = useMemo(
        () => (data && table ? data.tables[table] : null),
        [data, table],
    );

    const rows = useMemo(() => {
        if (!active) {
            return [];
        }
        if (!sort) {
            return active.rows;
        }
        const sign = sort.dir === 'asc' ? 1 : -1;
        // copy: never sort the fetched array in place
        return [...active.rows].sort((a, b) => sign * compare(a[sort.col], b[sort.col]));
    }, [active, sort]);

    const ringed = useMemo(
        () => rowsInWindow(rows, active?.columns ?? [], highlight),
        [rows, active, highlight],
    );
    const firstRing = useScrollToHighlight(highlight);

    /* long-text columns wrap; ids / splits / numbers stay on one line */
    const wide = useMemo(
        () => wideColumns(active?.rows ?? [], active?.columns ?? []),
        [active],
    );

    function toggleSort(col: string) {
        onSort(
            !sort || sort.col !== col
                ? {col, dir: 'asc'}
                : sort.dir === 'asc'
                    ? {col, dir: 'desc'}
                    : null, // third click clears the sort -> back to file order
        );
    }

    if (!patientId) {
        return <div className='raw muted pad'>{'← Select a patient to see their raw data'}</div>;
    }
    if (loading) {
        return <div className='raw muted pad'>{'Loading raw tables…'}</div>;
    }
    if (error) {
        return <div className='raw pad'><div className='alert error'>{error}</div></div>;
    }
    if (!data) {
        return null;
    }

    const entries = Object.entries(data.tables);
    const totalRows = entries.reduce((a, [, t]) => a + t.n_rows, 0);

    return (
        <div className='raw'>
            <div className='layer-banner'>
                <span className='layer-step'>{'2 · SOURCE'}</span>
                <code>{LAYER_BLURB.source.store}</code>
                <span className='roster-sub'>{LAYER_BLURB.source.what}</span>
            </div>

            <div className='raw-bar'>
                <strong>{data.patient_id}</strong>
                <span className='roster-sub'>
                    {entries.length + ' tables · ' + totalRows + ' rows'}
                </span>
                {data.index_date && (
                    <span className='as-of'>{'🕒 prediction date ' + data.index_date}</span>
                )}
            </div>

            {highlight?.note && ringed.size > 0 && (
                <div className='hl-note'>
                    {'🤖 '}
                    {highlight.note}
                    <span className='roster-sub'>{' · ' + ringed.size + ' rows ringed'}</span>
                </div>
            )}

            <div className='raw-tabs'>
                {entries.map(([name, t]) => (
                    <button
                        key={name}
                        className={
                            'raw-tab' +
                            (name === table ? ' active' : '') +
                            (t.n_rows === 0 ? ' empty' : '')
                        }
                        onClick={() => onTable(name)}
                    >
                        {name}
                        <span className='badge'>{t.n_rows}</span>
                    </button>
                ))}
            </div>

            <div className='raw-grid-wrap'>
                {!active || active.n_rows === 0 ? (
                    <div className='muted pad'>
                        {'“' + (table ?? '') + '” has no rows for this patient.'}
                    </div>
                ) : (
                    <table className='raw-grid'>
                        <thead>
                            <tr>
                                <th>{'#'}</th>
                                {active.columns.map((c) => (
                                    <th
                                        key={c}
                                        className={'sortable' + (sort?.col === c ? ' sorted' : '') +
                                            (wide.has(c) ? ' wrap' : '')}
                                        onClick={() => toggleSort(c)}
                                        title='Click to sort · click again to reverse · again to clear'
                                    >
                                        {c}
                                        <span className='sort-caret'>
                                            {sort?.col === c ? (sort.dir === 'asc' ? '▲' : '▼') : '↕'}
                                        </span>
                                    </th>
                                ))}
                            </tr>
                        </thead>
                        <tbody>
                            {rows.map((r, i) => {
                                const ring = ringed.has(i);
                                return (
                                    <tr
                                        key={i}
                                        ref={ring && i === Math.min(...ringed) ? firstRing : undefined}
                                        className={(r._after_index ? 'after-index' : '') + (ring ? ' ringed' : '')}
                                        title={
                                            r._after_index
                                                ? 'this row postdates the prediction — the model did not see it'
                                                : undefined
                                        }
                                    >
                                        <td className='rownum'>
                                            {r._after_index ? '⚠️' : i + 1}
                                        </td>
                                        {active.columns.map((c) => (
                                            <td key={c} className={wide.has(c) ? 'wrap' : undefined}>
                                                {cell(r[c])}
                                            </td>
                                        ))}
                                    </tr>
                                );
                            })}
                        </tbody>
                    </table>
                )}
            </div>

            <div className='raw-foot roster-sub'>
                {'⚠️ = row postdates the prediction date; the model did not see it.'}
            </div>
        </div>
    );
}
