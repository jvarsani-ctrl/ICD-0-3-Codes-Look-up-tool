/* ============================================================================
   demo_driver.mjs — drives the real engine through a recorded walk-through.

   The walk-throughs on the landing page are data (data/shared/demo_walkthroughs.json):
   a made-up case, and the clicks a clerk would make. This driver loads app.js
   and the data on disk into a vm context, finds each recorded control on the
   screen the engine has drawn, and fires it through the same delegated listeners
   the page registers. The check and the authoring helper both use it, so a path
   that replays here replays in the browser.

   A step names a control by what is on the screen, never by an index:

     { "act": "opt", "text": "Dysgerminoma" }          a button or label whose text contains `text`
     { "act": "markerset", "m": "CD3", "v": "pos" }    attributes, matched exactly
     { "act": "query", "type": "Burkitt lymphoma" }    types into a box (fires the input listener)
     { "act": "tick", "text": "Flow cytometry" }       a checkbox, matched by its label text

   `text` is matched on the text with tags removed, case-insensitively, as a
   substring (an exact match wins over a longer one), and must name exactly one
   control: zero or several is an error, so a renamed option fails the build
   instead of replaying the wrong answer. The matcher is PedsDemo.pick in demo.js,
   the same function the browser player runs.
   ========================================================================= */

import fs from 'node:fs';
import path from 'node:path';
import url from 'node:url';
import vm from 'node:vm';

export const ROOT = path.dirname(path.dirname(url.fileURLToPath(import.meta.url)));
const APP = process.env.APP || path.join(ROOT, 'app.js');

const decode = (s) => s.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;|&#x27;/g, "'");
const plain = (html) => decode(html.replace(/<(script|style)[\s\S]*?<\/\1>/g, '').replace(/<[^>]+>/g, ' ')).replace(/\s+/g, ' ').trim();

function fakeDom() {
  const dom = { appListeners: {}, docListeners: {}, els: {} };
  const mk = (id) => ({
    id, innerHTML: '', textContent: '', hidden: false,
    setAttribute() {},
    querySelector(sel) {
      if (sel === '.exitbar') return this.innerHTML.includes('class="exitbar"') ? { getBoundingClientRect: () => ({ bottom: 0 }) } : null;
      return null;
    },
  });
  ['app', 'appbar-context', 'appbar-home', 'rail', 'trail-rows', 'slot'].forEach((id) => { dom.els[id] = mk(id); });
  /* The search box rewrites the results list in place, without re-rendering the
     screen. The fake keeps that list apart and drops it on the next full render. */
  const slot = dom.els.slot;
  let html = '';
  Object.defineProperty(slot, 'innerHTML', { get: () => html + (dom.resultsHtml || ''), set: (v) => { html = v; dom.resultsHtml = ''; } });
  const plainQuery = slot.querySelector;
  slot.querySelector = function (sel) {
    if (sel === '.results') return { set innerHTML(v) { dom.resultsHtml = v; } };
    return plainQuery.call(this, sel);
  };
  dom.appEl = { addEventListener(type, fn) { (dom.appListeners[type] = dom.appListeners[type] || []).push(fn); } };
  dom.document = {
    addEventListener(type, fn) { dom.docListeners[type] = fn; },
    getElementById: (id) => dom.els[id] || null,
    querySelector: (sel) => (sel === '.app' ? dom.appEl : { focus() {} }),
    get activeElement() { return null; },
  };
  return dom;
}

export function loadEngine() {
  const src = fs.readFileSync(APP, 'utf8');
  const dom = fakeDom();
  const fromDisk = (p) => new Promise((resolve, reject) => {
    const f = path.join(ROOT, p);
    if (!fs.existsSync(f)) return reject(new Error('no such file: ' + p));
    resolve({ ok: true, json: () => Promise.resolve(JSON.parse(fs.readFileSync(f, 'utf8'))) });
  });
  const ctx = vm.createContext({
    document: dom.document, window: { location: { search: '' } },
    console, URLSearchParams, fetch: fromDisk,
  });
  vm.runInContext(src, ctx, { filename: APP });
  ctx.__dom = dom;
  dom.docListeners.DOMContentLoaded();
  return ctx;
}

