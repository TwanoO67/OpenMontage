#!/usr/bin/env python3
"""Search the awesome-opus-5-5-video-prompts library (LeaddeOpenLab).

Keeps a sparse, media-free clone in a local cache and queries the per-case
metadata in data/library/<id>.json.

    vpl.py sync                      # clone or pull (prompts + metadata only)
    vpl.py categories                # categories with case counts
    vpl.py search remotion explainer # keyword search (AND), ranked by likes
    vpl.py search --category manim --tool remotion --full-prompt --limit 10
    vpl.py show 2103449416325890146  # full prompt card (prompts/<id>.md)
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

REPO_URL = "https://github.com/LeaddeOpenLab/awesome-opus-5-5-video-prompts.git"
CACHE = Path(os.environ.get(
    "VPL_CACHE", Path.home() / ".cache" / "openmontage" / "awesome-opus-5-5-video-prompts"))
SPARSE = ["/README.md", "/prompts/", "/data/library/", "/data/categories/", "/data/docs/", "/templates/"]


def git(*args, cwd=None):
    subprocess.run(["git", *args], cwd=cwd, check=True)


def sync(_args=None):
    if (CACHE / ".git").exists():
        git("pull", "--ff-only", "--quiet", cwd=CACHE)
    else:
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        git("clone", "--quiet", "--depth", "1", "--filter=blob:none", "--sparse", REPO_URL, str(CACHE))
        git("sparse-checkout", "set", "--no-cone", *SPARSE, cwd=CACHE)
    n = len(list((CACHE / "data" / "library").glob("*.json")))
    print(f"synced {n} cases -> {CACHE}")


def ensure():
    if not (CACHE / "data" / "library").exists():
        sync()


def load_cases():
    ensure()
    for p in sorted((CACHE / "data" / "library").glob("*.json")):
        try:
            d = json.loads(p.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        a = d.get("analysis") or {}
        ev = a.get("caseEvidence") or {}
        post = d.get("post") or {}
        yield {
            "id": p.stem,
            "title": ev.get("title") or d.get("summaryEn") or "",
            "category": a.get("category") or ev.get("task") or "",
            "use": a.get("useCase") or "",
            "tools": [t.get("name", "") for t in ev.get("tools") or []],
            "inputs": (ev.get("fieldReview") or {}).get("inputSummary")
            or "; ".join(i.get("name") or i.get("description") or "" for i in ev.get("inputs") or [] if isinstance(i, dict)),
            "prompt_status": (ev.get("prompt") or {}).get("status") or "",
            "tier": (ev.get("publication") or {}).get("tier") or "",
            "likes": (post.get("metrics") or {}).get("likeCount") or 0,
            "duration": (ev.get("video") or {}).get("duration") or "",
            "aspect": (ev.get("video") or {}).get("aspectRatio") or "",
            "prompt": (a.get("translations") or {}).get("en") or d.get("prompt") or "",
            "summary": a.get("summary") or d.get("summary") or "",
            "url": post.get("canonicalUrl") or d.get("xUrl") or "",
        }


def search(args):
    terms = [t.lower() for t in args.terms]
    hits = []
    for c in load_cases():
        if args.category and c["category"] != args.category:
            continue
        if args.tool and not any(args.tool.lower() in t.lower() for t in c["tools"]):
            continue
        if args.full_prompt and c["prompt_status"] != "full_original":
            continue
        if args.verified and c["tier"] != "verified":
            continue
        hay = " ".join([c["title"], c["use"], c["summary"], c["prompt"], " ".join(c["tools"])]).lower()
        if all(t in hay for t in terms):
            hits.append(c)
    hits.sort(key=lambda c: c["likes"], reverse=True)
    for c in hits[: args.limit]:
        print(f"{c['id']}  [{c['category']}] {c['title']}")
        print(f"    use: {c['use']} | tools: {', '.join(c['tools']) or '-'} | "
              f"{c['duration'] or '?'} {c['aspect']} | prompt: {c['prompt_status']} | "
              f"tier: {c['tier']} | likes: {c['likes']}")
        print(f"    inputs: {c['inputs'] or '-'}")
    print(f"\n{len(hits)} match(es), showing {min(len(hits), args.limit)}")


def categories(_args):
    counts = {}
    for c in load_cases():
        counts[c["category"]] = counts.get(c["category"], 0) + 1
    for k, v in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"{v:5d}  {k or '(none)'}")


def show(args):
    ensure()
    p = CACHE / "prompts" / f"{args.id}.md"
    if not p.exists():
        sys.exit(f"no prompt card for {args.id}")
    print(p.read_text())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("sync").set_defaults(fn=sync)
    sub.add_parser("categories").set_defaults(fn=categories)
    s = sub.add_parser("search")
    s.add_argument("terms", nargs="*")
    s.add_argument("--category")
    s.add_argument("--tool")
    s.add_argument("--full-prompt", action="store_true", help="only cases whose full original prompt is published")
    s.add_argument("--verified", action="store_true", help="only cases the maintainers reproduced")
    s.add_argument("--limit", type=int, default=15)
    s.set_defaults(fn=search)
    sh = sub.add_parser("show")
    sh.add_argument("id")
    sh.set_defaults(fn=show)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
