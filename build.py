#!/usr/bin/env python3
"""Tree向け 渋谷散歩コース選択ページ（10/8-20）。 python3 build.py -> index.html"""
import json, html

# 写真は「ワクワク採点」で選ぶ。建物の外観でなく、そこで人が楽しんでいる絵を最優先。
# 採点と選定理由は photos.json の score / note を見る。
PH = json.load(open('photos.json'))
gm = lambda q: 'https://www.google.com/maps/search/?api=1&query=' + q.replace(' ', '+')
emb = lambda q: 'https://maps.google.com/maps?q=' + q.replace(' ', '+') + '&output=embed&z=12'
def route_emb(stops):
    s = [x.replace(' ', '+') for x in stops]
    return 'https://maps.google.com/maps?saddr=' + s[0] + '&daddr=' + '+to:'.join(s[1:]) + '&output=embed'
def route_link(stops):
    s = [x.replace(' ', '+') for x in stops]
    return ('https://www.google.com/maps/dir/?api=1&origin=' + s[0] + '&destination=' + s[-1]
            + ('&waypoints=' + '%7C'.join(s[1:-1]) if len(s) > 2 else '') + '&travelmode=transit')

COURSES = [
 dict(id='A', chips=['No tickets','Games and shops','Ends at a shrine'], name='Shibuya & Harajuku', tag='The walk your clients ask for',
  why='The crossing, the rooftop park, the Nintendo and Pokémon shops, then a back street to Harajuku and a forest walk at the end. You see it the way a guest would.',
  steps=[('11:00','Hachiko statue, Shibuya station','We meet at the dog.'),
         ('11:10','Scramble crossing','Cross it once, then watch it from the rooftop of MAGNET by SHIBUYA109 across the street.'),
         ('11:40','Miyashita Park','A park on the roof of a mall. Skate park, climbing wall, and Shibuya Yokocho food alley underneath.'),
         ('12:15','Shibuya PARCO, 6th floor','Nintendo TOKYO, Pokémon Center Shibuya, CAPCOM Store and the Jump Shop on one floor.'),
         ('13:15','Lunch','See the three picks below.'),
         ('14:00','Cat Street to Harajuku','A 15-minute walk on a quiet street of small shops.'),
         ('14:30','Takeshita street','The crowded one. Crepes, character shops, photo booths.'),
         ('15:00','Meiji Jingu','Forest walk to the shrine and back. We finish at Harajuku station around 15:45.')],
  stops=['Hachiko Statue Shibuya','Shibuya Scramble Crossing','Miyashita Park Shibuya','Shibuya PARCO','Cat Street Harajuku','Takeshita Street Harajuku','Meiji Jingu Shrine'],
  moves='Everything on foot. Shibuya station → PARCO 10 min. PARCO → Harajuku 15 min. Harajuku station has the JR Yamanote line back.',
  food=[('Uobei Shibuya Dogenzaka','Shibuya · conveyor sushi','Order on a tablet, plates arrive on a rail. About 15 minutes, 1,500 yen.','Uobei Shibuya Dogenzaka'),
        ('AFURI Harajuku','Harajuku · yuzu ramen','Light ramen with yuzu citrus. Counter seats, quick.','AFURI Harajuku'),
        ('Marion Crepes','Takeshita street · crepes','The original Harajuku crepe stand. Eaten while walking.','Marion Crepes Takeshita Street Harajuku')],
  good='No tickets. Easy to cut short. This is the standard Shibuya day, so it is useful to have walked it yourself.',
  mind='Takeshita street is crowded after noon on Saturday. The PARCO shops are busy but the queues move.',
  links=[('Nintendo TOKYO','https://www.nintendo.com/jp/officialstore/'),('Pokémon Center Shibuya','https://www.pokemon.co.jp/shop/pokecen/shibuya/'),('Meiji Jingu (official)','https://www.meijijingu.or.jp/en/')]),
 dict(id='B', chips=['Rooftop view','4 minutes by train','Vintage and curry'], name='Shibuya & Shimokitazawa', tag='The view, then the small-town side',
  why='Shibuya from 230 metres up, then one short train ride to Shimokitazawa, where Tokyo people go on weekends. Vintage shops, small theatres, curry.',
  steps=[('11:00','Hachiko statue, Shibuya station','We meet at the dog.'),
         ('11:15','Shibuya Sky','Open rooftop on top of Scramble Square. About 45 minutes. I book the timed ticket.'),
         ('12:15','Scramble crossing and Shibuya Stream','Cross at street level, then a short walk along the river side of the station.'),
         ('12:45','Keio Inokashira line to Shimokitazawa','Two stops, 4 minutes.'),
         ('13:00','Lunch','Curry is the local dish here. See the picks below.'),
         ('14:00','Shimokitazawa streets','Vintage shops, record shops and Bonus Track, a row of small shops on the old rail line.'),
         ('15:00','Coffee, and done','We finish at Shimokitazawa station. Shibuya is 4 minutes, Shinjuku 10.')],
  stops=['Hachiko Statue Shibuya','Shibuya Sky','Shibuya Stream','Shimokitazawa Station','Bonus Track Shimokitazawa'],
  moves='Shibuya on foot. Shibuya → Shimokitazawa 4 min on the Keio Inokashira line. Shimokitazawa → Shibuya or Shinjuku 4 to 10 min.',
  food=[('Rojiura Curry SAMURAI','Shimokitazawa · soup curry','Hokkaido-style soup curry with a plate of vegetables. The Shimokita branch is the busy one.','Rojiura Curry Samurai Shimokitazawa'),
        ('Curry Spice Gelateria KALPASI','Shimokitazawa · spice curry','Small counter, two or three curries on one plate, gelato after.','Curry Spice Gelateria KALPASI'),
        ('Bear Pond Espresso','Shimokitazawa · coffee','Tiny espresso bar, known in Tokyo. Cash only, no photos inside.','Bear Pond Espresso Shimokitazawa')],
  good='Two different sides of Tokyo in one afternoon. Best if you want to see where locals shop and eat.',
  mind='Shibuya Sky needs a timed ticket, about 2,500 yen, booked online. Windy on the roof.',
  links=[('Shibuya Sky (official)','https://www.shibuya-scramble-square.com/sky/'),('Bonus Track','https://bonus-track.jp/'),('Keio Inokashira line','https://www.keio.co.jp/english/')]),
 dict(id='C', chips=['All on foot','Quiet side streets','Books and coffee'], name='Shibuya, Daikanyama & Nakameguro', tag='Downhill to the river',
  why='Start in the noise, then walk 20 minutes downhill into the quiet part: the Daikanyama bookshop, then the Meguro river and its cafés. Easy pace, good for talking.',
  steps=[('13:00','Hachiko statue, Shibuya station','We meet at the dog.'),
         ('13:15','Scramble crossing and Shibuya Stream','Cross once, then follow the river side of the station.'),
         ('13:45','Walk to Daikanyama','20 minutes, mostly downhill, through a residential area.'),
         ('14:10','Daikanyama T-Site and Log Road','Tsutaya Books, three buildings of books and a lounge. Log Road is a garden path on an old rail line with a brewery.'),
         ('15:00','Late lunch or coffee','See the picks below. Ivy Place serves food all afternoon.'),
         ('15:50','Walk to Nakameguro','15 minutes.'),
         ('16:05','Meguro river','The cherry-tree street. Small shops and cafés on both banks.'),
         ('16:45','Starbucks Reserve Roastery, and done','The big four-floor one by the river. We finish at Nakameguro station around 17:15.')],
  stops=['Hachiko Statue Shibuya','Shibuya Stream','Daikanyama T-Site','Log Road Daikanyama','Nakameguro Station','Starbucks Reserve Roastery Tokyo'],
  moves='Everything on foot, about 4 km in total. Shibuya → Daikanyama 20 min. Daikanyama → Nakameguro 15 min. Nakameguro station has the Hibiya and Toyoko lines.',
  food=[('Ivy Place','Daikanyama · brunch','Pancakes, salads and pasta in the T-Site garden. Weekend queue, so we put our name down first.','Ivy Place Daikanyama'),
        ('Spring Valley Brewery Tokyo','Daikanyama · craft beer','Kirin’s brewery restaurant on Log Road. Beer flight and a proper lunch.','Spring Valley Brewery Tokyo Daikanyama'),
        ('Onibus Coffee Nakameguro','Nakameguro · coffee','Small roaster next to the tracks. Standing room, good beans.','Onibus Coffee Nakameguro')],
  good='The least crowded option. Flat and easy. Good if you want time to talk business.',
  mind='The Meguro river cherry trees are green in October, not pink. Ivy Place can be a 30-minute wait on Saturday.',
  links=[('Daikanyama T-Site','https://store.tsite.jp/daikanyama/english/'),('Log Road Daikanyama','https://www.logroad-daikanyama.jp/'),('Starbucks Reserve Roastery Tokyo','https://www.starbucks.co.jp/reserve/roastery/')]),
]

