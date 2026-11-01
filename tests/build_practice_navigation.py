"""Build reader-facing Practice hubs from one reviewed catalogue. Run from any cwd.

Outputs (byte-for-byte reproducible):
  templates/practice-editorial-v2.html      Practice home, WordPress page 935
  templates/practice-resource-directory.html All resources, page 1211 (/practice/tools/)
  templates/practice-topic-library.html      Topics, page 1212 (/practice/topics/)
  templates/practice-quickstarts.html        Quickstarts, page 1387
  template-parts/footer-editorial-blocks.html Practice runtime (navigation, catalogue, search) appended to the global footer;
                                              the header carries no Practice code

Editorial content (summaries, topic guides, related links, type labels) lives in
javascript/practice-catalogue.json. Change the catalogue, then rerun this script.
"""
import json, html, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
S = ROOT / 'src/wordpress'
data = json.loads((S / 'javascript/practice-catalogue.json').read_text())
E = html.escape
R = {r['id']: r for r in data['resources']}
TOPICS = {t['id']: t for t in data['topics']}
TYPES = {t['id']: t for t in data['types']}
MEDIA = 'https://workforcewonkery.com/wp-content/uploads/2026/09/'
PAGES = '.page-id-935,.page-id-1211,.page-id-1212,.page-id-1387'
N = len(data['resources'])
NQ = sum(r['type'] == 'Quickstart' for r in data['resources'])

# WordPress adds post-content padding and a block gap above custom HTML. Policy and Data
# zero both, so the Practice hubs do the same; the hero then sits flush under the site header.
reset = ('<style>body:is(' + PAGES + ') .wp-block-post-content{max-width:none!important;width:100%!important;margin:0!important;padding:0!important}'
         'body:is(' + PAGES + ') .wp-block-post-content>*{max-width:none!important;margin-block:0!important}'
         'body:is(' + PAGES + ') .wp-block-post-title{display:none}</style>')


def wrap(body, cls='', attrs=''):
    return ('<!-- wp:html -->\n' + reset + '<div id="ww-practice-v2" class="ww-practice-library' + (' ' + cls if cls else '') + '"'
            + (' ' + attrs if attrs else '') + '>' + body + '</div>\n<!-- /wp:html -->\n')


def label(r):
    return TYPES[r['type']]['label']


def href(r):
    return E(r['url'].replace('https://workforcewonkery.com', ''))


def count(topic):
    return sum(topic in r['topics'] for r in data['resources'])


def item(i, show_summary=True, tag=True):
    r = R[i]
    return ('<li>' + ('<span class="tag">' + E(label(r)) + '</span>' if tag else '') + '<a href="' + href(r) + '">' + E(r['title']) + '</a>'
            + ('<span class="sum">' + E(r['summary']) + '</span>' if show_summary else '') + '</li>')


def image(name, cls, width, height, eager=False):
    return ('<img class="' + cls + '" src="' + MEDIA + name + '" alt="" width="' + str(width) + '" height="' + str(height) + '" '
            + ('fetchpriority="high"' if eager else 'loading="lazy"') + ' decoding="async">')


