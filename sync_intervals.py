#!/usr/bin/env python3
"""
sync_intervals.py — push the plan to your Intervals.icu calendar with %HR targets.

Reads plan.json, turns each session into a structured workout (heart-rate targets
as % of max HR), then REPLACES the planned events in the plan's date range:
it deletes the existing planned workouts/notes we created and re-creates them.
Completed activities are never touched (those are a different endpoint).

The API key is read from the environment, NOT hardcoded:
    export INTERVALS_API_KEY=xxxxxxxx
    python3 sync_intervals.py

Options:
    --dry-run     show what would change, make no calls
"""
import os
import re
import sys
import json
import time
import base64
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).parent
API_KEY = os.environ.get("INTERVALS_API_KEY", "").strip()
ATHLETE_ID = os.environ.get("INTERVALS_ATHLETE_ID", "0").strip()
DRY = "--dry-run" in sys.argv
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")

# --- HR target bands as % of MAX HR (set Max HR correctly in Intervals.icu Run settings) ---
REC, EASY, LONG = "55-78% HR", "70-80% HR", "68-79% HR"
MP, TEMPO, THRESH = "80-86% HR", "86-92% HR", "90-98% HR"
STRIDE, HILL = "82-100% HR", "86-100% HR"

def steps_for(wo):
    n = wo["name"].lower(); dur = wo.get("durationMinutes"); dist = wo.get("distanceKm")
    m = re.search(r"long run — (\d+) km \(last (\d+) km @ mp\)", n)
    if m:
        t, mp = int(m.group(1)), int(m.group(2)); return [f"- {t-mp}km {LONG}", f"- {mp}km {MP}"]
    m = re.search(r"long run — (\d+) km", n)
    if m:
        km = int(m.group(1)); return [f"- 1km {REC}", f"- {km-1}km {LONG}"]
    m = re.search(r"easy \+ (\d+) strides — (\d+) min", n)
    if m:
        ns, mins = int(m.group(1)), int(m.group(2))
        return [f"- 15m {EASY}", f"{ns}x", f"- 20s {STRIDE}", f"- 60s {REC}", f"- {max(mins-15-ns,5)}m {EASY}"]
    m = re.search(r"easy run — (\d+) min", n)
    if m:
        mins = int(m.group(1)); return [f"- 5m {REC}", f"- {mins-10}m {EASY}", f"- 5m {REC}"]
    if "hill repeats" in n:
        mr = re.search(r"(\d+) x 30s uphill", wo.get("humanReadable", "")); reps = int(mr.group(1)) if mr else 5
        return [f"- 15m {EASY}", f"{reps}x", f"- 30s {HILL}", f"- 90s {REC}", f"- 10m {REC}"]
    m = re.search(r"(\d+)\s*x\s*(\d+)\s*min", n)
    if m and "tempo" in n:
        reps, mins = int(m.group(1)), int(m.group(2))
        return [f"- 15m {EASY}", f"{reps}x", f"- {mins}m {TEMPO}", f"- 3m {REC}", f"- 10m {REC}"]
    m = re.search(r"mp intervals — (\d+) x ([\d.]+)\s*(km|m)", n)
    if m:
        reps = int(m.group(1)); work = f"{m.group(2)}km" if m.group(3) == "km" else f"{m.group(2)}m"
        return [f"- 15m {EASY}", f"{reps}x", f"- {work} {MP}", f"- 2m {REC}", f"- 10m {REC}"]
    m = re.search(r"marathon pace block — (\d+) min", n)
    if m:
        return [f"- 15m {EASY}", f"- {int(m.group(1))}m {MP}", f"- 10m {REC}"]
    if "pre-race shake-out" in n:
        return [f"- 10m {EASY}", "4x", f"- 20s {STRIDE}", f"- 60s {REC}", f"- 5m {REC}"]
    if "valencia marathon" in n:
        return [f"- 10km 75-82% HR", f"- 22km {MP}", f"- 10.2km 80-90% HR"]
    if dur: return [f"- {dur}m {EASY}"]
    if dist: return [f"- {dist}km {EASY}"]
    return None

def build_events(plan):
    events = []
    for wk in plan["weeks"]:
        for day in wk["days"]:
            for wo in day["workouts"]:
                s, date = wo["sport"], day["date"]
                if s == "run":
                    steps = steps_for(wo); dur = wo.get("durationMinutes")
                    secs = int(dur * 60) if dur else (int(wo["distanceKm"] * 7.2 * 60) if wo.get("distanceKm") else 1800)
                    events.append({"category": "WORKOUT", "start_date_local": f"{date}T07:00:00", "type": "Run",
                                   "name": wo["name"], "moving_time": secs, "description": "\n".join(steps)})
                elif s == "strength":
                    events.append({"category": "WORKOUT", "start_date_local": f"{date}T18:00:00", "type": "WeightTraining",
                                   "name": wo["name"], "moving_time": wo.get("durationMinutes", 30) * 60,
                                   "description": wo.get("humanReadable", "")[:500]})
                elif s == "mobility":
                    events.append({"category": "NOTE", "start_date_local": f"{date}T12:00:00",
                                   "name": "🧘 " + wo["name"], "description": wo.get("humanReadable", "")[:300]})
                elif s == "rest":
                    events.append({"category": "NOTE", "start_date_local": f"{date}T12:00:00",
                                   "name": "😴 Rest Day", "description": "Full recovery. Sleep, hydrate, eat well."})
    return events

def req(method, url, body=None):
    auth = base64.b64encode(f"API_KEY:{API_KEY}".encode()).decode()
    headers = {"Authorization": f"Basic {auth}", "Accept": "application/json", "User-Agent": UA}
    data = None
    if body is not None:
        data = json.dumps(body).encode(); headers["Content-Type"] = "application/json"
    r = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(r, timeout=30) as resp:
        return resp.status, resp.read().decode("utf-8", "ignore")

def main():
    if not API_KEY and not DRY:
        sys.exit("ERROR: set INTERVALS_API_KEY in the environment first (or use --dry-run).")
    plan = json.loads((ROOT / "plan.json").read_text(encoding="utf-8"))
    start = plan["meta"]["planStartDate"]; end = plan["meta"]["eventDate"]
    events = build_events(plan)
    print(f"Plan {start} → {end}: {len(events)} events to sync.")
    if DRY:
        print("DRY RUN — no changes made. First 3 events:")
        for e in events[:3]:
            print(" ", e["name"], "|", e.get("description", "").replace("\n", " / ")[:60])
        return

    base = f"https://intervals.icu/api/v1/athlete/{ATHLETE_ID}/events"
    _, raw = req("GET", f"{base}?oldest={start}&newest={end}")
    existing = json.loads(raw) if raw.strip().startswith("[") else []
    old = [e for e in existing if e.get("category") in ("WORKOUT", "NOTE")]
    print(f"Removing {len(old)} existing planned entries...")
    for e in old:
        try: req("DELETE", f"{base}/{e['id']}")
        except Exception as ex: print("  del error:", ex)
        time.sleep(0.1)
    print(f"Creating {len(events)} updated entries...")
    ok = 0
    for e in events:
        try:
            st, _ = req("POST", base, e)
            if st in (200, 201): ok += 1
        except urllib.error.HTTPError as ex:
            print("  post error:", ex.code, ex.read().decode("utf-8", "ignore")[:120])
        time.sleep(0.1)
    print(f"Done. {ok}/{len(events)} synced. Re-import in Watchletic to pull the updates.")

if __name__ == "__main__":
    main()
