#!/usr/bin/env python3
"""
build_site.py — rebuild index.html (the visual plan) from plan.json + template.html.

Run after changing plan.json (or after generate_plan.py):
    python3 build_site.py

Writes index.html in the repo root, which GitHub Pages serves.
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
plan = (ROOT / "plan.json").read_text(encoding="utf-8")
template = (ROOT / "template.html").read_text(encoding="utf-8")

html = template.replace("__PLAN_JSON__", plan)
(ROOT / "index.html").write_text(html, encoding="utf-8")

p = json.loads(plan)
print(f"Built index.html — {p['meta']['event']}, {p['meta']['totalWeeks']} weeks "
      f"({p['meta']['planStartDate']} → {p['meta']['eventDate']})")