# ---------------------------------------------------------------- Icons
# The site's existing line icons (Data and homepage sprite) plus two drawn in the same style for partner
# handoffs and board governance. Decorative: each sits beside a visible heading.
ICON_PATHS = {
    'people': '<circle cx="12" cy="7" r="3"/><path d="M6 22v-5a6 6 0 0 1 12 0v5M5 5a3 3 0 0 0 0 6m14-6a3 3 0 0 1 0 6M2 20v-4a4 4 0 0 1 3-4m17 8v-4a4 4 0 0 0-3-4"/>',
    'cap': '<path d="m1 8 11-5 11 5-11 5Zm5 3v6c4 3 8 3 12 0v-6m5-3v9"/>',
    'buildings': '<path d="M3 22V8h6v14m0 0V2h9v20m0-10h4v10M1 22h23M6 11v2m0 3v2m6-13v2m3-2v2m-3 3v2m3-2v2m-3 3v2m3-2v2"/>',
    'handoff': '<path d="M4 8h14m-4-4 4 4-4 4M20 16H6m4-4-4 4 4 4"/>',
    'board': '<path d="M2 9 12 3l10 6M4 10v8m5.3-8v8m5.4-8v8M20 10v8M2 21h20M3 18.5h18"/>',
    'data': '<path d="M4 21v-7h3v7m4 0V7h3v14m4 0V2h3v19" fill="currentColor" stroke="none"/>',
    'checklist': '<path d="M10 6h11M10 12h11M10 18h11M3 6l1.5 1.5L7 5m-4 7 1.5 1.5L7 11m-4 7 1.5 1.5L7 17"/>',
    'policy': '<path d="M6 2h9l4 4v16H5V3a1 1 0 0 1 1-1Zm9 0v5h4M8 10h7M8 13h7M8 16h7M8 19h5"/>',
    'bulb': '<path d="M8 18h8M9 21h6M10 23h4M8 16c0-3-3-4-3-8a7 7 0 0 1 14 0c0 4-3 5-3 8Z"/>',
    'stars': '<path d="m12 3 2.2 5.8L20 11l-5.8 2.2L12 19l-2.2-5.8L4 11l5.8-2.2ZM21 1v6m-3-3h6M3 17v6m-3-3h6"/>',
}
TOPIC_ICON = {'participants': 'people', 'training': 'cap', 'employers': 'buildings', 'partners': 'handoff', 'oversight': 'board', 'performance': 'data'}


def sprite(names):
    return ('<svg class="pr-sprite" width="0" height="0" aria-hidden="true" focusable="false">'
            + ''.join('<symbol id="pr-i-' + n + '" viewBox="0 0 24 24">' + ICON_PATHS[n] + '</symbol>' for n in names) + '</svg>')


def icon(name, tone=''):
    return ('<span class="pr-icon' + (' ' + tone if tone else '') + '" aria-hidden="true"><svg focusable="false"><use href="#pr-i-' + name + '"/></svg></span>')


ICON_CSS = ('.pr-sprite{position:absolute;width:0;height:0;overflow:hidden}'
            '.pr-icon{display:flex;align-items:center;justify-content:center;width:48px;height:48px;border-radius:50%;background:#e9f3f4;color:#075f70;margin:0 0 14px}'
            '.pr-icon.gold{background:#f8f0df;color:#986714}'
            '.pr-icon svg{width:24px;height:24px;fill:none;stroke:currentColor;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}')


