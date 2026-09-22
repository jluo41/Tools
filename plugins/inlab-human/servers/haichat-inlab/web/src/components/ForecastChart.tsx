/* ForecastChart — a CGM endpoint's answer is a TRAJECTORY, not a score.
 *
 *   context (what the model was given)  │  forecast ──  vs  observed ┈┈
 *   ────────────────────────────────────┼──────────────────────────────
 *                                    anchor
 *
 * The observed curve is the whole point: a rolled-out forecast next to what actually
 * happened is the only honest way to read one. Values come from the endpoint verbatim;
 * nothing here smooths or rescales them.
 */
interface Props {
    values: number[];                       // the forecast
    observed?: number[] | null;             // what actually happened over the same horizon
    context?: number[] | null;              // the history the model saw
    unit: string;
    stepMin: number;
    mode?: string | null;                   // 'forecast' | 'teacher_forced'
    metrics?: {mae?: number; rmse?: number} | null;
}

const W = 760;
const H = 230;
const PAD = {l: 34, r: 10, t: 10, b: 20};

export default function ForecastChart(p: Props) {
    const {values, observed, context, unit, stepMin, mode, metrics} = p;
    const ctx = context ?? [];
    const all = [...ctx, ...values, ...(observed ?? [])];
    const lo = Math.min(55, Math.min(...all) - 10);
    const hi = Math.max(200, Math.max(...all) + 10);
    const n = ctx.length + values.length;   // total x span

    const x = (i: number) => PAD.l + (i / Math.max(1, n - 1)) * (W - PAD.l - PAD.r);
    const y = (v: number) => PAD.t + (1 - (v - lo) / (hi - lo)) * (H - PAD.t - PAD.b);
    const path = (vals: number[], offset: number) =>
        vals.map((v, i) => (i === 0 ? 'M' : 'L') + x(offset + i).toFixed(1) + ' ' + y(v).toFixed(1)).join(' ');

    const anchor = ctx.length;
    const hours = (values.length * stepMin) / 60;
    const rolled = mode === 'forecast';

    return (
        <div className='fc'>
            <div className='fc-head'>
                <span className='fc-last'>{values[values.length - 1] + ' ' + unit}</span>
                <span className='roster-sub'>
                    {rolled
                        ? hours + 'h forecast · ' + values.length + ' steps · rolled out from ' +
                          ctx.length + ' bins of history'
                        : values.length + ' steps · teacher-forced reconstruction (not a forecast)'}
                </span>
                {metrics?.mae !== undefined && (
                    <span className='badge'>{'MAE ' + metrics.mae + ' ' + unit}</span>
                )}
            </div>

            <svg viewBox={`0 0 ${W} ${H}`} className='fc-svg' preserveAspectRatio='none'>
                {/* clinical range */}
                <rect
                    x={PAD.l}
                    y={y(180)}
                    width={W - PAD.l - PAD.r}
                    height={Math.max(0, y(70) - y(180))}
                    className='fc-band'
                />
                {[70, 180].map((v) => (
                    <g key={v}>
                        <line x1={PAD.l} x2={W - PAD.r} y1={y(v)} y2={y(v)} className='fc-grid'/>
                        <text x={4} y={y(v) + 3} className='fc-tick'>{v}</text>
                    </g>
                ))}

                {/* the moment the model stops seeing the truth */}
                {ctx.length > 0 && (
                    <>
                        <line
                            x1={x(anchor)}
                            x2={x(anchor)}
                            y1={PAD.t}
                            y2={H - PAD.b}
                            className='fc-anchor'
                        />
                        <text x={x(anchor) + 4} y={PAD.t + 9} className='fc-tick'>{'now'}</text>
                        <path d={path(ctx, 0)} className='fc-line ctx'/>
                    </>
                )}

                {/* what actually happened — drawn under the forecast so the forecast reads on top */}
                {observed && observed.length > 0 && (
                    <path d={path(observed, anchor)} className='fc-line observed'/>
                )}

                <path d={path(values, anchor)} className='fc-line'/>
            </svg>

            <div className='fc-legend roster-sub'>
                {ctx.length > 0 && <span><i className='sw ctx'/>{'context (given)'}</span>}
                <span><i className='sw fc'/>{'forecast'}</span>
                {observed && observed.length > 0 && <span><i className='sw obs'/>{'observed'}</span>}
                <span>{'verbatim from the endpoint'}</span>
            </div>
        </div>
    );
}
