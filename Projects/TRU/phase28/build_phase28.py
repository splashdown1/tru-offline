#!/usr/bin/env python3
"""
Build TRU Phase 28 — Knowledge Graph Edition
"""
from pathlib import Path
import base64, json, shutil

PHASE = 28
CURRENT = Path('/home/workspace/Projects/TRU/phase28')
EXPORT = Path('/home/workspace/Projects/TRU/TRU_PHASE28_KNOWLEDGE_GRAPH.html')

def main():
    # load brain
    brain_doc = json.loads((CURRENT / 'brain.json').read_text(encoding='utf-8'))
    nodes = brain_doc['nodes'] if isinstance(brain_doc, dict) and 'nodes' in brain_doc else brain_doc
    
    # encode to base64
    b64 = base64.b64encode(
        json.dumps(nodes, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
    ).decode('ascii')
    
    # load template
    template = (CURRENT / 'template.html').read_text(encoding='utf-8', errors='ignore')
    
    if '__TRU_PHASE28_BRAIN_B64__' not in template:
        raise SystemExit('template missing brain placeholder')
    
    # inject brain
    html = template.replace('__TRU_PHASE28_BRAIN_B64__', b64)
    
    # write outputs
    (CURRENT / 'index.html').write_text(html, encoding='utf-8')
    shutil.copy2(CURRENT / 'index.html', EXPORT)
    
    print(f'✓ phase {PHASE} built: {len(nodes)} nodes')
    print(f'  → {CURRENT / "index.html"}')
    print(f'  → {EXPORT}')

if __name__ == '__main__':
    main()