# ---------------------------------------------------------------- Practice home
home_style = '''<style>
#ww-practice-v2.practice-home{padding:0 0 72px}
#ww-practice-v2 .pw{width:calc(100% - 88px);max-width:1320px;margin:0 auto}
#ww-practice-v2 .practice-hero{position:relative;isolation:isolate;overflow:hidden;height:18.78vw;min-height:18.78vw;background:#fcfaf6;border-bottom:1px solid #eee9de}
#ww-practice-v2 .practice-hero:after{content:"";position:absolute;inset:0;z-index:1;pointer-events:none;background:linear-gradient(90deg,#fcfaf6 0%,#fcfaf6 31%,rgba(252,250,246,.98) 38%,rgba(252,250,246,.84) 45%,rgba(252,250,246,.42) 53%,rgba(252,250,246,0) 65%)}
#ww-practice-v2 .practice-hero-photo{position:absolute;inset:0 0 0 auto;width:63%;height:100%;overflow:hidden;z-index:0}
#ww-practice-v2 .practice-hero-photo img{display:block;width:100%;height:100%;max-width:none;object-fit:cover;object-position:center 38%}
#ww-practice-v2 .practice-hero-inner{height:100%;position:relative;z-index:2;display:flex;align-items:center}
#ww-practice-v2 .practice-hero-copy{width:49%}
#ww-practice-v2 .practice-hero .eyebrow{display:block;color:#986714;font:600 clamp(11px,.72vw,15px)/1.5 Arial,Helvetica,sans-serif;letter-spacing:.16em;text-transform:uppercase;margin:0 0 clamp(12px,1.1vw,20px)}
#ww-practice-v2 .practice-hero h1{font-size:clamp(56px,5.1vw,94px)!important;line-height:.98!important;letter-spacing:-.052em!important;margin:0 0 clamp(18px,1.5vw,28px)!important;white-space:nowrap}
#ww-practice-v2 .practice-hero .deck{font:clamp(20px,1.45vw,29px)/1.42 Georgia,'Times New Roman',serif;color:#1d3546;max-width:760px;margin:0;text-wrap:pretty}
#ww-practice-v2.practice-home>section,#ww-practice-v2.practice-home .pw>section{margin-top:64px;padding-top:0;border-top:0}
#ww-practice-v2 .sec-head{max-width:760px;margin-bottom:28px}
#ww-practice-v2 .sec-head h2{margin-bottom:10px!important}
#ww-practice-v2 .sec-head .deck{font:19px/1.5 Georgia,'Times New Roman',serif;color:#344454;margin:0}
#ww-practice-v2 .pr-start{max-width:760px;margin-top:48px!important;padding:40px 0 0}
#ww-practice-v2 .pr-start h2{font-size:clamp(30px,2.6vw,40px)!important}
#ww-practice-v2 .pr-start .hint{font-size:15px;color:#4d5558;margin:14px 0 0}
#ww-practice-v2 .ideas-more h3{font:600 12px/1.5 Arial,Helvetica,sans-serif!important;letter-spacing:.16em!important;text-transform:uppercase!important;color:#986714!important;margin:6px 0 10px!important}
#ww-practice-v2 .work-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:40px 40px}
#ww-practice-v2 .work-grid article{border-top:1px solid #dedbd3;padding-top:22px}
#ww-practice-v2 .ww-practice-nav{display:none!important}
#ww-practice-v2 .desk .pr-icon{margin-bottom:12px}
#ww-practice-v2 .track{display:grid;grid-template-columns:48px minmax(0,1fr);column-gap:18px}
#ww-practice-v2 .track .pr-icon{grid-row:1/span 4;margin:2px 0 0}
#ww-practice-v2 .work-grid h3 a{color:#101c29;text-decoration:none}
#ww-practice-v2 .work-grid h3 a:hover,#ww-practice-v2 .work-grid h3 a:focus-visible{color:#075f70;text-decoration:underline}
#ww-practice-v2 .work-grid>article>p{color:#344454;margin:0 0 12px}
#ww-practice-v2 .links{list-style:none;margin:0 0 12px;padding:0}
#ww-practice-v2 .links li{padding:6px 0;border-top:1px solid #e8e3d8;font-size:16px;line-height:1.4}
#ww-practice-v2 .links .tag{display:block;margin-bottom:1px}
#ww-practice-v2 .more{font-size:15px;font-weight:600;margin:0}
#ww-practice-v2 .desks{display:grid;grid-template-columns:1fr 1fr;gap:0;background:#f4efe5;border-top:1px solid #e3dccd;border-bottom:1px solid #e3dccd}
#ww-practice-v2 .desk{padding:32px 36px 30px}
#ww-practice-v2 .desk+.desk{border-left:1px solid #e3dccd}
#ww-practice-v2 .desk h3{font-size:28px!important}
#ww-practice-v2 .desk h3 a{color:#101c29;text-decoration:none}
#ww-practice-v2 .desk h3 a:hover,#ww-practice-v2 .desk h3 a:focus-visible{color:#075f70;text-decoration:underline}
#ww-practice-v2 .desk>p{color:#344454;margin:0 0 16px}
#ww-practice-v2 .desk .links li{border-color:#e0d8c7}
#ww-practice-v2 .tracks{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:40px}
#ww-practice-v2 .track{border-top:1px solid #dedbd3;padding:22px 0 0}
#ww-practice-v2 .tracks>.more{grid-column:1/-1}
#ww-practice-v2 .track .step{font:600 12px/1.5 Arial,Helvetica,sans-serif;letter-spacing:.16em;text-transform:uppercase;color:#986714;margin:0 0 6px}
#ww-practice-v2 .track h3 a{color:#101c29}
#ww-practice-v2 .track p{color:#344454;margin:0 0 10px}
#ww-practice-v2 .inline{list-style:none;margin:0 0 12px;padding:0;display:flex;flex-wrap:wrap;gap:6px 22px;font-size:16px}
#ww-practice-v2 .ideas-lead{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:40px;align-items:stretch;margin-bottom:40px}
#ww-practice-v2 .ideas-image{display:block;width:100%;height:100%;min-height:300px;object-fit:cover}
#ww-practice-v2 .collections{list-style:none;margin:0;padding:0}
#ww-practice-v2 .collections li{border-top:1px solid #dedbd3;padding:16px 0}
#ww-practice-v2 .collections li:first-child{border-top:2px solid #101c29}
#ww-practice-v2 .collections a{font:24px/1.2 Georgia,'Times New Roman',serif;color:#101c29}
#ww-practice-v2 .collections p{margin:6px 0 0;color:#344454}
#ww-practice-v2 .stories{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:32px;margin-bottom:40px}
#ww-practice-v2 .stories article{border-top:1px solid #dedbd3;padding-top:16px}
#ww-practice-v2 .stories h3{font-size:24px!important}
#ww-practice-v2 .stories h3 a{color:#101c29;text-decoration:none}
#ww-practice-v2 .stories h3 a:hover,#ww-practice-v2 .stories h3 a:focus-visible{color:#075f70;text-decoration:underline}
#ww-practice-v2 .stories p{color:#344454;margin:0}
#ww-practice-v2 .ideas-more{display:grid;grid-template-columns:1fr 1fr;gap:40px}
#ww-practice-v2 .trust{margin-top:56px!important;padding-top:20px;border-top:1px solid #dedbd3;display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px 32px;font-size:15px;color:#4d5558}
#ww-practice-v2 .trust p{margin:0}
#ww-practice-v2 p.tag{color:#85590e;margin:0 0 6px}
@media(max-width:1000px){
#ww-practice-v2 .practice-hero-copy{width:55%}
#ww-practice-v2 .practice-hero-photo{width:59%}
#ww-practice-v2 .practice-hero h1{white-space:normal}
#ww-practice-v2 .practice-hero{height:auto}
#ww-practice-v2 .practice-hero-inner{height:auto;min-height:18.78vw;padding:22px 0}
#ww-practice-v2 .practice-hero h1{font-size:clamp(44px,5.1vw,56px)!important}
#ww-practice-v2 .practice-hero .deck{font-size:clamp(18px,2vw,20px)}
#ww-practice-v2 .tracks{grid-template-columns:1fr;gap:0}
#ww-practice-v2 .track{padding-bottom:16px}
#ww-practice-v2 .work-grid,#ww-practice-v2 .stories{grid-template-columns:1fr 1fr}
#ww-practice-v2 .ideas-lead{grid-template-columns:1fr;gap:24px}
#ww-practice-v2 .ideas-image{min-height:0;aspect-ratio:16/7;height:auto}
}
@media(max-width:760px){
#ww-practice-v2 .practice-hero{height:auto;min-height:0;border-bottom:0}
#ww-practice-v2 .practice-hero:after{display:none}
#ww-practice-v2 .practice-hero-photo{position:relative;inset:auto;width:100%;height:220px}
#ww-practice-v2 .practice-hero-inner{height:auto;min-height:0;display:block;padding:26px 0 22px}
#ww-practice-v2 .practice-hero-copy{width:100%}
#ww-practice-v2 .practice-hero .eyebrow{font-size:11px;margin-bottom:9px}
#ww-practice-v2 .practice-hero h1{font-size:44px!important;line-height:1.03!important;margin-bottom:12px!important}
#ww-practice-v2 .practice-hero .deck{font-size:19px;max-width:none}
#ww-practice-v2 .pr-start{margin-top:28px!important;padding-top:24px}
#ww-practice-v2 .work-grid,#ww-practice-v2 .stories,#ww-practice-v2 .desks,#ww-practice-v2 .ideas-more{grid-template-columns:1fr}
#ww-practice-v2 .desk+.desk{border-left:0;border-top:1px solid #e3dccd}
#ww-practice-v2 .desk{padding:26px 22px}
#ww-practice-v2.practice-home>section,#ww-practice-v2.practice-home .pw>section{margin-top:48px}
}
@media(max-width:600px){#ww-practice-v2 .pw{width:calc(100% - 36px)}}
</style>'''

