import React, {useEffect, useState} from 'react';
import ReactDOM from 'react-dom/client';

import Console, {type Scope} from './Console';
import './theme/mattermost.css';
import './theme/databricks.css';
import './console.css';

/* Skin: standalone pages default to the Databricks skin; iframe embeds keep the
 * host's Mattermost theme (HAI-Chat sets the tokens itself). `?theme=databricks`
 * or `?theme=mattermost` forces either way. */
const forced = new URLSearchParams(window.location.search).get('theme');
const skin = forced ?? (window.self !== window.top ? 'mattermost' : 'databricks');
if (skin === 'databricks') {
    document.documentElement.dataset.skin = 'databricks';
}

/* ── scope routing ──────────────────────────────────────────────────────────
 * /individual and /group are two SEPARATE logics that share one shell. The URL
 * path is the source of truth. Changing it REMOUNTS <Console> (key=scope), so
 * each side keeps its own state and its own HaiChat session — while the rail and
 * the topbar, being the same components, stay identical across the two. */
const scopeOf = (path: string): Scope =>
    path.replace(/\/+$/, '').endsWith('/group') ? 'group' : 'individual';

function App() {
    const [scope, setScope] = useState<Scope>(() => scopeOf(window.location.pathname));

    useEffect(() => {
        const onPop = () => setScope(scopeOf(window.location.pathname));
        window.addEventListener('popstate', onPop);
        return () => window.removeEventListener('popstate', onPop);
    }, []);

    const navigate = (s: Scope) => {
        if (s === scope) {
            return;
        }
        window.history.pushState(null, '', '/' + s + window.location.search);
        setScope(s);
    };

    return <Console key={scope} scope={scope} navigate={navigate}/>;
}

ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
        <App/>
    </React.StrictMode>,
);
