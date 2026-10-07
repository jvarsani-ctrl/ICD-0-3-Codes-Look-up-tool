/* ============================================================================
   drive_first_tap.mjs — one tap must be enough, with REAL input.

   A box the clerk types into used to re-render the whole screen when focus
   left it, which is the mousedown on whatever the clerk clicks next. The
   button under the pointer was replaced before the mouseup, so the browser
   fired no click: the first tap on a search result, on Continue under a typed
   number or free-text answer, or on "Not documented" did nothing, and Tab from
   the search box dropped focus to the page. Fixed 4 Oct 2026 in app.js (the
   'change' and 'input' listeners at the foot of the file).

   A scripted element.click() cannot reproduce it, because it never moves
   focus. This drives headless Google Chrome over the DevTools protocol with
   keystrokes, mouse presses and key presses, and prints the event trace.

   Not part of build_database.py: it needs Chrome and a running server, and the
   build needs neither. Run it after touching the event wiring:

     python3 -m http.server 8811            (in the repo root, one terminal)
     node build/drive_first_tap.mjs 8811    (another)

   CHROME= overrides the browser path. Exit 1 if any tap was lost or any
   control failed. Negative controls: docs/engine_flow_negative_controls.md.
   ========================================================================= */
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const PORT = process.argv[2] || '8811';
const TERMS = process.argv.slice(3).length ? process.argv.slice(3) : ['RCC', 'Nephroblastoma', 'PPNET'];
const PROFILE = fs.mkdtempSync(path.join(os.tmpdir(), 'drive-first-tap-'));
const chrome = spawn(process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
  '--headless=new', '--remote-debugging-port=9334', '--user-data-dir=' + PROFILE,
  '--no-first-run', '--no-default-browser-check', 'about:blank'], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

let ws, id = 0; const pending = new Map();
const send = (method, params = {}) => new Promise((res, rej) => {
  const n = ++id; pending.set(n, { res, rej }); ws.send(JSON.stringify({ id: n, method, params }));
});
async function connect() {
  for (let i = 0; i < 50; i++) {
    try {
      const page = (await (await fetch('http://127.0.0.1:9334/json/list')).json()).find((t) => t.type === 'page');
      if (page) {
        ws = new WebSocket(page.webSocketDebuggerUrl);
        await new Promise((r) => (ws.onopen = r));
        ws.onmessage = (e) => { const m = JSON.parse(e.data); const p = pending.get(m.id);
          if (p) { pending.delete(m.id); m.error ? p.rej(new Error(m.error.message)) : p.res(m.result); } };
        return;
      }
    } catch { /* starting */ }
    await sleep(200);
  }
  throw new Error('Chrome did not start');
}
async function js(expr) {
  const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true });
  if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description || r.exceptionDetails.text);
  return r.result.value;
}

/* Instrumentation: every event on the way, with whether the element the mouse
   went down on is still in the document when the click would fire. */
const INSTRUMENT = `(() => {
  window.__trace = []; let down = null;
  const log = (e) => window.__trace.push(e.type + ' on ' + (e.target.getAttribute && (e.target.closest('[data-act]') || {}).getAttribute ?
    (e.target.closest('[data-act]') ? e.target.closest('[data-act]').getAttribute('data-act') : e.target.tagName) : e.target.nodeName) +
    (down ? ' (pressed button connected: ' + down.isConnected + ')' : ''));
  ['mousedown'].forEach((t) => document.addEventListener(t, (e) => { down = e.target.closest('[data-act]'); log(e); }, true));
  ['blur', 'focusout', 'change', 'mouseup', 'click'].forEach((t) => document.addEventListener(t, log, true));
})()`;