# Icon styles are scoped to the Practice page, before the responsive rules.
home_style = home_style.replace('@media(max-width:1000px){', ''.join('#ww-practice-v2 ' + r + '\n' for r in ICON_CSS.replace('}', '}\n').strip().split('\n')) + '@media(max-width:1000px){', 1)

hero = ('<header class="practice-hero" aria-labelledby="wwp-practice-title"><div class="practice-hero-photo" aria-hidden="true">'
        + image('golden_hour_office_collaboration_with_la_skyline.png', 'practice-hero-image', 2172, 724, True)
        + '</div><div class="pw practice-hero-inner"><div class="practice-hero-copy"><p class="eyebrow">From practice to progress</p>'
        '<h1 id="wwp-practice-title">Practice <span>Decoded.</span></h1>'
        '<p class="deck">Answers for the question on your desk, ideas from other workforce systems, and the knowledge behind the work.</p>'
        '</div></div></header>')

start = ('<section class="pr-start" id="start" aria-labelledby="pr-start-h"><div class="pr-start-search"><p class="eyebrow">Start here</p>'
         '<h2 id="pr-start-h">What are you working on?</h2>'
         '<form role="search" action="/practice/tools/" method="get"><label for="practice-home-q">Search Practice</label><div class="search-row">'
         '<input id="practice-home-q" type="search" name="q" placeholder="Try ITA, new ETPL provider, or CalFresh" autocomplete="off"><button>Search</button></div></form>'
         '<p class="hint">Searches all ' + str(N) + ' Quickstarts, tools, lessons and examples. Or <a href="/practice/quickstarts/">browse the ' + str(NQ)
         + ' Quickstarts</a>.</p></div>'
         '</section>')

