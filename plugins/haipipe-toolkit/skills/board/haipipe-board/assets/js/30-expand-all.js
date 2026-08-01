
/* ── section「expand / collapse all」──────────────────────────────
   Pure enhancement over native <details>. Strip this block and every
   item is still individually openable; all text stays in the DOM. */
document.addEventListener('click', function (ev) {
  var b = ev.target.closest && ev.target.closest('.secall');