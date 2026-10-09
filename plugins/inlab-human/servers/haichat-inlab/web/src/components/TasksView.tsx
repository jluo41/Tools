/* TasksView — the work linked to this scope, read off the project ladder.
 *
 * A project's work is Blocks → Jobs → Tasks; this view draws that tree. The
 * individual/group split is per Task (its face's scope: line, else its task-type),
 * so the view is scope-filtered: the group console lists cohort-level Tasks, the
 * individual console per-subject ones. Read-only: it surfaces what work exists on
 * disk; running or opening a Task is a HaiChat/CLI job, not a button here yet.
 */
import {useEffect, useState} from 'react';

import type {Scope} from '../Console';

interface TaskItem {
    project: string;
    task: string;
    series: string | null;
    title: string;
    task_type?: string | null;
    kind: Scope;
    status: string;
}

interface JobNode {job: string | null; title: string | null; tasks: TaskItem[]}
interface BlockNode {block: string | null; title: string | null; jobs: JobNode[]}

interface TasksResp {
    root: string | null;
    scope?: string | null;
    n?: number;
    reason?: string;
    projects?: {project: string; world?: string | null; blocks: BlockNode[]}[];
    error?: string;
}

/** the number in front of a ladder folder: b01_x → b01 */
function code(name: string | null): string {
    return name ? name.split('_')[0] : '';
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
            <code>{'Project-*/tasks/bNN/jNN/tNN'}</code>
            <span className='roster-sub'>
                {scope === 'group'
                    ? 'group-level Tasks: cohort data, fit and eval work, under their Blocks and Jobs'
                    : 'individual-level Tasks: per-subject work, under their Blocks and Jobs'}
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
                <span className='roster-sub'>{'root ' + data.root}</span>
                <span className='topbar-space'/>
                <span className='roster-sub'>{'🟢 has-results · 🔵 reported · 🟡 planned · ⚪ scaffolded'}</span>
            </div>

            <div className='view-scroll'>
                {projects.length === 0 && (
                    <div className='muted pad'>
                        {scope === 'individual'
                            ? 'No individual (per-subject) Tasks yet. A Task whose face says scope: individual lands here.'
                            : 'No group Tasks found.'}
                    </div>
                )}
                {projects.map((p) => (
                    <div key={p.project} className='task-project'>
                        <div className='pane-header task-proj-head'>
                            {'📦 ' + p.project.replace(/^Project-/, '')}
                            {p.world && <span className='roster-sub'>{p.world}</span>}
                            <span className='badge'>
                                {p.blocks.reduce((n, b) => n + b.jobs.reduce((m, j) => m + j.tasks.length, 0), 0)}
                            </span>
                        </div>
                        {p.blocks.map((b) => (
                            <div key={b.block ?? 'flat'} className='task-block'>
                                {b.block && (
                                    <div className='task-block-head'>
                                        <code>{code(b.block)}</code>
                                        <span>{b.title}</span>
                                    </div>
                                )}
                                {b.jobs.map((j) => (
                                    <div key={j.job ?? 'flat'} className='task-job'>
                                        {j.job && (
                                            <div className='task-job-head'>
                                                <code>{code(j.job)}</code>
                                                <span>{j.title}</span>
                                            </div>
                                        )}
                                        <div className='task-list'>
                                            {j.tasks.map((t) => (
                                                <div key={t.task} className='task-row'
                                                    title={[p.project, b.block, j.job, t.task].filter(Boolean).join('/')}>
                                                    <span className='task-status'>{STATUS_ICON[t.status] ?? '⚪'}</span>
                                                    <code className='task-series'>{t.series ?? code(t.task)}</code>
                                                    <span className='task-title'>{t.title}</span>
                                                    <span className='topbar-space'/>
                                                    {t.task_type && <span className='chip'>{t.task_type}</span>}
                                                    <span className='badge task-status-label'>{t.status}</span>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        ))}
                    </div>
                ))}
            </div>

            <div className='raw-foot roster-sub'>
                {'read-only · scope from each Task face\'s scope: line, else its task-type; ' +
                    'projects not yet on the ladder are read flat'}
            </div>
        </div>
    );
}