# "Browse by the work you do": the area's starting reference plus core tasks, one click from the home page.
WORK = {'participants': [1114, 1558, 1389], 'training': [7531, 1388, 7533], 'employers': [1561, 1574, 1465],
        'partners': [1468, 1115, 7594], 'oversight': [1569, 1566, 1122], 'performance': [1567, 1105, 1390]}
work = ('<section id="topics" aria-labelledby="pr-work-h"><header class="sec-head"><p class="eyebrow">Browse by the work you do</p>'
        '<h2 id="pr-work-h">Six areas of workforce practice</h2><p class="deck">Each area brings together the Quickstarts, references, lessons and field examples for one part of the job.</p></header>'
        '<div class="work-grid">'
        + ''.join('<article>' + icon(TOPIC_ICON[t['id']], 'gold' if k % 2 else '') + '<h3><a href="/practice/topics/?topic=' + t['id'] + '">' + E(t['title']) + '</a></h3><p>' + E(t['summary']) + '</p><ul class="links">'
                  + ''.join(item(i, False, False) for i in WORK[t['id']]) + '</ul><p class="more"><a href="/practice/topics/?topic=' + t['id'] + '">All '
                  + str(count(t['id'])) + ' ' + E(t['title']) + ' resources<span aria-hidden="true"> →</span></a></p></article>' for k, t in enumerate(data['topics']))
        + '</div></section>')

