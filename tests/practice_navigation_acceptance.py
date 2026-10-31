"""Exercise Practice search, filtering, URL state and narrow layouts against public source."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];S=R/'src/wordpress'
def run():
 data=json.loads((S/'javascript/practice-catalogue.json').read_text())
 assert len({x['url'] for x in data['resources']})==len(data['resources'])
 assert sum(x['type']=='Quickstart' for x in data['resources'])==32
 with sync_playwright() as pw:
  browser=pw.chromium.launch()
  for width in [1440,768,390,320]:
   page=browser.new_page(viewport={'width':width,'height':900})
   def serve(route):
    path=route.request.url.split('?')[0]
    name={'/practice/':'practice-editorial-v2.html','/practice/topics/':'practice-topic-library.html','/practice/quickstarts/':'practice-quickstarts.html'}.get(path.replace('https://workforcewonkery.com',''),'practice-resource-directory.html')
    if '/quickstarts/quickstart-' in path:
     name=None
    content=(S/'templates'/name).read_text() if name else '<h1>Approve a Training Request</h1><p>Detail page stand-in.</p>'
    body='<style>body{margin:0}</style><style>'+(S/'css/practice-navigation.css').read_text()+'</style><main><div class="wp-block-post-content">'+content+'</div></main><script type="application/json" id="ww-practice-catalogue">'+json.dumps(data)+'</script><script>'+(S/'javascript/practice-navigation.js').read_text()+'</script>'
    route.fulfill(content_type='text/html',body='<!doctype html><meta name="viewport" content="width=device-width">'+body)
   page.route('**/*',serve)
   page.goto('https://workforcewonkery.com/practice/tools/?q=HR1')
   assert page.locator('[data-resource-id]:visible').count()==1
   page.get_by_label('Search Practice',exact=True).fill('on the job training')
   assert page.locator('[data-resource-id]:visible').count()>0
   page.get_by_role('button',name='Clear filters').click()
   page.get_by_label('Topic',exact=True).select_option('training')
   page.get_by_label('Resource type',exact=True).select_option('Quickstart')
   assert page.locator('[data-resource-id]:visible').count()>=8
   page.get_by_label('Search Practice',exact=True).fill('zzzznothing')
   assert page.locator('[data-empty]:visible').count()==1
   page.get_by_role('button',name='Clear filters').click()
   assert page.locator('[data-resource-id]:visible').count()==len(data['resources'])
   # Natural-language questions put the right guidance first.
   for question,first in [('How do I determine whether someone qualifies for WIOA services?','Determine Dislocated Worker Eligibility'),
                          ('What should I consider before approving an Individual Training Account?','Approve a Training Request'),
                          ('How should my board prepare for changes to CalFresh work requirements?','H.R. 1 Work Requirements'),
                          ('What should an ETPL coordinator do when reviewing a training provider?','Review a New Training Provider')]:
    page.goto('https://workforcewonkery.com/practice/tools/?q='+question)
    assert page.locator('[data-resource-id]:visible h3').first.inner_text()==first,(question,page.locator('[data-resource-id]:visible h3').first.inner_text())
   # Practice home: hero proportions match Policy and Data, and each journey is one choice away.
   page.goto('https://workforcewonkery.com/practice/')
   box=page.locator('.practice-hero').bounding_box()
   if width>1000:
    assert abs(box['height']-width*0.1878)<=2,box
   else:
    assert page.evaluate("(()=>{const h=document.querySelector('.practice-hero');return h.scrollHeight<=h.clientHeight+1})()"),'hero copy clipped'
   assert page.locator('.practice-hero + .ww-practice-nav').count()==1
   urls={r['url'].replace('https://workforcewonkery.com',''):r for r in data['resources']}
   home_links=page.locator('#ww-practice-v2 a').evaluate_all('(els)=>els.filter(e=>!e.closest(".ww-practice-nav")).map(e=>e.getAttribute("href"))')
   for target in ['/practice/quickstarts/quickstart-determine-dislocated-worker-eligibility/','/practice/quickstarts/quickstart-review-new-training-provider/','/practice/etpl-coordinator/',
                  '/practice-insight-employer-engagement/','/practice/foundations/wioa/','/practice/employer-commitments/','/national-practice-ideas/','/workforce-board-examples/']:
    assert target in home_links,target
   for h in home_links:
    assert h.startswith(('/practice/','/trust/','/workforce-board-examples/','/national-practice-ideas/','/implementation-lessons/','/practice-insight-')),h
    if not h.startswith(('/practice/topics/','/practice/tools/','/practice/quickstarts/','/trust/','/practice/#')) and h!='/practice/quickstarts/':
     assert h in urls,h
   assert not page.evaluate('document.documentElement.scrollWidth > innerWidth')
   # Topic guides: start here, tasks, references, learning and ideas for one area of work.
   page.goto('https://workforcewonkery.com/practice/topics/?topic=training')
   assert page.locator('h1').inner_text()=='Training & ETPL'
   assert page.locator('[data-topic-guide="training"]:visible .tg-start a').inner_text()=='ETPL Coordinator Desk'
   assert page.locator('[data-topic-guide]:visible').count()==1 and page.locator('[data-topic-overview]:visible').count()==0
   assert page.locator('.ww-practice-nav ol').inner_text().replace('\n',' ').count('Training & ETPL')==1
   page.goto('https://workforcewonkery.com/practice/topics/')
   assert page.locator('[data-topic-overview] article').count()==6 and page.locator('[data-results]:visible').count()==0
   # Resource pages: breadcrumb to the work area and curated related resources.
   page.goto('https://workforcewonkery.com/practice/quickstarts/quickstart-approve-training-request/')
   assert 'Training & ETPL' in page.locator('.ww-practice-nav ol').inner_text()
   related=page.locator('.ww-practice-related .links a').all_inner_texts()
   assert related[0].startswith('Training + Career Pathways') and len(related)==4,related
   page.goto('https://workforcewonkery.com/practice/quickstarts/')
   assert page.locator('[data-resource-id]:visible').count()==32
   assert not page.evaluate('document.documentElement.scrollWidth > innerWidth')
   page.get_by_label('Search Practice',exact=True).focus()
   page.keyboard.press('Tab')
   assert page.locator('#practice-topic').evaluate('(el)=>el===document.activeElement')
   page.close()
  browser.close()
 print('PASS: Practice home hero and journeys, ranked search, aliases, topic guides, filters, empty/reset, breadcrumbs, related resources, Quickstarts, keyboard and four widths')
if __name__=='__main__': run()
