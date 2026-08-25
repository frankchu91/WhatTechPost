#!/usr/bin/env node
/*
 * aiscan — pre-publish AI-writing check for WhatTechPost drafts.
 * Runs the installed avoid-ai-writing detector (conorbronsdon/avoid-ai-writing)
 * on a markdown file and prints a readable report + a pass/review verdict.
 *
 * Usage: node scripts/aiscan.js <path-to-draft.md>
 * Exit 0 = pass (score <= TARGET). Exit 1 = review/rewrite (score > TARGET).
 *
 * The verdict is a signal, not a verdict (the skill says so). Always fix the
 * real, consistent tells — em-dash overuse and bold overuse — and use judgment
 * on domain-term false positives (e.g. "harness" flagged as a fancy word).
 */
const os = require('os');
const fs = require('fs');
const path = require('path');

const TARGET = 2.0;          // aim at/below this; above triggers a rewrite pass
const EMDASH_MAX = 9;        // single digits per post
const BOLD_MAX = 2;          // bold phrases per post

const detectorPath = path.join(os.homedir(), '.claude/skills/avoid-ai-writing/detector/patterns.js');
if (!fs.existsSync(detectorPath)) {
  console.error('avoid-ai-writing not installed at ~/.claude/skills/avoid-ai-writing');
  process.exit(2);
}
const D = require(detectorPath);

const file = process.argv[2];
if (!file) { console.error('usage: node scripts/aiscan.js <draft.md>'); process.exit(2); }
const text = fs.readFileSync(file, 'utf8');
const r = D.analyzeText(text);

const byType = {};
for (const i of r.issues) byType[i.type] = (byType[i.type] || 0) + 1;

console.log(`\naiscan · ${path.basename(file)}`);
console.log(`  score ${r.score}  ·  ${r.issues.length} issues  ·  ${r.stats.wordCount} words  ·  target <= ${TARGET}`);
console.log('  ─────────────────────────────────────────────');
for (const i of r.issues) {
  const snip = (i.text || '').toString().replace(/\n/g, ' ').slice(0, 70);
  const fix = i.suggestion ? `  => ${i.suggestion}` : '';
  console.log(`  [${i.type}] ${JSON.stringify(snip)}${fix}`);
}

const verdict = r.score > TARGET ? 'REVIEW / REWRITE' : 'PASS';
console.log('  ─────────────────────────────────────────────');
console.log(`  VERDICT: ${verdict}`);
console.log('  Always fix: em-dash overuse (keep single digits), bold overuse (<=' + BOLD_MAX + ').');
console.log('  Use judgment on domain-term false positives before chasing the number.\n');

process.exit(r.score > TARGET ? 1 : 0);