def menu(c):
    x = PH[c['id']]['card']
    ch = ''.join(f'<li>{html.escape(t)}</li>' for t in c['chips'])
    return f'''<button class="mcard" type="button" data-course="{c['id']}" aria-expanded="false" aria-controls="detail-{c['id']}">
<img src="{x["thumb"]}" alt="{html.escape(x["title"])}" loading="lazy">
<span class="mb"><span class="mk">Course {c['id']}</span><span class="mt">{html.escape(c['name'])}</span>
<span class="mtag">{html.escape(c['tag'])}</span><ul class="mch">{ch}</ul><span class="mopen">See the plan</span></span></button>'''

def detail(c):
    ph = ''.join(f'<img src="{x["thumb"]}" alt="{html.escape(x["title"])}" loading="lazy">' for x in PH[c['id']]['detail'])
    st = ''.join(f'<li><b>{t}</b><div><strong>{h}</strong><span>{d}</span></div></li>' for t, h, d in c['steps'])
    fd = ''.join(f'<a class="eat" href="{gm(q)}" target="_blank" rel="noopener">'
                 f'<img src="{im["thumb"]}" alt="{html.escape(im["title"])}" loading="lazy">'
                 f'<span class="eb"><strong>{n}</strong><em>{a}</em><span>{d}</span>'
                 f'<i>Open in Google Maps ↗</i></span></a>'
                 for (n, a, d, q), im in zip(c['food'], PH[c['id']]['food']))
    ln = ' '.join(f'<a href="{u}" target="_blank" rel="noopener">{html.escape(t)} ↗</a>' for t, u in c['links'])
    sub = f'Shibuya walk: course {c["id"]} ({c["name"]})'
    return f'''<section class="detail" id="detail-{c['id']}" hidden><div class="dwrap"><div class="dtop"></div>
<div class="dhead"><div><p class="kicker">Course {c['id']} · {html.escape(c['tag'])}</p><h2>{html.escape(c['name'])}</h2></div>
<button class="dclose" type="button" aria-label="Close">Close ✕</button></div>
<p class="why">{html.escape(c['why'])}</p>
<div class="photos">{ph}</div>
<div class="dgrid">
<div><h3>The day</h3><ol class="steps">{st}</ol></div>
<div><h3>The route</h3><div class="mapbox"><iframe src="{route_emb(c['stops'])}" loading="lazy" title="Route for course {c['id']}" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
<p class="moves">{c['moves']} <a href="{route_link(c['stops'])}" target="_blank" rel="noopener">Open the route in Google Maps ↗</a></p></div>
</div>
<h3>Where we eat</h3><div class="eats">{fd}</div>
<div class="notes"><p><b>Good for</b> {html.escape(c['good'])}</p><p><b>Keep in mind</b> {html.escape(c['mind'])}</p></div>
<p class="links">{ln}</p>
<a class="choose" href="mailto:icchan417@gmail.com?subject={html.escape(sub)}">Choose course {c['id']}</a>
</div></section>'''

