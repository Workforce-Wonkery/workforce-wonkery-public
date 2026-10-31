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
# Reuse the owner-approved Practice imagery while retaining the task-first directory.
media='https://workforcewonkery.com/wp-content/uploads/2026/09/'
home_style='''<style>
#ww-practice-v2.practice-home{padding-top:0}
#ww-practice-v2 .practice-hero{position:relative;isolation:isolate;min-height:470px;display:flex;align-items:center;margin:0 calc(-1 * max(24px, (100vw - 1200px)/2));padding:64px max(24px,calc((100vw - 1200px)/2));overflow:hidden}
#ww-practice-v2 .practice-hero-image{position:absolute;z-index:-2;right:0;top:0;width:65%;height:100%;object-fit:cover;object-position:center}
#ww-practice-v2 .practice-hero:after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(90deg,#fcfaf6 0%,#fcfaf6 39%,rgba(252,250,246,.94) 44%,rgba(252,250,246,.64) 48%,rgba(252,250,246,.16) 54%,rgba(252,250,246,0) 61%)}
#ww-practice-v2 .practice-hero-copy{max-width:510px;width:44%}
#ww-practice-v2 .practice-hero h1{font-size:clamp(42px,4.5vw,64px)}
#ww-practice-v2 .practice-hero .intro{font-size:22px;line-height:1.45}
#ww-practice-v2 .practice-hero .eyebrow{text-transform:uppercase;letter-spacing:.12em;font-size:12px;margin-bottom:16px}
#ww-practice-v2 .practice-home-search{padding-top:8px}
#ww-practice-v2 .collection-image{display:block;width:100%;height:220px;object-fit:cover;margin-bottom:20px}
#ww-practice-v2 .learning-layout{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:start}
#ww-practice-v2 .learning-image{display:block;width:100%;height:330px;object-fit:cover}
#ww-practice-v2 .learning-links{display:grid;gap:24px}
#ww-practice-v2 .learning-links p{margin-bottom:0}
@media(max-width:900px){
#ww-practice-v2 .practice-hero{min-height:0;display:block;padding-top:0;padding-bottom:32px;overflow:visible}
#ww-practice-v2 .practice-hero-image{position:relative;width:calc(100% + 48px);max-width:none;height:280px;margin:0 -24px 28px;object-position:center 45%}
#ww-practice-v2 .practice-hero:after{display:none}
#ww-practice-v2 .practice-hero-copy{width:100%;max-width:680px}
#ww-practice-v2 .practice-hero h1{font-size:clamp(42px,7vw,60px)}
#ww-practice-v2 .learning-layout{gap:24px}
}
@media(max-width:640px){
#ww-practice-v2 .practice-hero{margin:0 -20px;padding:0 20px 12px}
#ww-practice-v2 .practice-hero-image{width:calc(100% + 40px);margin:0 -20px 28px;height:210px}
#ww-practice-v2 .practice-hero .intro{font-size:21px}
#ww-practice-v2 .collection-image{height:210px;margin-bottom:16px}
#ww-practice-v2 .learning-layout{grid-template-columns:1fr}
#ww-practice-v2 .learning-image{height:240px}
}
</style>'''
def image(name,cls,eager=False):
 return '<img class="'+cls+'" src="'+media+name+'" alt="" width="1600" height="900" '+('fetchpriority="high"' if eager else 'loading="lazy"')+' decoding="async">'
def illustrated_link(id,name):
 return link(id).replace('<article>','<article>'+image(name,'collection-image'),1)
hero='<header class="practice-hero" aria-labelledby="wwp-practice-title">'+image('golden_hour_office_collaboration_with_la_skyline.png','practice-hero-image',True)+'<div class="practice-hero-copy"><p class="eyebrow">From practice to progress</p><h1 id="wwp-practice-title">Practice <span>Decoded.</span></h1><p class="intro">A question on your desk. A decision to make. Find practical guidance, learn from other workforce boards, and build the knowledge behind the work.</p></div></header>'
body=home_style+hero+'<div class="practice-home-search">'+search+'</div><section id="wwp-practice-paths"><h2>Browse by the work you do</h2>'+tiles()+'</section><section id="wwp-desk-aids"><h2>Focused help for complex work</h2><div class="collection-grid">'+illustrated_link(7531,'practice-card-build-upscaled.png')+illustrated_link(7861,'practice-card-solve-upscaled.png')+'</div></section><section><h2>Learn the system. Strengthen your practice.</h2><p>New to workforce development? Start with Foundations. Ready to go deeper? Explore the decisions and tradeoffs in Workforce in Practice.</p><div class="learning-layout">'+image('practice-card-learn-upscaled.png','learning-image')+'<div class="learning-links">'+link(1210)+link(1427)+'</div></div></section><section id="wwp-deep-dives"><h2>Worth exploring</h2><div class="collection-grid">'+link(7594)+link(7584)+link(3851)+link(6546)+'</div><p><a href="/practice/tools/">Browse all resources →</a></p></section>'
(S/'templates/practice-editorial-v2.html').write_text(wrap(body).replace('class="ww-practice-library"','class="ww-practice-library practice-home"',1))
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
