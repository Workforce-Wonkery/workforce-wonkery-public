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
#ww-practice-v2 .pr-start{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:48px;margin-top:48px!important;padding:40px 0 0}
#ww-practice-v2 .pr-start h2{font-size:clamp(30px,2.6vw,40px)!important}
#ww-practice-v2 .pr-start .hint{font-size:15px;color:#4d5558;margin:14px 0 0}
#ww-practice-v2 :is(.pr-tasks,.ideas-more) h3{font:600 12px/1.5 Arial,Helvetica,sans-serif!important;letter-spacing:.16em!important;text-transform:uppercase!important;color:#986714!important;margin:6px 0 10px!important}
#ww-practice-v2 .pr-tasks ul{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:1fr 1fr;column-gap:32px}
#ww-practice-v2 .pr-tasks li{border-top:1px solid #dedbd3;padding:13px 0 14px}
#ww-practice-v2 .pr-tasks a{font:20px/1.3 Georgia,'Times New Roman',serif;color:#101c29;text-decoration:none}
#ww-practice-v2 .pr-tasks a:hover,#ww-practice-v2 .pr-tasks a:focus-visible{color:#075f70;text-decoration:underline}
#ww-practice-v2 .pr-tasks .via{display:block;font-size:14px;color:#4d5558;margin-top:4px}
#ww-practice-v2 .work-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:40px 40px}
#ww-practice-v2 .work-grid article{border-top:2px solid #101c29;padding-top:18px}
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
#ww-practice-v2 .learn{display:grid;grid-template-columns:minmax(0,4fr) minmax(0,8fr);gap:48px;align-items:start}
#ww-practice-v2 .learn-image{display:block;width:100%;aspect-ratio:4/3;height:auto;object-fit:cover;object-position:center 75%}
#ww-practice-v2 .track{border-top:1px solid #dedbd3;padding:20px 0 6px}
#ww-practice-v2 .track:first-child{border-top:0;padding-top:0}
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
#ww-practice-v2 .pr-start,#ww-practice-v2 .learn{grid-template-columns:1fr;gap:28px}
#ww-practice-v2 .learn-image{aspect-ratio:16/7}
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
#ww-practice-v2 .pr-tasks ul,#ww-practice-v2 .work-grid,#ww-practice-v2 .stories,#ww-practice-v2 .desks,#ww-practice-v2 .ideas-more{grid-template-columns:1fr}
#ww-practice-v2 .desk+.desk{border-left:0;border-top:1px solid #e3dccd}
#ww-practice-v2 .desk{padding:26px 22px}
#ww-practice-v2.practice-home>section,#ww-practice-v2.practice-home .pw>section{margin-top:48px}
}
@media(max-width:600px){#ww-practice-v2 .pw{width:calc(100% - 36px)}#ww-practice-v2 .pr-tasks a{font-size:19px}}
</style>'''

hero = ('<header class="practice-hero" aria-labelledby="wwp-practice-title"><div class="practice-hero-photo" aria-hidden="true">'
        + image('golden_hour_office_collaboration_with_la_skyline.png', 'practice-hero-image', 2172, 724, True)
        + '</div><div class="pw practice-hero-inner"><div class="practice-hero-copy"><p class="eyebrow">From practice to progress</p>'
        '<h1 id="wwp-practice-title">Practice <span>Decoded.</span></h1>'
        '<p class="deck">Answers for the question on your desk, ideas from other workforce systems, and the knowledge behind the work.</p>'
        '</div></div></header>')

# "Help me solve something": the questions people most often bring, each one choice from the answer.
QUESTIONS = [
    (1558, 'Does this person qualify as a Dislocated Worker?'),
    (1388, 'Should we approve this training request or ITA?'),
    (7533, 'A new training provider wants to join the ETPL'),
    (7861, 'Preparing for CalFresh and Medi-Cal work requirements'),
    (1394, 'An employer needs help hiring or training workers'),
    (1392, 'A monitoring finding just arrived'),
    (1391, 'Our performance report shows a red number'),
    (1395, 'This decision needs to go to the board'),
]
start = ('<section class="pr-start" id="start" aria-labelledby="pr-start-h"><div class="pr-start-search"><p class="eyebrow">Start here</p>'
         '<h2 id="pr-start-h">What are you working on?</h2>'
         '<form role="search" action="/practice/tools/" method="get"><label for="practice-home-q">Search Practice</label><div class="search-row">'
         '<input id="practice-home-q" type="search" name="q" placeholder="Try ITA, new ETPL provider, or CalFresh" autocomplete="off"><button>Search</button></div></form>'
         '<p class="hint">Searches all ' + str(N) + ' Quickstarts, tools, lessons and examples. Or <a href="/practice/quickstarts/">browse the ' + str(NQ)
         + ' Quickstarts</a>.</p></div>'
         '<div class="pr-tasks"><h3>Common questions</h3><ul>'
         + ''.join('<li><a href="' + href(R[i]) + '">' + E(q) + '</a><span class="via">' + E(label(R[i])) + ': ' + E(R[i]['title']) + '</span></li>' for i, q in QUESTIONS)
         + '</ul></div></section>')

# "Browse by the work you do": two or three direct links per area, distinct from the common questions above.
WORK = {'participants': [1114, 1389, 1557], 'training': [7531, 7548, 7538], 'employers': [1561, 1574, 1465],
        'partners': [1468, 1115, 7594], 'oversight': [1569, 1566, 1122], 'performance': [1567, 1105, 1390]}
work = ('<section id="topics" aria-labelledby="pr-work-h"><header class="sec-head"><p class="eyebrow">Browse by the work you do</p>'
        '<h2 id="pr-work-h">Six areas of workforce practice</h2><p class="deck">Each area brings together the Quickstarts, references, lessons and field examples for one part of the job.</p></header>'
        '<div class="work-grid">'
        + ''.join('<article><h3><a href="/practice/topics/?topic=' + t['id'] + '">' + E(t['title']) + '</a></h3><p>' + E(t['summary']) + '</p><ul class="links">'
                  + ''.join(item(i, False) for i in WORK[t['id']]) + '</ul><p class="more"><a href="/practice/topics/?topic=' + t['id'] + '">All '
                  + str(count(t['id'])) + ' ' + E(t['title']) + ' resources<span aria-hidden="true"> →</span></a></p></article>' for t in data['topics'])
        + '</div></section>')

DESKS = [(7531, [7550, 7544, 7543]), (7861, [7839, 7802, 7801])]
desks = ('<section id="desks" aria-labelledby="pr-desks-h"><header class="sec-head"><p class="eyebrow">Desks for specialized work</p>'
         '<h2 id="pr-desks-h">Focused help for complex responsibilities</h2><p class="deck">A desk gathers onboarding, everyday tasks, current guidance and source checks for one responsibility, so you do not have to assemble them yourself.</p></header>'
         '<div class="desks">'
         + ''.join('<article class="desk"><p class="tag">' + E(label(R[d])) + '</p><h3><a href="' + href(R[d]) + '">' + E(R[d]['title']) + '</a></h3><p>' + E(R[d]['summary'])
                   + '</p><ul class="links">' + ''.join(item(i, False) for i in subs) + '</ul></article>' for d, subs in DESKS)
         + '</div></section>')

learn = ('<section id="learn" aria-labelledby="pr-learn-h"><header class="sec-head"><p class="eyebrow">Learn and grow</p>'
         '<h2 id="pr-learn-h">Learn the system. Strengthen your practice.</h2><p class="deck">Start with the foundations, go deeper when you are ready, and test your judgment on realistic cases.</p></header>'
         '<div class="learn">' + image('practice-feature-case-upscaled.png', 'learn-image', 870, 714) + '<div class="tracks">'
         '<div class="track"><p class="step">New to workforce development</p><h3><a href="' + href(R[1210]) + '">Foundations Course</a></h3><p>' + E(R[1210]['summary'])
         + '</p><ul class="inline">' + ''.join('<li><a href="' + href(R[i]) + '">' + E(R[i]['title']) + '</a></li>' for i in [937, 936, 943]) + '</ul></div>'
         '<div class="track"><p class="step">Ready to go deeper</p><h3><a href="' + href(R[1427]) + '">Workforce in Practice</a></h3><p>' + E(R[1427]['summary'])
         + '</p><ul class="inline">' + ''.join('<li><a href="' + href(R[i]) + '">' + E(re.sub(r'^Workforce in Practice \d+: ', '', R[i]['title'])) + '</a></li>' for i in [1429, 1431, 1434]) + '</ul></div>'
         '<div class="track"><p class="step">Practice your judgment</p><ul class="links">' + ''.join(item(i) for i in [1193, 7547, 2645]) + '</ul></div>'
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

home = home_style + hero + '<div class="pw">' + start + work + desks + learn + ideas + trust + '</div>'
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
            + ''.join('<article><h2><a href="?topic=' + t['id'] + '">' + E(t['title']) + '</a></h2><p>' + E(t['summary']) + '</p>'
                      '<p class="start">Start with <a href="' + href(R[t['start']]) + '">' + E(R[t['start']]['title']) + '</a></p>'
                      '<p class="more"><a href="?topic=' + t['id'] + '">Open the topic guide · ' + str(count(t['id'])) + ' resources<span aria-hidden="true"> →</span></a></p></article>'
                      for t in data['topics']) + '</div></section>')


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
        extra = topic_overview() + '<div data-topic-guides></div>'
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
