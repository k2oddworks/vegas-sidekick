from pathlib import Path
import re

article = Path('news/activate-town-square-opens-october-3/index.html')
s = article.read_text(encoding='utf-8')

# Standard site chrome.
if '<div id="vs-header"></div>' not in s:
    s = s.replace('<body>', '<body>\n<div id="vs-header"></div>', 1)

if '<div id="vs-footer"></div>' not in s:
    s = s.replace('</body>', '<div id="vs-footer"></div>\n<script src="/components/header.js?v=13"></script>\n<script src="/components/footer.js?v=10"></script>\n</body>', 1)
elif '/components/header.js?v=13' not in s:
    s = s.replace('<div id="vs-footer"></div>', '<div id="vs-footer"></div>\n<script src="/components/header.js?v=13"></script>\n<script src="/components/footer.js?v=10"></script>', 1)

# Do not narrate small corrections to readers. Just show the current fact.
s = re.sub(
    r'<div class="note"><p><strong>Update:</strong> Activate’s current Las Vegas page lists <strong>14 game rooms</strong>\. Early opening information described 15 arenas, which is why the original version of this story used 15\. We’ve updated the article to the operator’s current count\.</p></div>',
    '<div class="note"><p>Activate currently lists <strong>14 game rooms</strong> at its Town Square location.</p></div>',
    s,
    count=1
)

# Byline: author avatar + published date only. dateModified stays in schema.
byline_old = 'By <a href="/about/kris-kidd/">Kris Kidd</a> · Published September 2, 2026 · Updated September 5, 2026'
byline_new = '<span class="author-inline"><img src="/images/kris-kidd-avatar.jpg" alt="Kris Kidd" width="30" height="30">By <a href="/about/kris-kidd/">Kris Kidd</a></span> · Published September 2, 2026'
s = s.replace(byline_old, byline_new)
# Cover any additional plain Kris bylines on this page.
s = re.sub(r'(?<!author-inline">)By <a href="/about/kris-kidd/">Kris Kidd</a>', '<span class="author-inline"><img src="/images/kris-kidd-avatar.jpg" alt="Kris Kidd" width="30" height="30">By <a href="/about/kris-kidd/">Kris Kidd</a></span>', s)

# Author image in NewsArticle JSON-LD.
s = s.replace('"author":{"@type":"Person","name":"Kris Kidd","url":"https://vegassidekick.com/about/kris-kidd/"}', '"author":{"@type":"Person","name":"Kris Kidd","url":"https://vegassidekick.com/about/kris-kidd/","image":"https://vegassidekick.com/images/kris-kidd-avatar.jpg"}')

# Mid-article email capture after the games section.
signup = '''<aside class="dispatch-signup" aria-labelledby="dispatch-signup-title">
  <div class="dispatch-signup-glow" aria-hidden="true"></div>
  <div class="dispatch-signup-kicker">🌵 Spike's Insider List</div>
  <h3 id="dispatch-signup-title">Want the Vegas stuff worth knowing?</h3>
  <p>New openings, show changes and genuinely useful Vegas deals. No daily spam. No email wall.</p>
  <form class="dispatch-signup-form" id="dispatchEmailForm">
    <label class="sr-only" for="dispatchEmail">Email address</label>
    <input id="dispatchEmail" type="email" inputmode="email" autocomplete="email" placeholder="you@example.com" required>
    <button type="submit" id="dispatchEmailBtn">Send me the good stuff →</button>
  </form>
  <div class="dispatch-signup-msg" id="dispatchEmailMsg" aria-live="polite">Unsubscribe anytime.</div>
</aside>'''
if 'id="dispatchEmailForm"' not in s:
    games = s.find('<h2 id="games">')
    if games == -1:
        raise SystemExit('games section not found')
    next_h2 = s.find('<h2', games + 12)
    if next_h2 == -1:
        raise SystemExit('next section after games not found')
    s = s[:next_h2] + signup + s[next_h2:]

