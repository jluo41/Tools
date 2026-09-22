/* ExternalView — the External insight: outside knowledge about this patient's
 * conditions (OpenEvidence-style: arXiv, medical journals, guidelines).
 *
 * v1 = an honest placeholder that shows WHAT would be searched (the patient's
 * problem list), so the view has the right shape before the discovery backend
 * is wired in.
 */
import type {PatientDetail} from '../types';

interface Props {
    patient: PatientDetail | null;
}

export default function ExternalView({patient}: Props) {
    const dx = (patient?.source_tables?.Dx ?? [])
        .map((r) => String(r.DxName ?? r.ICD10Code ?? ''))
        .filter(Boolean);
    const uniq = Array.from(new Set(dx)).slice(0, 12);

    return (
        <div className='view-scroll'>
            <div className='stub-card'>
                <div className='pane-header'>{'🌐 External discovery'}</div>
                <div className='roster-sub'>
                    {'OpenEvidence-style search over external literature for this patient’s '}
                    {'conditions — planned; will reuse the discovery layer as backend.'}
                </div>
                {uniq.length > 0 && (
                    <div className='stub-body'>
                        <div className='pane-header'>{'would search for'}</div>
                        <div className='pc-tables'>
                            {uniq.map((d) => (
                                <span key={d} className='badge'>{d}</span>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
