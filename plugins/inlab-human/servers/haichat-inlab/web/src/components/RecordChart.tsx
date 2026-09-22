/* RecordChart — the record layer as a TIMELINE, not a table.
 *
 * Every record stream is already binned onto the same 5-minute grid (DT_s), so they
 * share one x-axis and belong on one plot: the glucose curve, and on top of it the
 * events that move it — meals, exercise, medication. A table can show you a meal at
 * 07:40; only this can show you what the glucose did next.
 *
 *   mg/dL                                        ⇣ anchor (what ▶ Run scores)
 *     ╭──╮      🍽        ╭───╮   💊             ┊
 *   ──╯  ╰──────────╮──╭──╯   ╰────╮──────────╮──┊──
 *                   ╰──╯            ╰─────────╯  ┊
 *
 * Events are drawn AT the glucose value of their moment, so a marker sits on the
 * curve rather than in a separate lane — the response is the point.
 *
 * Plotly owns the mouse: drag to zoom, shift-drag to pan, hover for values, click a
 * legend entry to mute a stream, and the range slider underneath to move a window
 * over the whole series. Click any point to ring its row in the table below.
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

/** US wire format ("12/06/2021 06:45:00 PM") — what the stores emit. Date.parse
 *  handles it, but NaN-guard so one bad cell can't blank the plot. */
function parseDT(v: unknown): Date | null {
    if (!v) {
        return null;
    }
    const t = Date.parse(String(v));
    return Number.isNaN(t) ? null : new Date(t);
}

function num(v: unknown): number | null {
    if (v === null || v === undefined || v === '') {
        return null;
    }
    const n = Number(v);
    return Number.isFinite(n) ? n : null;
}

/** The one time column every record stream shares. */
const T_COLS = ['DT_s', 'DT_r', 'ObservationDateTime', 'AdministrationDate'];

function timeOf(r: Row): Date | null {
    for (const c of T_COLS) {
        const d = parseDT(r[c]);
        if (d) {
            return d;
        }
    }
    return null;
}

/* How each stream is drawn, and what its hover says. Keyed by the record table's
 * suffix so a cohort missing a stream (Ohio has no Exercise5Min) simply renders
 * fewer traces instead of breaking. */
const EVENTS: {
    match: RegExp;
    label: string;
    symbol: string;
    color: string;
    detail: (r: Row) => string;
}[] = [
    {
        match: /Diet/i,
        label: '🍽️ Meal',
        symbol: 'triangle-up',
        color: '#e8833a',
        detail: (r) => {
            const bits = [r.FoodName, r.ActivityType].filter(Boolean).join(' · ');
            const carbs = num(r.Carbs);
            const cal = num(r.Calories);
            return [bits, carbs !== null ? `${carbs} g carbs` : '',
                cal !== null ? `${cal} kcal` : ''].filter(Boolean).join('<br>');
        },
    },
    {
        match: /Exercise/i,
        label: '🏃 Exercise',
        symbol: 'square',
        color: '#3aa76d',
        detail: (r) => {
            const dur = num(r.ExerciseDuration);
            return [r.ExerciseType, r.ExerciseIntensity,
                dur !== null ? `${dur} min` : ''].filter(Boolean).join('<br>');
        },
    },
    {
        match: /Med/i,
        label: '💊 Medication',
        symbol: 'diamond',
        color: '#8a6fd4',
        detail: (r) => {
            const dose = num(r.Dose);
            const med = String(r.medication ?? r.MedicationID ?? '').slice(0, 60);
            return [med, dose !== null ? `dose ${dose}` : ''].filter(Boolean).join('<br>');
        },
    },
];

/** Where events with no glucose reading are drawn: a rug lane below the plausible
 *  glucose range, so they read as "an event happened here", never as a value. */
const RUG = 40;