const settle = () => new Promise((r) => setImmediate(r));
export async function ready(ctx) { for (let i = 0; i < 40; i++) { await settle(); if (ctx.state.stage !== 'boot') return; } }

/* Every control on the screen the engine drew, with the text that names it. */
export function controls(ctx) {
  const html = ctx.__dom.els.slot.innerHTML;
  const out = [];
  const re = /<(button|input|select|textarea)\b([^>]*)>/g;
  let m;
  while ((m = re.exec(html))) {
    const attrs = {};
    m[2].replace(/([\w-]+)="([^"]*)"/g, (_, k, v) => { attrs[k] = decode(v); return ''; });
    if (!attrs['data-act']) continue;
    let text = '';
    if (m[1] === 'button') {
      const end = html.indexOf('</button>', re.lastIndex);
      text = plain(html.slice(re.lastIndex, end));
    } else {
      /* a checkbox or radio sits inside its label: the label's text names it */
      const open = html.lastIndexOf('<label', m.index);
      const close = html.indexOf('</label>', m.index);
      if (open !== -1 && close !== -1 && html.lastIndexOf('</label>', m.index) < open) text = plain(html.slice(open, close));
      else text = decode(attrs['aria-label'] || attrs.placeholder || '');
    }
    out.push({ tag: m[1], attrs, text, disabled: / disabled(\s|>|=)/.test(m[0]) });
  }
  return out;
}

export function screenText(ctx) { return plain(ctx.__dom.els.slot.innerHTML); }

/* The player's own matcher, loaded from demo.js, so the control a recorded step
   names is chosen by the same function here and in the browser. */
const demoLib = (() => {
  const dctx = vm.createContext({ window: { location: { search: '' } }, URLSearchParams });
  vm.runInContext(fs.readFileSync(path.join(ROOT, 'demo.js'), 'utf8'), dctx, { filename: 'demo.js' });
  return dctx.PedsDemo;
})();

function find(ctx, step) {
  const list = controls(ctx);
  try { return list[demoLib.pick(list, step)]; }
  catch (e) {
    const here = list.filter((c) => c.attrs['data-act'] === step.act).map((c) => '  - ' + c.text).join('\n');
    throw new Error(e.message + '\n screen: ' + screenText(ctx).slice(0, 220) +
      '\n controls with data-act="' + step.act + '":\n' + here);
  }
}

function elOf(c) {
  const el = {
    tagName: c.tag.toUpperCase(), type: c.attrs.type || '', value: c.attrs.value || '', checked: 'checked' in c.attrs,
    getAttribute: (k) => (k in c.attrs ? c.attrs[k] : null),
    /* closest('[data-act]') is the control itself; any other ancestor is a stub whose children are inert */
    closest: (sel) => (sel === '[data-act]' ? el : { querySelector: () => ({ checked: false }) }),
    classList: { contains: () => false },
  };
  return el;
}

async function fire(ctx, type, target, key) {
  const ev = { target, key, preventDefault() {} };
  for (const fn of ctx.__dom.appListeners[type] || []) await fn(ev);
  for (let i = 0; i < 6; i++) await settle();
}

/* One recorded step. Returns nothing; throws on a control it cannot find. */
export async function doStep(ctx, step) {
  const c = find(ctx, step);
  const el = elOf(c);
  const typed = c.tag === 'textarea' || (c.tag === 'input' && !/^(checkbox|radio)$/.test(c.attrs.type || ''));
  if (typed) {
    el.value = step.type !== undefined ? step.type : (step.value || '');
    return fire(ctx, 'input', el);
  }
  if (c.attrs.type === 'checkbox' || c.attrs.type === 'radio') {
    el.checked = step.checked === undefined ? true : !!step.checked;
    return fire(ctx, 'change', el);
  }
  if (c.tag === 'select') { el.value = step.value; return fire(ctx, 'change', el); }
  return fire(ctx, 'click', el);
}

/* Replay a whole case. Returns what the output screen holds. */
export async function replay(steps, onStep) {
  const ctx = loadEngine();
  await ready(ctx);
  for (let i = 0; i < steps.length; i++) {
    await doStep(ctx, steps[i]);
    if (onStep) onStep(i, steps[i], ctx);
  }
  return ctx;
}
