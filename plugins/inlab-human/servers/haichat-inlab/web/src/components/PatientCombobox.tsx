/* PatientCombobox — the topbar's searchable patient drop-down.
 *
 * Selecting a patient is a ONE-SHOT act: the whole page binds to that patient
 * (one selected patient = one workspace), so there is no persistent roster pane.
 * Grouped by cohort, filterable, Enter picks the first match, Esc closes.
 */
import {useEffect, useMemo, useRef, useState} from 'react';

import {cohortOf, type PatientListItem} from '../types';

interface Props {
    patients: PatientListItem[];
    selected: string | null;
    onSelect: (id: string) => void;
}

export default function PatientCombobox({patients, selected, onSelect}: Props) {
    const [open, setOpen] = useState(false);
    const [query, setQuery] = useState('');
    const rootRef = useRef<HTMLDivElement>(null);
    const inputRef = useRef<HTMLInputElement>(null);

    useEffect(() => {
        if (!open) {
            return;
        }
        inputRef.current?.focus();
        const onDown = (e: MouseEvent) => {
            if (rootRef.current && !rootRef.current.contains(e.target as Node)) {
                setOpen(false);
            }
        };
        document.addEventListener('mousedown', onDown);
        return () => document.removeEventListener('mousedown', onDown);
    }, [open]);

    const groups = useMemo(() => {
        const q = query.trim().toLowerCase();
        const hit = patients.filter((p) => !q || p.patient_id.toLowerCase().includes(q));
        const by: Record<string, PatientListItem[]> = {};
        for (const p of hit) {
            const g = cohortOf(p.patient_id, p.summary);
            (by[g] = by[g] ?? []).push(p);
        }
        return Object.entries(by);
    }, [patients, query]);

    const first = groups[0]?.[1]?.[0];

    function pick(id: string) {
        onSelect(id);
        setOpen(false);
        setQuery('');
    }

    return (
        <div className='combo' ref={rootRef}>
            <button
                className='combo-btn'
                onClick={() => setOpen((o) => !o)}
                title='Select a patient — the whole page binds to this selection'
            >
                <span className='combo-label'>{'Patient'}</span>
                <span className='combo-value'>{selected ?? 'select…'}</span>
                {selected && <span className='chip'>{cohortOf(selected)}</span>}
                <span className='combo-caret'>{open ? '▴' : '▾'}</span>
            </button>

            {open && (
                <div className='combo-pop'>
                    <input
                        ref={inputRef}
                        className='combo-search'
                        placeholder={'🔎 filter ' + patients.length + ' patients…'}
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        onKeyDown={(e) => {
                            if (e.key === 'Escape') {
                                setOpen(false);
                            }
                            if (e.key === 'Enter' && first) {
                                pick(first.patient_id);
                            }
                        }}
                    />
                    <div className='combo-list'>
                        {groups.length === 0 && (
                            <div className='roster-sub combo-empty'>{'no match'}</div>
                        )}
                        {groups.map(([cohort, items]) => (
                            <div key={cohort}>
                                <div className='combo-group'>
                                    {cohort}
                                    <span className='badge'>{items.length}</span>
                                </div>
                                {items.map((p) => (
                                    <div
                                        key={p.patient_id}
                                        className={
                                            'roster-item' +
                                            (p.patient_id === selected ? ' selected' : '')
                                        }
                                        onClick={() => pick(p.patient_id)}
                                    >
                                        <div className='roster-main'>
                                            <span className='roster-id'>{p.patient_id}</span>
                                        </div>
                                        <div className='roster-sub'>
                                            {(p.summary.sex ?? '?') + ' · ' +
                                                Object.values(p.summary.table_counts ?? {})
                                                    .reduce((a, b) => a + b, 0) + ' rows'}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}
