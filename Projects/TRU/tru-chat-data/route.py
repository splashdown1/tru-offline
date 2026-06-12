import json, sys, re
from pathlib import Path
kjv = json.loads(Path('/home/workspace/Projects/TRU/data/kjv_full.json').read_text())
kjv_map = {v['ref'].lower(): v['text'] for v in kjv}
body = json.loads(sys.stdin.read())
q = (body.get('q') or body.get('query') or '').strip()
BOOK = {
  "gen":"genesis","exo":"exodus","ex":"exodus","lev":"leviticus","nu
