from pathlib import Path
root=Path('.')
changed=[]
patterns=[
('"author":{"@type":"Person","name":"Kris Kidd"','"author":{"@type":"Person","@id":"https://vegassidekick.com/about/kris-kidd/#kris","name":"Kris Kidd"'),
('"author": {"@type": "Person", "name": "Kris Kidd"','"author": {"@type": "Person", "@id": "https://vegassidekick.com/about/kris-kidd/#kris", "name": "Kris Kidd"'),
('"author": { "@type": "Person", "name": "Kris Kidd"','"author": { "@type": "Person", "@id": "https://vegassidekick.com/about/kris-kidd/#kris", "name": "Kris Kidd"')]
for folder in ['news','guides','shows']:
    for p in (root/folder).rglob('*.html'):
        s=p.read_text(encoding='utf-8')
        old=s
        for a,b in patterns:s=s.replace(a,b)
        if s!=old:
            p.write_text(s,encoding='utf-8');changed.append(str(p))
print('\n'.join(changed) if changed else 'No author IDs needed normalization')
