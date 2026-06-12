#!/usr/bin/env python3
from pathlib import Path
import re, base64, json
html = Path('/home/workspace/Projects/TRU/current/index.html').read_text(encoding='utf-8', errors='ignore')
m = re.search(r'const _b64="([^"]+)"', html)
assert m, 'missing embedded brain'
nodes = json.loads(base64.b64decode(m.group(1)))
assert len(nodes) == 31015, f'expected 31015 nodes, got {len(nodes)}'
by_key = {n.get('k'): n for n in nodes}
assert by_key['john_3:16']['v'].lower().startswith('for god so loved'), 'john 3:16 failed'
assert by_key['genesis_1:1']['v'].lower().startswith('in the beginning'), 'genesis 1:1 failed'
for needle in ['TRU Phase 27', 'VERSION', 'normalBook', 'STORAGE_PREFIX', 'X means Y']:
    assert needle in html, f'missing {needle}'
print('phase 27 smoke ok:', len(nodes), 'nodes')
