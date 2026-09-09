#!/usr/bin/env python3
from pathlib import Path
p=Path('shows/comedy/carrot-top/index.html')
s=p.read_text(encoding='utf-8')
repls={
'Tickets currently start at $62. Your date and seat determine the final total.':'Tickets currently start at $62. Other price points may be available depending on the performance and seating section.',
'Center section is my Sweet Spot for a straight-on stage view. Front rows put you closest to the action; farther back gives you more distance. Use the live seat map on the booking screen to compare rows and prices.':'Reserved 2 is the Vegas Sidekick Sweet Spot / Our Pick for Carrot Top. It gives you the best balance of stage detail and the full-room view. Reserved 1 is closest to the stage, while Reserved 3 and Reserved 4 sit farther back.',
'Spotlight currently lists the show length as 75 minutes.':'Carrot Top runs about 75 minutes.',
'The typical schedule is Monday through Saturday at 8 PM. Some dates are dark and extra performances are added from time to time, so check the booking screen for the live dates and times.':'The regular schedule is Monday through Saturday at 8 PM. Some dates can differ, so check the available dates and times for your trip.'
}
for old,new in repls.items():
    assert old in s, old
    s=s.replace(old,new)
p.write_text(s,encoding='utf-8')
for banned in ['Your date and seat determine the final total','Center section is my Sweet Spot','closest to the action','Spotlight currently lists','The typical schedule is']:
    assert banned not in s, banned
assert s.count('Reserved 2 is the Vegas Sidekick Sweet Spot / Our Pick for Carrot Top') >= 3
print('Carrot Top FAQ aligned with Reserved 2 seating system')
