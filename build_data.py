#!/usr/bin/env python3
"""Generates poems.js (full data with slugs) consumed by index.html and poem.html."""
import json
import re

with open("poems-data.json") as f:
    poems = json.load(f)

def slugify(title):
    s = title.lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    s = re.sub(r"-+", "-", s)
    return s[:60]

seen = {}
for i, p in enumerate(poems):
    base = slugify(p["title"])
    slug = base
    n = 2
    while slug in seen:
        slug = f"{base}-{n}"
        n += 1
    seen[slug] = True
    p["slug"] = slug
    p["id"] = i + 1
    p["wordCount"] = len(p["body"].split())
    lines = [l for l in p["body"].split("\n") if l.strip()]
    p["firstLine"] = lines[0] if lines else ""

with open("js/poems-data.js", "w") as f:
    f.write("// Auto-generated. Source of truth: poems-data.json\n")
    f.write("const POEMS = ")
    f.write(json.dumps(poems, indent=2, ensure_ascii=False))
    f.write(";\n")

print(f"Wrote {len(poems)} poems to js/poems-data.js")
for p in poems:
    print(f"  {p['id']:2d}. /poem.html?p={p['slug']}")
