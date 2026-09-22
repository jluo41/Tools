/* useHaiChat — the agent session, and the bridge it drives the console through.
 *
 * This hook owns the WebSocket. It is mounted ONCE by Console and is deliberately
 * NOT keyed on the patient, for two reasons that used to be bugs:
 *
 *   1. The socket used to live inside HaiChatDrawer, which Console unmounted when
 *      you closed the drawer — so closing the drawer silently destroyed the
 *      conversation. The drawer is now just a view onto this state.
 *   2. The socket used to be re-created whenever `patientId` changed. That made an
 *      agent-driven patient switch impossible: the agent would close its own
 *      connection mid-turn, and the tool call it was blocked on would never return.
 *
 * TWO DIRECTIONS, ONE SOCKET:
 *
 *   agent → console   `ui_call`  →  dispatch(action, 'agent')  →  `ui_result`
 *   console → agent   the snapshot + the clinician's actions ride on every message
 *
 * Every callback is read through a ref. `ws.onmessage` is installed once, inside an
 * effect that never re-runs — so anything it closed over directly would be frozen at
 * mount and the agent would be driving a console that no longer exists.
 */
import {useCallback, useEffect, useRef, useState} from 'react';

import {describe, isAutoAllowed, type ActionResult, type ConsoleAction, type Dispatch} from './actions';
import type {ConsoleEvent, ConsoleSnapshot} from './types';

export type ChatItem =
    | {kind: 'user'; text: string}
    | {kind: 'draft'; text: string}
    | {kind: 'assistant'; text: string}
    | {kind: 'tool_call'; tool: string; input: string}
    | {kind: 'tool_result'; content: string; isError: boolean}
    | {kind: 'approval'; id: string; tool: string; input: string; status: 'pending' | 'allowed' | 'denied'}
    /** something the agent DID to the console — always shown, gated or not */
    | {kind: 'ui_action'; text: string; auto: boolean; ok?: boolean}
    /** the patient changed: a hard visible boundary in the conversation */
    | {kind: 'divider'; text: string}
    | {kind: 'info'; text: string}
    | {kind: 'error'; text: string};

export type ChatStatus = 'connecting' | 'ready' | 'busy' | 'offline';

interface Args {
    enabled: boolean;
    patientId: string | null;
    dispatch: Dispatch;
    snapshot: () => ConsoleSnapshot;
    drainUserEvents: () => ConsoleEvent[];
    /** bumped on every console action — the trigger for Follow mode */
    pulse: number;
}

/* Follow mode: react to the clinician's clicks, without becoming a nuisance or a
 * quiet way to burn the subscription. Quiet for this long after the last click, at
 * most one reaction per MIN_GAP, and never more than CAP in one session. */
const FOLLOW_DEBOUNCE_MS = 1500;
const FOLLOW_MIN_GAP_MS = 8000;
const FOLLOW_CAP = 40;