HERO_CSS = """
.hpic{position:relative;background:#111;color:#fff}
.slides{position:absolute;inset:0;overflow:hidden}
.slides img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transform:scale(1.06);transition:opacity 1.1s ease,transform 5s linear}
.slides img.on{opacity:1;transform:scale(1)}
.slides:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.08) 30%,rgba(0,0,0,.74))}
.hcap{position:relative;z-index:1;min-height:62vh;max-height:600px;display:flex;flex-direction:column;justify-content:flex-end;padding-top:48px;padding-bottom:22px}
.hcap .kicker{color:#9ee3b8}
.fixed{position:relative;z-index:1;display:inline-block;align-self:flex-start;font-size:13.5px;font-weight:600;color:#fff;background:rgba(0,0,0,.42);border:1px solid rgba(255,255,255,.45);border-radius:999px;padding:8px 15px;margin:0 0 14px;backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px)}
.hcap h1{color:#fff;margin:0 0 14px;text-shadow:0 2px 14px rgba(0,0,0,.3)}
.snav{display:flex;align-items:center;gap:10px}
.slabel{font:inherit;font-size:12.5px;font-weight:600;color:#fff;background:rgba(0,0,0,.38);border:1px solid rgba(255,255,255,.4);border-radius:999px;padding:7px 13px;cursor:pointer;backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);max-width:100%;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.dots{display:flex;gap:7px;margin-left:auto;flex:none}
.dots button{width:9px;height:9px;padding:0;border:none;border-radius:50%;background:rgba(255,255,255,.45);cursor:pointer}
.dots button.on{background:#fff}
.hbody{padding-top:22px;padding-bottom:26px}
@media(prefers-reduced-motion:reduce){.slides img{transition:none;transform:none}}
"""
HERO_JS = """
 (function(){
  var sl=[].slice.call(document.querySelectorAll('.slides img')),dots=[].slice.call(document.querySelectorAll('.dots button')),lab=document.querySelector('.slabel'),i=0,t;
  function show(n){i=n;sl.forEach(function(x,k){x.classList.toggle('on',k===n)});dots.forEach(function(x,k){x.classList.toggle('on',k===n)});
   lab.textContent='Course '+sl[n].dataset.course+' · '+sl[n].dataset.name;lab.dataset.course=sl[n].dataset.course}
  function go(){clearInterval(t);if(!matchMedia('(prefers-reduced-motion: reduce)').matches)t=setInterval(function(){show((i+1)%sl.length)},4000)}
  dots.forEach(function(d,k){d.addEventListener('click',function(){show(k);go()})});
  lab.addEventListener('click',function(){document.querySelector('.mcard[data-course="'+lab.dataset.course+'"]').click()});
  show(0);go();
 })();
"""

