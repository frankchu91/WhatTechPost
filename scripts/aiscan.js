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

const grabRaw = (k) => (front.match(new RegExp(`^${k}:\\s*"?(.*?)"?\\s*$`, 'm')) || [])[1] || '';

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

// Split the verdict instead of averaging one score (2026-10-06).
//
// Prompted by @danorie, who runs a checker with the same mixed scoring and
// reached the same conclusion independently. The old single scalar let the
// density terms be driven down by padding until they absorbed the phrase
// terms: the same nine em dashes scored 9 at 78 words and 3 at 648.
//
// Two families, two thresholds, either can fail the draft on its own, nothing
// averaged. PHRASE issues are set-based — the detector dedups them, so one
// instance is the whole signal and length is irrelevant. DENSITY issues are
// explicitly ratios over word count.
//
// @danorie also asked whether a minimum-words floor on the density denominator
// would do instead. Measured on this archive: no. The floor fixes the opposite
// failure, a short body judged as if it were an essay, and my shortest post is
// 337 words, so a floor of 100 or 250 is a no-op here. More to the point, the
// padding attack moves a body UP past any floor: at 648 words a floor of 500 is
// already inactive. It is a real fix for a real bug, just not for this one.
const PHRASE = new Set(['tier1', 'tier1-clarity', 'tier2', 'hollow-intensifier',
                        'transition', 'lets-construction', 'real-actual-inflation']);
// Hard-failing on any phrase tell removed my ability to exercise judgment on
// homographs, which CLAUDE.md explicitly says to use judgment about. Two real
// cases on the day the split shipped: "underscores" flagged as the verb meaning
// "highlights" in a post about the `_` character, and "unpack" flagged as the
// verb meaning "explain" in a post discussing struct.unpack.
//
// The escape hatch is an explicit front-matter list, written by hand, echoed in
// the output. Same shape as audit.py's excerpt marker: an exception you have to
// type and that nobody can mistake for the check not firing.
//   aiscan_allow: underscores, unpack
const allow = new Set(grabRaw('aiscan_allow').split(',')
  .map((w) => w.trim().toLowerCase()).filter(Boolean));

const phraseIssues = r.issues.filter(
  (i) => PHRASE.has(i.type) && !allow.has(String(i.text || '').toLowerCase()));
const allowed = r.issues.filter(
  (i) => PHRASE.has(i.type) && allow.has(String(i.text || '').toLowerCase()));
const densityIssues = r.issues.filter((i) => !PHRASE.has(i.type));

// The density test reads the ratio out of the issue text rather than reusing
// r.score. r.score is the AGGREGATE, phrase contributions included, so using it
// as "the density score" would just rebuild the thing being fixed under a name
// that hides it. EMDASH_MAX is the house rule: single digits per post.
const emIssue = r.issues.find((i) => i.type === 'em-dash');
const emCount = emIssue ? parseInt(String(emIssue.text), 10) : 0;
const emPer1k = r.stats.wordCount ? (emCount / r.stats.wordCount) * 1000 : 0;
const EMDASH_PER_1K = 12;    // ~9 dashes in a 750-word post, our median length

const byType = {};
for (const i of r.issues) byType[i.type] = (byType[i.type] || 0) + 1;

console.log(`\naiscan · ${path.basename(file)}`);
console.log(`  aggregate score ${r.score} (advisory)  ·  ${r.issues.length} issues  ·  ${r.stats.wordCount} words`);
console.log(`  phrase ${phraseIssues.length}  ·  density ${densityIssues.length}  ·  em dashes ${emCount} (${emPer1k.toFixed(1)}/1k)`);
console.log('  ─────────────────────────────────────────────');
for (const i of r.issues) {
  const snip = (i.text || '').toString().replace(/\n/g, ' ').slice(0, 70);
  const fix = i.suggestion ? `  => ${i.suggestion}` : '';
  console.log(`  [${i.type}] ${JSON.stringify(snip)}${fix}`);
}

if (allowed.length) {
  console.log(`  ── allowed by aiscan_allow: ${allowed.map((i) => i.text).join(', ')}`);
}

if (metaIssues.length) {
  console.log('  ── title + description (scored separately; metadata, not prose)');
  for (const i of metaIssues) {
    console.log(`  [meta/${i.type}] ${JSON.stringify((i.text || '').toString().slice(0, 60))}`);
  }
}

// Metadata tells fail the post on their own. The title is the most-read
// sentence in it, and averaging it into the body's score let a bad one hide.
//
// Each family fails independently. The aggregate score is still printed because
// it is useful to eyeball, and it no longer decides anything.
const fails = [];
if (phraseIssues.length) {
  fails.push(`${phraseIssues.length} phrase tell(s): ${phraseIssues.map((i) => i.text).join(', ')}`);
}
if (emCount > EMDASH_MAX || emPer1k > EMDASH_PER_1K) {
  fails.push(`${emCount} em dashes (${emPer1k.toFixed(1)}/1k, max ${EMDASH_MAX} or ${EMDASH_PER_1K}/1k)`);
}
if (metaIssues.length) fails.push(`${metaIssues.length} metadata tell(s)`);
const verdict = fails.length ? `REVIEW / REWRITE (${fails.join('; ')})` : 'PASS';
console.log('  ─────────────────────────────────────────────');
console.log(`  VERDICT: ${verdict}`);
console.log('  Always fix: em-dash overuse (keep single digits), bold overuse (<=' + BOLD_MAX + ').');
console.log('  Use judgment on domain-term false positives before chasing the number.\n');

process.exit(fails.length ? 1 : 0);
