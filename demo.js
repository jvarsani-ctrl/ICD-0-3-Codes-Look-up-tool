/* ============================================================================
   demo.js — the walk-through player on the landing page.

   A walk-through is data (data/shared/demo_walkthroughs.json): a made-up case and
   the clicks a clerk would make, grouped into beats with a caption each. This
   file finds each recorded control on the screen the engine has drawn and fires
   it through the page's own listeners, so the tool above is driven by the same
   code a clerk drives. There is no clinical content here and none in the engine
   for it: app.js neither knows nor needs this file.

   pick() is pure and is also run by build/demo_driver.mjs against the real
   engine, so the control a recorded step names is chosen by one function in the
   build and in the browser.

   Left out on purpose when the page is embedded (?host=redcap): a clerk filling a
   form has no use for a demo, and the iframe has no room for one.
   ========================================================================== */
var PedsDemo = (function () {
  'use strict';

  var DATA_URL = 'data/shared/demo_walkthroughs.json';

  /* ----------------------------------------------------------- matching (pure) */
  function norm(s) { return String(s == null ? '' : s).replace(/\s+/g, ' ').trim().toLowerCase(); }

  /* list: [{ attrs: {'data-act': …, 'data-i': …}, text: '…' }]. A step names a
     control by its act, by data attributes (step.attrs, without the "data-"
     prefix) and by text. The text matches as a substring, and an exact match
     wins over a longer option that merely contains it. Zero or several matches
     throw: a renamed option must stop the demo, not replay the wrong answer. */
  function pick(list, step) {
    var want = norm(step.text), hits = [];
    list.forEach(function (c, i) {
      if (c.attrs['data-act'] !== step.act) return;
      var a = step.attrs || {};
      for (var k in a) if (Object.prototype.hasOwnProperty.call(a, k) && c.attrs['data-' + k] !== String(a[k])) return;
      if (want && norm(c.text).indexOf(want) === -1) return;
      hits.push(i);
    });
    if (want) {
      var exact = hits.filter(function (i) { return norm(list[i].text) === want; });
      if (exact.length === 1) return exact[0];
    }
    if (hits.length !== 1) {
      var err = new Error((hits.length ? 'matches ' + hits.length + ' controls' : 'matches no control') + ' for ' + JSON.stringify(step));
      err.count = hits.length;
      throw err;
    }
    return hits[0];
  }

  /* A caption's reading time: long enough to read aloud, never longer than a breath. */
  function dwell(text) { return Math.min(7000, 1800 + 32 * String(text || '').length); }

  /* ------------------------------------------------------------------ browser */
  var doc = typeof document !== 'undefined' ? document : null;
  var els = {}, cases = [], run = null, slot = null, observer = null;

  var sleep = function (ms) { return new Promise(function (r) { setTimeout(r, ms); }); };
  var reduced = function () { return !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches); };
  var stage = function () { return typeof state !== 'undefined' && state ? state.stage : null; };

  function textOf(el) {
    var tag = el.tagName;
    if (tag === 'BUTTON') return el.textContent;
    var label = el.closest('label');
    if (label) return label.textContent;
    return el.getAttribute('aria-label') || el.getAttribute('placeholder') || '';
  }

  function controls() {
    var out = [];
    Array.prototype.forEach.call(slot.querySelectorAll('[data-act]'), function (el) {
      var attrs = {};
      Array.prototype.forEach.call(el.attributes, function (a) { attrs[a.name] = a.value; });
      out.push({ el: el, attrs: attrs, text: textOf(el) });
    });
    return out;
  }

  /* The control a step names, waiting for the engine to draw it. A group's file
     loads on first use, so the next screen can be a moment away. */
  function waitFor(step, token) {
    var t0 = Date.now();
    return new Promise(function (resolve, reject) {
      (function poll() {
        if (run && run.token !== token) return reject(new Error('stopped'));
        var list = controls();
        try { return resolve(list[pick(list, step)]); }
        catch (e) {
          if (e.count > 1 || Date.now() - t0 > 6000) return reject(e);
        }
        setTimeout(poll, 60);
      })();
    });
  }

  function perform(c, step) {
    var el = c.el, tag = el.tagName, type = el.type || '';
    if (tag === 'SELECT') {
      el.value = step.value;
      el.dispatchEvent(new Event('change', { bubbles: true }));
    } else if (tag === 'TEXTAREA' || (tag === 'INPUT' && !/^(checkbox|radio)$/.test(type))) {
      el.focus();
      el.value = step.type !== undefined ? step.type : (step.value || '');
      el.dispatchEvent(new Event('input', { bubbles: true }));
    } else if (tag === 'INPUT' && type === 'checkbox') {
      if (el.checked !== (step.checked === undefined ? true : !!step.checked)) el.click();
    } else {
      el.click();
    }
  }

  /* While a beat runs every button but Close is off, except Pause during Play all,
     which takes effect when the beat in hand has finished. */
  function setBusy(on) {
    Array.prototype.forEach.call(els.bar.querySelectorAll('button'), function (b) {
      var what = b.getAttribute('data-demo');
      if (what === 'close') return;
      b.disabled = on && !(what === 'play' && run && run.playing);
    });
  }

  async function doBeat(token) {
    var beat = run.c.beats[run.i];
    run.busy = true;
    setBusy(true);
    for (var k = 0; k < beat.do.length; k++) {
      var step = beat.do[k], c = await waitFor(step, token);
      if (run.token !== token) return false;
      c.el.classList.add('demo-focus');
      c.el.scrollIntoView({ block: 'nearest', behavior: reduced() ? 'auto' : 'smooth' });
      await sleep(run.fast ? 120 : 420);
      if (run.token !== token) return false;
      perform(c, step);
      await sleep(run.fast ? 90 : 220);
      c.el.classList.remove('demo-focus');
    }
    /* Let the screen the last click led to finish drawing before the caption names it. */
    await sleep(160);
    run.i++;
    run.busy = false;
    return true;
  }

  /* ----------------------------------------------------------------------- UI */
  function show(node, on) { node.hidden = !on; }

  function paint() {
    var idle = !run, landing = stage() === 'landing';
    show(els.section, idle ? landing : false);
    show(els.bar, !idle);
    doc.body.classList.toggle('has-demobar', !idle);
    if (idle) { doc.documentElement.style.removeProperty('--demobar-h'); return; }

    var c = run.c, n = c.beats.length, done = run.i >= n;
    els.title.textContent = c.title;
    /* The caption describes the step just taken, so the count names that step. */
    els.count.textContent = done ? 'Step ' + n + ' of ' + n + ' · result' : (run.i === 0 ? n + ' steps' : 'Step ' + run.i + ' of ' + n);
    els.say.textContent = run.i === 0 ? 'A made-up case. Press Next step, or Play all, and the tool above fills itself in.'
      : c.beats[run.i - 1].say;
    var next = els.bar.querySelector('[data-demo="next"]'), play = els.bar.querySelector('[data-demo="play"]'),
        again = els.bar.querySelector('[data-demo="replay"]');
    next.hidden = done; play.hidden = done; again.hidden = !done;
    play.textContent = run.playing ? 'Pause' : (run.i === 0 ? 'Play all' : 'Play the rest');
    setBusy(!!run.playing || !!run.busy);
    measure();
  }

  function measure() {
    var h = els.bar.offsetHeight;
    if (h) doc.documentElement.style.setProperty('--demobar-h', h + 'px');
  }

  function fileList(c) {
    els.file.innerHTML = '';
    c.file.forEach(function (line) {
      var li = doc.createElement('li');
      li.textContent = line;
      els.file.appendChild(li);
    });
    els.details.open = true;
  }

  function begin(id) {
    var c = cases.filter(function (x) { return x.id === id; })[0];
    if (!c || stage() !== 'landing') return;
    run = { c: c, i: 0, token: {}, playing: false, fast: false };
    fileList(c);
    paint();
    els.bar.querySelector('[data-demo="next"]').focus();
  }

  async function step() {
    if (!run || run.busy || run.i >= run.c.beats.length) return;
    var token = run.token;
    els.details.open = false;
    try {
      if (!(await doBeat(token))) return;
    } catch (e) {
      if (e.message === 'stopped') return;
      return fail(e);
    }
    paint();
  }

  /* A wait that ends early when the loop that asked for it is no longer the one playing. */
  async function nap(ms, alive) {
    for (var t = 0; t < ms && alive(); t += 100) await sleep(100);
  }

  async function play() {
    if (!run || run.busy) { if (run && run.playing) { run.playing = false; run.loop = null; paint(); } return; }
    if (run.playing) { run.playing = false; run.loop = null; paint(); return; }
    var token = run.token, me = run.loop = {};
    var mine = function () { return run && run.token === token && run.loop === me; };
    run.playing = true; paint();
    while (mine() && run.i < run.c.beats.length) {
      els.details.open = false;
      try { if (!(await doBeat(token))) return; } catch (e) { if (e.message !== 'stopped') fail(e); return; }
      paint();
      if (mine() && run.i < run.c.beats.length) await nap(dwell(run.c.beats[run.i - 1].say), mine);
    }
    if (run && run.token === token && run.loop === me) { run.playing = false; run.loop = null; paint(); }
  }

  function fail(e) {
    var token = run && run.token;
    els.say.textContent = 'The walk-through stopped: the tool no longer matches this recording (' + e.message + '). The case on screen is still yours to continue.';
    if (run) { run.playing = false; run.loop = null; run.busy = false; run.token = {}; }
    setBusy(false);
    els.bar.querySelector('[data-demo="next"]').hidden = true;
    els.bar.querySelector('[data-demo="play"]').hidden = true;
    els.bar.querySelector('[data-demo="replay"]').hidden = false;
    return token;
  }

  function close() {
    if (run) run.token = {};
    run = null;
    Array.prototype.forEach.call(doc.querySelectorAll('.demo-focus'), function (e) { e.classList.remove('demo-focus'); });
    paint();
  }

  /* Back to the start: the engine is reset and redrawn exactly as its own
     "Start new case" does (reset() clears the state, the page redraws after it). */
  function replay() {
    if (!run || typeof window.reset !== 'function') return;
    var c = run.c;
    run.token = {}; run.loop = null;
    window.reset();
    window.render();
    run = { c: c, i: 0, token: {}, playing: false, fast: false };
    fileList(c);
    paint();
    els.bar.querySelector('[data-demo="next"]').focus();
  }

  /* The clerk starts a new case, or goes Home, while a walk-through is open: it is
     over. Changes the player itself makes never reach here, because it only acts
     between a click and the engine's next draw. */
  function watch() {
    var last = stage();
    observer = new MutationObserver(function () {
      var now = stage();
      if (run && now === 'landing' && last !== 'landing' && run.i > 0) { close(); }
      else if (now !== last) paint();
      last = now;
    });
    observer.observe(slot, { childList: true });
  }

  function build() {
    els.section = doc.getElementById('demos');
    els.list = doc.getElementById('demos-list');
    els.bar = doc.getElementById('demobar');
    els.title = els.bar.querySelector('.demobar__title');
    els.count = els.bar.querySelector('.demobar__count');
    els.say = els.bar.querySelector('.demobar__say');
    els.file = els.bar.querySelector('.demobar__file ul');
    els.details = els.bar.querySelector('.demobar__file');
    cases.forEach(function (c) {
      var li = doc.createElement('li'), b = doc.createElement('button');
      b.type = 'button'; b.className = 'demo-card card'; b.setAttribute('data-case', c.id);
      [['demo-card__group', c.group], ['demo-card__title', c.title], ['demo-card__teaser', c.teaser], ['demo-card__go', 'Watch it step by step']]
        .forEach(function (p) { var s = doc.createElement('span'); s.className = p[0]; s.textContent = p[1]; b.appendChild(s); });
      li.appendChild(b); els.list.appendChild(li);
    });
    els.section.addEventListener('click', function (ev) {
      var b = ev.target.closest('[data-case]');
      if (b) begin(b.getAttribute('data-case'));
    });
    els.bar.addEventListener('click', function (ev) {
      var b = ev.target.closest('[data-demo]');
      if (!b || b.disabled) return;
      var what = b.getAttribute('data-demo');
      if (what === 'next') step(); else if (what === 'play') play();
      else if (what === 'replay') replay(); else if (what === 'close') close();
    });
    if (window.ResizeObserver) new ResizeObserver(measure).observe(els.bar);
    watch();
    paint();
  }

  function init() {
    if (!doc || !doc.getElementById('demos')) return;
    if (new URLSearchParams(window.location.search).get('host') === 'redcap') return;
    slot = doc.getElementById('slot');
    fetch(DATA_URL).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (d) { cases = d.cases || []; if (cases.length) build(); })
      .catch(function () { /* no walk-throughs: the section stays hidden and the tool is untouched */ });
  }

  if (doc && doc.addEventListener) doc.addEventListener('DOMContentLoaded', init);
  return { pick: pick, dwell: dwell };
})();
