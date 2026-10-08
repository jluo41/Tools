/* One Block workbench, reachable from any Task Page on that Block. */
(function () {
  'use strict';
  if (!window.boardWorkbenches) return;
  function url() { return '/_board/work-board?path=' + encodeURIComponent(boardPath()); }
  window.boardWorkbenches.register({
    id: 'task-board', label: '📋 Task Block', order: 29, menu: 'workbench',
    hint: 'Jobs, Task progress, Run receipts and readings across this Block',
    applies: function (page, type) {
      if (document.body.getAttribute('data-board-kind') === 'task-block') return true;
      return (type === 'task' || (page && page.getAttribute('data-folder-kind') === 'task')) &&
        /^j\d{2}_[^/]+\/t\d{2}_[^/]+\/t\d{2}_[^/]+\.md$/.test((page && page.getAttribute('data-file')) || '');
    },
    open: function () { window.open(url(), '_blank', 'noopener'); },
    tab: {url: url, write: function (page, done, fail) {
      fetch('/_board/work-board', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({path: boardPath()})})
        .then(function (r) { return r.json(); })
        .then(function (data) { if (data.ok) { if (done) done(data); } else if (fail) fail(data.err); })
        .catch(function (error) { if (fail) fail(String(error)); });
    }}
  });
})();
