/* grid — shared helpers for the .raw-grid tables (Source + Record panels).
 *
 * A free-text column (a clinical note, a dialogue transcript, a JSON metadata
 * blob) is worth wrapping onto several lines; an id / split / number column reads
 * better crisp on one line. We can't know which is which from the schema, so we
 * measure: a column whose longest cell exceeds a threshold is "wide" and gets the
 * .wrap class, everything else stays nowrap.
 */

/** Columns whose content is long enough to wrap instead of running off-screen.
 *  Scans only until a column clears the threshold — cheap even on wide tables. */
export function wideColumns(
    rows: Record<string, unknown>[],
    columns: string[],
    threshold = 60,
): Set<string> {
    const wide = new Set<string>();
    for (const c of columns) {
        for (const r of rows) {
            const v = r[c];
            if (v === null || v === undefined) {
                continue;
            }
            if (String(v).length > threshold) {
                wide.add(c);
                break;
            }
        }
    }
    return wide;
}
