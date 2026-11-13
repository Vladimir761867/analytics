#!/usr/bin/env python3
"""Собирает data/commits.json из git-истории репозиториев.
Использование: python3 tools/build_commits.py WINNER_APP_DIR FOOTBALL_DIR PATH_DIR [AFTERBURN_DIR]
Время пишется по Москве (UTC+3)."""
import subprocess, json, sys, datetime, os
MSK = datetime.timezone(datetime.timedelta(hours=3))
def log(repo, *args):
    out = subprocess.check_output(['git', '-C', repo, 'log', *args, '--format=%H|%at|%s'], text=True)
    for l in out.strip().split('\n'):
        if l:
            h, ts, s = l.split('|', 2)
            yield h, datetime.datetime.fromtimestamp(int(ts), MSK), s
def row(h, t, s, app, kind):
    return {"time": t.strftime('%Y-%m-%dT%H:%M'), "day": t.strftime('%Y-%m-%d'), "hour": t.hour + t.minute / 60,
            "app": app, "kind": kind, "hash": h[:7], "subject": s}
store_words = ('RuStore', 'Слияние', 'чек-лист', 'Android', 'release', 'Capacitor', 'CI:', 'Pages', 'бет', 'APK', 'AAB')
def kind(s): return 'Магазин и сборка' if any(w in s for w in store_words) else 'Игра'
rows, seen = [], set()
w, f, p = sys.argv[1:4]
a = sys.argv[4] if len(sys.argv) > 4 else None
for h, t, s in log(w, '--all'):
    if h in seen: continue
    seen.add(h)
    low = s.lower()
    app = 'Junior' if 'junior' in low else ('Общее' if s.startswith(('Слияние', 'Merge', 'RuStore: описание')) else 'Взрослая')
    rows.append(row(h, t, s, app, kind(s)))
for h, t, s in log(f, 'origin/main'):
    if s.startswith('Merge'): continue
    rows.append(row(h, t, s, 'Футбол', kind(s)))
for h, t, s in log(p, 'origin/main'):
    if s.startswith('Merge pull request'): continue
    rows.append(row(h, t, s, 'Рядом', kind(s)))
if a:
    for h, t, s in log(a, 'origin/main'):
        rows.append(row(h, t, s, 'Afterburn', kind(s)))
rows.sort(key=lambda r: r['time'])
out = os.path.join(os.path.dirname(__file__), '..', 'data', 'commits.json')
json.dump(rows, open(out, 'w'), ensure_ascii=False)
from collections import Counter
print(len(rows), Counter(r['app'] for r in rows), rows[0]['time'], rows[-1]['time'])
