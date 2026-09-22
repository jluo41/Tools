/* HaiChatDrawer — the platform's conversational surface, inside the console.
 *
 * Genie-pattern, HaiChat brand: a summonable right drawer scoped to the selected
 * patient. STANDALONE MODE ONLY — embedded beside a Mattermost thread, the thread IS
 * HaiChat, so the shell hides this drawer there (Console.tsx).
 *
 * PRESENTATIONAL. The session — the WebSocket, the transcript, the approval futures —
 * is owned by useHaiChat, which Console mounts once and never tears down. This drawer
 * is a window onto it: closing the drawer now hides the conversation instead of
 * destroying it, and the agent survives the clinician collapsing the panel mid-answer.
 *
 * Everything the agent does is visible here — streamed text, tool calls, tool results,
 * and every action it took on the console (🤖). Consequential tool calls BLOCK on the
 * clinician's Allow/Deny; these buttons answer the server-side gate. The agent narrates
 * scores; it never computes them.
 */
import {useEffect, useRef, useState} from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

import type {ChatItem, ChatStatus} from '../useHaiChat';

interface Props {
    patientId: string | null;
    items: ChatItem[];
    status: ChatStatus;
    follow: boolean;
    onFollow: (on: boolean) => void;
    onSend: (text: string) => void;
    onAnswer: (id: string, approved: boolean) => void;
    onInterrupt: () => void;
    onClose: () => void;
}

/** strip the mcp prefix for display: mcp__endpoint-predict__get_patient → get_patient */
const toolLabel = (t: string) => t.split('__').pop() ?? t;

export default function HaiChatDrawer(props: Props) {
    const {patientId, items, status, follow, onFollow, onSend, onAnswer, onInterrupt, onClose} = props;
    const [draft, setDraft] = useState('');
    const bodyRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        bodyRef.current?.scrollTo({top: bodyRef.current.scrollHeight});
    }, [items]);

    function send() {
        const text = draft.trim();
        if (!text || status !== 'ready') {
            return;
        }
        setDraft('');
        onSend(text);
    }

    const dotClass = status === 'offline' ? 'down' : status === 'busy' ? 'busy' : 'live';

    return (
        <aside className='drawer'>
            <div className='drawer-head'>
                <span className='drawer-title'>
                    {'💬 HaiChat'}
                    <span className={'dot ' + dotClass} title={status}/>
                    {patientId && <span className='chip'>{patientId}</span>}
                </span>
                <span className='drawer-head-btns'>
                    {/* Follow mode is a capability the clinician GRANTS, not a default.
                        Off, the agent only reads the console when spoken to. */}
                    <button
                        className={'follow-toggle' + (follow ? ' on' : '')}
                        onClick={() => onFollow(!follow)}
                        title={follow
                            ? 'Follow me is ON — HaiChat reacts when you click around the console'
                            : 'Follow me is OFF — HaiChat only reads the console when you message it'}
                    >
                        {'👣 Follow'}
                    </button>
                    {status === 'busy' && (
                        <button
                            className='drawer-close'
                            title='Interrupt the agent'
                            onClick={onInterrupt}
                        >
                            {'⏹'}
                        </button>
                    )}
                    <button className='drawer-close' onClick={onClose} title='Hide HaiChat'>
                        {'✕'}
                    </button>
                </span>
            </div>

            <div className='drawer-body' ref={bodyRef}>
                {items.length === 0 && (
                    <div className='drawer-hello'>
                        <div className='roster-sub'>
                            {patientId
                                ? 'Ask about ' + patientId + '’s record, or ask HaiChat to open a tab, ' +
                                  'point at a row, or run a model.'
                                : 'Select a patient first — HaiChat is scoped to one patient at a time.'}
                        </div>
                        <div className='roster-sub'>
                            {'It can navigate the console freely (🤖 marks what it opened). '}
                            {'Running a model, changing the selection, or writing the checklist ' +
                             'waits for your Allow/Deny. Scores come from the endpoint verbatim.'}
                        </div>
                        {status === 'offline' && (
                            <div className='roster-sub'>
                                {'⚠ agent offline — is the service running with the Agent SDK installed?'}
                            </div>
                        )}
                    </div>
                )}

                {items.map((it, i) => {
                    switch (it.kind) {
                    case 'user':
                        return <div key={i} className='drawer-msg user'>{it.text}</div>;
                    case 'assistant':
                    case 'draft':
                        // the agent answers in markdown — render it (react-markdown emits
                        // no raw HTML, so agent output cannot inject markup)
                        return (
                            <div key={i} className='drawer-msg assistant md'>
                                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                    {it.text}
                                </ReactMarkdown>
                                {it.kind === 'draft' && <span className='cursor'>{'▌'}</span>}
                            </div>
                        );
                    case 'ui_action':
                        // what the agent DID to the console — auto-allowed or not, it shows
                        return (
                            <div
                                key={i}
                                className={'ui-act' + (it.auto ? '' : ' gated') +
                                    (it.ok === false ? ' failed' : '')}
                            >
                                {'🤖 '}
                                {it.text}
                                {it.ok === false && <span className='roster-sub'>{' · refused'}</span>}
                            </div>
                        );
                    case 'divider':
                        return (
                            <div key={i} className='chat-divider'>
                                <span>{it.text}</span>
                            </div>
                        );
                    case 'tool_call':
                        return (
                            <div key={i} className='tc-chip' title={it.input}>
                                {'🔧 ' + toolLabel(it.tool)}
                                <span className='tc-args'>{it.input.slice(0, 80)}</span>
                            </div>
                        );
                    case 'tool_result':
                        return (
                            <details key={i} className={'tr-block' + (it.isError ? ' error' : '')}>
                                <summary>{(it.isError ? '⚠ ' : '↩ ') + 'tool result'}</summary>
                                <pre>{it.content}</pre>
                            </details>
                        );
                    case 'approval':
                        return (
                            <div key={i} className='appr-card'>
                                <div className='appr-title'>
                                    {'🔐 Approve tool call?'}
                                    <span className='chip'>{toolLabel(it.tool)}</span>
                                </div>
                                <pre className='appr-input'>{it.input}</pre>
                                {it.status === 'pending' ? (
                                    <div className='appr-btns'>
                                        <button className='run-btn allow' onClick={() => onAnswer(it.id, true)}>
                                            {'Allow'}
                                        </button>
                                        <button className='run-btn ghost' onClick={() => onAnswer(it.id, false)}>
                                            {'Deny'}
                                        </button>
                                    </div>
                                ) : (
                                    <div className='roster-sub'>
                                        {it.status === 'allowed' ? '✓ allowed' : '✕ denied'}
                                    </div>
                                )}
                            </div>
                        );
                    case 'info':
                        return <div key={i} className='drawer-info'>{it.text}</div>;
                    case 'error':
                        return <div key={i} className='alert error'>{it.text}</div>;
                    default:
                        return null;
                    }
                })}
            </div>

            <div className='drawer-input'>
                <input
                    value={draft}
                    placeholder={
                        status === 'offline' ? 'agent offline'
                            : status === 'connecting' ? 'starting agent…'
                                : patientId ? 'Ask HaiChat…' : 'select a patient first'
                    }
                    disabled={!patientId || status === 'offline'}
                    onChange={(e) => setDraft(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && send()}
                />
                <button
                    className='run-btn ghost send'
                    disabled={!patientId || status !== 'ready'}
                    onClick={send}
                >
                    {'↑'}
                </button>
            </div>
        </aside>
    );
}
