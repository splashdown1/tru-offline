#!/usr/bin/env python3
"""build tru_giga.html.

core idea:
- build the live tru logos engine from the canonical shell + manifest
- merge in the biggest local knowledge files we have
- append archived lineage html builds as base64 payloads so the file can grow huge
"""
from __future__ import annotations

import base64
import json
import os
import re
from pathlib import Path

BASE = Path("/home/workspace")
SOURCE = BASE / "Projects/TRU/ship/tru-logos-source"
SHELL = SOURCE / "shell/TRU_LOGOS_shell.html"
MANIFEST = SOURCE / "manifest.json"
OUT = BASE / "TRU_GIGA.html"

TAG_RE = re.compile(r'(<script type="application/json" id="([^"]+)">)(</script>)')

EXTRA_JSON = [
    (BASE / "Projects/TRU/data/wordnet_compact.json", "wordnet-compacted"),
    (BASE / "Projects/TRU/data/kjv_full.json", "kjv-full"),
    (BASE / "Projects/TRU/data/TRU_MEGA_BRAIN.json", "tru-mega-brain"),
    (BASE / "Projects/TRU/data/brain_canonical.json", "brain-canonical"),
    (BASE / "Projects/TRU/data/tru_merged_brain.json", "tru-merged-brain"),
    (BASE / "Projects/TRU/data/xref_compact.json", "xref-compact"),
    (BASE / "Projects/TRU/data/strongs_verse_index.json", "strongs-verse-index"),
    (BASE / "Projects/TRU/data/strongs_verse_index_compact.json", "strongs-verse-index-compact"),
    (BASE / "Projects/TRU/data/strongs_lexicon_kaiserlik.json", "strongs-lexicon-kaiserlik"),
    (BASE / "Projects/TRU/omega/data/glossary.json", "omega-glossary"),
    (BASE / "Projects/TRU/omega/data/index.json", "omega-index"),
]

ARCHIVE_GROUPS = [
    ("TRU_*.html", "tru-html-archive"),
    ("TRU_APEX*.html", "tru-apex-archive"),
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: Path):
    return json.loads(read_text(path))


def fill_shell() -> str:
    shell = read_text(SHELL)
    manifest = load_json(MANIFEST)
    modules = {m["id"]: m for m in manifest}

    def fill(match: re.Match) -> str:
        open_tag, sid, close_tag = match.group(1), match.group(2), match.group(3)
        if sid not in modules:
            raise SystemExit(f"shell references missing data id: {sid}")
        data_path = SOURCE / modules[sid]["file"]
        return f"{open_tag}{read_text(data_path)}{close_tag}"

    return TAG_RE.sub(fill, shell)


def inject_extra_json_blocks(html: str) -> str:
    insert_at = html.rfind("</body>")
    if insert_at == -1:
        raise SystemExit("could not find </body> in shell output")

    head = html[:insert_at]
    tail = html[insert_at:]

    parts = [head]
    for path, block_id in EXTRA_JSON:
        if not path.exists():
            continue
        raw = read_text(path)
        parts.append(f'<script type="application/json" id="{block_id}">{raw}</script>')
    parts.append(tail)

    return "\n".join(parts)


def append_archive_payloads(out_path: Path) -> None:
    groups: list[Path] = []
    for pattern, _ in ARCHIVE_GROUPS:
        groups.extend(sorted(BASE.glob(pattern)))
    groups = [p for p in groups if p.is_file() and p.name != out_path.name]

    with out_path.open("a", encoding="utf-8") as f:
        f.write("\n<script type=\"application/json\" id=\"tru-archive-index\">[\n")
        first = True
        for path in groups:
            data = path.read_bytes()
            b64 = base64.b64encode(data).decode("ascii")
            item = {"name": path.name, "bytes": path.stat().st_size, "b64": b64}
            if not first:
                f.write(",\n")
            first = False
            f.write(json.dumps(item, ensure_ascii=False, separators=(",", ":")))
        f.write("\n]</script>\n")


def main() -> None:
    core = fill_shell()
    core = core.replace("TRU LOGOS", "TRU GIGA", 1)
    core = core.replace("offline • sovereign", "offline • sovereign • merged • archive", 1)

    merged = inject_extra_json_blocks(core)
    OUT.write_text(merged, encoding="utf-8")
    append_archive_payloads(OUT)

    sz = OUT.stat().st_size
    print(f"built {OUT}")
    print(f"size: {sz:,} bytes ({sz/1024/1024:.2f} MB)")
    print(f"archive payload files: {len([p for pattern,_ in ARCHIVE_GROUPS for p in BASE.glob(pattern) if p.is_file() and p.name != OUT.name])}")


if __name__ == "__main__":
    main()
