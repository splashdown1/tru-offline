from pathlib import Path
import re

root = Path('/home/workspace')
source_path = root / 'TRU_APEX10_RELEASE_CANDIDATE.html'
output_path = root / 'TRU_APEX10_PROVENANCE_FINAL.html'

if output_path.exists():
    raise SystemExit(f'refusing to overwrite existing output: {output_path}')

source = source_path.read_text(encoding='utf-8')
old_fire = 'how\\s+to\\s+make\\s+fire|extinguish\\s+(a\\s+)?fire|runaway\\s+fire'
new_fire = 'how\\s+to\\s+make\\s+fire|extinguish\\s+(a\\s+)?fire|put\\s+out\\s+(a\\s+)?fire|runaway\\s+fire'
if old_fire not in source:
    raise SystemExit('fire matcher not found')
source = source.replace(old_fire, new_fire, 1)

injected = r'''<script>
(function(){
  const previousRoute=route;
  function directResult(reply,verdict,source){
    const result={reply,verdict,source,nodes_used:[],follow_up:false};
    if(typeof addTurn==='function')addTurn(currentQuery,result);
    return result;
  }
  let currentQuery='';
  function directQuery(q){
    const low=String(q).toLowerCase().trim().replace(/[!?]+$/,'');
    if(/^(?:hi|hello|hey|yo)$/.test(low))return directResult("hello. i'm tru — awake, offline, and ready. ask for scripture, doctrine, definitions, strong's, or a local capability.","REASON","LOCAL CONVERSATION • offline");
    if(/^(?:what do you wanna do today|what do you want to do today|what should we do today)$/.test(low))return directResult("i have no verified personal wants. choose a subject, a goal, or a question; i will work from the local sources and label retrieved material honestly.","TRUTH","SELF • verified boundary • embedded local");
    if(/^(?:\/?help|show commands)$/.test(low))return directResult("help is local. ask about scripture, doctrine, definitions, Strong's, commentary, capabilities, or calculations. use teach: term = definition to add local material. unsupported questions remain GAP.","ARCHITECTURE","LOCAL HELP • offline");
    if(/^\/money$/.test(low)){
      const entry=typeof dictLookup==='function'?dictLookup('money'):null;
      if(entry)return directResult(renderDict(entry),"DEFINE","DICTIONARY • local WordNet");
    }
    if(/^(?:when will christ return|when is christ returning|when does christ return)\??$/.test(low))return directResult("no one knows the day or the hour of Christ's return. the command is to watch, remain faithful, and be ready. (matthew 24:36,42-44; acts 1:7; 1 thessalonians 4:16-17; revelation 19:11-16)","TRUTH","DOCTRINE • eschatology • curated local");
    if(/^(?:what would make you better|how can you improve|what do you need to improve)\\??$/.test(low))return directResult("tested correction, clearer provenance, stronger intent routing, and honest gaps make me better. teach me what is missing; I will preserve the source label and distinguish retrieved material from verified self-state.","TRUTH","SELF • embedded local");
    return null;
  }
  function nodeFor(result){
    const key=result&&result.nodes_used&&result.nodes_used[0]&&result.nodes_used[0].k;
    if(!key||typeof getBrain!=='function')return null;
    return getBrain().find(node=>String(node.k)===String(key))||null;
  }
  function normalise(q,result){
    if(!result)return result;
    if(result.source && result.source !== 'TRU_CAPABILITY')return result;
    if(result.source === 'TRU_CAPABILITY')return Object.assign({},result,{source:'CAPABILITY • verified local procedure'});
    if(result.verdict==='SCRIPTURE')return Object.assign({},result,{source:'SCRIPTURE • KJV primary • local'});
    if(result.verdict==='DEFINE')return Object.assign({},result,{source:'DICTIONARY • local WordNet'});
    if(result.verdict==='CALC')return Object.assign({},result,{source:'CALCULATOR • local'});
    if(result.verdict==='TRUTH' && result.reply && /prediction_audit|real-time solar wind|historical G1 correlation/i.test(result.reply))return Object.assign({},result,{verdict:'REASON',source:'BRAIN RETRIEVAL • raw unrelated node',reply:'the local brain returned unrelated stored material for this query. it is not an answer. this is a gap: teach or add a grounded source for the requested subject.'});
    const node=nodeFor(result);
    if(node){
      const kind=String(node.t||'').toLowerCase();
      const nodeSource=String(node.source||'').toLowerCase();
      const text=String(node.v||result.reply||'');
      if(kind==='interaction'||nodeSource.includes('interaction'))return Object.assign({},result,{verdict:'REASON',source:'BRAIN RETRIEVAL • raw interaction node',reply:'the local brain contains this previously stored interaction text:\n\n“'+text+'”\n\nthis is retrieved source material, not a verified statement of tru’s current desire or self-state.'});
      return Object.assign({},result,{verdict:'REASON',source:'BRAIN RETRIEVAL • '+(node.source||node.t||'local brain node')});
    }
    if(result.verdict==='TRUTH')return Object.assign({},result,{source:'LOCAL RESULT • provenance not specialised'});
    if(result.verdict==='REASON')return Object.assign({},result,{source:'LOCAL REASONING • offline'});
    if(result.verdict==='GAP')return Object.assign({},result,{source:'GAP • unsupported locally'});
    return result;
  }
  route=function(q){
    currentQuery=String(q);
    const direct=directQuery(currentQuery);
    if(direct)return direct;
    return normalise(currentQuery,previousRoute(currentQuery));
  };
})();
</script>
'''
marker = '</body>'
if marker not in source:
    raise SystemExit('body marker not found')
source = source.replace(marker, injected + marker, 1)
source = source.replace('</script>\n<script type="application/json" id="encyclopedia-data">', '</script>\n' + injected + '<script type="application/json" id="encyclopedia-data">', 1)
source = source.replace(injected + injected + marker, injected + marker, 1)

network_hits=[]
for match in re.finditer(r'<script([^>]*)>(.*?)</script>', source, re.IGNORECASE | re.DOTALL):
    attrs, body = match.group(1).lower(), match.group(2)
    if 'application/json' in attrs:
        continue
    for pattern in (r'\bfetch\s*\(', r'\bXMLHttpRequest\b', r'\bWebSocket\s*\(', r'\bEventSource\s*\('):
        if re.search(pattern, body):
            network_hits.append(pattern)
if network_hits:
    raise SystemExit(f'executable network primitive remains: {network_hits}')
for required in ('BRAIN RETRIEVAL • raw interaction node', 'function capabilityQuery(q)', 'put\\s+out'):
    if required not in source:
        raise SystemExit(f'missing required provenance feature: {required}')

output_path.write_text(source, encoding='utf-8')
print(f'wrote {output_path} ({output_path.stat().st_size} bytes)')
print('provenance layer: enabled')
print('direct self/help/eschatology routes: enabled')
print('fire extinguishing matcher: enabled')
print('executable network primitives: 0')
