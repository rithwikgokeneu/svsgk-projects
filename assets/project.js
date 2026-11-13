(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  // mobile menu
  const burger = $('#burger'), menu = $('#menu');
  burger.addEventListener('click', () => burger.setAttribute('aria-expanded', menu.classList.toggle('open')));
  $$('#menu a').forEach(a => a.addEventListener('click', () => menu.classList.remove('open')));

  // back-to-top button
  const top = $('#totop');
  const onScroll = () => top.classList.toggle('show', scrollY > 600);
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  // generic tab groups
  const tabGroup = (tabsSel, itemsSel, key) => {
    const tabs = $$(tabsSel);
    tabs.forEach(t => t.addEventListener('click', () => {
      tabs.forEach(x => x.setAttribute('aria-selected', x === t));
      $$(itemsSel).forEach(el => el.hidden = el.dataset[key] !== t.dataset[key]);
    }));
  };
  tabGroup('#ltabs button', '#checks li', 'k');
  tabGroup('#atabs button', '#agrid .am', 'c');

  // gallery: centre slide + one peek either side
  const figs = $$('#gal figure'), cap = $('#galcap');
  let idx = 0;
  const paint = () => {
    const n = figs.length;
    figs.forEach(f => f.className = '');
    if (n > 2) figs[(idx - 1 + n) % n].className = 'side';
    figs[idx].className = 'mid';
    if (n > 1) figs[(idx + 1) % n].className = 'side';
    // keep DOM order visually: prev, mid, next
    const track = $('#gal');
    if (n > 2) track.append(figs[(idx - 1 + n) % n], figs[idx], figs[(idx + 1) % n]);
    cap.textContent = figs[idx].dataset.cap || '';
  };
  $$('.gal .arr').forEach(b => b.addEventListener('click', () => {
    idx = (idx + +b.dataset.dir + figs.length) % figs.length; paint();
  }));
  figs.forEach((f, i) => f.addEventListener('click', () => {
    if (f.classList.contains('side')) { idx = i; paint(); } else openLb(f.dataset.full, f.dataset.cap);
  }));
  let sx = null;
  $('#gal').addEventListener('touchstart', ev => sx = ev.touches[0].clientX, { passive: true });
  $('#gal').addEventListener('touchend', ev => {
    if (sx === null) return; const dx = ev.changedTouches[0].clientX - sx; sx = null;
    if (Math.abs(dx) > 40) { idx = (idx + (dx < 0 ? 1 : -1) + figs.length) % figs.length; paint(); }
  });
  paint();

  // faq accordion + view more
  $$('#faq .item').forEach(it => $('.q', it).addEventListener('click', () => {
    const open = it.classList.toggle('open');
    $('.q', it).setAttribute('aria-expanded', open);
  }));
  const vm = $('#vm');
  vm.addEventListener('click', () => {
    const hidden = $$('#faq .item[hidden]');
    if (hidden.length) { hidden.forEach(h => h.hidden = false); vm.textContent = 'View Less'; }
    else { $$('#faq .item').forEach((h, i) => { if (i >= 3) h.hidden = true; }); vm.textContent = 'View More'; }
  });

  // lightbox
  const lb = $('#lb'), lbImg = $('#lb img');
  const openLb = (src, alt) => { lbImg.src = src; lbImg.alt = alt || ''; lb.classList.remove('zoomed'); lb.showModal(); };
  $$('.layout-img').forEach(el => el.addEventListener('click', () => openLb(el.dataset.full, el.querySelector('img').alt)));
  lbImg.addEventListener('click', ev => { ev.stopPropagation(); lb.classList.toggle('zoomed'); });
  $('#lb .x').addEventListener('click', () => lb.close());
  lb.addEventListener('click', ev => { if (ev.target === lb || ev.target.classList.contains('stage')) lb.close(); });

  // enquiry modal -> WhatsApp
  const m = $('#enqm'), f = $('#enqf');
  $$('[data-enq]').forEach(b => b.addEventListener('click', ev => { ev.preventDefault(); m.showModal(); }));
  $('[data-close]', m).addEventListener('click', () => m.close());
  m.addEventListener('click', ev => { if (ev.target === m) m.close(); });
  f.addEventListener('submit', ev => {
    ev.preventDefault();
    const d = new FormData(f);
    const txt = `Hi SVSGK, I'm enquiring about ${f.dataset.project}.\nName: ${d.get('name')}\nPhone: ${d.get('phone')}\n${d.get('msg')}`;
    window.open(`${f.dataset.wa}?text=${encodeURIComponent(txt)}`, '_blank', 'noopener');
    m.close();
  });
})();
