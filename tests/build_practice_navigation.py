"""Build reader-facing Practice hubs from one reviewed catalogue. Run from any cwd."""
import json,html,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; S=ROOT/'src/wordpress'
data=json.loads((S/'javascript/practice-catalogue.json').read_text()); E=html.escape
nav='<nav class="ww-practice-nav" aria-label="Practice"><a href="/practice/">Practice home</a><a href="/practice/topics/">Topics</a><a href="/practice/tools/">All resources</a><a href="/practice/tools/?type=Course">Courses</a></nav>'
css=(S/'css/practice-navigation.css').read_text()
reset='<style>body:is(.page-id-935,.page-id-1211,.page-id-1212,.page-id-1387) .wp-block-post-content{max-width:none!important}body:is(.page-id-935,.page-id-1211,.page-id-1212,.page-id-1387) .wp-block-post-title{display:none}</style>'
def wrap(body,attrs=''):
 return '<!-- wp:html -->\n'+reset+'<div id="ww-practice-v2" class="ww-practice-library" '+attrs+'>'+body+'</div>\n<!-- /wp:html -->\n'
def tiles():
 return '<div class="topic-grid">'+''.join('<article><h3><a href="/practice/topics/?topic='+t['id']+'">'+E(t['title'])+'</a></h3><p>'+E(t['summary'])+'</p></article>' for t in data['topics'])+'</div>'
def link(id):
 r=next(r for r in data['resources'] if r['id']==id)
 return '<article><h3><a href="'+E(r['url'])+'">'+E(r['title'])+'</a></h3><p>'+E(r['summary'])+'</p></article>'
search='<form action="/practice/tools/" method="get"><label for="practice-home-q">What are you working on?</label><div class="search-row"><input id="practice-home-q" type="search" name="q" placeholder="Try training approval, employer engagement, or CalFresh"><button>Search Practice</button></div></form>'
body='<p class="eyebrow">Find a useful next step</p><h1>Practice <span>Decoded.</span></h1><p class="intro">A question on your desk. A decision to make. Find practical guidance, learn from other workforce boards, and build the knowledge behind the work.</p>'+search+'<section id="wwp-practice-paths"><h2>Browse by the work you do</h2>'+tiles()+'</section><section id="wwp-desk-aids"><h2>Focused help for complex work</h2><div class="collection-grid">'+link(7531)+link(7861)+'</div></section><section><h2>Learn the system. Strengthen your practice.</h2><p>New to workforce development? Start with Foundations. Ready to go deeper? Explore the decisions and tradeoffs in Workforce in Practice.</p><div class="collection-grid">'+link(1210)+link(1427)+'</div></section><section id="wwp-deep-dives"><h2>Worth exploring</h2><div class="collection-grid">'+link(7594)+link(7584)+link(3851)+link(6546)+'</div><p><a href="/practice/tools/">Browse all resources →</a></p></section>'
(S/'templates/practice-editorial-v2.html').write_text(wrap(body))
for filename,title,default,extra in [('practice-resource-directory.html','Find the resource for your next step.','',''),('practice-topic-library.html','Start with the work in front of you.','',tiles()),('practice-quickstarts.html','Quickstarts','Quickstart','')]:
 options='<option value="">All topics</option>'+''.join('<option value="'+t['id']+'">'+E(t['title'])+'</option>' for t in data['topics'])
 types='<option value="">All resource types</option>'+''.join('<option>'+E(t)+'</option>' for t in sorted({r['type'] for r in data['resources']}))
 form='<form action="" method="get"><div class="filters"><div><label for="practice-q">Search Practice</label><input type="search" name="q" id="practice-q" placeholder="A task, topic, or acronym"></div><div><label for="practice-topic">Topic</label><select name="topic" id="practice-topic">'+options+'</select></div><div><label for="practice-type">Resource type</label><select name="type" id="practice-type">'+types+'</select></div></div><p><button>Find resources</button> <button type="button" data-reset>Clear filters</button></p></form>'
 rows=''.join('<article class="resource" data-resource-id="'+str(r['id'])+'"><p class="meta">'+E(r['type'])+'</p><h3><a href="'+E(r['url'])+'">'+E(r['title'])+'</a></h3><p>'+E(r['summary'])+'</p></article>' for r in data['resources'])
 body='<p class="eyebrow">Practice / '+('Topics' if 'topic' in filename else 'Resource library')+'</p><h1>'+title+'</h1><p class="intro">Choose a topic, search for a task, or narrow the list to guides, tools, examples, and learning.</p>'+extra+form+'<section data-topic-guide hidden></section><p role="status" aria-live="polite">'+str(len(data['resources']))+' resources</p><p data-empty hidden>No resources match these filters. Try a shorter phrase or clear a filter.</p><noscript><p>The complete resource list is below. Enable JavaScript to use search and filters, or use your browser’s Find command.</p></noscript>'+rows+'<p class="muted">Review dates, sources, evidence limits, and local policy checks are on each resource. Official sources control. <a href="/trust/">Our trust standards</a>.</p>'
 (S/'templates'/filename).write_text(wrap(body,'data-practice-directory data-default-type="'+default+'"'))
# The global header remains the sole site header. The enhancement adds only section navigation.
header=S/'template-parts/header-editorial-blocks.html';text=header.read_text();text=re.sub(r'\n<!-- PRACTICE NAVIGATION START -->[\s\S]*?<!-- PRACTICE NAVIGATION END -->\n','\n',text)
js=(S/'javascript/practice-navigation.js').read_text()
fragment='<!-- wp:html -->\n<style>'+css+'</style><script type="application/json" id="ww-practice-catalogue">'+json.dumps(data,ensure_ascii=False).replace('<','\\u003c')+'</script><script>'+js+'</script>\n<!-- /wp:html -->'
header.write_text(text+'\n<!-- PRACTICE NAVIGATION START -->\n'+fragment+'\n<!-- PRACTICE NAVIGATION END -->\n')
print('Built Practice home, topics, resource directory, Quickstarts, and shared section navigation.')
