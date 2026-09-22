/* PatientChart — the selected patient's full chart, clinician-readable.
 * Source of truth lives here, in HAI-Chat. The REACH D01 demo imports it from
 * this folder rather than keeping a copy — one component, no fork.
 */
import type {PatientDetail} from '../types';

interface Props {
    patient: PatientDetail | null;
    loading: boolean;
}

/** Tables worth showing first, with clinician-facing labels + the columns that matter. */
const VIEWS: {table: string; label: string; cols: string[]}[] = [
    {table: 'Dx', label: '🩺 Problem list', cols: ['ICD10Code', 'DxName', 'EncContactDate']},
    {table: 'Med', label: '💊 Medications', cols: ['MedDisplayName', 'MedName', 'StartDate', 'EndDate']},
    {table: 'Questionnaire', label: '📝 Questionnaires', cols: ['FormName', 'Question', 'QuestAnswer']},
    {table: 'Vital', label: '📈 Vitals', cols: ['MeasDispName', 'MeasName', 'MeasValue', 'RecordedTime']},
    {table: 'Lab', label: '🧪 Labs', cols: ['ComponentName', 'Value', 'ResultDate']},
    {table: 'Encounter', label: '🏥 Visits', cols: ['ContactDate', 'EncType', 'DepSpeciality']},
];

function cell(v: unknown): string {
    if (v === null || v === undefined || v === 'NaT') {
        return '—';
    }
    const s = String(v);
    return s.length > 40 ? s.slice(0, 38) + '…' : s;
}

export default function PatientChart({patient, loading}: Props) {
    if (loading) {
        return <div className='pane-section muted'>{'Loading chart…'}</div>;
    }
    if (!patient) {
        return <div className='pane-section muted'>{'← Select a patient'}</div>;
    }

    const s = patient.summary;
    return (
        <div className='pane-section chart'>
            <div className='pane-header'>{'📋 Chart'}</div>
            <div className='demographics'>
                <strong>{patient.patient_id}</strong>
                <div className='roster-sub'>
                    {[
                        patient.age_at_index === null ? '?' : patient.age_at_index + 'y',
                        s.sex,
                        s.race,
                    ]
                        .filter(Boolean)
                        .join(' · ')}
                </div>
                {patient.index_date && (
                    <div className='as-of'>
                        {'🕒 as of ' + patient.index_date}
                        <span className='roster-sub'>{' (prediction date)'}</span>
                    </div>
                )}
                {patient.post_index_rows_hidden > 0 && (
                    <div className='roster-sub'>
                        {'· ' + patient.post_index_rows_hidden + ' later rows hidden — they postdate the score'}
                    </div>
                )}
            </div>

            {VIEWS.map(({table, label, cols}) => {
                const rows = patient.source_tables?.[table] ?? [];
                if (!rows.length) {
                    return (
                        <details key={table} className='chart-table'>
                            <summary>
                                {label}
                                <span className='badge empty'>{'empty'}</span>
                            </summary>
                        </details>
                    );
                }
                const present = cols.filter((c) => rows.some((r) => r[c] !== undefined));
                return (
                    <details
                        key={table}
                        open={rows.length <= 8}
                        className='chart-table'
                    >
                        <summary>
                            {label}
                            <span className='badge'>{rows.length}</span>
                        </summary>
                        <table>
                            <tbody>
                                {rows.slice(0, 12).map((r, i) => (
                                    <tr key={i}>
                                        {present.map((c) => (
                                            <td key={c}>{cell(r[c])}</td>
                                        ))}
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                        {rows.length > 12 && (
                            <div className='roster-sub'>{'+ ' + (rows.length - 12) + ' more'}</div>
                        )}
                    </details>
                );
            })}
        </div>
    );
}
