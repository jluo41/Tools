/* RecordChart — the record layer as a TIMELINE, not a table, for any dataset.
 *
 * Every record table that carries a time column becomes one lane, and all lanes share one
 * time axis, so what happened in one table can be read against what happened in another:
 *
 *   lane 1  ─╮╭──╮╭───╮╭──      a table with numbers: one line per numeric column
 *   lane 2      ▲      ▲          a table with no numbers: one marker per row, hover lists it
 *   lane 3   ■           ■
 *            ┊ anchor (what ▶ Run scores)
 *
 * Nothing here names a dataset, a table or a column (JL 261009: "we might have any dataset with
 * any type of table"). Which column is the time, which columns are numbers, and which numeric
 * column is only a row counter are all read from the values. A table with no time column is
 * not drawn: it is still in the grid below.
 *
 * Plotly owns the mouse: drag to zoom, shift-drag to pan, hover for values, click a legend
 * entry to mute a column, the range slider to move a window over the whole series. Click any
 * point to ring its row in the table below.
 */
import {useEffect, useMemo, useRef} from 'react';
import Plotly from 'plotly.js-dist-min';

import type {RecordLayer} from '../types';

interface Props {
    data: RecordLayer;
    /** the prediction trigger — drawn as the anchor line when present */
    anchor?: string | null;
    /** clicking a point asks the panel to open that table and ring that row */
    onPick?: (table: string, rowIndex: number) => void;
}

type Row = Record<string, unknown>;

/** a value that reads as a moment: a date or date-time string, or a Date */
const DATEISH = /^\d{4}-\d{2}-\d{2}|^\d{1,2}\/\d{1,2}\/\d{2,4}/;

function parseDT(v: unknown): Date | null {
    if (v === null || v === undefined || v === '') {
        return null;
    }
    const s = String(v);
    if (!DATEISH.test(s)) {
        return null;
    }
    const t = Date.parse(s);
    return Number.isNaN(t) ? null : new Date(t);
}

function num(v: unknown): number | null {
    if (v === null || v === undefined || v === '' || typeof v === 'boolean') {
        return null;
    }
    const n = Number(v);
    return Number.isFinite(n) ? n : null;
}

/** share of a column's non-empty cells that pass a test */
function share(rows: Row[], col: string, ok: (v: unknown) => boolean): number {
    let n = 0;
    let hit = 0;
    for (const r of rows) {
        const v = r[col];
        if (v === null || v === undefined || v === '') {
            continue;
        }
        n += 1;
        if (ok(v)) {
            hit += 1;
        }
    }
    return n ? hit / n : 0;
}

/** a numeric column that only counts rows (whole numbers, each one more than the last) */
function isCounter(rows: Row[], col: string): boolean {
    const xs = rows.map((r) => num(r[col])).filter((x): x is number => x !== null);
    if (xs.length < 3 || xs.some((x) => !Number.isInteger(x))) {
        return false;
    }
    return xs.every((x, i) => i === 0 || x > xs[i - 1]);
}

const MAX_LINES = 6;      // numeric columns drawn per lane; the rest stay in the grid

interface Lane {
    table: string;
    time: string;
    numeric: string[];
    more: number;
}

/** what each table can draw: its time column and its numeric columns, read from the values */
function lanesOf(tables: RecordLayer['tables']): Lane[] {
    const out: Lane[] = [];
    for (const [table, t] of Object.entries(tables)) {
        const rows = (t.rows ?? []) as Row[];
        const cols = t.columns?.length ? t.columns : Object.keys(rows[0] ?? {});
        if (!rows.length) {
            continue;
        }
        const time = cols.find((c) => share(rows, c, (v) => parseDT(v) !== null) >= 0.8);
        if (!time) {
            continue;
        }
        const numeric = cols
            .filter((c) => c !== time && share(rows, c, (v) => num(v) !== null) >= 0.8 && !isCounter(rows, c))
            .sort((a, b) => rows.filter((r) => num(r[b]) !== null).length -
                rows.filter((r) => num(r[a]) !== null).length);
        out.push({table, time, numeric: numeric.slice(0, MAX_LINES), more: Math.max(0, numeric.length - MAX_LINES)});
    }
    // tables with numbers first (they carry the shape), then event tables
    return out.sort((a, b) => Number(b.numeric.length > 0) - Number(a.numeric.length > 0));
}

/** a row's hover: its short fields, the time column first */
function describe(r: Row, time: string): string {
    const bits = Object.entries(r)
        .filter(([k, v]) => k !== time && v !== null && v !== undefined && v !== '' && String(v).length <= 60)
        .slice(0, 8)
        .map(([k, v]) => `${k}: ${v}`);
    return bits.join('<br>') || '—';
}

