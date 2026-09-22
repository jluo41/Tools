/* RawFilesPanel — the DATA layer's first stage: the files exactly as they arrived.
 *
 * Nothing is parsed here. This is the ground truth a reader can point at when they ask
 * "but what did we actually receive?" — the OhioT1DM XML, not our tables.
 */
import {useEffect, useState} from 'react';

import type {LayerUnavailable, RawFilesLayer} from '../types';
import {LAYER_BLURB} from '../views';

/* CONTROLLED — which file is expanded is owned by useConsole, so HaiChat can open the
 * OhioT1DM XML and say "look at this" through the same dispatch a click goes through. */
interface Props {
    patientId: string | null;
    dataset: string | null;
    open: string | null;
    onOpen: (file: string) => void;
}

const kb = (n: number) => (n < 1e6 ? (n / 1e3).toFixed(0) + ' KB' : (n / 1e6).toFixed(1) + ' MB');

export default function RawFilesPanel({patientId, dataset, open, onOpen}: Props) {
    const [data, setData] = useState<RawFilesLayer | LayerUnavailable | null>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (!patientId) {
            setData(null);
            return;
        }
        setError(null);
        setData(null);
        const qs = dataset ? `?dataset=${encodeURIComponent(dataset)}` : '';
        fetch(`/api/patients/${patientId}/layer/raw${qs}`)
            .then((r) => r.json())
            .then((d) => (d.error ? setError(d.error) : setData(d)))
            .catch(() => setError('failed to load the raw layer'));
    }, [patientId, dataset]);

    if (!patientId) {
        return <div className='view-scroll muted'>{'Select a patient.'}</div>;
    }
    if (error) {
        return <div className='view-scroll'><div className='alert error'>{error}</div></div>;
    }
    if (!data) {
        return <div className='view-scroll muted'>{'Loading raw files…'}</div>;
    }

    const blurb = LAYER_BLURB.raw;

    return (
        <div className='view-scroll'>
            <div className='layer-banner'>
                <span className='layer-step'>{'1 · RAW'}</span>
                <code>{blurb.store}</code>
                <span className='roster-sub'>{blurb.what}</span>
            </div>

            {!data.available ? (
                <div className='stub-card'>
                    <div className='roster-sub'>{(data as LayerUnavailable).reason}</div>
                </div>
            ) : (
                (data as RawFilesLayer).files.map((f) => (
                    <div key={f.name} className='raw-file'>
                        <div
                            className='raw-file-head'
                            onClick={() => onOpen(open === f.name ? '' : f.name)}
                        >
                            <span className='roster-id'>{'📄 ' + f.name}</span>
                            <span className='badge'>{kb(f.bytes)}</span>
                            <span className='roster-sub'>
                                {open === f.name ? 'hide' : 'preview'}
                            </span>
                        </div>
                        {open === f.name && (
                            <>
                                <pre className='raw-file-pre'>{f.preview}</pre>
                                <div className='roster-sub'>
                                    {'first lines only — the file is read by the pipeline, not by this console'}
                                </div>
                            </>
                        )}
                    </div>
                ))
            )}
        </div>
    );
}