export function useHaiChat({enabled, patientId, dispatch, snapshot, drainUserEvents, pulse}: Args) {
    const [items, setItems] = useState<ChatItem[]>([]);
    const [status, setStatus] = useState<ChatStatus>('connecting');
    const [follow, setFollow] = useState(false);
    const wsRef = useRef<WebSocket | null>(null);

    /* The whole point of this block: onmessage is installed once and must see the
     * CURRENT dispatch/snapshot, not the ones that existed at mount. */
    const cb = useRef({dispatch, snapshot, drainUserEvents});
    cb.current = {dispatch, snapshot, drainUserEvents};

    const followState = useRef({on: false, last: 0, used: 0, busy: false});
    followState.current.on = follow;
    followState.current.busy = status === 'busy';

    const push = useCallback((it: ChatItem) => setItems((xs) => [...xs, it]), []);

    /* ── the socket: opened once, for the life of the console ─────────────────── */
    useEffect(() => {
        if (!enabled) {
            return;
        }
        const proto = window.location.protocol === 'https:' ? 'wss' : 'ws';
        const ws = new WebSocket(`${proto}://${window.location.host}/ws/haichat`);
        wsRef.current = ws;

        const reply = (id: string, body: Record<string, unknown>) => {
            if (ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({type: 'ui_result', id, ...body}));
            }
        };

        ws.onmessage = (e) => {
            const m = JSON.parse(e.data);
            switch (m.type) {
            case 'ready':
                setStatus('ready');
                break;

            /* THE AGENT IS DRIVING. Its action goes through the same dispatch a rail
             * click goes through — there is no agent-only path into the console. */
            case 'ui_call': {
                const action = m.action as ConsoleAction;
                // a pure read is not an event in the clinician's console — don't chip it
                const chip = action.type !== 'state/read'
                    ? {kind: 'ui_action' as const, text: describe(action), auto: isAutoAllowed(action)}
                    : null;
                if (chip) {
                    push(chip);
                }
                void (async () => {
                    let res: ActionResult;
                    try {
                        res = await cb.current.dispatch(action, 'agent');
                    } catch (err) {
                        res = {ok: false, error: String(err)};
                    }
                    // let React commit the action before we photograph the result. The
                    // SCORE is returned from dispatch DIRECTLY and never read back out of
                    // this snapshot, so a stale frame here is cosmetic, not clinical.
                    await new Promise((r) => setTimeout(r, 60));
                    if (chip) {
                        setItems((xs) => xs.map((it) =>
                            it === chip ? {...it, ok: res.ok} : it));
                    }
                    reply(m.id, {
                        ok: res.ok,
                        error: res.error,
                        result: res.run ?? res.checklist ?? null,
                        state: cb.current.snapshot(),
                    });
                })();
                break;
            }

            case 'delta':
                setItems((xs) => {
                    const last = xs[xs.length - 1];
                    if (last?.kind === 'draft') {
                        return [...xs.slice(0, -1), {kind: 'draft', text: last.text + m.text}];
                    }
                    return [...xs, {kind: 'draft', text: m.text}];
                });
                break;
            case 'assistant':
                setItems((xs) => {
                    const base = xs[xs.length - 1]?.kind === 'draft' ? xs.slice(0, -1) : xs;
                    return [...base, {kind: 'assistant', text: m.text}];
                });
                break;
            case 'tool_call':
                push({kind: 'tool_call', tool: m.tool, input: JSON.stringify(m.input)});
                break;
            case 'tool_result':
                push({kind: 'tool_result', content: m.content, isError: Boolean(m.is_error)});
                break;
            case 'approval_request':
                push({kind: 'approval', id: m.id, tool: m.tool,
                    input: JSON.stringify(m.input, null, 1), status: 'pending'});
                break;
            case 'done':
                setStatus('ready');
                // a Follow turn that had nothing to say leaves no trace at all
                setItems((xs) => {
                    const drop = xs[xs.length - 1]?.kind === 'draft';
                    const base = drop ? xs.slice(0, -1) : xs;
                    return m.quiet ? base : [...base, {
                        kind: 'info',
                        text: (m.duration_ms / 1000).toFixed(1) + 's · ' + m.num_turns + ' turns' +
                            (m.cost_usd ? ' · $' + m.cost_usd.toFixed(4) : ''),
                    }];
                });
                break;
            case 'error':
                setStatus((s) => (s === 'busy' ? 'ready' : s));
                push({kind: 'error', text: m.message});
                break;
            }
        };
        ws.onclose = () => setStatus('offline');
        ws.onerror = () => setStatus('offline');
        return () => ws.close();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [enabled]);   // NOT patientId — see the header

    /* ── the patient changed: mark it, loudly ─────────────────────────────────── */
    const prevPatient = useRef<string | null>(null);
    useEffect(() => {
        if (patientId && prevPatient.current && patientId !== prevPatient.current) {
            push({kind: 'divider', text: '👤 ' + patientId});
        }
        prevPatient.current = patientId;
    }, [patientId, push]);

    /* ── Follow mode: the clinician clicked; should the agent say anything? ────── */
    useEffect(() => {
        const f = followState.current;
        if (!f.on || !enabled || pulse === 0 || f.busy || f.used >= FOLLOW_CAP) {
            return;
        }
        const t = setTimeout(() => {
            const ws = wsRef.current;
            const now = Date.now();
            if (!ws || ws.readyState !== WebSocket.OPEN || followState.current.busy) {
                return;
            }
            if (now - followState.current.last < FOLLOW_MIN_GAP_MS) {
                return;
            }
            const evs = cb.current.drainUserEvents();
            if (evs.length === 0) {
                return;    // the pulse came from the agent's own action — not news
            }
            followState.current.last = now;
            followState.current.used += 1;
            setStatus('busy');
            ws.send(JSON.stringify({
                type: 'follow',
                events: evs.map((e) => e.what),
                snapshot: cb.current.snapshot(),
            }));
        }, FOLLOW_DEBOUNCE_MS);
        return () => clearTimeout(t);
    }, [pulse, follow, enabled, status]);

    /* ── the clinician speaks ─────────────────────────────────────────────────── */
    const send = useCallback((text: string) => {
        const ws = wsRef.current;
        if (!text.trim() || !ws || ws.readyState !== WebSocket.OPEN) {
            return;
        }
        push({kind: 'user', text});
        setStatus('busy');
        ws.send(JSON.stringify({
            type: 'user',
            text,
            snapshot: cb.current.snapshot(),
            events: cb.current.drainUserEvents().map((e) => e.what),
        }));
    }, [push]);

    const answer = useCallback((id: string, approved: boolean) => {
        wsRef.current?.send(JSON.stringify({type: 'approval_response', id, approved}));
        setItems((xs) => xs.map((it) =>
            it.kind === 'approval' && it.id === id
                ? {...it, status: approved ? 'allowed' : 'denied'}
                : it));
    }, []);

    const interrupt = useCallback(() => {
        wsRef.current?.send(JSON.stringify({type: 'interrupt'}));
    }, []);

    return {items, status, follow, setFollow, send, answer, interrupt};
}
