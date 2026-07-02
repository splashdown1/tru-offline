#!/usr/bin/env python3
"""build tru_all_knowledge.html.

one file, one engine, all knowledge layers merged into the main brain:
- canonical brain
- core / super / mega / knowledge-bank nodes
- drop brain / scripture / lexicon / encyclopedia / filings
- the normal shell modules for dictionary, encyclopedia, kjv, strongs, xref, life, and ancient knowledge
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

BASE = Path("/home/workspace")
SOURCE = BASE / "Projects/TRU/ship/tru-logos-source"
SHELL = SOURCE / "shell/TRU_LOGOS_shell.html"
MANIFEST = SOURCE / "manifest.json"
OUT = BASE / "TRU_ALL_KNOWLEDGE.html"

CORE_BRAIN_SOURCES = [
    BASE / "Projects/TRU/data/TRU_CORE_KB.json",
    BASE / "Projects/TRU/data/TRU_SUPER_BRAIN.json",
    BASE / "Projects/TRU/data/TRU_MEGA_BRAIN.json",
    BASE / "Projects/TRU/data/tru-knowledge-bank.json",
    BASE / "Projects/TRU/data/tru_phase15_brain.json",
    BASE / "Projects/TRU/data/tru_brain_1290_nodes.json",
]

DROP_DIRS = [
    BASE / "Projects/TRU/drop/brain",
    BASE / "Projects/TRU/drop/scripture",
    BASE / "Projects/TRU/drop/lexicon",
    BASE / "Projects/TRU/drop/encyclopedia",
    BASE / "Projects/TRU/drop/filings",
]

NODE_FIELDS = ("k", "v", "w", "t", "source", "ref")
TAG_RE = re.compile(r'(<script type="application/json" id="([^"]+)">)(</script>)')


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: Path):
    return json.loads(read_text(path))


def norm(value) -> str:
    return str(value).strip().lower().replace(" ", "_")


def compact(value) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def node_ok(node) -> bool:
    return isinstance(node, dict) and "k" in node and "v" in node


def coerce_node(node, fallback_source: str = ""):
    if not isinstance(node, dict):
        return None
    k = node.get("k") or node.get("key") or node.get("id") or node.get("ref")
    v = node.get("v")
    if v is None:
        v = node.get("value") or node.get("definition") or node.get("text") or node.get("d") or node.get("gloss") or node.get("meaning")
    if k is None or v is None:
        return None
    out = {"k": str(k), "v": str(v)}
    for field in NODE_FIELDS[2:]:
        val = node.get(field)
        if val is not None:
            out[field] = val
    if fallback_source and "source" not in out:
        out["source"] = fallback_source
    return out


def extract_nodes(data, fallback_source: str = ""):
    if isinstance(data, list):
        out = []
        for item in data:
            node = coerce_node(item, fallback_source)
            if node:
                out.append(node)
        return out

    if isinstance(data, dict):
        for key in ("brain", "nodes", "entries", "data", "items"):
            if key in data and isinstance(data[key], list):
                out = []
                for item in data[key]:
                    if key == "entries" and isinstance(item, dict):
                        node = {
                            "k": item.get("key") or item.get("id") or item.get("ref") or item.get("k"),
                            "v": item.get("definition") or item.get("text") or item.get("value") or item.get("v"),
                            "w": item.get("score") if item.get("score") is not None else item.get("w"),
                            "t": item.get("type") or item.get("t") or "fact",
                            "source": item.get("source") or fallback_source or "KB",
                            "ref": item.get("ref"),
                        }
                        node = coerce_node(node, fallback_source)
                    else:
                        node = coerce_node(item, fallback_source)
                    if node:
                        out.append(node)
                return out
        vals = list(data.values())
        if vals and all(isinstance(v, dict) for v in vals):
            out = []
            for key, item in data.items():
                node = coerce_node({"k": key, **item}, fallback_source)
                if node:
                    out.append(node)
            if out:
                return out
    node = coerce_node(data, fallback_source)
    return [node] if node else []


def add_node(merged, node):
    if not node_ok(node):
        return 0
    key = norm(node["k"])
    current = merged.get(key)
    if current is None or len(str(node.get("v", ""))) > len(str(current.get("v", ""))):
        merged[key] = {field: node.get(field) for field in NODE_FIELDS if node.get(field) is not None}
        return 1
    return 0


def ingest_json_file(path: Path, merged, fallback_source: str = ""):
    if not path.exists():
        return 0
    try:
        data = load_json(path)
    except Exception:
        return 0
    count = 0
    for node in extract_nodes(data, fallback_source):
        count += add_node(merged, node)
    return count


def ingest_dir(pattern: Path, merged, fallback_source: str = ""):
    count = 0
    for path in sorted(pattern.glob("*")):
        if path.suffix.lower() not in {".json", ".txt"}:
            continue
        if path.name.lower().startswith("wordnet"):
            continue
        try:
            if path.suffix.lower() == ".txt":
                text = path.read_text(encoding="utf-8", errors="ignore")
                node = {"k": path.stem, "v": text, "source": fallback_source or path.parent.name.upper(), "t": path.parent.name}
                count += add_node(merged, node)
                continue
            data = load_json(path)
        except Exception:
            continue
        if path.parent.name == "scripture":
            verses = data if isinstance(data, list) else data.get("verses") or data.get("data") or []
            for verse in verses:
                if not isinstance(verse, dict):
                    continue
                ref = verse.get("ref") or verse.get("k")
                text = verse.get("text") or verse.get("v")
                if not ref or not text:
                    continue
                count += add_node(
                    merged,
                    {
                        "k": f"scripture_{norm(ref)}",
                        "v": str(text),
                        "source": "DROP_SCRIPTURE",
                        "t": "scripture",
                        "ref": str(ref),
                    },
                )
            continue
        if path.parent.name == "lexicon":
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, dict):
                        text = value.get("def") or value.get("d") or value.get("gloss") or value.get("meaning") or value.get("text")
                    else:
                        text = value
                    if not text:
                        continue
                    count += add_node(
                        merged,
                        {
                            "k": f"lex_{norm(key)}",
                            "v": str(text),
                            "source": "DROP_LEXICON",
                            "t": "lexicon",
                            "ref": str(key),
                        },
                    )
            continue
        for node in extract_nodes(data, fallback_source or f"DROP_{path.parent.name.upper()}"):
            count += add_node(merged, node)
    return count


def fill_shell() -> str:
    shell = read_text(SHELL)
    manifest = load_json(MANIFEST)
    modules = {m["id"]: m for m in manifest}

    def fill(match: re.Match) -> str:
        open_tag, sid, close_tag = match.group(1), match.group(2), match.group(3)
        if sid not in modules:
            raise SystemExit(f"shell references missing id: {sid}")
        return f"{open_tag}{read_text(SOURCE / modules[sid]['file'])}{close_tag}"

    return TAG_RE.sub(fill, shell)


def main() -> None:
    merged = {}

    print("merge canonical shell brain")
    ingest_json_file(SOURCE / "data/brain-data.json", merged, "SHELL_BRAIN")

    print("merge core knowledge banks")
    for path in CORE_BRAIN_SOURCES:
        added = ingest_json_file(path, merged, path.stem.upper())
        print(f"  +{added} from {path.name}")

    print("merge drop knowledge")
    for directory in DROP_DIRS:
        added = ingest_dir(directory, merged, directory.name.upper())
        print(f"  +{added} from {directory.name}/")

    brain_json = compact(list(merged.values()))
    print(f"merged brain nodes: {len(merged)}")

    out = fill_shell()
    out = re.sub(
        r'<script type="application/json" id="brain-data">.*?</script>',
        f'<script type="application/json" id="brain-data">{brain_json}</script>',
        out,
        count=1,
        flags=re.DOTALL,
    )
    out = out.replace("TRU LOGOS", "TRU ALL KNOWLEDGE", 1)
    out = out.replace("offline • sovereign", "offline • sovereign • all knowledge", 1)

    OUT.write_text(out, encoding="utf-8")
    sz = OUT.stat().st_size
    print(f"built {OUT}")
    print(f"size: {sz:,} bytes ({sz/1024/1024:.2f} MB)")


if __name__ == "__main__":
    main()
