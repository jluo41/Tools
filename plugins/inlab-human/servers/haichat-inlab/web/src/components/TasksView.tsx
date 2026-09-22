/* TasksView — the work linked to this scope, from the research projects.
 *
 * The individual/group split is per-task, so this view is scope-filtered: the
 * group console lists group-level tasks (cohort data/case/eval pipelines), the
 * individual console lists per-subject tasks. Grouped by project, read-only —
 * it surfaces what work exists on disk (each project's tasks folder); running
 * or opening a task is a HaiChat/CLI job, not a button here yet.
 */
import {useEffect, useState} from 'react';

import type {Scope} from '../Console';

interface TaskItem {
    project: string;
    task: string;
    series: string | null;
    title: string;
    kind: Scope;
    status: string;
}

interface TasksResp {
    root: string | null;
    scope?: string | null;
    n?: number;
    reason?: string;
    projects?: {project: string; tasks: TaskItem[]}[];
    error?: string;
}

const STATUS_ICON: Record<string, string> = {
    'has-results': '🟢',
    reported: '🔵',
    planned: '🟡',
    scaffolded: '⚪',
};

export default function TasksView({scope}: {scope: Scope}) {
    const [data, setData] = useState<TasksResp | null>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        setData(null);
        setError(null);
        fetch('/api/tasks?scope=' + scope)
            .then((r) => r.json())
            .then((d) => (d.error ? setError(d.error) : setData(d)))
            .catch(() => setError('failed to load tasks'));
    }, [scope]);

    const banner = (
        <div className='layer-banner'>
            <span className='layer-step'>{'📋 TASKS'}</span>
            <code>{'examples/Project-*/tasks'}</code>
            <span className='roster-sub'>
                {scope === 'group'
                    ? 'group-level tasks — cohort data / case / eval pipelines across your projects'
                    : 'individual-level tasks — per-subject queries (haipipe for-individual, E-series)'}
            </span>
        </div>
    );

    if (error) {
        return <div className='view-scroll'>{banner}<div className='alert error'>{error}</div></div>;
    }
    if (!data) {
        return <div className='view-scroll'>{banner}<div className='muted pad'>{'Loading tasks…'}</div></div>;
    }
    if (!data.root) {
        return (
            <div className='view-scroll'>
                {banner}
                <div className='stub-card'>
                    <div className='pane-header'>{'📋 no projects root mounted'}</div>
                    <div className='roster-sub'>{data.reason}</div>
                </div>
            </div>
        );
    }

    const projects = data.projects ?? [];

    return (
        <div className='raw'>
            {banner}

            <div className='case-bar'>
                <span className='badge'>{(data.n ?? 0) + ' ' + scope + ' tasks'}</span>
                <span className='badge'>{projects.length + ' projects'}</span>
                <span className='topbar-space'/>
                <span className='roster-sub'>{'🟢 has-results · 🔵 reported · 🟡 planned · ⚪ scaffolded'}</span>
            </div>

            <div className='view-scroll'>
                {projects.length === 0 && (
                    <div className='muted pad'>
                        {scope === 'individual'
                            ? 'No individual (per-subject) tasks yet — none of your projects have E-series / for-individual tasks. Create one and it lands here.'
                            : 'No group tasks found.'}
                    </div>
                )}
                {projects.map((p) => (
                    <div key={p.project} className='task-project'>
                        <div className='pane-header task-proj-head'>
                            {'📦 ' + p.project.replace(/^Project-/, '')}
                            <span className='badge'>{p.tasks.length}</span>
                        </div>
                        <div className='task-list'>
                            {p.tasks.map((t) => (
                                <div key={t.task} className='task-row' title={t.project + '/tasks/' + t.task}>
                                    <span className='task-status'>{STATUS_ICON[t.status] ?? '⚪'}</span>
                                    {t.series && <code className='task-series'>{t.series}</code>}
                                    <span className='task-title'>{t.title}</span>
                                    <span className='topbar-space'/>
                                    <span className='badge task-status-label'>{t.status}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                ))}
            </div>

            <div className='raw-foot roster-sub'>
                {'read-only — classification: E-series / “individual” → individual, else group; ' +
                    'override with .inlab-scope or scope: in a task yaml'}
            </div>
        </div>
    );
}
