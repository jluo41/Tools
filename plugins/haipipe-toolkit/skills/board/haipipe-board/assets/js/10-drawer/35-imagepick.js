  /* 🖼 Attach an image WITHOUT a clipboard (QD14, JL 260801: "然后我们手机上的话，
     如何 upload 这个 image 呢?").

     Until now the only two ways an image could enter the board were `paste`
     listeners — the terminal pane in 30-terminal.js and the comment box in
     10-comment/40-paste.js — and pasting an image into a pane is a DESKTOP
     gesture. A phone offers a photo library and a camera, and both of those are
     an `<input type="file">`, which this board never had. So on a phone the
     board simply could not take a screenshot or a photo at all.

     The server half needed nothing: /_board/image already accepts a base64 data
     URL and writes into the board's fig/, so the whole gap was this gesture.

     Why it re-encodes instead of forwarding the file untouched: live/write.py
     caps an image at 8MB and accepts png/jpeg/gif/webp ONLY, while a modern
     phone routinely shoots larger than the cap and an iPhone shoots HEIC, which
     is not on that list. Drawing the file through a canvas both shrinks it and
     normalises the format, so one button serves a 12MP photo and a screenshot.
     A small PNG is passed through instead, because re-encoding a screenshot to
     JPEG blurs exactly the text you took the screenshot to show. */
  var PICK_MAX = 1600, PICK_Q = 0.85, PICK_PNG_KEEP = 3 * 1024 * 1024;

  function shrinkImage(file) {
    return new Promise(function (res, rej) {
      if (file.type === 'image/png' && file.size < PICK_PNG_KEEP) {
        var fr = new FileReader();
        fr.onload = function () { res(fr.result); };
        fr.onerror = function () { rej(new Error('could not read that file')); };
        return fr.readAsDataURL(file);
      }
      var url = URL.createObjectURL(file);
      var img = new Image();
      img.onload = function () {
        var w = img.naturalWidth, h = img.naturalHeight;
        var s = Math.min(1, PICK_MAX / Math.max(w, h));
        var c = document.createElement('canvas');
        c.width = Math.max(1, Math.round(w * s));
        c.height = Math.max(1, Math.round(h * s));
        c.getContext('2d').drawImage(img, 0, 0, c.width, c.height);
        URL.revokeObjectURL(url);
        /* toDataURL throws on a tainted canvas; a local file cannot taint one,
           so this only fires on a decode the browser half-managed. */
        try { res(c.toDataURL('image/jpeg', PICK_Q)); }
        catch (e) { rej(new Error('could not convert that image')); }
      };
      img.onerror = function () {
        URL.revokeObjectURL(url);
        rej(new Error('this browser cannot decode that image (HEIC outside Safari?)'));
      };
      img.src = url;
    });
  }

  /* Where the path GOES depends on which half is showing, because the two halves
     want different things: the CLI wants a bare repo-root-relative path it can
     hand to its Read tool, the chat composer wants markdown it can send. Both
     are repo-root-relative rather than board-relative, because the session's cwd
     is the SPACE root and a bare fig/… does not resolve there. */
  async function attachImageFile(file) {
    if (!cq || !file) return;
    var data;
    try { data = await shrinkImage(file); }
    catch (e) { return say(e.message); }
    var j = null;
    try {
      j = await post('/_board/image',
        { file: cq.file, name: file.name || 'photo', data: data });
    } catch (e) { j = null; }
    if (!j || !j.ok) {
      return say((j && j.err) || 'image upload failed (is serve.py running?)');
    }
    var dir = boardDirPath().replace(/^\//, '');
    var path = (dir ? dir + '/' : '') + j.rel;
    if (termOn && termWS && termWS.readyState === 1) {
      termWS.send('0' + path);
      say('Attached ' + j.rel + ' — it is on the prompt line, press Enter');
    } else {
      var ta = chat.querySelector('.ft textarea');
      if (ta) insertAtCursor(ta, '![image](' + path + ')');
      else say('Saved ' + j.rel);
    }
  }

  (function () {
    var btn = chat.querySelector('.imgpick');
    if (!btn) return;
    var inp = document.createElement('input');
    inp.type = 'file';
    inp.accept = 'image/*';
    /* deliberately NOT `capture`: that attribute forces the camera and takes the
       photo library away, and a screenshot already in the library is the common
       case here. Without it a phone offers both. */
    inp.style.display = 'none';
    chat.appendChild(inp);
    btn.onclick = function () { inp.value = ''; inp.click(); };
    inp.onchange = function () {
      if (inp.files && inp.files[0]) attachImageFile(inp.files[0]);
    };
  })();