let lost = 0;
try {
  await connect();
  await send('Page.enable'); await send('Runtime.enable'); await send('Network.setCacheDisabled', { cacheDisabled: true });
  await send('Emulation.setDeviceMetricsOverride', { width: 1180, height: 900, deviceScaleFactor: 1, mobile: false });
  for (const term of TERMS) {
    await send('Page.navigate', { url: 'http://localhost:' + PORT + '/?t=' + Date.now() });
    await js(`(async () => { for (let i = 0; i < 100; i++) { if (window.state && state.stage === 'landing') return; await new Promise(r => setTimeout(r, 50)); } throw new Error('no landing'); })()`);
    await js(INSTRUMENT);
    await js(`document.querySelector('input[data-act="query"]').focus()`);
    await send('Input.insertText', { text: term });
    const box = await js(`(() => { const b = [...document.querySelectorAll('[data-act="alias"]')]
      .find(e => e.querySelector('.opt__label').firstChild.textContent.trim() === ${JSON.stringify(term)});
      const r = b.getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2 }; })()`);
    await js(`window.__trace.push('--- one tap on "${term}" ---')`);
    await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: box.x, y: box.y });
    await send('Input.dispatchMouseEvent', { type: 'mousePressed', x: box.x, y: box.y, button: 'left', clickCount: 1 });
    await send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: box.x, y: box.y, button: 'left', clickCount: 1 });
    await sleep(400);
    const r = await js(`({ stage: state.stage, trail: state.trail.map(t => t.label + ': ' + t.value), trace: window.__trace })`);
    const ok = r.stage !== 'landing' && r.trail[0] === 'Search: ' + term;
    if (!ok) lost++;
    console.log((ok ? 'OK   ' : 'LOST ') + JSON.stringify(term) + ' → stage ' + r.stage + ', trail ' + JSON.stringify(r.trail));
    for (const t of r.trace) console.log('       ' + t);
  }
  /* The same seam on tree questions: a box the clerk types into, then the
     Continue button under it. Setup goes straight to the node; the typing and
     the press are real. */
  const NODES = [
    { group: 1, tree: 'tree_acute_leukemia', node: 'ac_blast_gate', sel: 'input[type="number"][data-act="draft"]', text: '25' },
    { group: 1, tree: 'tree_acute_leukemia', node: 'ac_apl_confirm', sel: 'textarea[data-act="draft"]', text: 'PML::RARA detected' },
  ];
  for (const c of NODES) {
    await send('Page.navigate', { url: 'http://localhost:' + PORT + '/?t=' + Date.now() });
    await js(`(async () => { for (let i = 0; i < 100; i++) { if (window.state && state.stage === 'landing') return; await new Promise(r => setTimeout(r, 50)); } throw new Error('no landing'); })()`);
    await js(`(async () => { await enterGroup(${c.group}, '${c.tree}', '${c.node}'); render(); })()`);
    await js(INSTRUMENT);
    await js(`document.querySelector('${c.sel}').focus()`);
    await send('Input.insertText', { text: c.text });
    const box = await js(`(() => { const r = document.querySelector('[data-act="resolve"]').getBoundingClientRect();
      return { x: r.left + r.width / 2, y: r.top + r.height / 2 }; })()`);
    await js(`window.__trace.push('--- one tap on Continue at ${c.node} ---')`);
    await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: box.x, y: box.y });
    await send('Input.dispatchMouseEvent', { type: 'mousePressed', x: box.x, y: box.y, button: 'left', clickCount: 1 });
    await send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: box.x, y: box.y, button: 'left', clickCount: 1 });
    await sleep(400);
    const r = await js(`({ node: state.nodeId, result: !!state.result, err: state.error, trail: state.trail.map(t => t.label + ': ' + t.value), trace: window.__trace })`);
    const ok = r.node !== c.node || r.result;
    if (!ok) lost++;
    console.log((ok ? 'OK   ' : 'LOST ') + c.node + ' with ' + JSON.stringify(c.text) + ' → node ' + r.node + (r.err ? ', error ' + r.err : '') + ', trail ' + JSON.stringify(r.trail));
    for (const t of r.trace) console.log('       ' + t);
  }
  /* Controls that must STILL redraw the screen on 'change', and the keyboard. */
  const load = async () => {
    await send('Page.navigate', { url: 'http://localhost:' + PORT + '/?t=' + Date.now() });
    await js(`(async () => { for (let i = 0; i < 100; i++) { if (window.state && state.stage === 'landing') return; await new Promise(r => setTimeout(r, 50)); } throw new Error('no landing'); })()`);
  };
  const press = async (sel) => {
    const b = await js(`(() => { const r = document.querySelector('${sel}').getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2 }; })()`);
    for (const type of ['mouseMoved', 'mousePressed', 'mouseReleased']) {
      await send('Input.dispatchMouseEvent', { type, x: b.x, y: b.y, button: 'left', clickCount: 1 });
    }
    await sleep(300);
  };
  const key = async (k, code, vk) => {
    await send('Input.dispatchKeyEvent', { type: 'rawKeyDown', key: k, code, windowsVirtualKeyCode: vk });
    if (k === 'Enter') await send('Input.dispatchKeyEvent', { type: 'char', text: '\r', key: k, code, windowsVirtualKeyCode: vk });
    await send('Input.dispatchKeyEvent', { type: 'keyUp', key: k, code, windowsVirtualKeyCode: vk });
    await sleep(200);
  };
  const check = (name, ok, detail) => { if (!ok) lost++; console.log((ok ? 'OK   ' : 'FAIL ') + name + (ok ? '' : ' — ' + detail)); };

  await load(); await js(`(async () => { await enterGroup(1, 'tree_acute_leukemia', 'ac_blast_gate'); render(); })()`);
  await js(`document.querySelector('input[type="number"]').focus()`);
  await send('Input.insertText', { text: '12' });
  await press('input[type="checkbox"][data-k="not_documented"]');
  let r = await js(`({ disabled: document.querySelector('input[type="number"]').disabled, undoc: state.draft.not_documented, value: state.draft.value })`);
  check('"Not documented" clicked after typing a number: the number box is disabled', r.disabled && r.undoc === true, JSON.stringify(r));

  await load(); await js(`(async () => { await enterGroup(1, 'tree_acute_leukemia', 'ac_ball_cytogenetics'); render(); })()`);
  r = await js(`({ before: document.querySelector('[data-act="resolve"]').disabled })`);
  /* The list is a filtered radio list since 6 October 2026, not a select. */
  await js(`(() => { const s = document.querySelector('input[type="radio"][data-act="draft"][data-k="option"][value="1"]'); s.focus(); s.checked = true; s.dispatchEvent(new Event('change', { bubbles: true })); })()`);
  r.after = await js(`document.querySelector('[data-act="resolve"]').disabled`);
  check('choosing a finding from the list enables Continue', r.before === true && r.after === false, JSON.stringify(r));

  await load();
  await js(`document.querySelector('input[data-act="query"]').focus()`);
  await send('Input.insertText', { text: 'Nephroblastoma' });
  await key('Tab', 'Tab', 9);
  const focused = await js(`(() => { const a = document.activeElement; return a && a.getAttribute('data-act') + ': ' + a.textContent.trim().slice(0, 30); })()`);
  await key('Enter', 'Enter', 13);
  await sleep(300);
  r = await js(`({ stage: state.stage, trail: state.trail.map(t => t.label + ': ' + t.value) })`);
  check('keyboard: type, Tab to the first result (' + focused + '), Enter enters the case',
    r.stage !== 'landing' && r.trail.length > 0, 'focus went to ' + focused + '; ' + JSON.stringify(r));
} finally {
  try { ws && ws.close(); } catch {}
  chrome.kill(); await sleep(300); fs.rmSync(PROFILE, { recursive: true, force: true });
}
process.exit(lost ? 1 : 0);
