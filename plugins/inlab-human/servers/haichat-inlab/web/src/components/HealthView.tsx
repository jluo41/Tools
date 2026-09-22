/* HealthView — the console's own status: resolved config + which endpoints
 * answer. Mirrors GET /api/health verbatim; about the service, not the patient.
 */
import {useEffect, useState} from 'react';

interface Props {
    api?: string;
}

export default function HealthView({api = ''}: Props) {
    const [health, setHealth] = useState<Record<string, unknown> | null>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        fetch(`${api}/api/health`)
            .then((r) => r.json())
            .then(setHealth)
            .catch(() => setError('cannot reach /api/health'));
    }, [api]);

    if (error) {
        return <div className='view-scroll'><div className='alert error'>{error}</div></div>;
    }
    if (!health) {
        return <div className='view-scroll muted pad'>{'Loading health…'}</div>;
    }

    return (
        <div className='view-scroll'>
            <div className='stub-card'>
                <div className='pane-header'>{'❤️ Console health'}</div>
                <table className='health-table'>
                    <tbody>
                        {Object.entries(health).map(([k, v]) => (
                            <tr key={k}>
                                <td className='roster-id'>{k}</td>
                                <td>
                                    {typeof v === 'object'
                                        ? JSON.stringify(v, null, 1)
                                        : String(v)}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
