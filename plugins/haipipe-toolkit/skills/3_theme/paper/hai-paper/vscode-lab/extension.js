// Paper Writing Lab: when a window opens, open what its workspace lists in `haipipeLab.terminals`:
// each Section's draft page (its `url`, the workbench) side by side in the editor area, and below them, in the
// terminal panel, each Section's session (its `command`), split side by side in the same order.
// open_writing_lab.py (/hai-paper lab) writes the list into a lab's .code-workspace; a window without the
// list is left alone. Rewriting the list (open_writing_lab.py --apply again) reopens whatever is missing;
// `haipipeLab.window` {action: close|restart, at} closes the window, or closes and reopens the lab's terminals,
// when the script changes it.
const vscode = require("vscode");

const pages = new Map(); // unit name -> its webview panel

function pageHtml(url) {
  const origin = new URL(url).origin;
  return `<!doctype html><html><head><meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; frame-src ${origin}; style-src 'unsafe-inline';">
<style>html,body{margin:0;padding:0;height:100%;overflow:hidden}iframe{border:0;width:100%;height:100%}</style>
</head><body><iframe src="${url}"></iframe></body></html>`;
}

function openPage(item, column) {
  const old = pages.get(item.name);
  if (old) {
    old.webview.html = pageHtml(item.url);
    return;
  }
  const panel = vscode.window.createWebviewPanel(
    "haipipeLab.page",
    item.name,
    { viewColumn: column, preserveFocus: true },
    { enableScripts: true, retainContextWhenHidden: true }
  );
  panel.webview.html = pageHtml(item.url);
  panel.onDidDispose(() => pages.delete(item.name));
  pages.set(item.name, panel);
}

// The integrated browser (VS Code 1.109+): a real browser tab with its address bar, back, forward and reload
// (JL 261114: "I think what I want it the real website to be open"). The iframe webview stays the fallback.
const BROWSER = "workbench.action.browser.open";
const FOCUS = ["First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth"]
  .map((n) => `workbench.action.focus${n}EditorGroup`);

async function openBrowserPages(items) {
  const have = (await vscode.commands.getCommands(true)).includes(BROWSER);
  if (!have) return false;
  // Every open is a fresh page (JL 261114: "I want the website to be ready and be refreshed"): each column's old
  // tabs (a restored, empty webview; yesterday's browser tab) are closed, then its page is opened again.
  for (let i = 0; i < items.length && i < FOCUS.length; i++) {
    const group = vscode.window.tabGroups.all[i];
    if (group && group.tabs.length) await vscode.window.tabGroups.close(group.tabs, true);
    await vscode.commands.executeCommand(FOCUS[i]);
    await vscode.commands.executeCommand(BROWSER, items[i].url);
  }
  return true;
}

async function refreshPages() {
  const items = (vscode.workspace.getConfiguration("haipipeLab").get("terminals") || []).filter((x) => x.url);
  if (!(await openBrowserPages(items))) items.forEach((item, i) => openPage(item, i + 1));
}

let running = false;

async function openLab() {
  if (running) return;
  running = true;
  try {
    const items = vscode.workspace.getConfiguration("haipipeLab").get("terminals") || [];
    if (!items.length) return;
    const withPage = items.filter((x) => x.url);
    if (withPage.length) {
      await vscode.commands.executeCommand("workbench.action.closeSidebar");
      await vscode.commands.executeCommand("vscode.setEditorLayout", {
        orientation: 0,
        groups: withPage.map(() => ({})),
      });
      if (!(await openBrowserPages(withPage))) withPage.forEach((item, i) => openPage(item, i + 1));
    }
    // A split lands right after its parent, so each new terminal splits from the one before it in the list;
    // splitting every one from the first put the third beside the first (JL 261114: t03, Appendix, t04).
    const open = new Map(vscode.window.terminals.map((t) => [t.name, t]));
    let first = items.map((x) => open.get(x.name)).find(Boolean);
    let prev = null;
    for (const item of items) {
      if (open.has(item.name)) {
        prev = open.get(item.name);
        continue;
      }
      const parent = prev || first;
      const term = vscode.window.createTerminal({
        name: item.name,
        cwd: item.cwd,
        location: parent ? { parentTerminal: parent } : vscode.TerminalLocation.Panel,
      });
      term.sendText(item.command, true);
      prev = term;
      first = first || term;
    }
    if (first) first.show(true);
  } finally {
    running = false;
  }
}

// --restart: a window reload restores the old terminals by name, so the lab saw them as open and started
// nothing, even when their session had ended (JL 261114). Close the lab's own terminals, then open them again;
// each new terminal resumes its Section session from its transcript.
async function restartLab() {
  const names = new Set((vscode.workspace.getConfiguration("haipipeLab").get("terminals") || []).map((x) => x.name));
  for (const t of vscode.window.terminals) if (names.has(t.name)) t.dispose();
  await new Promise((r) => setTimeout(r, 1500));
  return openLab();
}

function activate(context) {
  context.subscriptions.push(
    vscode.commands.registerCommand("haipipeLab.open", openLab),
    vscode.commands.registerCommand("haipipeLab.refresh", refreshPages),
    vscode.workspace.onDidChangeConfiguration((e) => {
      if (e.affectsConfiguration("haipipeLab.window")) {
        // open_writing_lab.py --close / --restart: acted on only when it changes, never when a window opens
        const act = (vscode.workspace.getConfiguration("haipipeLab").get("window") || {}).action;
        if (act === "close") return vscode.commands.executeCommand("workbench.action.closeWindow");
        if (act === "restart") return restartLab();
        if (act === "refresh") return refreshPages();
      }
      if (e.affectsConfiguration("haipipeLab.terminals")) openLab();
    })
  );
  return openLab();
}

function deactivate() {}

module.exports = { activate, deactivate };
