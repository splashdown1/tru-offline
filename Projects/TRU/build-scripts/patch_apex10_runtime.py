from pathlib import Path

root = Path('/home/workspace')
src = root / 'TRU_APEX10_FINAL.html'
out = root / 'TRU_APEX10.html'
s = src.read_text(encoding='utf-8')
if 'const CAPABILITY_COUNT=5;' not in s:
    raise SystemExit('missing capability count')
old_stats = '  return {reply:"brain: "+b.length+" nodes • overlay: "+Object.keys(OVERLAY.added).length+" added, "+Object.keys(OVERLAY.corrected).length+" corrected, "+Object.keys(OVERLAY.removed).length+" forgotten • kjv: "+KJV_COUNT.toLocaleString()+" verses.",verdict:"MEMORY",nodes_used:[],follow_up:false};'
new_stats = '  return {reply:"brain: "+b.length+" runtime nodes • "+CAPABILITY_COUNT+" capability nodes • "+(b.length+CAPABILITY_COUNT)+" total local nodes • overlay: "+Object.keys(OVERLAY.added).length+" added, "+Object.keys(OVERLAY.corrected).length+" corrected, "+Object.keys(OVERLAY.removed).length+" forgotten • kjv: "+KJV_COUNT.toLocaleString()+" verses.",verdict:"MEMORY",nodes_used:[],follow_up:false};'
if old_stats not in s:
    raise SystemExit('stats source string not found')
s = s.replace(old_stats, new_stats, 1)
old_format = '  addMsg("tru",res.reply,res.verdict,res.source?("· "+res.source):"");'
new_format = '  addMsg("tru",res.reply,res.verdict,res.source||"");'
if old_format not in s:
    raise SystemExit('source formatting source string not found')
s = s.replace(old_format, new_format, 1)
marker = '// patch route to intercept encyclopedia + dictionary queries'
insert = '''function apex10DictionaryGuard(q){
  const m=String(q).toLowerCase().trim().match(/^(?:what is|what are|define|definition of)\\s+(?:an? |the )?([a-z][a-z-]*)[?!.]*$/i);
  if(!m)return null;
  const term=m[1];
  const r=typeof dictLookup==='function'?dictLookup(term):null;
  return r?{verdict:"DEFINE",reply:renderDict(r)}:null;
}

'''
if marker not in s:
    raise SystemExit('route marker missing')
s = s.replace(marker, insert + marker, 1)
old_cap = '''    const _cap = capabilityQuery(q);
    if(_cap){addTurn(q,_cap);return _cap;}

    // 0. POLYSEM first'''
new_cap = '''    const _cap = capabilityQuery(q);
    if(_cap){addTurn(q,_cap);return _cap;}
    if(/^(?:what is|what are|define|definition of)\s+/i.test(low)){
      const _dictGuard = apex10DictionaryGuard(q);
      if(_dictGuard){addTurn(q,_dictGuard);return _dictGuard;}
    }

    // 0. POLYSEM first'''
if old_cap not in s:
    raise SystemExit('cap insertion point missing')
s = s.replace(old_cap, new_cap, 1)
if 'runtime nodes' not in s or 'total local nodes' not in s:
    raise SystemExit('stats patch missing')
if 'addMsg("tru",res.reply,res.verdict,res.source||"");' not in s:
    raise SystemExit('source formatting patch missing')
if 'function apex10DictionaryGuard' not in s:
    raise SystemExit('dictionary guard missing')
out.write_text(s, encoding='utf-8')
print(f'wrote {out} ({out.stat().st_size} bytes)')
