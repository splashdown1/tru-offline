#!/usr/bin/env python3
"""smoke test for tru_ghost.py — builds the smallest possible ghost and asserts
the output is a self-contained html with bible data baked in.

run: python3 tests/test_ghost_build.py
exit 0 = pass, non-zero = fail
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GHOST = ROOT / "tru_ghost.py"


def run(args, stdin=None):
    r = subprocess.run(
        ["python3", str(GHOST), *args],
        capture_output=True,
        text=True,
        cwd=ROOT,
        input=stdin,
    )
    if r.returncode != 0:
        raise RuntimeError(f"ghost failed: {r.stderr}")
    return r.stdout


def assert_lookup(query, expect_kind, label):
    out = run(["--nt-only", "--cap", "50", "--lookup", query])
    r = json.loads(out)
    assert r.get("ok"), f"{label}: not ok: {r}"
    res = r.get("result", {})
    kind = res.get("kind")
    print(f"  {label}: {query!r} -> {kind} score={res.get('score')}")
    assert kind == expect_kind, f"{label}: expected {expect_kind}, got {kind}: {res}"


def test_lookups():
    print("[1/3] lookup routing")
    assert_lookup("john 3:16", "SCRIPTURE", "nt verse")
    assert_lookup("matt 5:9", "SCRIPTURE", "nt verse 2")


def test_min_build():
    print("[2/3] minimal build (nt-only, cap=50)")
    with tempfile.TemporaryDirectory() as tmp:
        run(["--nt-only", "--cap", "50", "--out-dir", tmp, "--ts", "smoke"])
        files = list(Path(tmp).glob("*.html"))
        assert files, "no html produced"
        html = files[0].read_text(encoding="utf-8")
        size = len(html)
        print(f"  produced {files[0].name} ({size} bytes)")
        assert size < 2_000_000, f"nt-only cap=50 should be <2mb, got {size}"
        assert "tru ghost" in html.lower(), "missing ghost branding"
        assert "const BRAIN=" in html, "brain not inlined"
        assert "const KJV=" in html, "kjv not inlined"
        assert "const SESSION=" in html, "session not inlined"
        # the smallest NT verse reference baked in
        assert "john 3:16" in html.lower() or "In the beginning" in html, "no scripture baked"


def test_full_build_no_cap():
    print("[3/3] full build (no cap) — sanity check, builds the 11.9mb monster")
    with tempfile.TemporaryDirectory() as tmp:
        out = run(["--out-dir", tmp, "--ts", "smoke-full"])
        r = json.loads(out)
        assert r.get("ok"), r
        size = r["bytes"]
        path = Path(r["path"])
        assert path.exists(), f"file missing: {path}"
        print(f"  produced {path.name} ({size} bytes)")
        # no cap should give us > 5mb (full kjv alone is 4.7mb)
        assert size > 5_000_000, f"full build should be >5mb, got {size}"


if __name__ == "__main__":
    if not GHOST.exists():
        print(f"FAIL: {GHOST} missing", file=sys.stderr)
        sys.exit(2)
    try:
        test_lookups()
        test_min_build()
        test_full_build_no_cap()
        print("\nOK — all smoke tests passed")
    except AssertionError as e:
        print(f"\nFAIL: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR: {e}", file=sys.stderr)
        sys.exit(2)
