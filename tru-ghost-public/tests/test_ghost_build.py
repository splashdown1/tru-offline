#!/usr/bin/env python3
"""smoke test for tru_ghost.py.
asserts: (1) --help works, (2) --lookup routes a known verse
to SCRIPTURE, (3) a minimal build produces a valid html.

requires TRU_KJV env var pointing to a kjv json. if not set,
the test only runs (1) and (3) without scripture.
"""
import json, os, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GHOST = ROOT / "tru_ghost.py"
KJV = os.environ.get("TRU_KJV")


def run(args, stdin=None):
    r = subprocess.run(
        ["python3", str(GHOST), *args],
        capture_output=True, text=True, cwd=ROOT, input=stdin,
    )
    if r.returncode != 0:
        raise RuntimeError(f"ghost failed: stderr={r.stderr}")
    return r.stdout


def test_help():
    print("[1/3] --help")
    out = run(["--help"])
    assert "--nt-only" in out
    assert "--cap" in out
    print("  ok")


def test_lookup():
    print("[2/3] --lookup scripture routing")
    if not KJV or not Path(KJV).exists():
        print("  skip (TRU_KJV not set)")
        return
    out = run(["--nt-only", "--cap", "10", "--lookup", "john 3:16"])
    r = json.loads(out)
    assert r.get("ok"), r
    assert r["result"]["kind"] == "SCRIPTURE", r
    print(f"  john 3:16 -> {r['result']['kind']} score={r['result']['score']}")


def test_build():
    print("[3/3] minimal build (cap=10, no kjv)")
    with tempfile.TemporaryDirectory() as tmp:
        out = run(["--cap", "10", "--out-dir", tmp, "--ts", "smoke"])
        r = json.loads(out)
        assert r.get("ok"), r
        path = Path(r["path"])
        assert path.exists()
        html = path.read_text()
        assert "tru ghost" in html.lower()
        assert "const BRAIN=" in html
        print(f"  built {path.name} ({r['bytes']} bytes)")


if __name__ == "__main__":
    if not GHOST.exists():
        print(f"FAIL: {GHOST} missing", file=sys.stderr)
        sys.exit(2)
    try:
        test_help()
        test_lookup()
        test_build()
        print("\nOK")
    except AssertionError as e:
        print(f"\nFAIL: {e}", file=sys.stderr)
        sys.exit(1)
