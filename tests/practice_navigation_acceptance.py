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
    name='practice-quickstarts.html' if path.endswith('/quickstarts/') else 'practice-resource-directory.html'
    body='<style>body{margin:0}</style><style>'+(S/'css/practice-navigation.css').read_text()+'</style><main><div class="wp-block-post-content">'+(S/'templates'/name).read_text()+'</div></main><script type="application/json" id="ww-practice-catalogue">'+json.dumps(data)+'</script><script>'+(S/'javascript/practice-navigation.js').read_text()+'</script>'
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
   page.goto('https://workforcewonkery.com/practice/quickstarts/')
   assert page.locator('[data-resource-id]:visible').count()==32
   assert not page.evaluate('document.documentElement.scrollWidth > innerWidth')
   page.get_by_label('Search Practice',exact=True).focus()
   page.keyboard.press('Tab')
   assert page.locator('#practice-topic').evaluate('(el)=>el===document.activeElement')
   page.close()
  browser.close()
 print('PASS: Practice search, aliases, topic/type filters, empty/reset, Quickstarts, keyboard and four widths')
if __name__=='__main__': run()
