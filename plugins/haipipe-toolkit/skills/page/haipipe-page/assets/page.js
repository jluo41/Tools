/* Native details remain usable without script, including static exports. */
document.addEventListener('click', event => {
  const button = event.target.closest('.secall');
  if (!button) return;
  event.preventDefault();
  event.stopPropagation();
  const section = button.closest('details');
  if (!section) return;
  const nested = [...section.querySelectorAll('details')];
  const open = nested.some(item => !item.open);
  section.open = true;
  nested.forEach(item => { item.open = open; });
  const label = button.querySelector('.lbl');
  if (label) label.textContent = open ? 'collapse all' : 'expand all';
});
