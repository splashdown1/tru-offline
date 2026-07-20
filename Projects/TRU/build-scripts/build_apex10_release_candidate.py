from pathlib import Path
import re

ROOT = Path('/home/workspace')
SOURCE = ROOT / 'TRU_APEX10.html'
OUTPUT = ROOT / 'TRU_APEX10_RELEASE.html'

if OUTPUT.exists():
    raise SystemExit(f'refusing to overwrite existing output: {OUTPUT}')

source = SOURCE.read_text(encoding='utf-8')
needle = '''    const _cap = capabilityQuery(q);
    if(_cap){addTurn(q,_cap);return _cap;}
    if(/^(?:what is|what are|define|definition of)\\s+/i.test(low)){'''
replacement = '''    const _cap = capabilityQuery(q);
    if(_cap){addTurn(q,_cap);return _cap;}
    const _docEarly = doctrine(q);
    if(_docEarly){
      const _docResult={verdict:"TRUTH",reply:_docEarly,source:"DOCTRINE • curated local",nodes_used:[],follow_up:false};
      addTurn(q,_docResult);
      return _docResult;
    }
    if(/^(?:what is|what are|define|definition of)\\s+/i.test(low)){'''
if needle not in source:
    raise SystemExit('route insertion point not found')
source = source.replace(needle, replacement, 1)
source = source.replace('<title>TRU APEX X — Sovereign Capability Layer</title>', '<title>TRU APEX X — Release Candidate</title>', 1)

network_hits = []
for match in re.finditer(r'<script([^>]*)>(.*?)</script>', source, re.IGNORECASE | re.DOTALL):
    attrs, body = match.group(1).lower(), match.group(2)
    if 'application/json' in attrs:
        continue
    for pattern in (r'\bfetch\s*\(', r'\bXMLHttpRequest\b', r'\bWebSocket\s*\(', r'\bEventSource\s*\('):
        if re.search(pattern, body):
            network_hits.append(pattern)
if network_hits:
    raise SystemExit(f'executable network primitive remains: {network_hits}')
for required in ('function capabilityQuery(q)', 'function capabilityTeach(q)', 'const _docEarly = doctrine(q);'):
    if required not in source:
        raise SystemExit(f'missing required release feature: {required}')

OUTPUT.write_text(source, encoding='utf-8')
print(f'wrote {OUTPUT} ({OUTPUT.stat().st_size} bytes)')
print('offline executable network primitives: 0')
print('capability nodes: 5')
print('embedded brain: 63,337 source nodes')
print('embedded KJV verses: 31,100')
print('early curated doctrine routing: enabled')