credits = '; '.join(html.escape(x['title'].replace('File:','')) + ' (' + x['lic'] + ')' for v in PH.values() for x in [v['card']] + v['detail'] + v['food'])
page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Shibuya, three ways: a walk with Yuuki</title><meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{{--bg:#fffdf6;--card:#fff;--ink:#111;--mute:#767065;--line:#eae4d6;--acc:#1a5c3a;--r:10px}}
*{{box-sizing:border-box;min-width:0}} html,body{{overflow-x:hidden;max-width:100%}} img{{max-width:100%}}
body{{margin:0;font-family:Inter,-apple-system,"Hiragino Sans",sans-serif;color:var(--ink);background:var(--bg);line-height:1.6}}
.wrap{{max-width:1080px;margin:0 auto;padding:0 20px}}
.kicker{{font-size:12px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--acc);margin:0 0 10px}}
h1,h2,.mt{{text-wrap:balance}} .nb{{white-space:nowrap}}
h1{{font-weight:800;font-size:clamp(34px,5.4vw,54px);line-height:1.06;letter-spacing:-.025em;margin:0 0 16px}}
h2{{font-weight:800;font-size:clamp(30px,4.2vw,42px);line-height:1.06;letter-spacing:-.025em;margin:0}}
h3{{font-size:12px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--acc);margin:0 0 12px}}
{HERO_CSS}
header p{{font-size:18px;color:var(--mute);margin:0;max-width:620px}}
.facts{{display:flex;flex-wrap:wrap;gap:6px 20px;margin:20px 0 0;padding:0;list-style:none;font-size:14px;color:var(--mute)}} .facts b{{color:var(--ink);font-weight:600}}
.sechead{{display:flex;align-items:baseline;gap:14px;padding:26px 0 16px;border-top:1px solid var(--line)}}
.sechead .n{{font-weight:800;font-size:26px;line-height:1;letter-spacing:-.02em;color:var(--acc)}}
.sechead b{{font-size:19px;font-weight:600}} .sechead span{{font-size:14px;color:var(--mute)}}
.menu{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}}
.mcard{{display:flex;flex-direction:column;text-align:left;font:inherit;color:inherit;background:var(--card);border:1px solid var(--line);border-radius:var(--r);overflow:hidden;padding:0;cursor:pointer;transition:transform .18s,box-shadow .18s,border-color .18s}}
.mcard:hover{{transform:translateY(-3px);box-shadow:0 10px 24px rgba(34,31,27,.10)}}
.menu.picked .mcard:not([aria-expanded=true]){{opacity:.42;filter:saturate(.45)}}
.menu.picked .mcard:not([aria-expanded=true]):hover{{opacity:.75;filter:none}}
.mcard[aria-expanded=true]{{border:2px solid var(--ink);box-shadow:0 12px 28px rgba(17,17,17,.16);transform:translateY(-3px)}}
.mcard[aria-expanded=true] .mopen{{color:var(--acc);border-bottom-color:var(--acc)}}
.mcard>img{{display:block;width:100%;aspect-ratio:4/3;object-fit:cover;background:#f0ebe0}}
.mb{{display:flex;flex-direction:column;flex:1;padding:18px 20px 20px}}
.mk{{display:block;font-size:12px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--acc);margin-bottom:6px}}
.mt{{display:block;font-weight:800;font-size:26px;line-height:1.12;letter-spacing:-.025em;margin-bottom:6px}}
.mtag{{display:block;font-size:15px;color:var(--mute);margin-bottom:12px}}
.mch{{list-style:none;margin:auto 0 14px;padding:0;display:flex;flex-wrap:wrap;gap:6px}}
.mch li{{font-size:11px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;border:1px solid var(--line);border-radius:4px;padding:3px 8px;color:var(--mute)}}
.mopen{{align-self:flex-start;display:inline-block;font-size:14px;font-weight:600;border-bottom:2px solid var(--acc);padding-bottom:1px}}
.mcard[aria-expanded=true] .mopen::after{{content:" ▲"}} .mcard[aria-expanded=false] .mopen::after{{content:" ▾"}}
.detail{{scroll-margin-top:12px;display:grid;grid-template-rows:0fr;transition:grid-template-rows .32s ease;margin-top:14px;position:relative}}
.detail[hidden]{{display:none}} .detail.open{{grid-template-rows:1fr}}
.dwrap{{overflow:hidden;min-height:0;background:var(--card);border:2px solid var(--ink);border-radius:var(--r);position:relative}}
.detail::before{{content:'';position:absolute;top:-11px;left:var(--arrow,50%);width:20px;height:20px;margin-left:-10px;background:var(--acc);border-left:2px solid var(--acc);border-top:2px solid var(--acc);transform:rotate(45deg);z-index:2;opacity:0;transition:opacity .2s .12s}}
.detail.open::before{{opacity:1}}
.dtop{{height:5px;background:var(--acc)}}
.detail.open .dwrap{{overflow:visible}}
.dwrap>*{{margin-left:26px;margin-right:26px}} .dwrap>.dtop{{margin:0}} .dwrap>.photos{{margin-left:26px;margin-right:26px}}
.dhead{{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;padding-top:26px}}
.dclose{{flex:none;font:inherit;font-size:12px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;color:var(--mute);background:none;border:1px solid var(--line);border-radius:6px;padding:8px 14px;cursor:pointer}}
.dclose:hover{{color:var(--ink);border-color:var(--ink)}}
.why{{font-size:17px;color:var(--mute);margin:10px 0 20px;max-width:640px}}
.photos{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin-bottom:26px}}
.photos img{{display:block;width:100%;aspect-ratio:16/10;object-fit:cover;border-radius:8px;background:#f0ebe0}}
.dgrid{{display:grid;grid-template-columns:1fr 1fr;gap:30px;margin-bottom:28px}}
.steps{{list-style:none;padding:0;margin:0;border-top:1px solid var(--line)}}
.steps li{{display:grid;grid-template-columns:60px minmax(0,1fr);gap:12px;padding:11px 0;border-bottom:1px solid var(--line)}}
.steps b{{font-variant-numeric:tabular-nums;color:var(--acc);font-weight:600;font-size:14px}} .steps strong{{display:block;font-weight:600;font-size:16px}} .steps span{{color:var(--mute);font-size:14px}}
.mapbox{{border-radius:8px;overflow:hidden;background:#f0ebe0}} .mapbox iframe{{display:block;width:100%;height:300px;border:0}}
.moves{{font-size:14px;color:var(--mute);margin:12px 0 0}} .moves a{{color:var(--ink);text-decoration:underline;text-underline-offset:3px;white-space:nowrap}}
.eats{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-bottom:26px}}
.eat{{display:flex;flex-direction:column;text-decoration:none;color:inherit;background:var(--bg);border:1px solid var(--line);border-radius:8px;overflow:hidden}}
.eat>img{{display:block;width:100%;aspect-ratio:3/2;object-fit:cover;background:#f0ebe0}}
.eb{{display:flex;flex-direction:column;flex:1;padding:14px 16px 16px}}
.eat:hover{{border-color:var(--ink)}}
.eat strong{{display:block;font-weight:700;font-size:18px;line-height:1.2;letter-spacing:-.015em}}
.eat em{{display:block;font-style:normal;font-size:11px;color:var(--acc);font-weight:600;letter-spacing:.08em;text-transform:uppercase;margin:5px 0 9px}}
.eb>span{{display:block;font-size:14px;color:var(--mute)}} .eat i{{display:block;font-style:normal;font-size:12px;margin-top:auto;padding-top:10px;text-decoration:underline;text-underline-offset:3px}}
.notes{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:20px;font-size:14px}} .notes p{{margin:0;padding:16px 18px;background:var(--bg);border:1px solid var(--line);border-radius:8px}} .notes b{{display:block;font-weight:600;margin-bottom:3px}}
.links{{margin:0 0 22px;font-size:14px;display:flex;flex-wrap:wrap;gap:6px 18px}} .links a{{color:var(--ink);text-decoration:underline;text-underline-offset:3px}}
.choose{{display:inline-block;background:var(--ink);color:#fff;text-decoration:none;font-weight:700;padding:16px 32px;border-radius:8px;font-size:16px;letter-spacing:-.01em;margin-bottom:28px}} .choose:hover{{background:#333}}
.arrival{{display:grid;grid-template-columns:1fr 1fr;gap:26px;align-items:start;padding-bottom:40px}}
.arrival p{{margin:0 0 10px;font-size:16px}} .arrival .hint{{color:var(--mute);font-size:15px}}
.arrival .mapbox iframe{{height:260px}}
footer.wrap{{padding:26px 20px 60px;font-size:13px;color:var(--mute);border-top:1px solid var(--line)}} footer p{{margin:0 0 6px}}
.cred summary{{cursor:pointer;font-size:12px;color:var(--mute);opacity:.75;list-style:none;display:inline-block;text-decoration:underline;text-underline-offset:3px}}
.cred summary::-webkit-details-marker{{display:none}} .cred p{{margin:8px 0 0;font-size:11.5px;line-height:1.6;opacity:.8}}
@media(max-width:820px){{
 .menu{{grid-template-columns:1fr}} .mcard>img{{aspect-ratio:16/9}}
 .dgrid,.eats,.notes,.arrival,.photos{{grid-template-columns:1fr}}
 .dwrap>*{{margin-left:18px;margin-right:18px}} .mapbox iframe{{height:230px}}
}}
@media(max-width:560px){{
 .wrap{{padding:0 18px}}
 .hcap{{min-height:58vh;padding-bottom:18px}} .hbody{{padding-top:18px;padding-bottom:22px}} .kicker{{margin-bottom:12px}}
 h1{{font-size:33px;line-height:1.08;letter-spacing:-.03em;margin-bottom:14px}}
 header p{{font-size:16px;line-height:1.55;max-width:none}}
 .facts{{display:grid;grid-template-columns:auto 1fr;gap:3px 10px;margin-top:16px;font-size:13px;line-height:1.5}}
 .facts li{{display:contents}} .facts b{{white-space:nowrap}}
 .sechead{{display:block;padding:22px 0 12px}}
 .sechead .n{{font-size:20px;margin-right:8px;display:inline}}
 .sechead b{{font-size:17px}} .sechead span{{display:block;font-size:13px;line-height:1.5;margin-top:2px}}
 .menu{{gap:12px}}
 .mb{{padding:15px 16px 16px}} .mt{{font-size:23px;line-height:1.15}} .mtag{{font-size:14px;margin-bottom:10px}}
 .mch{{gap:5px;margin-bottom:12px}} .mch li{{font-size:10.5px;padding:2px 7px}}
 .mopen{{font-size:13.5px}}
 h2{{font-size:26px;line-height:1.12}}
 .dhead{{padding-top:20px}} .why{{font-size:15.5px;line-height:1.55;margin:8px 0 16px}}
 .dwrap>*{{margin-left:16px;margin-right:16px}}
 .photos{{gap:8px;margin-bottom:20px}} .photos img{{aspect-ratio:3/2}}
 h3{{margin:22px 0 10px}} .dgrid{{gap:0;margin-bottom:0}}
 .steps li{{grid-template-columns:52px minmax(0,1fr);gap:10px;padding:10px 0}}
 .steps strong{{font-size:15.5px}} .steps span{{font-size:13.5px;line-height:1.5}}
 .eats{{gap:10px;margin-bottom:20px}} .eat>img{{aspect-ratio:16/9}} .eb{{padding:12px 14px 14px}}
 .notes{{gap:10px;margin-bottom:16px}} .notes p{{padding:14px 16px;font-size:13.5px}}
 .links{{font-size:13.5px;gap:4px 14px;margin-bottom:18px}}
 .choose{{display:block;text-align:center;padding:15px 0;margin-bottom:22px}}
 .arrival{{gap:16px;padding-bottom:32px}} .arrival p{{font-size:15.5px;line-height:1.55}} .arrival .hint{{font-size:14px}}
 .mapbox iframe{{height:210px}}
 footer.wrap{{padding:20px 18px 44px;font-size:11.5px;line-height:1.55}}
}}
</style></head><body>
<header class="hero">
<div class="hpic"><div class="slides">{''.join(f'<img src="{PH[c["id"]]["card"]["thumb"]}" alt="{html.escape(c["name"])}" data-course="{c["id"]}" data-name="{html.escape(c["name"])}">' for c in COURSES)}</div>
<div class="wrap hcap">
<p class="kicker">Tokyo · Friday, October 9</p>
<h1>Shibuya, <span class="nb">three ways.</span></h1>
<p class="fixed">Confirmed: course C, Friday October 9, 13:00 at the Hachiko statue.</p>
<div class="snav"><button class="slabel" type="button"></button><div class="dots">{''.join(f'<button type="button" aria-label="Show course {c["id"]}"></button>' for c in COURSES)}</div></div>
</div></div>
<div class="wrap hbody">
<p>About four hours on foot, all the way down to the Meguro river. Courses A and B stay on this page if you want to swap.</p>
<ul class="facts"><li><b>With</b> Yuuki</li><li><b>Day</b> Friday, October 9</li><li><b>Time</b> 13:00 to about 17:15</li><li><b>Start</b> Hachiko statue, Shibuya</li></ul>
</div>
</header>
<div class="wrap">
<div class="sechead"><span class="n">1</span><div><b>The plan</b> <span>Course C is the one we are doing. Tap any card to see the plan, the route and where we eat.</span></div></div>
<div class="menu">{''.join(menu(c) for c in COURSES)}</div>
{''.join(detail(c) for c in COURSES)}
<div class="sechead"><span class="n">2</span><div><b>Where we meet</b> <span>Hachiko statue, Hachiko exit of Shibuya station.</span></div></div>
<div class="arrival">
<div><p>Every train line stops at Shibuya, so the statue is the easiest place to find each other.</p>
<p class="hint">If your hotel is near Shibuya, tell me the name and I will come to the lobby instead. The 13:00 start can move if your morning runs long.</p></div>
<div class="mapbox"><iframe src="{emb('Hachiko Statue Shibuya')}" loading="lazy" title="Hachiko statue, Shibuya" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
</div>
</div>
<footer class="wrap"><p>Times are approximate and can move on the day. Message Yuuki if you want to change anything.</p>
<details class="cred"><summary>Photo credits</summary><p>{credits}, via Wikimedia Commons.</p></details></footer>
<script>
(function(){{
 var cards=[].slice.call(document.querySelectorAll('.mcard'));
 function close(id,now){{var d=document.getElementById('detail-'+id);d.classList.remove('open');document.querySelector('.menu').classList.remove('picked');if(now){{d.hidden=true;return}}setTimeout(function(){{if(!d.classList.contains('open'))d.hidden=true}},320);
   document.querySelector('.mcard[data-course="'+id+'"]').setAttribute('aria-expanded','false')}}
 function land(id){{var d=document.getElementById('detail-'+id),done=false;function go(){{if(done)return;done=true;d.scrollIntoView({{behavior:'smooth',block:'start'}})}}
   d.addEventListener('transitionend',function f(e){{if(e.target===d){{d.removeEventListener('transitionend',f);go()}}}});setTimeout(go,420)}}
 var menuEl=document.querySelector('.menu');
 function point(id){{var b=document.querySelector('.mcard[data-course="'+id+'"]'),d=document.getElementById('detail-'+id);
   var r=b.getBoundingClientRect(),w=d.getBoundingClientRect();
   d.style.setProperty('--arrow',(r.left+r.width/2-w.left)+'px')}}
 function open_(id){{var d=document.getElementById('detail-'+id);d.hidden=false;menuEl.classList.add('picked');
   requestAnimationFrame(function(){{d.classList.add('open');point(id)}});
   document.querySelector('.mcard[data-course="'+id+'"]').setAttribute('aria-expanded','true')}}
 window.addEventListener('resize',function(){{var o=document.querySelector('.mcard[aria-expanded=true]');if(o)point(o.dataset.course)}});
 var want=(location.hash.match(/^#detail-([ABC])$/)||[])[1]||(location.search.match(/[?&]open=([ABC])/)||[])[1]||'C';
 if(want){{open_(want);setTimeout(function(){{document.getElementById('detail-'+want).scrollIntoView()}},80)}}
 cards.forEach(function(b){{
  b.addEventListener('click',function(){{
   var id=b.dataset.course,was=b.getAttribute('aria-expanded')==='true';
   cards.forEach(function(o){{if(o.getAttribute('aria-expanded')==='true')close(o.dataset.course,true)}});
   if(was)return;
   open_(id);history.replaceState(null,'','#detail-'+id);
   land(id);
  }});
 }});
 document.querySelectorAll('.dclose').forEach(function(x){{
  x.addEventListener('click',function(){{var d=x.closest('.detail'),id=d.id.replace('detail-','');close(id);
   document.querySelector('.mcard[data-course="'+id+'"]').scrollIntoView({{behavior:'smooth',block:'center'}})}});
 }});
}})();
{HERO_JS}
</script>
{{DEVBAR}}</body></html>'''
open('index.html', 'w').write(page.replace('{DEVBAR}', ''))
open('preview.html', 'w').write(page.replace(
    '{DEVBAR}',
    '<script>window.DEVBAR_FORCE=1</script><script src="devbar.js?v=3"></script>'))
print('written', len(page), '-> index.html + preview.html')
