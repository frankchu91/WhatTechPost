#!/usr/bin/env node
/*
 * techcheck — enforces the "substance" bar on a technical post.
 * The author's rule (2026-09-14): of the 3 posts a day, at least one must be a
 * REAL technical piece — actual code, actual artifacts — not pure prose.
 * Added after 9 of 10 consecutive published posts shipped with zero code blocks.
 *
 * Usage: node scripts/techcheck.js <path-to-draft.md>
 * Exit 0 = passes the substance bar. Exit 1 = prose, needs real code.
 */
const fs = require('fs');
const path = require('path');

const MIN_BLOCKS = 2;      // at least two fenced code blocks
const MIN_CODE_LINES = 12; // substantive, not two one-liners
const MIN_LANGS = 1;       // fences should be tagged (```js, ```python, ```yaml)

const file = process.argv[2];
if (!file) { console.error('usage: node scripts/techcheck.js <draft.md>'); process.exit(2); }

// strip the REVIEW NOTES comment so notes never count as content
const raw = fs.readFileSync(file, 'utf8').replace(/^\s*<!--[\s\S]*?-->\s*/, '');

const fences = [...raw.matchAll(/^```([a-zA-Z0-9+-]*)\n([\s\S]*?)^```/gm)];
const blocks = fences.length;
const codeLines = fences.reduce((n, m) => n + m[2].split('\n').filter(l => l.trim()).length, 0);
const langs = new Set(fences.map(m => m[1]).filter(Boolean));
const tables = (raw.match(/^\|.*\|$/gm) || []).length;
const diagrams = (raw.match(/!\[/g) || []).length;

const checks = [
  [blocks >= MIN_BLOCKS, `${blocks} code blocks (need >= ${MIN_BLOCKS})`],
  [codeLines >= MIN_CODE_LINES, `${codeLines} lines of code (need >= ${MIN_CODE_LINES})`],
  [langs.size >= MIN_LANGS, `fences tagged with a language: ${[...langs].join(', ') || 'NONE'}`],
];

console.log(`\ntechcheck · ${path.basename(file)}`);
for (const [ok, msg] of checks) console.log(`  ${ok ? 'ok  ' : 'FAIL'} ${msg}`);
console.log(`  info  ${tables} table rows, ${diagrams} images`);

const pass = checks.every(([ok]) => ok);
console.log(`  VERDICT: ${pass ? 'TECHNICAL' : 'PROSE — add real code or reclassify'}\n`);
process.exit(pass ? 0 : 1);
