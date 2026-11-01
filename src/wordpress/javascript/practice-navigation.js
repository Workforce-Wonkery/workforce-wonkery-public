// Retire the earlier header copy of this runtime, if a cached or unpublished header still carries it.
(function(){const old=document.getElementById('ww-practice-catalogue');if(old)old.remove();})();
document.addEventListener('DOMContentLoaded', function () {
 'use strict';
 const dataNode=document.getElementById('ww-practice-data');if(!dataNode)return;
 const data=JSON.parse(dataNode.textContent);
 const safe=u=>{try{const x=new URL(u);return x.protocol==='https:'&&x.hostname==='workforcewonkery.com';}catch(e){return false;}};
 data.resources=data.resources.filter(r=>safe(r.url));
 const byId=new Map(data.resources.map(r=>[r.id,r]));
 const topicOf=id=>data.topics.find(t=>t.id===id);
 const typeLabel=t=>((data.types||[]).find(x=>x.id===t)||{label:t}).label;
 const slash=p=>p.replace(/\/?$/,'/');
 const pathOf=u=>slash(new URL(u).pathname);
 const path=slash(location.pathname);
 const current=data.resources.find(r=>pathOf(r.url)===path);
 if(!path.startsWith('/practice/')&&!current)return;
 const main=document.querySelector('.wp-block-post-content')||document.querySelector('main');if(!main)return;
 const make=(tag,attrs,...kids)=>{const n=document.createElement(tag);Object.entries(attrs||{}).forEach(([k,v])=>{if(v!=null)n.setAttribute(k,v);});kids.forEach(k=>{if(k!=null)n.append(k);});return n;};
 const link=(text,url)=>make('a',{href:url},text);
 const params=new URLSearchParams(location.search);
 const ALL=data.topics.length;
 const LEARN=['Learning','/practice/tools/?type=Course'],IDEAS=['Ideas worth borrowing','/practice/#ideas'];
 const topicCrumb=t=>[t.title,'/practice/topics/?topic='+encodeURIComponent(t.id)];
 // The section a resource belongs to: its desk or course when the URL says so, otherwise its first work area.
 function parents(r){
  const p=pathOf(r.url),under=(prefix,id)=>p.startsWith(prefix)&&r.id!==id&&byId.get(id);
  if(under('/practice/etpl-coordinator/',7531))return[topicCrumb(topicOf('training')),[byId.get(7531).title,'/practice/etpl-coordinator/']];
  if(under('/practice/foundations/',1210))return r.type==='Course'?[LEARN,['Foundations Course','/practice/foundations/']]:[topicCrumb(topicOf(r.topics[0])),['Foundations Course','/practice/foundations/']];
  if(under('/practice/workforce-in-practice/',1427))return[LEARN,['Workforce in Practice','/practice/workforce-in-practice/']];
  if(r.type==='Course'&&r.topics.length===ALL)return[LEARN];
  if((r.type==='Example'||r.type==='Research')&&r.topics.length===ALL)return[IDEAS];
  return[topicCrumb(topicOf(r.topics[0]))];
 }
 // One navigation row: breadcrumb on the left, the Practice sections on the right.
 const hubNode=document.querySelector('[data-practice-directory]'),hub=hubNode&&hubNode.querySelector('[data-results]')?hubNode:null;
 const nav=make('nav',{class:'ww-practice-nav','aria-label':'Practice'});
 let trail=null;
 if(current&&!hub){trail=[['Practice','/practice/'],...parents(current),[current.title]];}
 else if(hub){const kind=hub.dataset.page,t=topicOf(params.get('topic')||'');trail=[['Practice','/practice/']];
  if(kind==='topics'){trail.push(t?['Topics','/practice/topics/']:['Topics']);if(t)trail.push([t.title]);}
  else trail.push([kind==='quickstarts'?'Quickstarts':'All resources']);}
 if(trail){const ol=make('ol',{'aria-label':'Breadcrumb'});trail.forEach(([text,url],i)=>{ol.append(make('li',i===trail.length-1&&!url?{'aria-current':'page'}:{},url?link(text,url):text));});nav.append(ol);}
 const ul=make('ul');
 [['Practice home','/practice/'],['Topics','/practice/topics/'],['Quickstarts','/practice/quickstarts/'],['Learning','/practice/tools/?type=Course'],['All resources','/practice/tools/']].forEach(([text,url],i)=>{const a=link(text,url);const here=url.includes('?')?location.pathname+location.search===url:path===url&&!(url==='/practice/tools/'&&params.get('type')==='Course');if(here)a.setAttribute('aria-current','page');ul.append(make('li',i===0?{class:'home'}:{},a));});
 nav.append(ul);
 const hero=document.querySelector('#ww-practice-v2 .practice-hero');
 if(hero)hero.after(nav);else main.prepend(nav);

 // ---------- Ranked search: plain words, acronyms and common synonyms, best matches first.
 const normalize=s=>' '+String(s).toLowerCase().replace(/&/g,' and ').replace(/[^a-z0-9]+/g,' ').trim()+' ';
 const STOP=new Set('a an and are as at be been before being can could do does doing for from get has have help how i if in into is it its me my need of on or our should so someone something that the their them there this to us we what when where whether which who why will with would you your up am im ive dont lets get got also just any some'.split(' '));
 const SYN=[['eligibility','eligible','qualify','qualifies','qualified','qualifying'],['ita','individual training account','tuition'],['etpl','eligible training provider'],['employer','employers','business','businesses'],['ojt','on the job training'],['iwt','incumbent worker'],['ajcc','one stop','job center','americas job center'],['calfresh','snap','abawd'],['layoff','layoffs','laid off','closure','rapid response'],['monitoring','audit','finding','findings'],['performance','outcomes','results','measures'],['wdb','workforce development board'],['youth','young adult','young adults'],['new to workforce','new to the field','beginner','onboarding','introduction'],['mou','memorandum of understanding'],['ifa','infrastructure funding'],['supportive','support service','supportive services'],['apprenticeship','apprentice','apprentices'],['procure','procurement','rfp']];
 const WEAK=new Set(['service','services','wioa','workforce','program','programs','staff','work','works','working','process','local','california','development']);
 const stem=w=>{const s=w.replace(/(ies|ing|ed|es|s)$/,'');return s.length>=4?s:w;};
 function terms(q){let s=normalize(q);const out=[];
  SYN.forEach(g=>{const hit=g.filter(x=>x.includes(' ')).find(x=>s.includes(' '+x+' '));if(hit){out.push(g);s=s.replace(' '+hit+' ',' ');}});
  let words=s.trim().split(/\s+/).filter(w=>w&&!STOP.has(w));if(out.length||words.some(w=>!WEAK.has(w)))words=words.filter(w=>!WEAK.has(w));
  words.forEach(w=>{const g=SYN.find(g=>g.includes(w)||g.includes(stem(w)));out.push(g?g.concat([stem(w)]):[w,stem(w)]);});
  return out;}
 const fields=r=>[[normalize(r.title),3],[normalize(r.aliases.join(' ')),2],[normalize(r.summary),1.5],[normalize(r.topics.map(t=>topicOf(t).title).join(' ')+' '+typeLabel(r.type)+' '+r.type),.5]];
 const index=new Map(data.resources.map(r=>[r.id,fields(r)]));
 const matchWeight=(f,variants)=>f.reduce((m,[text,w])=>variants.some(v=>text.includes(' '+v))?Math.max(m,w):m,0);
 function rank(q){const ts=terms(q);if(!ts.length)return null;
  const n=data.resources.length,scores=new Map();
  const idf=ts.map(v=>{const df=data.resources.filter(r=>matchWeight(index.get(r.id),v)>0).length;return df?Math.log(1+n/df):0;});
  data.resources.forEach(r=>{let s=0,hits=0;ts.forEach((v,i)=>{const w=matchWeight(index.get(r.id),v);if(w){s+=w*idf[i];hits++;}});scores.set(r.id,{s,hits});});
  let need=Math.max(1,Math.ceil(ts.length/2));
  if(![...scores.values()].some(x=>x.hits>=need))need=1;
  return {need,scores};}

 // ---------- Hub pages: search, filters, topic guides and URL state.
 if(hub){
  const form=hub.querySelector('form'),q=form.elements.q,topic=form.elements.topic,type=form.elements.type;
  const kind=hub.dataset.page,list=hub.querySelector('[data-results]');
  // The list and topic guides are rendered from the one shared catalogue.
  data.resources.forEach(r=>list.append(make('article',{class:'resource','data-resource-id':String(r.id)},
   make('p',{class:'meta'},make('span',{class:'tag'},typeLabel(r.type)),' '+(ALL>r.topics.length?r.topics.map(t=>topicOf(t).title).join(' · '):'All topics')),
   make('h3',{},link(r.title,r.url)),make('p',{},r.summary))));
  const guides=hub.querySelector('[data-topic-guides]');
  if(guides)data.topics.forEach(t=>{const st=byId.get(t.start);if(!st)return;
   const ulOf=(ids,cls)=>{const ul=make('ul',{class:'links'+(cls?' '+cls:'')});ids.map(i=>byId.get(i)).filter(Boolean).forEach(r=>ul.append(make('li',{},make('span',{class:'tag'},typeLabel(r.type)),link(r.title,new URL(r.url).pathname),make('span',{class:'sum'},r.summary))));return ul;};
   const col=(title,note,ids)=>ids.length?make('div',{},make('h3',{},title),make('p',{class:'note'},note),ulOf(ids)):null;
   guides.append(make('section',{class:'topic-guide','data-topic-guide':t.id,'aria-label':t.title+' guide',hidden:''},
    make('div',{class:'tg-start'},make('p',{class:'tag'},'Start here · '+typeLabel(st.type)),make('h2',{},link(st.title,new URL(st.url).pathname)),make('p',{},st.summary)),
    make('div',{class:'tg-cols'},col('Get a task done','Step-by-step help with a specific decision.',t.tasks.filter(i=>i!==t.start)),col('Keep at hand','References and tools to keep open while you work.',t.keep),col('Build your knowledge','Lessons that explain the system behind the task.',t.learn)),
    make('div',{class:'tg-ideas'},make('h3',{},'Ideas worth borrowing'),ulOf(t.ideas,'cols'))));});
  const items=Array.from(hub.querySelectorAll('[data-resource-id]'));const original=items.slice();
  const title=hub.querySelector('[data-hub-title]'),intro=hub.querySelector('[data-hub-intro]');
  const baseTitle=title&&title.textContent,baseIntro=intro&&intro.textContent,baseDoc=document.title;
  function restore(){const p=new URLSearchParams(location.search);q.value=p.get('q')||'';topic.value=topicOf(p.get('topic')||'')?p.get('topic'):'';const ty=p.get('type');type.value=(data.types||[]).some(t=>t.id===ty)?ty:(ty===null?hub.dataset.defaultType||'':'');}
  restore();
  function render(update){
   const ranked=rank(q.value);let n=0;
   const shown=original.filter(el=>{const r=byId.get(Number(el.dataset.resourceId));if(!r){el.hidden=true;return false;}
    const sc=ranked&&ranked.scores.get(r.id);
    const show=(!topic.value||r.topics.includes(topic.value))&&(!type.value||r.type===type.value)&&(!ranked||sc.hits>=ranked.need);
    el.hidden=!show;if(show)n++;return show;});
   if(ranked)shown.slice().sort((a,b)=>ranked.scores.get(Number(b.dataset.resourceId)).s-ranked.scores.get(Number(a.dataset.resourceId)).s).forEach(el=>list.append(el));
   else original.forEach(el=>list.append(el));
   const t=topicOf(topic.value);
   if(kind==='topics'){
    const browsing=!t&&!q.value&&!type.value;
    hub.querySelectorAll('[data-topic-guide]').forEach(g=>{g.hidden=!t||g.dataset.topicGuide!==t.id;});
    const ov=hub.querySelector('[data-topic-overview]');if(ov)ov.hidden=!!t;
    list.hidden=browsing;
    if(title)title.textContent=t?t.title:baseTitle;if(intro)intro.textContent=t?t.intro:baseIntro;
    document.title=t?t.title+' · Practice topics · Workforce Wonkery':baseDoc;
    const rt=hub.querySelector('[data-results-title]');if(rt)rt.textContent=t?'Everything on '+t.title:'Search all topics';
    hub.querySelector('[role=status]').textContent=browsing?'Choose a topic above, or search across all '+data.resources.length+' resources.':n+' resource'+(n===1?'':'s')+(ranked?', best matches first':'');
   }else hub.querySelector('[role=status]').textContent=n+' resource'+(n===1?'':'s')+(ranked?' found, best matches first':'');
   hub.querySelector('[data-empty]').hidden=n>0;
   if(update){const p=new URLSearchParams();if(q.value)p.set('q',q.value);if(topic.value)p.set('topic',topic.value);if(type.value&&type.value!==(hub.dataset.defaultType||''))p.set('type',type.value);else if(!type.value&&hub.dataset.defaultType)p.set('type','');history.replaceState(null,'',location.pathname+(p.size?'?'+p:''));}
  }
  form.addEventListener('submit',e=>{e.preventDefault();render(true);});
  q.addEventListener('input',()=>render(true));[topic,type].forEach(e=>e.addEventListener('change',()=>render(true)));
  hub.querySelector('[data-reset]').addEventListener('click',()=>{q.value='';topic.value='';type.value='';render(true);q.focus();});
  window.addEventListener('popstate',()=>{restore();render(false);});
  render(false);
 }

 // ---------- Resource pages: genuinely related next steps, then a way back to the collection.
 if(current&&!hub){
  const home=parents(current)[0];
  const words=r=>new Set(normalize(r.title+' '+r.aliases.join(' ')).trim().split(' ').filter(w=>w.length>3&&!STOP.has(w)).map(stem));
  const mine=words(current);
  const curated=(current.related||[]).map(id=>byId.get(id)).filter(Boolean);
  const scored=data.resources.filter(r=>r.id!==current.id&&!curated.includes(r)&&ALL>r.topics.length&&r.topics.some(t=>current.topics.includes(t)))
   .map((r,i)=>{const w=words(r);let shared=0;w.forEach(x=>{if(mine.has(x))shared++;});return{r,i,s:shared*2+r.topics.filter(t=>current.topics.includes(t)).length+(r.type!==current.type?1:0)+(r.topics[0]===current.topics[0]?1:0)};})
   .sort((a,b)=>b.s-a.s||a.i-b.i).map(x=>x.r);
  const picks=curated.concat(scored).slice(0,4);
  if(picks.length){
   const aside=make('aside',{class:'ww-practice-library ww-practice-related','aria-labelledby':'ww-practice-related-title'});
   aside.append(make('p',{class:'eyebrow'},'Keep going'),make('h2',{id:'ww-practice-related-title'},'Related resources'));
   const ul=make('ul',{class:'links'});
   picks.forEach(r=>ul.append(make('li',{},make('span',{class:'tag'},typeLabel(r.type)),link(r.title,new URL(r.url).pathname),make('span',{class:'sum'},r.summary))));
   aside.append(ul);
   if(home&&home[1])aside.append(make('p',{class:'more'},link('Back to '+home[0]+' →',home[1])));
   main.append(aside);
  }
 }
});
