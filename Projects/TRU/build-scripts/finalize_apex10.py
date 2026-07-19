from pathlib import Path

root = Path('/home/workspace')
src = root / 'TRU_APEX10_FIXED.html'
out = root / 'TRU_APEX10_FINAL.html'
s = src.read_text(encoding='utf-8')
s = s.replace('d.vd.textContent=(VNAME[verdict]||verdict)+(ms?" · "+ms+"ms":"");', 'd.vd.textContent=(VNAME[verdict]||verdict)+(ms?" · "+ms:"");', 1)
s = s.replace("'<div style=\"color:#9ed7ff;margin-bottom:8px;font-size:13px\">'+BRAIN_COUNT.toLocaleString()+' brain nodes + '+KJV_COUNT.toLocaleString()+' KJV verses.</div>'", "'<div style=\"color:#9ed7ff;margin-bottom:8px;font-size:13px\">'+BRAIN_COUNT.toLocaleString()+' embedded brain nodes + '+CAPABILITY_COUNT+' capability nodes + '+KJV_COUNT.toLocaleString()+' KJV verses.</div>'", 1)
out.write_text(s, encoding='utf-8')
print(f'wrote {out} ({out.stat().st_size} bytes)')