DESKS = [(7531, [7550, 7544, 7543], 'checklist', ''), (7861, [7839, 7802, 7801], 'policy', 'gold')]
desks = ('<section id="desks" aria-labelledby="pr-desks-h"><header class="sec-head"><p class="eyebrow">Desks for specialized work</p>'
         '<h2 id="pr-desks-h">Focused help for complex responsibilities</h2><p class="deck">A desk gathers onboarding, everyday tasks, current guidance and source checks for one responsibility, so you do not have to assemble them yourself.</p></header>'
         '<div class="desks">'
         + ''.join('<article class="desk">' + icon(ic, tone) + '<h3><a href="' + href(R[d]) + '">' + E(R[d]['title']) + '</a></h3><p>' + E(R[d]['summary'])
                   + '</p><ul class="links">' + ''.join(item(i, False, False) for i in subs) + '</ul></article>' for d, subs, ic, tone in DESKS)
         + '</div></section>')

learn = ('<section id="learn" aria-labelledby="pr-learn-h"><header class="sec-head"><p class="eyebrow">Learn and grow</p>'
         '<h2 id="pr-learn-h">Learn the system. Strengthen your practice.</h2><p class="deck">Start with the foundations, go deeper when you are ready, and test your judgment on realistic cases.</p></header>'
         '<div class="learn"><div class="tracks">'
         '<div class="track">' + icon('bulb') + '<p class="step">New to workforce development</p><h3><a href="' + href(R[1210]) + '">Foundations Course</a></h3><p>' + E(R[1210]['summary'])
         + '</p><ul class="inline">' + ''.join('<li><a href="' + href(R[i]) + '">' + E(R[i]['title']) + '</a></li>' for i in [937, 936, 943]) + '</ul></div>'
         '<div class="track">' + icon('cap', 'gold') + '<p class="step">Ready to go deeper</p><h3><a href="' + href(R[1427]) + '">Workforce in Practice</a></h3><p>' + E(R[1427]['summary'])
         + '</p><ul class="inline">' + ''.join('<li><a href="' + href(R[i]) + '">' + E(re.sub(r'^Workforce in Practice \d+: ', '', R[i]['title'])) + '</a></li>' for i in [1429, 1431, 1434]) + '</ul></div>'
         '<div class="track">' + icon('stars') + '<p class="step">Practice your judgment</p><ul class="links">' + ''.join(item(i, False, False) for i in [1193, 7547, 2645]) + '</ul></div>'
         '<p class="more"><a href="/practice/tools/?type=Course">All ' + str(sum(r['type'] == 'Course' for r in data['resources'])) + ' lessons and courses<span aria-hidden="true"> →</span></a></p>'
         '</div></div></section>')

# Places and subjects are taken from each story's own page.
STORIES = [(7596, 'Detroit · Service design'), (7585, 'Massachusetts · Employer engagement'), (7595, 'Washington · Economic security')]
ideas = ('<section id="ideas" aria-labelledby="pr-ideas-h"><header class="sec-head"><p class="eyebrow">Ideas worth borrowing</p>'
         '<h2 id="pr-ideas-h">What other workforce systems are learning</h2><p class="deck">Examples and evidence from California and beyond, written to help you decide what is worth testing locally, and what the evidence cannot yet prove.</p></header>'
         '<div class="ideas-lead">' + image('golden_hour_vineyard_valley.png', 'ideas-image', 1672, 941) + '<ul class="collections">'
         + ''.join('<li><a href="' + href(R[i]) + '">' + E(R[i]['title']) + '</a><p>' + E(R[i]['summary']) + '</p></li>' for i in [3851, 6546, 6547]) + '</ul></div>'
         '<div class="stories">' + ''.join('<article><p class="tag">' + E(place) + '</p><h3><a href="' + href(R[i]) + '">' + E(R[i]['title']) + '</a></h3><p>' + E(R[i]['summary']) + '</p></article>' for i, place in STORIES)
         + '</div><div class="ideas-more"><div><h3>Deep dives on hard questions</h3><ul class="links">' + ''.join(item(i, False, False) for i in [6551, 6554, 7474, 6553])
         + '</ul><p class="more"><a href="/practice/tools/?type=Research">All deep dives<span aria-hidden="true"> →</span></a> · <a href="/practice/tools/?type=Example">All examples<span aria-hidden="true"> →</span></a></p></div>'
         '<div><h3>Workbooks to test an idea</h3><ul class="links">' + ''.join(item(i, True, False) for i in [7594, 7584]) + '</ul></div></div></section>')

