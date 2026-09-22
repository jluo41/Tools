  // Shared text escaping for the workbench drawer.
  function esc(s) { return s.replace(/[&<>]/g, function (c) {
    return { '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]; }); }