css = '''
/* Dispatch integration: shared chrome, author avatar, newsletter */
.author-inline{display:inline-flex;align-items:center;gap:7px;vertical-align:middle}.author-inline img{width:30px;height:30px;border-radius:50%;object-fit:cover;border:2px solid rgba(255,255,255,.72);box-shadow:0 2px 10px rgba(0,0,0,.18)}.byline .author-inline img{border-color:#fff}.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}.dispatch-signup{position:relative;overflow:hidden;margin:42px 0;padding:30px;border-radius:22px;background:linear-gradient(135deg,#17082e 0%,#341253 56%,#102d43 100%);color:#fff;box-shadow:0 20px 55px rgba(33,10,60,.2)}.dispatch-signup-glow{position:absolute;right:-70px;top:-80px;width:240px;height:240px;border-radius:50%;background:radial-gradient(circle,rgba(28,210,220,.32),rgba(239,61,136,.13) 48%,transparent 72%);pointer-events:none}.dispatch-signup-kicker{position:relative;font:700 .7rem 'IBM Plex Mono',monospace;letter-spacing:.1em;text-transform:uppercase;color:#dff442;margin-bottom:9px}.dispatch-signup h3{position:relative;color:#fff!important;font-size:clamp(1.55rem,4vw,2.25rem)!important;line-height:1.08!important;letter-spacing:-.035em;margin:0 0 10px!important;max-width:620px}.dispatch-signup p{position:relative;color:#e7ddeb!important;margin:0 0 19px!important;max-width:610px}.dispatch-signup-form{position:relative;display:flex;gap:9px}.dispatch-signup-form input{flex:1;min-width:0;border:1px solid rgba(255,255,255,.24);background:rgba(255,255,255,.1);color:#fff;border-radius:11px;padding:13px 14px;font:600 .9rem Inter,sans-serif;outline:none}.dispatch-signup-form input::placeholder{color:#c8bbcf}.dispatch-signup-form input:focus{border-color:#dff442;box-shadow:0 0 0 3px rgba(223,244,66,.14)}.dispatch-signup-form button{border:2px solid #fff;background:linear-gradient(90deg,#ff2e7e,#ff6b35);color:#fff;border-radius:11px;padding:12px 17px;font:800 .88rem 'Plus Jakarta Sans',sans-serif;cursor:pointer;transition:.2s;white-space:nowrap}.dispatch-signup-form button:hover{transform:translateY(-2px);filter:brightness(1.06)}.dispatch-signup-form button:disabled{opacity:.65;cursor:default;transform:none}.dispatch-signup-msg{position:relative;margin-top:10px;font-size:.72rem;color:#c9bdcf}@media(max-width:620px){.dispatch-signup{padding:24px 20px}.dispatch-signup-form{display:grid}.dispatch-signup-form button{width:100%}.author-inline img{width:28px;height:28px}}
'''
if '/* Dispatch integration: shared chrome' not in s:
    s = s.replace('</style>', css + '</style>', 1)

js = '''
<script>
(function(){
  const form=document.getElementById('dispatchEmailForm');
  if(!form) return;
  const input=document.getElementById('dispatchEmail');
  const btn=document.getElementById('dispatchEmailBtn');
  const msg=document.getElementById('dispatchEmailMsg');
  form.addEventListener('submit',async function(e){
    e.preventDefault();
    const email=input.value.trim();
    if(!email || !email.includes('@')){msg.textContent='Enter a valid email and try again.';return;}
    btn.disabled=true;btn.textContent='Signing you up…';msg.textContent='';
    try{
      const r=await fetch('https://brevo-subscribe.vegassidekickcom.workers.dev',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email})});
      if(!r.ok) throw new Error('subscribe failed');
      input.value='';msg.textContent='You’re on the list. 🌵';btn.textContent='You’re in';
    }catch(err){
      msg.textContent='That didn’t go through. Try again in a moment.';btn.disabled=false;btn.textContent='Send me the good stuff →';
    }
  });
})();
</script>
'''
if "dispatchEmailForm');" not in s:
    s = s.replace('</body>', js + '</body>', 1)

article.write_text(s, encoding='utf-8')

# Dispatch index: author avatar on the featured Activate card.
idx = Path('news/index.html')
t = idx.read_text(encoding='utf-8')
old = '<span class="featured-author">By Kris Kidd</span>'
new = '<span class="featured-author featured-author-with-avatar"><img src="/images/kris-kidd-avatar.jpg" alt="Kris Kidd" width="26" height="26">By Kris Kidd</span>'
t = t.replace(old, new, 1)
if '.featured-author-with-avatar' not in t:
    t = t.replace('</style>', '.featured-author-with-avatar{display:inline-flex;align-items:center;gap:7px}.featured-author-with-avatar img{width:26px;height:26px;border-radius:50%;object-fit:cover;border:2px solid #fff;box-shadow:0 2px 8px rgba(0,0,0,.13)}\n</style>', 1)
idx.write_text(t, encoding='utf-8')

print('Patched Activate Dispatch integration, signup and author avatar.')