trust = ('<div class="trust"><p>Each resource shows its review date, sources and evidence limits. Official sources and your local policy control. <a href="/trust/">Our trust standards</a></p>'
         '<p><a href="/practice/tools/">Browse all ' + str(N) + ' resources<span aria-hidden="true"> →</span></a></p></div>')

home = home_style + sprite(['people', 'cap', 'buildings', 'handoff', 'board', 'data', 'checklist', 'policy', 'bulb', 'stars']) + hero + '<div class="pw">' + start + work + desks + learn + ideas + trust + '</div>'
(S / 'templates/practice-editorial-v2.html').write_text(wrap(home, 'practice-home'))


# ---------------------------------------------------------------- Hubs: all resources, topics, Quickstarts
def directory_form():
    options = '<option value="">All topics</option>' + ''.join('<option value="' + t['id'] + '">' + E(t['title']) + '</option>' for t in data['topics'])
    types = '<option value="">All resource types</option>' + ''.join('<option value="' + E(t['id']) + '">' + E(t['label']) + '</option>' for t in data['types'])
    return ('<form action="" method="get" role="search"><div class="filters"><div><label for="practice-q">Search Practice</label>'
            '<input type="search" name="q" id="practice-q" placeholder="A task, question, topic or acronym" autocomplete="off"></div>'
            '<div><label for="practice-topic">Topic</label><select name="topic" id="practice-topic">' + options + '</select></div>'
            '<div><label for="practice-type">Resource type</label><select name="type" id="practice-type">' + types + '</select></div></div>'
            '<p class="actions"><button>Find resources</button> <button type="button" class="secondary" data-reset>Clear filters</button></p></form>')


type_legend = ('<details class="type-legend"><summary>What the resource types mean</summary><dl>'
               + ''.join('<div><dt>' + E(t['label']) + '</dt><dd>' + E(t['what']) + '</dd></div>' for t in data['types']) + '</dl></details>')


def topic_overview():
    return ('<section class="topic-overview" data-topic-overview aria-label="Topics"><div class="topic-grid">'
            + ''.join('<article>' + icon(TOPIC_ICON[t['id']], 'gold' if k % 2 else '') + '<h2><a href="?topic=' + t['id'] + '">' + E(t['title']) + '</a></h2><p>' + E(t['summary']) + '</p>'
                      '<p class="start">Start with <a href="' + href(R[t['start']]) + '">' + E(R[t['start']]['title']) + '</a></p>'
                      '<p class="more"><a href="?topic=' + t['id'] + '">Open the topic guide · ' + str(count(t['id'])) + ' resources<span aria-hidden="true"> →</span></a></p></article>'
                      for k, t in enumerate(data['topics'])) + '</div></section>')


