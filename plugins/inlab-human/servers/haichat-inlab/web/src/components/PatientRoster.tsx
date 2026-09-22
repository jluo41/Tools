/* PatientRoster — clickable patient list.
 * Source of truth lives here, in HAI-Chat. The REACH D01 demo imports it from
 * this folder rather than keeping a copy — one component, no fork.
 */
import type {PatientListItem} from '../types';

interface Props {
    patients: PatientListItem[];
    selected: string | null;
    onSelect: (id: string) => void;
}

function rows(p: PatientListItem): number {
    return Object.values(p.summary.table_counts ?? {}).reduce((a, b) => a + b, 0);
}

function family(p: PatientListItem): string {
    if (p.patient_id.startsWith('reach-1')) {
        return 'ADHD';
    }
    if (p.patient_id.startsWith('reach-2')) {
        return 'PD2D';
    }
    return 'MIMIC';
}

export default function PatientRoster({patients, selected, onSelect}: Props) {
    return (
        <div className='pane-section'>
            <div className='pane-header'>
                {'👥 Patients'}
                <span className='badge'>{patients.length}</span>
            </div>
            <ul className='roster'>
                {patients.map((p) => (
                    <li
                        key={p.patient_id}
                        className={'roster-item' + (p.patient_id === selected ? ' selected' : '')}
                        onClick={() => onSelect(p.patient_id)}
                    >
                        <div className='roster-main'>
                            <span className='roster-id'>{p.patient_id}</span>
                            <span className='chip'>{family(p)}</span>
                        </div>
                        <div className='roster-sub'>
                            {(p.summary.sex ?? '?') + ' · ' + rows(p) + ' rows'}
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    );
}
