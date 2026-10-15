#!/usr/bin/env node
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const source = fs.readFileSync(path.join(__dirname, '../src/wordpress/templates/homepage-editorial.html'), 'utf8');
const pell = 'https://workforcewonkery.com/2026/10/15/general-26-64-workforce-pell-implementation-faqs/';
const policySection = source.match(/<section class="ep-policy" id="policy-watch"[\s\S]*?<\/section>/)?.[0];
const mobileSection = source.match(/<section class="ep-mobile-week"[\s\S]*?<\/section>/)?.[0];
assert.ok(policySection, 'Policy Watch section exists');
assert.ok(mobileSection, 'mobile weekly feature section exists');
const cards = [...policySection.matchAll(/<article class="ep-policy-card">[\s\S]*?<\/article>/g)].map(x => x[0]);
assert.equal(cards.length, 3, 'homepage retains three editorial policy cards');
assert.match(cards[0], /WSIN26-17/);
assert.match(cards[0], /Comment deadline: Oct\. 23, 2026\./);
assert.match(cards[1], /AB 1534/);
assert.match(cards[1], /July 1, 2028/);
assert.match(cards[2], /GENERAL-26-64/);
assert.match(cards[2], /Workforce Pell gets practical implementation guidance/);
assert.match(cards[2], /Program approval is not automatic/);
assert.match(cards[2], /NEW GUIDANCE/);
assert.ok(cards[2].includes(pell), 'new card links to published Workforce Pell brief');
assert.ok(!policySection.includes('EO N-6-26'), 'old AI deadline card is rotated out');
assert.ok(mobileSection.includes(pell), 'mobile featured policy also links to Pell');
assert.match(mobileSection, /Policy Brief · Oct\. 15/);
assert.ok(!mobileSection.includes('Policy Pulse · Oct. 1'), 'October 1 digest is not presented as new');
console.log('PASS: three homepage policy cards, new Workforce Pell link, and fresh mobile weekly highlight');
