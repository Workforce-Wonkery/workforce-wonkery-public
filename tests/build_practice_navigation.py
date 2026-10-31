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
# The hero reuses the owner-approved Practice photo at its native 2172x724 size, aligned with the Policy and Data heroes.
# Supporting card images were removed: they were ~410px mockup crops upscaled 4x and rendered blurry.
media='https://workforcewonkery.com/wp-content/uploads/2026/09/'
home_style='''<style>
#ww-practice-v2.practice-home{padding-top:0;margin-top:0}
#ww-practice-v2 .practice-hero{position:relative;isolation:isolate;min-height:18.78vw;display:flex;align-items:center;margin:0 calc(-1 * max(24px, (100vw - 1200px)/2));padding:clamp(26px,2.4vw,44px) max(24px,calc((100vw - 1200px)/2));overflow:hidden;background:#fcfaf6;border-bottom:1px solid #eee9de}
#ww-practice-v2 .practice-hero-image{position:absolute;z-index:-2;right:0;top:0;width:63%;max-width:none;height:100%;object-fit:cover;object-position:center 38%}
#ww-practice-v2 .practice-hero:after{content:"";position:absolute;inset:0;z-index:-1;pointer-events:none;background:linear-gradient(90deg,#fcfaf6 0%,#fcfaf6 31%,rgba(252,250,246,.98) 38%,rgba(252,250,246,.84) 45%,rgba(252,250,246,.42) 53%,rgba(252,250,246,0) 65%)}
#ww-practice-v2 .practice-hero-copy{width:50%;max-width:620px}
#ww-practice-v2 .practice-hero .eyebrow{display:block;color:#986714;font:600 clamp(11px,.72vw,15px)/1.5 Arial,Helvetica,sans-serif;letter-spacing:.16em;text-transform:uppercase;margin:0 0 clamp(12px,1.1vw,20px)}
#ww-practice-v2 .practice-hero h1{font-size:clamp(56px,5.1vw,94px)!important;line-height:.98!important;letter-spacing:-.052em!important;margin:0 0 clamp(16px,1.4vw,26px)!important;white-space:nowrap}
#ww-practice-v2 .practice-hero .intro{font:clamp(19px,1.45vw,28px)/1.42 Georgia,'Times New Roman',serif;color:#1d3546;max-width:30em;margin:0;text-wrap:pretty}
#ww-practice-v2 .practice-home-search{padding-top:8px}
@media(max-width:1000px){
#ww-practice-v2 .practice-hero-copy{width:55%}
#ww-practice-v2 .practice-hero:after{background:linear-gradient(90deg,#fcfaf6 0%,#fcfaf6 39%,rgba(252,250,246,.94) 45%,rgba(252,250,246,.7) 52%,rgba(252,250,246,.3) 60%,rgba(252,250,246,0) 70%)}
#ww-practice-v2 .practice-hero h1{white-space:normal}
}
@media(max-width:900px){
#ww-practice-v2 .practice-hero{min-height:0;display:block;padding:0 24px 24px;border-bottom:0}
#ww-practice-v2 .practice-hero-image{position:relative;display:block;width:calc(100% + 48px);height:220px;margin:0 -24px 26px;object-position:center 35%}
#ww-practice-v2 .practice-hero:after{display:none}
#ww-practice-v2 .practice-hero-copy{width:100%;max-width:none}
#ww-practice-v2 .practice-hero .eyebrow{font-size:11px;margin-bottom:9px}
#ww-practice-v2 .practice-hero h1{font-size:44px!important;line-height:1.03!important;margin-bottom:12px!important}
#ww-practice-v2 .practice-hero .intro{font-size:19px}
}
@media(max-width:640px){
#ww-practice-v2 .practice-hero{margin:0 -20px;padding:0 20px 20px}
#ww-practice-v2 .practice-hero-image{width:calc(100% + 40px);margin:0 -20px 22px}
}
</style>'''
def image(name,cls,width,height,eager=False):
 return '<img class="'+cls+'" src="'+media+name+'" alt="" width="'+str(width)+'" height="'+str(height)+'" '+('fetchpriority="high"' if eager else 'loading="lazy"')+' decoding="async">'
hero='<header class="practice-hero" aria-labelledby="wwp-practice-title">'+image('golden_hour_office_collaboration_with_la_skyline.png','practice-hero-image',2172,724,True)+'<div class="practice-hero-copy"><p class="eyebrow">From practice to progress</p><h1 id="wwp-practice-title">Practice <span>Decoded.</span></h1><p class="intro">A question on your desk. A decision to make. Find practical guidance, learn from other workforce boards, and build the knowledge behind the work.</p></div></header>'
body=home_style+hero+'<div class="practice-home-search">'+search+'</div><section id="wwp-practice-paths"><h2>Browse by the work you do</h2>'+tiles()+'</section><section id="wwp-desk-aids"><h2>Focused help for complex work</h2><div class="collection-grid">'+link(7531)+link(7861)+'</div></section><section><h2>Learn the system. Strengthen your practice.</h2><p>New to workforce development? Start with Foundations. Ready to go deeper? Explore the decisions and tradeoffs in Workforce in Practice.</p><div class="collection-grid">'+link(1210)+link(1427)+'</div></section><section id="wwp-deep-dives"><h2>Worth exploring</h2><div class="collection-grid">'+link(7594)+link(7584)+link(3851)+link(6546)+'</div><p><a href="/practice/tools/">Browse all resources →</a></p></section>'
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
