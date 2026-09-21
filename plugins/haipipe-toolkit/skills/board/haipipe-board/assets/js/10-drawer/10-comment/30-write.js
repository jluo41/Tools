  // Explicit plugin workspace requests; Page prose has no write routes.
  async function post(url, payload) {
    payload.path = boardPath();
    var r = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' },
                               body: JSON.stringify(payload) });
    if (r.status === 404 || r.status === 501) return null;
    return await r.json();
  }
