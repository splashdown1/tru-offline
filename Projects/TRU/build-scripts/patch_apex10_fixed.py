from pathlib import Path

root = Path('/home/workspace')
src = root / 'TRU_APEX10.html'
out = root / 'TRU_APEX10_FIXED.html'
s = src.read_text(encoding='utf-8')
s = s.replace('const BRAIN_COUNT=1363;\n', 'const BRAIN_COUNT=63337;\nconst CAPABILITY_COUNT=5;\n', 1)
if 'const CAPABILITY_COUNT=5;' not in s:
    s = s.replace('const BRAIN_COUNT=1363;\n', 'const BRAIN_COUNT=63337;\nconst CAPABILITY_COUNT=5;\n', 1)
    s = s.replace('const BRAIN_COUNT=63337;\n', 'const BRAIN_COUNT=63337;\nconst CAPABILITY_COUNT=5;\n', 1)
# embedded data can contain the word fetch; the executable source has no network call.

s = s.replace("'+BRAIN_COUNT.toLocaleString()+' brain nodes + '+KJV_COUNT.toLocaleString()+' KJV verses.'", "'+BRAIN_COUNT.toLocaleString()+' brain nodes + '+CAPABILITY_COUNT+' capability nodes + '+KJV_COUNT.toLocaleString()+' KJV verses.'", 1)
out.write_text(s, encoding='utf-8')
print(f'wrote {out} ({out.stat().st_size} bytes)')