export default function RecordChart({data, anchor, onPick}: Props) {
    const host = useRef<HTMLDivElement>(null);

    /* traces + the table/row each point came from, so a click can reach the grid */
    const {traces, origin, lanes, layoutAxes, height} = useMemo(() => {
        const ls = lanesOf(data.tables);
        const weight = ls.map((l) => (l.numeric.length ? 3 : 1));
        const total = weight.reduce((a, b) => a + b, 0) || 1;
        const gap = ls.length > 1 ? 0.04 : 0;
        const out: Partial<Plotly.PlotData>[] = [];
        const org: {table: string; row: number}[][] = [];
        const axes: Record<string, Partial<Plotly.LayoutAxis>> = {};

        let top = 1;
        ls.forEach((lane, k) => {
            const h = (weight[k] / total) * (1 - gap * (ls.length - 1));
            const yName = k === 0 ? 'y' : `y${k + 1}`;
            const axisKey = k === 0 ? 'yaxis' : `yaxis${k + 1}`;
            axes[axisKey] = {
                domain: [Math.max(0, top - h), top],
                gridcolor: 'rgba(128,128,128,.18)',
                zeroline: false,
                showticklabels: lane.numeric.length > 0,
                title: {text: lane.table.replace(/^Rec\./, ''), font: {size: 10}, standoff: 4},
                fixedrange: lane.numeric.length === 0,
            };
            top = top - h - gap;

            const rows = (data.tables[lane.table].rows ?? []) as Row[];
            const times = rows.map((r) => parseDT(r[lane.time]));
            if (lane.numeric.length) {
                for (const col of lane.numeric) {
                    const xs: Date[] = [];
                    const ys: number[] = [];
                    const idx: number[] = [];
                    rows.forEach((r, i) => {
                        const t = times[i];
                        const v = num(r[col]);
                        if (t && v !== null) {
                            xs.push(t);
                            ys.push(v);
                            idx.push(i);
                        }
                    });
                    out.push({
                        type: 'scatter',
                        mode: xs.length >= 20 ? 'lines' : 'lines+markers',
                        name: `${lane.table.replace(/^Rec\./, '')} · ${col} (${xs.length})`,
                        x: xs,
                        y: ys,
                        yaxis: yName,
                        line: {width: 1.5},
                        hovertemplate: `<b>${col}</b> %{y}<br>%{x|%b %d %H:%M}<extra></extra>`,
                    });
                    org.push(idx.map((i) => ({table: lane.table, row: i})));
                }
            } else {
                const xs: Date[] = [];
                const text: string[] = [];
                const idx: number[] = [];
                rows.forEach((r, i) => {
                    const t = times[i];
                    if (t) {
                        xs.push(t);
                        text.push(describe(r, lane.time));
                        idx.push(i);
                    }
                });
                out.push({
                    type: 'scatter',
                    mode: 'markers',
                    name: `${lane.table.replace(/^Rec\./, '')} (${xs.length})`,
                    x: xs,
                    y: xs.map(() => 0),
                    yaxis: yName,
                    text,
                    marker: {size: 10, symbol: 'triangle-up'},
                    hovertemplate: `<b>${lane.table.replace(/^Rec\./, '')}</b><br>%{text}` +
                        '<br>%{x|%b %d %H:%M}<extra></extra>',
                });
                org.push(idx.map((i) => ({table: lane.table, row: i})));
            }
        });

        return {
            traces: out,
            origin: org,
            lanes: ls,
            layoutAxes: axes,
            height: Math.min(560, 90 + 60 * total),
        };
    }, [data]);

    useEffect(() => {
        const el = host.current;
        if (!el || !traces.length) {
            return;
        }
        const a = anchor ? parseDT(anchor) ?? new Date(anchor) : null;
        const anchorOk = a && !Number.isNaN(a.getTime());

        const layout: Partial<Plotly.Layout> = {
            margin: {l: 64, r: 12, t: 8, b: 28},
            height,
            hovermode: 'closest',
            dragmode: 'zoom',
            showlegend: true,
            legend: {orientation: 'h', y: 1.14, x: 0, font: {size: 11}},
            xaxis: {
                type: 'date',
                anchor: lanes.length > 1 ? `y${lanes.length}` as Plotly.AxisName : 'y',
                // SVG traces (not scattergl) so the slider actually previews the
                // series — a WebGL trace leaves it an empty white band.
                rangeslider: {thickness: 0.08},
                gridcolor: 'rgba(128,128,128,.18)',
            },
            ...layoutAxes,
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: {size: 11},
            shapes: anchorOk ? [{
                type: 'line', xref: 'x', yref: 'paper',
                x0: a, x1: a, y0: 0, y1: 1,
                line: {color: '#d1443f', width: 2, dash: 'dot'},
            }] : [],
            annotations: anchorOk ? [{
                // Plotly's annotation typing wants a primitive on a date axis
                x: (a as Date).toISOString(), y: 1, yref: 'paper',
                text: '⇣ prediction anchor',
                showarrow: false, font: {size: 10, color: '#d1443f'},
                xanchor: 'right', yanchor: 'bottom',
            }] : [],
        };

        Plotly.react(el, traces as Plotly.Data[], layout, {
            displaylogo: false,
            responsive: true,
            scrollZoom: true,
            modeBarButtonsToRemove: ['select2d', 'lasso2d'],
        });

        const onClick = (e: {points?: {curveNumber: number; pointIndex: number}[]}) => {
            const p = e.points?.[0];
            if (!p || !onPick) {
                return;
            }
            const o = origin[p.curveNumber]?.[p.pointIndex];
            if (o) {
                onPick(o.table, o.row);
            }
        };
        (el as unknown as {on: (ev: string, cb: typeof onClick) => void})
            .on('plotly_click', onClick);

        return () => {
            Plotly.purge(el);
        };
    }, [traces, origin, lanes, layoutAxes, height, anchor, onPick]);

    if (!traces.length) {
        return null;
    }
    const more = lanes.filter((l) => l.more > 0);
    return (
        <div className='record-chart'>
            <div ref={host} />
            <div className='record-chart-hint'>
                {'one lane per table with a time column · drag to zoom · shift-drag to pan · '}
                {'click a legend entry to mute a column · click a point to find its row · double-click to reset'}
                {more.length > 0 && (' · not drawn: ' +
                    more.map((l) => `${l.more} more numeric columns of ${l.table.replace(/^Rec\./, '')}`).join(', '))}
            </div>
        </div>
    );
}