HUBS = [
    ('practice-resource-directory.html', 'All resources', 'Find the resource for your next step.',
     'Search ' + str(N) + ' Quickstarts, tools, lessons, deep dives and examples, or narrow the list by topic and type.', '', 'directory'),
    ('practice-topic-library.html', 'Topics', 'Start with the work in front of you.',
     'Choose an area of work to see where to start, the tasks people bring most often, and the lessons and ideas behind them.', '', 'topics'),
    ('practice-quickstarts.html', 'Quickstarts', 'Quickstarts',
     'Step-by-step help with a specific decision: when to use it, what to check, what to decide and when to escalate. Each one points to the sources that control.', 'Quickstart', 'quickstarts'),
]
for filename, crumb, title, intro, default, kind in HUBS:
    head = ('<header class="hub-head"><h1 id="practice-hub-title" data-hub-title>' + E(title) + '</h1><p class="intro" data-hub-intro>' + E(intro) + '</p></header>')
    extra = ''
    if kind == 'topics':
        extra = '<style>' + ' '.join('#ww-practice-v2 ' + r for r in ICON_CSS.replace('}', '}\n').strip().split('\n')) + '</style>' + sprite(list(TOPIC_ICON.values())) + topic_overview() + '<div data-topic-guides></div>'
    results_head = ('<h2 class="results-title" data-results-title>' + ('Search all topics' if kind == 'topics' else 'Resources') + '</h2>')
    body = (head + extra + '<section class="hub-results" data-results-section aria-labelledby="practice-results-title">'
            + results_head.replace('<h2 class', '<h2 id="practice-results-title" class') + directory_form()
            + (type_legend if kind == 'directory' else '')
            + '<p role="status" aria-live="polite" class="status">' + str(N) + ' resources</p>'
            '<p data-empty hidden>No resources match. Try a shorter phrase, an acronym such as ITA or OJT, or clear a filter.</p>'
            '<noscript><p>Search and the resource list need JavaScript. You can still browse every area of work from the <a href="/practice/">Practice home</a>.</p></noscript>'
            '<div class="resource-list" data-results></div></section>'
            '<p class="muted">Each resource shows its review date, sources and evidence limits. Official sources and your local policy control. <a href="/trust/">Our trust standards</a>.</p>')
    (S / 'templates' / filename).write_text(wrap(body, 'practice-hub', 'data-practice-directory data-page="' + kind + '" data-default-type="' + default + '"'))

# ---------------------------------------------------------------- Shared Practice runtime (footer)
# The Practice runtime lives at the end of the small global footer, not the large site header, so routine
# catalogue and navigation updates touch one small template part. It adds section navigation, breadcrumbs,
# related resources, hub lists, topic guides and search. Only the fields the browser needs are embedded.
css = (S / 'css/practice-navigation.css').read_text()
js = (S / 'javascript/practice-navigation.js').read_text()
# WordPress treats '<' followed by a letter as the start of a tag when it renders template parts and
# entity-encodes the '&&' that follows, which breaks inline JavaScript. Keep the runtime free of them.
assert not re.search(r'<[A-Za-z!/?]', js), 'Inline Practice runtime must not contain "<" followed by a letter'
embed = {'version': data['version'], 'types': data['types'],
         'topics': [{k: t[k] for k in ('id', 'title', 'summary', 'intro', 'start', 'tasks', 'keep', 'learn', 'ideas')} for t in data['topics']],
         'resources': data['resources']}
MARK = re.compile(r'\n*<!-- PRACTICE NAVIGATION START -->[\s\S]*?<!-- PRACTICE NAVIGATION END -->\n?')
header = S / 'template-parts/header-editorial-blocks.html'
header.write_text(MARK.sub('', header.read_text()).rstrip('\n') + '\n')
footer = S / 'template-parts/footer-editorial-blocks.html'
base = MARK.sub('', footer.read_text()).rstrip('\n') + '\n'
fragment = ('<!-- wp:html -->\n<style>' + css + '</style><script type="application/json" id="ww-practice-data">'
            + json.dumps(embed, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c') + '</script><script>' + js + '</script>\n<!-- /wp:html -->')
footer.write_text(base + '\n<!-- PRACTICE NAVIGATION START -->\n' + fragment + '\n<!-- PRACTICE NAVIGATION END -->\n')
print('Built Practice home, topics, resource directory, Quickstarts, and the shared Practice runtime in the footer.')
