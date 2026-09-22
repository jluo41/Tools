/* PatientCard — the persistent preview strip above every view.
 *
 * Once a patient is selected the page is theirs; this card keeps the context
 * (who, cohort, as-of date, what tables exist) visible no matter which view
 * the rail has active. It is the "preview the dataset" step, always on.
 */
import {cohortOf, type PatientDetail} from '../types';

interface Props {
    patient: PatientDetail | null;
    loading: boolean;
}

export default function PatientCard({patient, loading}: Props) {
    if (loading) {
        return <div className='patient-card muted'>{'Loading patient…'}</div>;
    }
    if (!patient) {
        return (
            <div className='patient-card muted'>
                {'Select a patient above — the page binds to that single dataset.'}
            </div>
        );
    }

    const s = patient.summary;
    const counts = Object.entries(s.table_counts ?? {});

    return (
        <div className='patient-card'>
            <div className='pc-main'>
                <span className='pc-id'>{patient.patient_id}</span>
                <span className='chip'>{cohortOf(patient.patient_id, patient.summary)}</span>
                <span className='roster-sub'>
                    {[
                        patient.age_at_index === null ? '?' : patient.age_at_index + 'y',
                        s.sex,
                        s.race,
                    ]
                        .filter(Boolean)
                        .join(' · ')}
                </span>
                {patient.index_date && (
                    <span className='as-of'>{'🕒 as of ' + patient.index_date}</span>
                )}
                {patient.post_index_rows_hidden > 0 && (
                    <span className='roster-sub'>
                        {patient.post_index_rows_hidden + ' later rows postdate the score'}
                    </span>
                )}
            </div>
            <div className='pc-tables'>
                {counts.map(([name, n]) => (
                    <span key={name} className={'badge' + (n === 0 ? ' empty' : '')}>
                        {name + ' ' + n}
                    </span>
                ))}
            </div>
        </div>
    );
}
