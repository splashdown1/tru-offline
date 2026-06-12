#!/usr/bin/env python3
from pathlib import Path
import base64, json, re, shutil

CURRENT = Path('/home/workspace/Projects/TRU/current')
EXPORT = Path('/home/workspace/Projects/TRU/TRU_PHASE27_CANONICAL.html')
brain_doc = json.loads((CURRENT / 'brain.json').read_text(encoding='utf-8'))
nodes = brain_doc['nodes'] if isinstance(brain_doc, dict) and 'nodes' in brain_doc else brain_doc
b64 = base64.b64encode(json.dumps(nodes, separators=(',', ':'), ensure_ascii=False).encode('utf-8')).decode('ascii')
template = (CURRENT / 'template.html').read_text(encoding='utf-8', errors='ignore')
if '__TRU_PHASE27_BRAIN_B64__' not in template:
    raise SystemExit('template missing brain placeholder')
html = template.replace('__TRU_PHASE27_BRAIN_B64__', b64)
(CURRENT / 'index.html').write_text(html, encoding='utf-8')
shutil.copy2(CURRENT / 'index.html', EXPORT)
print(f'rebuilt phase 27 canonical: {len(nodes)} nodes -> {CURRENT / "index.html"}')