/** The glucose stream: the only one with a y-value of its own. */
function glucoseTable(tables: RecordLayer['tables']): string | null {
    const keys = Object.keys(tables);
    return keys.find((k) => /CGM/i.test(k)) ?? null;
}

/** Glucose at time t, by nearest 5-min bin — so an event marker lands ON the curve.
 *  Returns null when the nearest reading is more than 15 min away (a real gap). */
function nearest(xs: Date[], ys: number[], t: Date): number | null {
    if (!xs.length) {
        return null;
    }
    let lo = 0;
    let hi = xs.length - 1;
    while (lo < hi) {
        const mid = (lo + hi) >> 1;
        if (xs[mid].getTime() < t.getTime()) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    const cands = [xs[lo - 1] ? lo - 1 : lo, lo];
    let best = cands[0];
    for (const i of cands) {
        if (Math.abs(xs[i].getTime() - t.getTime()) < Math.abs(xs[best].getTime() - t.getTime())) {
            best = i;
        }
    }
    return Math.abs(xs[best].getTime() - t.getTime()) <= 15 * 60_000 ? ys[best] : null;
}

export default function RecordChart({data, anchor, onPick}: Props) {
    const host = useRef<HTMLDivElement>(null);

    /* traces + the table/row each point came from, so a click can reach the grid */
    const {traces, origin, empty, hasRug} = useMemo(() => {
        const tables = data.tables;
        const gKey = glucoseTable(tables);
        const out: Partial<Plotly.PlotData>[] = [];
        const org: {table: string; row: number}[][] = [];

        let gx: Date[] = [];
        let gy: number[] = [];
        if (gKey) {
            const rows = (tables[gKey].rows ?? []) as Row[];
            const idx: number[] = [];
            rows.forEach((r, i) => {
                const t = timeOf(r);
                const v = num(r.BGValue ?? r.Value);
                if (t && v !== null) {
                    gx.push(t);
                    gy.push(v);
                    idx.push(i);
                }
            });
            out.push({
                type: 'scatter',
                mode: 'lines',
                name: `📈 Glucose (${gy.length})`,
                x: gx,
                y: gy,
                line: {color: '#2f7fd1', width: 1.6},
                hovertemplate: '<b>%{y:.0f} mg/dL</b><br>%{x|%b %d %H:%M}<extra></extra>',
            });
            org.push(idx.map((i) => ({table: gKey, row: i})));
        }

        for (const ev of EVENTS) {
            const key = Object.keys(tables).find((k) => ev.match.test(k) && k !== gKey);
            if (!key) {
                continue;
            }
            const rows = (tables[key].rows ?? []) as Row[];
            /* An event only sits ON the curve if there is a reading near it. Events
             * outside the glucose window (the CGM table is row-capped, the event
             * tables are not) have NO glucose value — parking them at a made-up y
             * would draw a reading that does not exist, so they go to a rug lane
             * under the axis instead: still visible, still clickable, not a value. */
            const on = {xs: [] as Date[], ys: [] as number[], text: [] as string[], idx: [] as number[]};
            const off = {xs: [] as Date[], text: [] as string[], idx: [] as number[]};
            rows.forEach((r, i) => {
                const t = timeOf(r);
                if (!t) {
                    return;
                }
                const y = nearest(gx, gy, t);
                if (y === null) {
                    off.xs.push(t);
                    off.text.push(ev.detail(r) || '—');
                    off.idx.push(i);
                } else {
                    on.xs.push(t);
                    on.ys.push(y);
                    on.text.push(ev.detail(r) || '—');
                    on.idx.push(i);
                }
            });
            if (!on.xs.length && !off.xs.length) {
                continue;
            }
            const total = on.xs.length + off.xs.length;
            out.push({
                type: 'scatter',
                mode: 'markers',
                name: `${ev.label} (${total})`,
                legendgroup: ev.label,
                x: on.xs,
                y: on.ys,
                text: on.text,
                marker: {symbol: ev.symbol, size: 11, color: ev.color,
                    line: {color: '#fff', width: 1}},
                hovertemplate: `<b>${ev.label}</b><br>%{text}<br>` +
                    'glucose %{y:.0f} · %{x|%b %d %H:%M}<extra></extra>',
            });
            org.push(on.idx.map((i) => ({table: key, row: i})));

            if (off.xs.length) {
                out.push({
                    type: 'scatter',
                    mode: 'markers',
                    name: `${ev.label} · no CGM`,
                    legendgroup: ev.label,
                    showlegend: false,
                    x: off.xs,
                    y: off.xs.map(() => RUG),
                    text: off.text,
                    marker: {symbol: 'line-ns-open', size: 9, color: ev.color,
                        line: {color: ev.color, width: 2}},
                    hovertemplate: `<b>${ev.label}</b><br>%{text}<br>` +
                        'no CGM within 15 min · %{x|%b %d %H:%M}<extra></extra>',
                });
                org.push(off.idx.map((i) => ({table: key, row: i})));
            }
        }

        return {
            traces: out,
            origin: org,
            empty: !out.length,
            hasRug: out.some((t) => t.name?.includes('no CGM')),
        };
    }, [data]);

    useEffect(() => {
        const el = host.current;
        if (!el || empty) {
            return;
        }
        const a = anchor ? parseDT(anchor) : null;

        const layout: Partial<Plotly.Layout> = {
            margin: {l: 46, r: 12, t: 8, b: 28},
            height: 300,
            hovermode: 'closest',
            dragmode: 'zoom',
            showlegend: true,
            legend: {orientation: 'h', y: 1.16, x: 0, font: {size: 11}},
            xaxis: {
                type: 'date',
                // SVG traces (not scattergl) so the slider actually previews the
                // series — a WebGL trace leaves it an empty white band.
                rangeslider: {thickness: 0.12},
                gridcolor: 'rgba(128,128,128,.18)',
            },
            yaxis: {
                title: {text: 'mg/dL', standoff: 8},
                gridcolor: 'rgba(128,128,128,.18)',
                zeroline: false,
            },
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: {size: 11},
            shapes: [
                // the clinical target band — the reference every CGM chart is read against
                {
                    type: 'rect', xref: 'paper', x0: 0, x1: 1,
                    yref: 'y', y0: 70, y1: 180,
                    fillcolor: 'rgba(58,167,109,.10)', line: {width: 0}, layer: 'below',
                },
                ...(a ? [{
                    type: 'line' as const, xref: 'x' as const, yref: 'paper' as const,
                    x0: a, x1: a, y0: 0, y1: 1,
                    line: {color: '#d1443f', width: 2, dash: 'dot' as const},
                }] : []),
            ],
            annotations: [
                ...(a ? [{
                    // Plotly's annotation typing wants a primitive on a date axis
                    x: a.toISOString(), y: 1, yref: 'paper' as const,
                    text: '⇣ prediction anchor',
                    showarrow: false, font: {size: 10, color: '#d1443f'},
                    xanchor: 'right' as const, yanchor: 'bottom' as const,
                }] : []),
                ...(hasRug ? [{
                    xref: 'paper' as const, x: 0, y: RUG, yref: 'y' as const,
                    text: 'events with no CGM ⇢',
                    showarrow: false, font: {size: 9, color: 'rgba(128,128,128,.9)'},
                    xanchor: 'left' as const, yanchor: 'bottom' as const,
                }] : []),
            ],
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
    }, [traces, origin, empty, hasRug, anchor, onPick]);

    if (empty) {
        return null;
    }
    return (
        <div className='record-chart'>
            <div ref={host} />
            <div className='record-chart-hint'>
                {'drag to zoom · shift-drag to pan · scroll to zoom · '}
                {'click a legend entry to mute a stream · click a point to find its row · '}
                {'double-click to reset'}
            </div>
        </div>
    );
}
