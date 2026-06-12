#!/usr/bin/env python3
"""
TRU Contradiction Scanner
Detects when symbolic/mythological claims diverge from verified primaries.

Usage:
  python contradiction_scanner.py scan <claim>
  python contradiction_scanner.py batch
  python contradiction_scanner.py report
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

PRIMARIES_DIR = Path("/home/workspace/primaries")
CACHE_DIR = Path("/home/workspace/Projects/TRU/cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Known symbolic claims that should be checked against primaries
SYMBOLIC_CLAIMS = [
    {
        "id": "singularity_feb_2026",
        "claim": "The singularity arrived in February 2026",
        "source": "Peter Diamandis",
        "source_url": "https://x.com/PeterDiamandis",
        "category": "SYMBOL",
        "check_against": ["CURRENT_EVENTS", "TRUTH"],
        "verifiable": True,
    },
    {
        "id": "anthropic_s1_june_2026",
        "claim": "Anthropic filed S-1 in June 2026",
        "source": "SEC EDGAR",
        "source_url": "https://sec.gov",
        "category": "TRUTH",
        "check_against": ["TRUTH"],
        "verifiable": True,
    },
    {
        "id": "red_heifer_shiloh_2026",
        "claim": "Four red heifers are at Shiloh as of 2026",
        "source": "Temple Institute",
        "source_url": "https://templeinstitute.org",
        "category": "TRUTH",
        "check_against": ["TRUTH"],
        "verifiable": True,
    },
    {
        "id": "spacex_anthropic_compute",
        "claim": "Anthropic has $1.25B/month compute deal with SpaceX through 2029",
        "source": "SpaceX S-1",
        "source_url": "https://sec.gov",
        "category": "TRUTH",
        "check_against": ["TRUTH"],
        "verifiable": True,
    },
    {
        "id": "musk_180_day_lease",
        "claim": "Anthropic-SpaceX deal is a 180-day cancelable lease",
        "source": "Elon Musk X post",
        "source_url": "https://x.com/elonmusk",
        "category": "CURRENT_EVENTS",
        "check_against": ["TRUTH"],
        "verifiable": True,
        "contradicts": "spacex_anthropic_compute",
    },
    {
        "id": "newton_2060_2026",
        "claim": "Newton's 2060 prophecy compressed to 2026 via AI acceleration",
        "source": "MarineMechanic2",
        "source_url": "https://x.com/MarineMechanic2",
        "category": "SYMBOL",
        "check_against": [],
        "verifiable": False,
        "note": "Interpretive overlay, not falsifiable",
    },
    {
        "id": "april_3_singularity",
        "claim": "Singularity event occurred April 3, 2026",
        "source": "MarineMechanic2",
        "source_url": "https://x.com/MarineMechanic2",
        "category": "SYMBOL",
        "check_against": ["CURRENT_EVENTS", "TRUTH"],
        "verifiable": True,
    },
]


def load_primaries() -> Dict[str, List[Dict]]:
    """Load all primaries into memory, grouped by type."""
    primaries = {
        "sec": [],
        "temple": [],
        "arxiv": [],
    }
    
    # SEC filings
    sec_dir = PRIMARIES_DIR / "sec"
    if sec_dir.exists():
        for cik_dir in sec_dir.iterdir():
            if not cik_dir.is_dir():
                continue
            for fp in cik_dir.glob("*.json"):
                if fp.name.startswith("_") or fp.name == "compute_signals.json":
                    continue
                try:
                    with open(fp) as f:
                        rec = json.load(f)
                    primaries["sec"].append(rec)
                except Exception:
                    pass
    
    # Temple posts
    temple_file = PRIMARIES_DIR / "temple" / "temple_posts.json"
    if temple_file.exists():
        try:
            with open(temple_file) as f:
                primaries["temple"] = json.load(f)
        except Exception:
            pass
    
    # arxiv papers
    arxiv_file = PRIMARIES_DIR / "arxiv" / "arxiv_papers.json"
    if arxiv_file.exists():
        try:
            with open(arxiv_file) as f:
                primaries["arxiv"] = json.load(f)
        except Exception:
            pass
    
    return primaries


def verify_claim_against_primaries(claim: Dict, primaries: Dict) -> Dict:
    """Check if a claim is supported by primaries."""
    claim_id = claim["id"]
    claim_text = claim["claim"].lower()
    category = claim["category"]
    verifiable = claim.get("verifiable", True)
    
    if not verifiable:
        return {
            "claim_id": claim_id,
            "claim": claim["claim"],
            "category": category,
            "verdict": "NON_FALSIFIABLE",
            "confidence": 0.0,
            "evidence": [],
            "note": claim.get("note", "Symbolic claim, not verifiable"),
        }
    
    evidence = []
    
    # Check SEC filings
    if "TRUTH" in claim.get("check_against", []):
        for filing in primaries.get("sec", []):
            text = f"{filing.get('name', '')} {filing.get('form', '')} {filing.get('text_excerpt', '')}".lower()
            if any(kw in text for kw in extract_keywords(claim_text)):
                evidence.append({
                    "type": "sec_filing",
                    "source": filing.get("name"),
                    "form": filing.get("form"),
                    "date": filing.get("filing_date"),
                    "url": filing.get("source_url"),
                })
    
    # Check Temple posts
    if "TRUTH" in claim.get("check_against", []) and "red heifer" in claim_text:
        for post in primaries.get("temple", []):
            text = f"{post.get('title', '')} {post.get('content', '')}".lower()
            if "red heifer" in text or "shiloh" in text:
                evidence.append({
                    "type": "temple_post",
                    "title": post.get("title"),
                    "date": post.get("published") or post.get("date"),
                    "url": post.get("link") or post.get("url"),
                })
    
    # Determine verdict
    if category == "TRUTH":
        verdict = "VERIFIED" if evidence else "UNVERIFIED"
        confidence = 0.9 if evidence else 0.3
    elif category == "CURRENT_EVENTS":
        verdict = "CORROBORATED" if evidence else "UNSUBSTANTIATED"
        confidence = 0.7 if evidence else 0.3
    elif category == "SYMBOL":
        verdict = "SYMBOLIC_ONLY" if not evidence else "SYMBOL_WITH_EVIDENCE"
        confidence = 0.5 if evidence else 0.1
    else:
        verdict = "UNKNOWN"
        confidence = 0.0
    
    # Check for contradictions
    contradiction = None
    if claim.get("contradicts"):
        contradiction = {
            "contradicts_claim": claim["contradicts"],
            "description": f"This claim may contradict {claim['contradicts']}",
        }
    
    return {
        "claim_id": claim_id,
        "claim": claim["claim"],
        "category": category,
        "verdict": verdict,
        "confidence": confidence,
        "evidence": evidence[:5],
        "contradiction": contradiction,
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }


def extract_keywords(text: str) -> List[str]:
    """Extract meaningful keywords from claim text."""
    stopwords = {"the", "a", "an", "is", "are", "was", "were", "in", "on", "at", "to", "for"}
    words = re.findall(r"\b[a-z]{3,}\b", text.lower())
    return [w for w in words if w not in stopwords]


def scan_claim(claim_text: str) -> Dict:
    """Scan a single claim against primaries."""
    primaries = load_primaries()
    
    # Find matching claim template
    claim_template = None
    for c in SYMBOLIC_CLAIMS:
        if c["claim"].lower() in claim_text.lower() or claim_text.lower() in c["claim"].lower():
            claim_template = c
            break
    
    if not claim_template:
        claim_template = {
            "id": "custom_claim",
            "claim": claim_text,
            "category": "UNKNOWN",
            "check_against": ["TRUTH", "CURRENT_EVENTS"],
            "verifiable": True,
        }
    
    return verify_claim_against_primaries(claim_template, primaries)


def batch_scan() -> List[Dict]:
    """Scan all known claims."""
    primaries = load_primaries()
    results = []
    
    for claim in SYMBOLIC_CLAIMS:
        result = verify_claim_against_primaries(claim, primaries)
        results.append(result)
    
    # Save report
    report_path = CACHE_DIR / "contradiction_report.json"
    with open(report_path, "w") as f:
        json.dump({
            "scanned_at": datetime.now(timezone.utc).isoformat(),
            "total_claims": len(results),
            "results": results,
        }, f, indent=2)
    
    return results


def generate_report() -> str:
    """Generate human-readable report."""
    report_path = CACHE_DIR / "contradiction_report.json"
    if not report_path.exists():
        results = batch_scan()
    else:
        with open(report_path) as f:
            data = json.load(f)
        results = data.get("results", [])
    
    lines = [
        "# TRU Contradiction Scan Report",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Summary",
        f"Total claims scanned: {len(results)}",
        "",
    ]
    
    # Group by verdict
    by_verdict = {}
    for r in results:
        v = r["verdict"]
        by_verdict.setdefault(v, []).append(r)
    
    for verdict in ["VERIFIED", "CORROBORATED", "SYMBOL_WITH_EVIDENCE", "UNVERIFIED", "UNSUBSTANTIATED", "SYMBOLIC_ONLY", "NON_FALSIFIABLE"]:
        if verdict in by_verdict:
            lines.append(f"### {verdict} ({len(by_verdict[verdict])})")
            for r in by_verdict[verdict]:
                lines.append(f"- **{r['claim_id']}**: {r['claim']}")
                lines.append(f"  - Confidence: {r['confidence']:.1%}")
                if r.get("evidence"):
                    lines.append(f"  - Evidence: {len(r['evidence'])} sources")
                if r.get("contradiction"):
                    lines.append(f"  - ⚠️ Contradicts: {r['contradiction']['contradicts_claim']}")
            lines.append("")
    
    return "\n".join(lines)


def main():
    import sys
    
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "scan":
        if len(sys.argv) < 3:
            print("Usage: python contradiction_scanner.py scan <claim>")
            sys.exit(1)
        claim = " ".join(sys.argv[2:])
        result = scan_claim(claim)
        print(json.dumps(result, indent=2))
    
    elif cmd == "batch":
        results = batch_scan()
        print(f"Scanned {len(results)} claims")
        for r in results:
            print(f"  {r['claim_id']}: {r['verdict']} ({r['confidence']:.0%})")
    
    elif cmd == "report":
        report = generate_report()
        print(report)
    
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
