#!/usr/bin/env node
'use strict';
// Regression: both policy-title styles must show the existing source identifier
// in the ID / date column without changing the document title or metadata.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const template = fs.readFileSync(path.join(__dirname, '../src/wordpress/templates/policy-editorial.html'), 'utf8');
const helper = template.match(/function splitPolicyTitle\(rawTitle\)\{[\s\S]*?\n\}/);
assert.ok(helper, 'policy-title parser is present in the template');
assert.match(template, /const \{identifier,title\}=splitPolicyTitle\(p.title\)/, 'cards use the shared parser');
const splitPolicyTitle = vm.runInNewContext(helper[0] + '; splitPolicyTitle');

const examples = [
  ['GENERAL-26-64 — Workforce Pell FAQs Turn Federal Rules Into Implementation Decisions',
    'GENERAL-26-64', 'Workforce Pell FAQs Turn Federal Rules Into Implementation Decisions'],
  ['SB 1030: CalWORKs Will Retire a Household Contribution Rule',
    'SB 1030', 'CalWORKs Will Retire a Household Contribution Rule'],
  ['SB 1012: Fire Camp Experience Counts Toward Apprenticeships',
    'SB 1012', 'Fire Camp Experience Counts Toward Apprenticeships'],
  ['TEGL 10-23, Change 3: What Rescission Means for Access',
    'TEGL 10-23, Change 3', 'What Rescission Means for Access'],
  ['ACL 26-28: CalWORKs Changes When and How Sanctions Apply',
    'ACL 26-28', 'CalWORKs Changes When and How Sanctions Apply'],
  ['ACL 26-31: Transportation Comes Before CalWORKs Participation',
    'ACL 26-31', 'Transportation Comes Before CalWORKs Participation'],
  ['ACL 26-32: CalWORKs Makes Job Search a Choice, Not the Default',
    'ACL 26-32', 'CalWORKs Makes Job Search a Choice, Not the Default'],
  ['WSIN26-13 — Innovative Water Infrastructure Workforce Development Program — Grant Opportunity',
    'WSIN26-13', 'Innovative Water Infrastructure Workforce Development Program — Grant Opportunity'],
  ['WIOA Section 188 / 29 CFR Part 38 — The Civil Rights Operating Rules Behind the AJCC System',
    'WIOA Section 188 / 29 CFR Part 38', 'The Civil Rights Operating Rules Behind the AJCC System'],
  ['What works: a guide', '', 'What works: a guide'],
  ['A title with no separator', '', 'A title with no separator'],
];

for (const [full, expectedId, expectedTitle] of examples) {
  const value = splitPolicyTitle(full);
  assert.equal(value.identifier, expectedId, full);
  assert.equal(value.title, expectedTitle, full);
}

const match = template.match(/const POSTS=(\[.*?\]);\n/);
assert.ok(match, 'policy index is embedded in the source fixture');
const posts = JSON.parse(match[1]);
assert.ok(posts.length > 200, 'enough policy rows for a representative check');
for (const post of posts) {
  const parts = splitPolicyTitle(post.title);
  assert.ok(parts.identifier, 'source ID is visible: ' + post.id);
  assert.ok(parts.title, 'reader-facing title is not empty: ' + post.id);
}

console.log('PASS: ' + examples.length + ' format cases and ' + posts.length + ' source records');
