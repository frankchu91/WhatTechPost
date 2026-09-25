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
const raw = fs.readFileSync(file, 'utf8');

// Score the prose, and only the prose.
//
// This used to hand the detector the whole file, which meant it scored my
// private REVIEW NOTES, the front matter, and the contents of every code
// block. Real consequences, all measured: a title change with a byte-identical
// body moved the score from 0 to 42; front-matter words padded the em-dash
// denominator enough to flip one published post's verdict; and `struct.unpack`
// inside a Python snippet was flagged as the English word "unpack".
//
// Each region gets stripped for its own reason:
//   notes  — they are about the writing, they are not the writing
//   front  — metadata, and its word count distorts every density ratio
//   code   — identifiers are not prose; nobody reads `features` in a log line
// The metadata still matters and is not exempt; it is scored separately below.
const notes = raw.match(/^\s*<!--[\s\S]*?-->\s*/);
let rest = notes ? raw.slice(notes[0].length) : raw;

const fm = rest.match(/^---\n([\s\S]*?)\n---\n/);
const front = fm ? fm[1] : '';
let body = fm ? rest.slice(fm[0].length) : rest;

body = body
  .replace(/^```[\s\S]*?^```/gm, '')      // fenced blocks
  .replace(/^(?: {4}|\t).*$/gm, '')       // indented blocks
  .replace(/`[^`\n]+`/g, '');             // inline code

const r = D.analyzeText(body);

// Title and description are scored together, as one "metadata" region.
//
// Scoring the title alone does not work: the detector returns nothing below
// ten words (`if (wordCount < 10) return ...`), and a headline is eight to
// fourteen. The first version of this check was therefore incapable of firing
// on most titles, which I only found by feeding it a deliberately terrible one
// and watching it pass. Together the two fields clear the threshold, and they
// are the right pair anyway: both are reader-facing, neither is article prose.
const grab = (k) => (front.match(new RegExp(`^${k}:\\s*"?(.*?)"?\\s*$`, 'm')) || [])[1] || '';
const meta = [grab('title'), grab('description')].filter(Boolean).join('. ');
const metaIssues = meta.split(/\s+/).length >= 10 ? D.analyzeText(meta).issues : [];

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

if (metaIssues.length) {
  console.log('  ── title + description (scored separately; metadata, not prose)');
  for (const i of metaIssues) {
    console.log(`  [meta/${i.type}] ${JSON.stringify((i.text || '').toString().slice(0, 60))}`);
  }
}

// Metadata tells fail the post on their own. The title is the most-read
// sentence in it, and averaging it into the body's score let a bad one hide.
const verdict = (r.score > TARGET || metaIssues.length) ? 'REVIEW / REWRITE' : 'PASS';
console.log('  ─────────────────────────────────────────────');
console.log(`  VERDICT: ${verdict}`);
console.log('  Always fix: em-dash overuse (keep single digits), bold overuse (<=' + BOLD_MAX + ').');
console.log('  Use judgment on domain-term false positives before chasing the number.\n');

process.exit((r.score > TARGET || metaIssues.length) ? 1 : 0);
