# Valencia Marathon 2026 — Training Plan Project

This repo holds a personal marathon training plan and publishes it as an interactive
web page via GitHub Pages. It can also sync the plan to Intervals.icu.

## Files

- `plan.json` — the single source of truth for the whole plan (weeks, workouts, zones, race strategy).
- `generate_plan.py` — rebuilds `plan.json` from code. Edit this for structural changes (phases, long-run ramp, paces), then run it.
- `template.html` — the viewer UI. Contains the placeholder `__PLAN_JSON__`.
- `build_site.py` — injects `plan.json` into `template.html` and writes `index.html`.
- `index.html` — the built site that GitHub Pages serves. **Generated — do not hand-edit.**
- `sync_intervals.py` — pushes the plan to Intervals.icu as structured workouts with heart-rate targets. Reads `INTERVALS_API_KEY` from the environment.

## How to make changes

When the user asks to change the plan (e.g. "shift the goal pace", "add a week", "make week 12 a recovery week", "the race moved"):

1. Edit `generate_plan.py` (preferred) or `plan.json` directly for small tweaks.
2. Run `python3 generate_plan.py` if you edited the generator.
3. **Always** run `python3 build_site.py` afterward to rebuild `index.html` so the visual stays in sync.
4. If the user wants the watch/calendar updated too, run `python3 sync_intervals.py`
   (only works when `INTERVALS_API_KEY` is set — it is provided as a secret in CI).
5. Commit with a clear message and open a pull request. Do not force-push to `main`.

## Conventions

- The plan is for a first-time marathoner. Keep progression conservative: long-run jumps ≤ ~2 km/week, a recovery (cutback) week every 3–4 weeks, never shorten the 3-week taper, peak long run 30 km.
- All workout intensity targets are **heart-rate based** (`% HR` of max HR). Do not switch to pace targets unless explicitly asked.
- Max HR assumption is 188, LTHR 168. If the user updates these, change them in `generate_plan.py` zones and mention they must also be set in Intervals.icu Run settings.
- Keep `index.html` a single self-contained file (no external assets besides Google Fonts).

## Guardrails

- Never print or echo `INTERVALS_API_KEY` or any secret.
- `sync_intervals.py` deletes and recreates planned events in the plan's date range only; it never touches completed activities. Mention this when you run it.
- After any change, verify `python3 build_site.py` runs cleanly before committing.
