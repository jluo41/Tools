/* InternalView — the Internal insight: "what does this patient have?"
 *
 * v1 = the curated clinician chart (as of the prediction date). The DIKW
 * insight cards (D/I/K/W over this record) arrive later and will stack above
 * the chart; the placeholder marks the slot so the view's shape is honest.
 */
import type {PatientDetail} from '../types';

import PatientChart from './PatientChart';

interface Props {
    patient: PatientDetail | null;
    loading: boolean;
}

export default function InternalView({patient, loading}: Props) {
    return (
        <div className='view-scroll'>
            <div className='stub-card'>
                <div className='pane-header'>{'🧬 DIKW insight cards'}</div>
                <div className='roster-sub'>
                    {'Data → Information → Knowledge → Wisdom cards over this record — planned; '}
                    {'generated per patient by the DIKW pipeline.'}
                </div>
            </div>
            <PatientChart patient={patient} loading={loading}/>
        </div>
    );
}
