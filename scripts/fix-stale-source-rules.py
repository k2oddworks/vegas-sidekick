#!/usr/bin/env python3
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]

def rewrite(path, fn):
    p=ROOT/path
    text=p.read_text(encoding='utf-8')
    new=fn(text)
    if new!=text:
        p.write_text(new,encoding='utf-8')
        print(path)

def brand(text):
    text=text.replace('*Accurate as of 2026-08-27.*','*Accurate as of 2026-09-07.*')
    text=text.replace('> Handpicked Las Vegas show tickets at legit discounts. No membership, no hidden fees,\n> no markup games. Your Vegas insider — guaranteed.', '> Independent Las Vegas show recommendations, practical ticket guidance and honest tradeoffs.\n> Your Vegas insider without the sales-floor nonsense.')
    text=text.replace('5. **No fake urgency.** "Selling fast" only if it is. "Prices may increase closer to\n   show date" is true and is as far as we go.', '5. **No generic urgency or scarcity.** Do not use phrases like "selling fast," "prices may increase," or countdown-style pressure unless a current, verifiable fact specifically requires it. Prefer the useful fact: current price, showtime, dark day, availability status or closure date.')
    return text

def builder(text):
    text=re.sub(r'## Urgency Copy — Locked\n\n✅ \*\*Allowed:\*\* "Prices may increase closer to show date"\n❌ \*\*Never:\*\* "Prices increase closer to show date" — removing "may" makes it a false claim\n❌ \*\*Never:\*\* Fake countdown timers, fake social proof, fabricated scarcity, made-up reviews', '## Urgency Copy — Locked\n\n❌ **Never use generic urgency:** "selling fast," "prices may increase," "book early," fake countdowns, fake social proof, fabricated scarcity, or made-up reviews.\n✅ **Use current facts instead:** price, date, showtime, dark days, verified availability status, closure/extension status, and practical seat guidance.', text)
    text=re.sub(r'<div class="trust-card"><div class="trust-icon">🔒</div><div class="trust-title">Secure Booking</div><div class="trust-body">.*?</div></div>', '<div class="trust-card"><div class="trust-icon">🎟️</div><div class="trust-title">Useful Ticket Details</div><div class="trust-body">Show the current price, schedule, venue and practical booking context without unsupported checkout claims.</div></div>', text, flags=re.S)
    text=re.sub(r'<div class="trust-card"><div class="trust-icon">[^<]*</div><div class="trust-title">No Hidden Fees</div><div class="trust-body">.*?</div></div>', '<div class="trust-card"><div class="trust-icon">🌵</div><div class="trust-title">Honest Tradeoffs</div><div class="trust-body">Say who the show fits, what to know first and one real downside when it matters.</div></div>', text, flags=re.S)
    text=text.replace('*Last updated: 2026-05-31*','*Last updated: 2026-09-07*')
    return text

def context(text):
    text=re.sub(r'no hidden fees', 'clear ticket details', text, flags=re.I)
    text=re.sub(r'prices may increase closer to show date', 'generic price-pressure language', text, flags=re.I)
    return text

rewrite('BRAND.md',brand)
rewrite('SHOW-BUILDER-PROMPT.md',builder)
rewrite('VS_CHAT_CONTEXT.md',context)
