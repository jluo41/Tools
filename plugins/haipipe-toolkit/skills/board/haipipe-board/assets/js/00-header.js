/* Every write posts `path`, and the server takes that path's PARENT as the
   board folder. In the board/ tree a page lives at
   `<board>/board/<GROUP>/<page>.html`, so the naive pathname makes the server
   look for board.md inside `board/<GROUP>/` and every write silently fails
   (found by driving a real submit, JL 260731). Collapse the tree tail back to
   the board root so both packagings post the same thing.
   Declared at file scope on purpose: SEVEN separate writers call it. */
function boardPath() {
  var p = location.pathname;
  var i = p.lastIndexOf('/board/');
  // Name the board by its SOURCE, `board.md`, not by a generated artifact.
  // This said `board.html` until 260731 and kept working only because the
  // server takes the path's PARENT and never stats the file: once the
  // monolith was retired it pointed at something that no longer exists.
  return (i === -1 ? p.replace(/\/[^/]*$/, '') : p.slice(0, i)) + '/board.md';
}

/* ─────────────────────────────────────────────────────────────
   Comment layer — PURE ENHANCEMENT. The prose is already real HTML;
   this script only ADDS "select -> comment -> highlight right away".
   Strip this script block and the board still reads fine (just no commenting).

   Comments go straight to the server, which writes each one beneath its
   selected sentence in the source Markdown.
   ───────────────────────────────────────────────────────────── */