/* highlight — the agent's pointing finger, and the least invasive thing it can do.
 *
 * "There is a 6-hour CGM gap on day 3" is a sentence the clinician has to go hunting
 * for. A ring around the rows, scrolled into view, is the same claim made checkable in
 * one glance. So `highlight` is auto-allowed: it opens no new surface, changes no
 * selection, and fades on its own — the console never accumulates stale agent marks.
 *
 * A highlight names EITHER a row (1-based, as the grid shows it) or a time window,
 * which is matched against the table's first datetime-ish column — because the agent
 * reasons in timestamps ("02:00 to 08:00"), not in row offsets it would have to count.
 */
import {useEffect, useRef} from 'react';

import {HIGHLIGHT_TTL_MS, type Highlight} from '../types';

/** true while the ring should still be drawn (they fade, so old marks don't pile up) */
export const isLive = (h: Highlight | null): boolean =>
    Boolean(h) && Date.now() - (h as Highlight).at < HIGHLIGHT_TTL_MS;

const DATEISH = /(date|time|dt|timestamp)/i;

/** the column a time window should be matched against */
export function timeColumn(columns: string[]): string | null {
    return columns.find((c) => DATEISH.test(c)) ?? null;
}

/** Which displayed rows fall inside the highlight, as a set of 0-based indices.
 *
 *  Dates are compared as Date values when both sides parse, and lexicographically
 *  otherwise — ISO-ish strings sort correctly either way, and a cohort that ships
 *  "%m/%d/%Y %I:%M:%S %p" still lands on the right rows via Date.parse. */
export function rowsInWindow(
    rows: Record<string, unknown>[],
    columns: string[],
    h: Highlight | null,
): Set<number> {
    const hit = new Set<number>();
    if (!h || !isLive(h)) {
        return hit;
    }

    /* A row number is only authoritative if it is a REAL one. Models routinely fill an
     * unused optional field with 0, and `row: 0` was silently ringing index -1: a
     * highlight that reported "1 row ringed", rang nothing, and anchored no scroll.
     * Rows are 1-based and must exist; anything else falls through to the time window,
     * which is what the agent actually meant. */
    const row = h.row ?? 0;
    if (row >= 1 && row <= rows.length) {
        hit.add(row - 1);                   // the agent counts the way the grid displays
        return hit;
    }
    if (!h.from && !h.to) {
        return hit;
    }
    const col = h.table && columns.includes(h.table) ? h.table : timeColumn(columns);
    if (!col) {
        return hit;
    }
    const num = (v: unknown): number | null => {
        const t = Date.parse(String(v));
        return isNaN(t) ? null : t;
    };
    const lo = h.from ? num(h.from) : null;
    const hi = h.to ? num(h.to) : null;
    rows.forEach((r, i) => {
        const t = num(r[col]);
        if (t === null) {
            return;
        }
        if ((lo === null || t >= lo) && (hi === null || t <= hi)) {
            hit.add(i);
        }
    });
    return hit;
}

/** Scroll the first ringed row into view — a mark you cannot see is not a pointer.
 *  Keyed on the highlight's timestamp so re-pointing at the SAME row scrolls again. */
export function useScrollToHighlight(h: Highlight | null) {
    const ref = useRef<HTMLTableRowElement | null>(null);
    useEffect(() => {
        if (h && isLive(h) && ref.current) {
            ref.current.scrollIntoView({block: 'center', behavior: 'smooth'});
        }
    }, [h?.at, h]);
    return ref;
}
