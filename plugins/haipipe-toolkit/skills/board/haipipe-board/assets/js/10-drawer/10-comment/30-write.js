  /* ── 写盘：优先让服务器写 ───────────────────────────────────
     板文件在服务器上，浏览器在你自己的机器上（Remote-SSH）——
     File System Access 的文件夹选择器只看得到你本机的盘，够不着这些文件。
     所以第一选择是发个 POST 让服务器写（serve.py），它写完顺手重新生成 html。
     只有服务器不支持时，才退回浏览器直接写文件 / 复制补丁。          */
  var srvOK = null;                       // null=没试过, true/false=试过
  async function post(url, payload) {
    payload.path = boardPath();
    var r = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' },
                               body: JSON.stringify(payload) });
    if (r.status === 404 || r.status === 501) { srvOK = false; return null; }
    srvOK = true;
    return await r.json();
  }
  async function srvComment(c) {
    try {
      var j = await post('/_board/comment',
        { file: c.file, who: c.who, sentence: c.sentence, text: c.text,
          quote: c.quote, when: c.when || stamp() });
      if (!j) return null;
      return j.ok ? true : j.err;
    } catch (e) { srvOK = false; return null; }
  }
  /* ── 兜底：浏览器自己写文件（只在服务器不支持时才用到）
     文件夹句柄记在 IndexedDB 里，授权一次，之后每次保存直接写盘 ──
     浏览器规定：第一次挑文件夹必须由用户点击触发，无法自动。
     但句柄可以存下来；之后每次「Save」本身就是一次点击，够格再申请权限，
     所以正常情况下你一个 session 只会看到一次 Allow。                */
  function idb(fn) {
    return new Promise(function (res) {
      var r = indexedDB.open('board-fs', 1);
      r.onupgradeneeded = function () { r.result.createObjectStore('h'); };
      r.onsuccess = function () {
        var db = r.result, tx = db.transaction('h', 'readwrite');
        fn(tx.objectStore('h'), res);
      };
      r.onerror = function () { res(null); };
    });
  }
  function getDir() { return idb(function (s, res) {
    var g = s.get('dir'); g.onsuccess = function () { res(g.result || null); }; }); }
  function putDir(h) { return idb(function (s, res) { s.put(h, 'dir'); res(1); }); }

  var dirH = null;
  async function ensureDir(ask) {
    if (!window.showDirectoryPicker) return null;
    if (!dirH) dirH = await getDir();
    if (dirH) {
      var st = await dirH.queryPermission({ mode: 'readwrite' });
      if (st === 'granted') return dirH;
      if (ask) {
        st = await dirH.requestPermission({ mode: 'readwrite' });
        if (st === 'granted') return dirH;
      }
      return null;
    }
    if (!ask) return null;
    try {
      dirH = await window.showDirectoryPicker({ mode: 'readwrite' });
      await putDir(dirH);
      return dirH;
    } catch (e) { return null; }
  }

  async function edit(dir, file, fn) {
    var fh = await dir.getFileHandle(file);
    var txt = await (await fh.getFile()).text();
    var next = fn(txt);
    if (next === txt) return false;
    var w = await fh.createWritable();
    await w.write(next); await w.close();
    return true;
  }
  /* 把已经写盘的从待办里剔掉；写不进去的留着，面板里还看得见 */
  async function drain(ask) {
    if (!db.length) return 0;
    if (srvOK !== false) {                       // 先试服务器
      var n = 0, err = null;
      for (var i = 0; i < db.length; i++) {
        var r = await srvComment(db[i]);
        if (r === true) { db[i].written = 1; n++; }
        else if (typeof r === 'string') { err = r; }
        else break;                              // null = 服务器不支持，退出去走老路
      }
      if (n || srvOK) {
        db = db.filter(function (c) { return !c.written; });
        localStorage.setItem(KEY, JSON.stringify(db));
        paint();
        if (err) say(err);
        if (srvOK) return n;
      }
    }
    return 0;
  }
