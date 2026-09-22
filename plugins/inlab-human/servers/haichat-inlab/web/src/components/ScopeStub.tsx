/* ScopeStub — an honest placeholder for a view whose behavior at the CURRENT
 * scope isn't built yet: a group-level view still scoped to one patient's code,
 * or the individual "apply a guideline" surface. It says exactly what this view
 * WILL show here, so the Individual⇄Group toggle is fully navigable while each
 * view's depth at the new scope is filled in.
 */
export default function ScopeStub({icon, title, lines}: {
    icon: string;
    title: string;
    lines: string[];
}) {
    return (
        <div className='view-scroll'>
            <div className='stub-card'>
                <div className='pane-header'>{icon + ' ' + title}</div>
                {lines.map((l, i) => (
                    <div key={i} className='roster-sub scope-line'>{l}</div>
                ))}
            </div>
        </div>
    );
}
