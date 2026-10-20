/* ============================================================================
   check_demo_walkthroughs.mjs — every walk-through on the landing page must
   replay through the real engine to the code it says it reaches.

   The walk-throughs (data/shared/demo_walkthroughs.json) are recordings of a
   clerk's clicks. A recording rots the moment an option is renamed, a question is
   added or a rule changes, and nothing in the page would say so: the player would
   stop part-way, in front of the audience. So each case is replayed here, click by
   click, through app.js and the data on disk, and must end on its output screen
   with the code, behaviour and topography the case promises.

   Three things are checked, none of them off a flag in the recording:

     REPLAY   each recorded control is found on the screen the engine drew (one
              match, by the player's own matcher) and the case ends on the output
              screen, with state.result.code and the screen text as promised. A
              step left over after an early finish finds no control and fails here.
     SHAPE    the recording is well formed: a made-up file, a caption on every beat,
              an act on every step, an expected result.
     WIRING   every element the player looks up exists in index.html, and the
              script and data path the page loads are the ones that exist. A missing
              id would hide the section without an error, which is the failure a
              data check never sees.

   Run:  node build/check_demo_walkthroughs.mjs
   ========================================================================= */

import fs from 'node:fs';
import path from 'node:path';
import { ROOT, loadEngine, ready, doStep, screenText } from './demo_driver.mjs';

const DATA = process.env.DEMOS || path.join(ROOT, 'data', 'shared', 'demo_walkthroughs.json');
let checks = 0;
const failures = [];
const ok = (name, cond, detail) => {
  checks++;
  if (cond) console.log('  OK    ' + name);
  else { failures.push(name); console.log('  FAIL  ' + name + (detail ? '\n        ' + String(detail).replace(/\n/g, '\n        ') : '')); }
};

const doc = JSON.parse(fs.readFileSync(DATA, 'utf8'));
const cases = doc.cases || [];

console.log('\nShape — the recordings are well formed\n');
ok('the file holds at least one case', cases.length >= 1);
ok('case ids are unique', new Set(cases.map((c) => c.id)).size === cases.length);
for (const c of cases) {
  const lines = Array.isArray(c.file) && c.file.length > 0 && c.file.every((l) => typeof l === 'string' && l.trim());
  ok(c.id + ': title, group, teaser and a made-up file are present', !!(c.title && c.group && c.teaser) && lines);
  const beats = Array.isArray(c.beats) ? c.beats : [];
  ok(c.id + ': every beat has a caption and at least one step with an act',
    beats.length > 0 && beats.every((b) => b.say && b.say.trim() && Array.isArray(b.do) && b.do.length > 0 && b.do.every((s) => s && s.act)));
  const e = c.expect || {};
  ok(c.id + ': an expected code, behaviour and screen text are named', !!(e.code && e.behavior && Array.isArray(e.screen) && e.screen.length));
}

console.log('\nReplay — each case reaches its code through the real engine\n');
for (const c of cases) {
  let beatAt = -1, err = null, ctx = null;
  try {
    ctx = loadEngine(); await ready(ctx);
    for (let b = 0; b < c.beats.length; b++) {
      beatAt = b;
      for (const s of c.beats[b].do) await doStep(ctx, s);
      if (ctx.state.error) throw new Error('the engine reported an error: ' + (ctx.state.error.message || ctx.state.error));
    }
  } catch (e) { err = e; }
  if (err) { ok(c.id + ': replays to the end', false, 'beat ' + (beatAt + 1) + ' of ' + c.beats.length + ': ' + err.message); continue; }
  const r = ctx.state.result || {};
  const text = screenText(ctx);
  ok(c.id + ': replays to the end and stops on the output screen', ctx.state.stage === 'output', 'stage is ' + ctx.state.stage);
  ok(c.id + ': the code is ' + c.expect.code + '/' + c.expect.behavior,
    String(r.code) === c.expect.code && String(r.entry && r.entry.behavior_code) === c.expect.behavior,
    'result is ' + r.code + '/' + (r.entry && r.entry.behavior_code));
  for (const t of c.expect.screen) ok(c.id + ': the screen reads "' + t + '"', text.includes(t), text.slice(0, 260));
  /* A typed figure or a chosen status that never registered still leaves the code unchanged, so
     the code alone proves nothing about them: each is read back off the case the engine holds. */
  const trailText = ctx.state.trail.map((t) => t.label + ' ' + t.value).join(' | ');
  for (const t of c.expect.trail || []) ok(c.id + ': the trail holds "' + t + '"', trailText.includes(t), trailText.slice(0, 400));
  for (const [test, status] of Object.entries(c.expect.workup || {})) {
    const w = ctx.state.workup.find((x) => x.test === test);
    ok(c.id + ': the workup for ' + test + ' reads "' + status + '"', !!w && w.status === status, JSON.stringify(ctx.state.workup));
  }
}

console.log('\nWiring — the page holds what the player looks up\n');
const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
const js = fs.readFileSync(path.join(ROOT, 'demo.js'), 'utf8');
const ids = [...js.matchAll(/getElementById\('([^']+)'\)/g)].map((m) => m[1]);
ok('demo.js looks up ids, and index.html has each', ids.length > 0 && ids.every((id) => html.includes('id="' + id + '"')),
  'missing: ' + ids.filter((id) => !html.includes('id="' + id + '"')).join(', '));
const classes = [...js.matchAll(/querySelector\('\.([\w-]+)(?: ul)?'\)/g)].map((m) => m[1]);
ok('demo.js looks up classes, and index.html has each', classes.length > 0 && classes.every((k) => html.includes(k)),
  'missing: ' + classes.filter((k) => !html.includes(k)).join(', '));
const buttons = [...js.matchAll(/data-demo="(\w+)"/g)].map((m) => m[1]);
ok('every player button the script uses is in index.html', buttons.length > 0 && buttons.every((b) => html.includes('data-demo="' + b + '"')),
  'missing: ' + buttons.filter((b) => !html.includes('data-demo="' + b + '"')).join(', '));
ok('index.html loads demo.js after app.js', html.indexOf('<script src="app.js">') !== -1 && html.indexOf('<script src="demo.js">') > html.indexOf('<script src="app.js">'));
const url = (js.match(/DATA_URL = '([^']+)'/) || [])[1];
ok('the data path demo.js fetches exists', !!url && fs.existsSync(path.join(ROOT, url)), String(url));
ok('the demo section is hidden until the player shows it', /id="demos"[^>]*\shidden/.test(html) && /id="demobar"[^>]*\shidden/.test(html));
ok('the page is left alone when embedded (?host=redcap)', /get\('host'\)\s*===\s*'redcap'/.test(js));

console.log('\n' + (failures.length ? failures.length + ' of ' + checks + ' checks FAILED' : 'demo walk-throughs: ' + checks + ' checks passed'));
process.exit(failures.length ? 1 : 0);
