"""Valencia Marathon 2026 — REVISION 2 (June 23 check-in).
24 weeks from Mon June 22, 2026 → race Sun Dec 6, 2026.
Athlete ahead of schedule: skipped re-base, running 4x/week continuous,
HR dropped ~20bpm at same pace over 3 weeks. Recalibrated paces + faster long-run build."""
import json
from datetime import date, timedelta

PLAN_START = date(2026, 6, 22)   # Monday — current week
RACE_DATE  = date(2026, 12, 6)   # Sunday
TOTAL_WEEKS = 24

STRENGTH_A = {"name": "Strength A — Lower Body Foundation", "description": "Knee insurance. Single-leg & glute work. Non-negotiable now that long runs are growing.",
    "humanReadable": ("Warm-up (5 min): leg swings, hip circles, glute bridges 2x10\nMain (3 rounds, 60s rest):\n  • Bodyweight squats — 12 reps (slow & controlled)\n  • Reverse lunges — 8 reps each leg\n  • Single-leg glute bridges — 10 reps each leg\n  • Calf raises — 15 reps\n  • Side-lying clamshells — 12 reps each side\nCool-down (5 min): hip flexor & quad stretches"), "durationMinutes": 30}
STRENGTH_B = {"name": "Strength B — Core & Stability", "description": "Core + single-leg balance for running economy and knee tracking.",
    "humanReadable": ("Warm-up (5 min): cat-cow, bird-dog 2x8\nMain (3 rounds, 45s rest):\n  • Plank — 30–45s\n  • Side plank — 20–30s each side\n  • Dead bug — 8 reps each side\n  • Single-leg deadlift (no weight) — 8 reps each leg\n  • Step-ups onto chair — 10 each leg\nCool-down (5 min): pigeon stretch, child's pose"), "durationMinutes": 25}
SHORT_MOBILITY = {"name": "Mobility & Recovery", "description": "Light movement — supports recovery.",
    "humanReadable": ("10–15 min total:\n  • Foam roll quads, calves, glutes (5 min)\n  • Hip flexor stretch — 60s each side\n  • Hamstring stretch — 60s each side\n  • Ankle circles & calf stretch — 30s each"), "durationMinutes": 15}

def make_id(week, day, sport): return f"w{week}-{day.lower()[:3]}-{sport}"
def rest_day(week, dayname, mobility=False):
    if mobility:
        wo = dict(SHORT_MOBILITY); wo.update(id=make_id(week,dayname,"mob"), sport="mobility", type="recovery", primaryZone="Recovery", completed=False); return wo
    return {"id": make_id(week,dayname,"rest"), "sport":"rest", "type":"rest", "name":"Rest Day", "description":"Full recovery — fitness is built during rest.", "humanReadable":"Sleep, hydrate, eat well. Light walking is fine.", "completed":False}
def strength(week, dayname, variant="A"):
    base = STRENGTH_A if variant=="A" else STRENGTH_B
    wo = dict(base); wo.update(id=make_id(week,dayname,"str"), sport="strength", type="strength", primaryZone="Z2", completed=False); return wo
def run(week, dayname, kind, **kw):
    wo = {"id": make_id(week,dayname,"run"), "sport":"run", "type":kind, "completed":False}; wo.update(kw); return wo

def easy_run(minutes, dist_km=None, notes="Easy/conversational. Keep HR under 150. This pace should feel comfortable."):
    return {"name": f"Easy Run — {minutes} min", "description": notes, "durationMinutes": minutes, "distanceKm": dist_km, "primaryZone": "Z2 Easy",
        "humanReadable": f"Warm-up: 5 min walk + light jog\nMain: {minutes-10} min easy (HR 135–150, pace 6:30–7:00/km)\nCool-down: 5 min walk + stretch"}
def opt_easy_run(minutes, dist_km=None):
    return {"name": f"Easy Run — {minutes} min (optional 4th run)", "description": "Optional. Run it if recovery is good — skip without guilt if tired or short on sleep.", "durationMinutes": minutes, "distanceKm": dist_km, "primaryZone": "Z2 Easy",
        "humanReadable": f"OPTIONAL 4th run — only if you feel fresh.\nWarm-up: 5 min walk\nMain: {minutes-10} min very easy (HR <145, pace 6:45–7:15/km)\nCool-down: 5 min walk\n\nIf knee feels anything, or sleep was bad, do mobility instead."}
def long_run(km, mp_km=0, notes=""):
    if mp_km>0:
        ez = km-mp_km
        return {"name": f"Long Run — {km} km (last {mp_km} km @ MP)", "description": notes or "Marathon-specific. Practice fueling & race pace on tired legs.", "distanceKm": km, "durationMinutes": int(km*7.1), "primaryZone": "Z2 + Z3 (MP)",
            "humanReadable": f"Warm-up: 1 km very easy\nMain:\n  • {ez} km @ easy (7:00–7:30/km, HR <150)\n  • {mp_km} km @ marathon pace (6:55/km, HR 155–165)\nCool-down: 5 min walk\nFuel: 30g carbs every 30 min after the first hour. Sip water every 15 min."}
    return {"name": f"Long Run — {km} km", "description": notes or "The engine of your marathon. Keep it SLOW — slower than your easy runs. Time on feet matters more than pace.", "distanceKm": km, "durationMinutes": int(km*7.3), "primaryZone": "Z2 Easy",
        "humanReadable": f"Warm-up: 5 min walk\nMain: {km} km easy (7:00–7:30/km, HR 135–150). Deliberately slow.\nCool-down: 5 min walk + stretches\nFuel: After 75 min, 30g carbs (gel/banana). Water every 15 min."}
def strides_run(minutes, n):
    return {"name": f"Easy + {n} Strides — {minutes} min", "description": "Easy aerobic with short pickups to keep leg speed sharp.", "durationMinutes": minutes, "primaryZone": "Z2 + Strides",
        "humanReadable": f"Warm-up: 5 min walk + 10 min easy\nMain: {minutes-25} min easy (6:30–7:00/km)\nStrides: {n} x 20s acceleration to ~5K pace on flat, 60s walk between\nCool-down: 5 min walk"}
def hill_run(minutes, n):
    return {"name": f"Hill Repeats — {minutes} min", "description": "Strength without speed-work impact. Great for the knee.", "durationMinutes": minutes, "primaryZone": "Z4 (uphill)",
        "humanReadable": f"Warm-up: 15 min easy to a 4–6% hill\nMain: {n} x 30s uphill strong (~5K effort), walk/jog down (90s)\nCool-down: 10 min easy"}
def tempo_run(minutes, txt, name):
    return {"name": name, "description": "Threshold work — builds the engine to hold marathon pace.", "durationMinutes": minutes, "primaryZone": "Z4 Tempo", "humanReadable": txt}
def mp_intervals(minutes, work, n, rec):
    return {"name": f"MP Intervals — {n} x {work}", "description": "Lock in goal marathon pace and rhythm.", "durationMinutes": minutes, "primaryZone": "Z3 Marathon Pace",
        "humanReadable": f"Warm-up: 15 min easy\nMain: {n} x {work} @ marathon pace (6:55/km, HR 155–165), {rec} jog recovery\nCool-down: 10 min easy"}
def mp_block(minutes, mp):
    return {"name": f"Marathon Pace Block — {mp} min @ MP", "description": "Sustained goal-pace work. Cornerstone of marathon prep.", "durationMinutes": minutes, "primaryZone": "Z3 Marathon Pace",
        "humanReadable": f"Warm-up: 15 min easy\nMain: {mp} min continuous @ marathon pace (6:55/km, HR 155–165)\nCool-down: 10 min easy"}

# week template: (phase, focus, target_h, recovery, mon, tue, wed, thu, fri, sat, sun)
W = []
# ───── BASE (wk 1–8) ─────
W.append(("Base","Settle into recalibrated easy pace",4.5,False,("strength","B"),("run",strides_run(35,4)),("run",opt_easy_run(30,4.3)),("run",easy_run(35,5)),("strength","A"),("run",long_run(7)),"rest"))
W.append(("Base","Introduce hill strength",5.0,False,("strength","B"),("run",easy_run(40,6)),("run",opt_easy_run(30,4.3)),("run",hill_run(40,5)),("strength","A"),("run",long_run(8)),"rest"))
W.append(("Base","Long run to 9 km",5.5,False,("strength","B"),("run",strides_run(40,5)),("run",opt_easy_run(35,5)),("run",easy_run(40,6)),("strength","A"),("run",long_run(9)),"rest"))
W.append(("Base","Recovery week — absorb",4.0,True,"rest",("run",easy_run(35,5)),("mob",None),("run",easy_run(35,5)),("strength","A"),("run",long_run(7)),"rest"))
W.append(("Base","Build to 10 km",5.5,False,("strength","B"),("run",strides_run(40,5)),("run",opt_easy_run(35,5)),("run",hill_run(45,6)),("strength","A"),("run",long_run(10)),"rest"))
W.append(("Base","First 12 km long run",6.0,False,("strength","B"),("run",easy_run(45,6.5)),("run",opt_easy_run(35,5)),("run",strides_run(45,6)),("strength","A"),("run",long_run(12,0,"🎉 Past your old 12K limit — new territory!")),"rest"))
W.append(("Base","Recovery week",4.5,True,"rest",("run",easy_run(35,5)),("mob",None),("run",easy_run(40,5.5)),("strength","A"),("run",long_run(9)),"rest"))
W.append(("Base","Tempo intro + 13 km",6.5,False,("strength","B"),("run",easy_run(45,6.5)),("run",opt_easy_run(35,5)),("run",tempo_run(50,"Warm-up: 15 min easy\nMain: 2 x 8 min @ tempo (6:00/km, HR 162–170), 3 min jog recovery\nCool-down: 10 min easy","Tempo Intro — 2x8 min")),("strength","A"),("run",long_run(13)),"rest"))
# ───── BUILD (wk 9–16) ─────
W.append(("Build","Extend tempo work",6.5,False,("strength","B"),("run",easy_run(45,6.5)),("run",opt_easy_run(40,5.5)),("run",tempo_run(55,"Warm-up: 15 min easy\nMain: 2 x 10 min @ tempo (6:00/km, HR 162–170), 3 min recovery\nCool-down: 10 min easy","Tempo — 2x10 min")),("strength","A"),("run",long_run(15)),"rest"))
W.append(("Build","Tempo + 16 km",7.5,False,("strength","B"),("run",easy_run(50,7)),("run",opt_easy_run(40,5.5)),("run",tempo_run(60,"Warm-up: 15 min easy\nMain: 3 x 10 min @ tempo (6:00/km, HR 162–170), 3 min recovery\nCool-down: 10 min easy","Tempo — 3x10 min")),("strength","A"),("run",long_run(16)),"rest"))
W.append(("Build","Recovery week",5.5,True,"rest",("run",easy_run(40,5.5)),("mob",None),("run",easy_run(45,6)),("strength","A"),("run",long_run(12)),"rest"))
W.append(("Build","Marathon-pace intro",7.5,False,("strength","B"),("run",easy_run(50,7)),("run",opt_easy_run(40,5.5)),("run",mp_intervals(55,"1 km",4,"2 min")),("strength","A"),("run",long_run(17)),"rest"))
W.append(("Build","MP intervals + 18 km",8.0,False,("strength","B"),("run",easy_run(50,7)),("run",opt_easy_run(40,5.5)),("run",mp_intervals(60,"1 km",5,"2 min")),("strength","A"),("run",long_run(18)),"rest"))
W.append(("Build","Recovery week",6.0,True,"rest",("run",easy_run(40,5.5)),("mob",None),("run",easy_run(45,6)),("strength","A"),("run",long_run(14)),"rest"))
W.append(("Build","First 20 km — half-marathon+",8.5,False,("strength","B"),("run",easy_run(50,7)),("run",opt_easy_run(40,5.5)),("run",mp_block(55,20)),("strength","A"),("run",long_run(20,0,"🏁 Half-marathon distance and beyond!")),"rest"))
W.append(("Build","Push to 22 km",9.0,False,("strength","B"),("run",easy_run(50,7)),("run",opt_easy_run(40,5.5)),("run",mp_block(60,25)),("strength","A"),("run",long_run(22)),"rest"))
# ───── PEAK (wk 17–21) ─────
W.append(("Peak","Marathon-specific endurance",9.5,False,("strength","B"),("run",easy_run(50,7)),("run",opt_easy_run(40,5.5)),("run",mp_block(60,30)),("strength","A"),("run",long_run(24,6,"Last 6 km @ MP. Full race-day fuel rehearsal.")),"rest"))
W.append(("Peak","Long run to 26 km",10.0,False,("strength","B"),("run",easy_run(50,7)),("run",opt_easy_run(40,5.5)),("run",mp_block(60,35)),("strength","A"),("run",long_run(26,8,"Last 8 km @ MP. Practice fueling protocol exactly.")),"rest"))
W.append(("Peak","Recovery week — DON'T skip",6.5,True,"rest",("run",easy_run(40,5.5)),("mob",None),("run",easy_run(45,6)),("strength","A"),("run",long_run(18)),"rest"))
W.append(("Peak","Long run to 28 km",10.0,False,("strength","B"),("run",easy_run(55,7.5)),("run",opt_easy_run(40,5.5)),("run",mp_block(60,40)),("strength","A"),("run",long_run(28,8,"Big day. Rehearse race gear, breakfast, fuel.")),"rest"))
W.append(("Peak","🏔️ PEAK — 30 km",10.5,False,("strength","B"),("run",easy_run(50,7)),("run",opt_easy_run(40,5.5)),("run",mp_block(55,25)),("strength","A"),("run",long_run(30,0,"🏔️ Peak long run. Easy pace. This is your confidence bank.")),"rest"))
# ───── TAPER (wk 22–24) ─────
W.append(("Taper","Begin taper — cut volume, hold sharpness",7.5,True,("strength","B"),("run",easy_run(45,6)),("run",opt_easy_run(35,5)),("run",mp_block(50,20)),"rest",("run",long_run(20)),"rest"))
W.append(("Taper","Stay sharp, legs fresh",5.5,True,("strength","A"),("run",easy_run(40,5.5)),("mob",None),("run",mp_intervals(40,"800 m",4,"2 min")),"rest",("run",long_run(14)),"rest"))
W.append(("Taper","🏁 RACE WEEK",4.0,True,"rest",("run",easy_run(30,4,"Easy shake-out. Legs should feel springy.")),("mob",None),("run",strides_run(25,4)),"rest",
    ("run",{"name":"Pre-race shake-out — 15 min","description":"Fire the legs, nothing more.","durationMinutes":15,"primaryZone":"Z2 Easy","humanReadable":"10 min very easy + 4x 20s strides + 5 min walk. Eat well, hydrate, sleep early. Lay out gear tonight."}),
    ("run",{"name":"🏁 VALENCIA MARATHON 42.2 km","description":"RACE DAY! See Race Strategy tab.","distanceKm":42.2,"durationMinutes":290,"primaryZone":"Z3 Marathon Pace","humanReadable":"Goal 6:55/km (~4:51). Negative split: first 10K at 7:05/km, settle into MP. Walk aid stations to fuel. 30g carbs every 30 min from km 8. Trust the build — it's in your legs."})))

assert len(W)==TOTAL_WEEKS, f"{len(W)} weeks"

def build(week_num, t):
    order=["mon","tue","wed","thu","fri","sat","sun"]; names=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    ws = PLAN_START + timedelta(weeks=week_num-1); days=[]; run_h=run_km=run_n=0
    cells = t[4:]
    for i,(dkey,cell) in enumerate(zip(order,cells)):
        d = ws + timedelta(days=i)
        if cell=="rest": wos=[rest_day(week_num,names[i])]
        elif isinstance(cell,tuple) and cell[0]=="mob": wos=[rest_day(week_num,names[i],mobility=True)]
        elif isinstance(cell,tuple) and cell[0]=="strength": wos=[strength(week_num,names[i],cell[1])]
        elif isinstance(cell,tuple) and cell[0]=="run":
            wo=run(week_num,names[i],"run",**cell[1]); wos=[wo]
            mins=cell[1].get("durationMinutes",0) or 0; run_h+=mins/60
            if cell[1].get("distanceKm"): run_km+=cell[1]["distanceKm"]
            run_n+=1
        else: wos=[]
        days.append({"date":d.isoformat(),"dayOfWeek":names[i],"workouts":wos})
    return days, {"totalHours":round(run_h,1),"bySport":{"run":{"sessions":run_n,"hours":round(run_h,1),"km":round(run_km,1)}}}

weeks_out=[]
for i,t in enumerate(W,1):
    days,summary=build(i,t); ws=PLAN_START+timedelta(weeks=i-1)
    weeks_out.append({"weekNumber":i,"startDate":ws.isoformat(),"endDate":(ws+timedelta(days=6)).isoformat(),
        "phase":t[0],"focus":t[1],"targetHours":t[2],"isRecoveryWeek":t[3],"days":days,"summary":summary})

plan={"version":"2.0","meta":{"id":"valencia-marathon-2026","athlete":"First-Time Marathoner","event":"Valencia Marathon 2026",
    "eventDate":RACE_DATE.isoformat(),"planStartDate":PLAN_START.isoformat(),"planEndDate":RACE_DATE.isoformat(),
    "createdAt":"2026-06-23T00:00:00Z","updatedAt":"2026-06-23T00:00:00Z","totalWeeks":TOTAL_WEEKS,"generatedBy":"Claude Coach",
    "revisionNote":"Revision 2 (June 23). Athlete ahead of plan after 3 strong weeks — skipped re-base, running 4x/week, HR down ~20bpm at same pace. Paces recalibrated faster; long-run ramp accelerated; now 24 weeks from current week."},
  "preferences":{"swim":"meters","bike":"kilometers","run":"kilometers","firstDayOfWeek":"monday"},
  "assessment":{
    "foundation":{"raceHistory":["No prior races — first marathon"],"peakTrainingLoad":"Now running 4x/week, 15–20 km/week","foundationLevel":"beginner→novice","yearsInSport":10,
      "notes":"3 weeks of consistent training logged. Adapted faster than expected — graduated out of re-base."},
    "currentForm":{"weeklyVolume":{"total":18,"run":18},"longestSessions":{"run":6},"consistency":"Strong — 11 runs in 3 weeks, no gaps",
      "notes":"Easy pace ~6:30/km at HR 140. Same pace as May baseline but 20 bpm lower HR — clear aerobic gains. Knee symptom-free. Added cycling + walks as cross-training."},
    "strengths":[{"sport":"run","evidence":"HR dropped from 159→139 at same 6:30/km pace over 3 weeks"},
      {"sport":"run","evidence":"Consistent 4x/week, tolerating continuous running well"},
      {"sport":"general","evidence":"Good long-run pacing instinct (ran 6km at 7:41/km, kept HR 141)"}],
    "limiters":[{"sport":"run","evidence":"Longest run still only 6 km — endurance is the gap to close"},
      {"sport":"strength","evidence":"Strength work only done occasionally — knee insurance is under-used"},
      {"sport":"general","evidence":"Recovery constrained by 1yo + work; 4 runs/week leaves little margin"}],
    "constraints":["3–4 training days/week","9-to-5 work + two children (1 yo & 11 yo)","Bodyweight strength only (home)","Knee currently symptom-free — keep it that way"]},
  "zones":{"run":{"hr":{"lthr":168,"maxEstimated":188,
      "notes":"Refined from 11 logged runs. Max HR 180 seen at hard effort; true max ~185–190. Validate Z4/Z5 with a 5K time trial around week 6.",
      "zones":[{"zone":1,"name":"Recovery","hrLow":0,"hrHigh":130,"feels":"Very easy — chatty"},
        {"zone":2,"name":"Easy/Aerobic","hrLow":130,"hrHigh":150,"feels":"Conversational — where most runs live"},
        {"zone":3,"name":"Marathon Pace","hrLow":150,"hrHigh":162,"feels":"Comfortably hard, full sentences"},
        {"zone":4,"name":"Tempo","hrLow":162,"hrHigh":172,"feels":"Hard — short phrases only"},
        {"zone":5,"name":"Threshold","hrLow":172,"hrHigh":185,"feels":"Very hard — single words"}]},
    "pace":{"marathonGoalPace":"6:55/km","marathonGoalRange":"6:45–7:05/km (4:45–4:59 finish)",
      "easy":"6:30–7:00/km","longRun":"7:00–7:30/km (deliberately slower)","tempo":"5:55–6:10/km","threshold":"5:30–5:45/km",
      "notes":"Recalibrated UP from your logged data. Long runs slower than easy runs on purpose. Goal pace held conservative until your 18–22km runs prove what you can sustain — likely revisit down then."}}},
  "phases":[
    {"name":"Base","startWeek":1,"endWeek":8,"focus":"Aerobic base + long run to 13 km","weeklyHoursRange":{"low":4,"high":6.5},"keyWorkouts":["Long run","Hill repeats","Strides","Tempo intro"]},
    {"name":"Build","startWeek":9,"endWeek":16,"focus":"Tempo + MP work, long run to 22 km","weeklyHoursRange":{"low":5.5,"high":9},"keyWorkouts":["Tempo runs","MP intervals","MP blocks","Long runs"]},
    {"name":"Peak","startWeek":17,"endWeek":21,"focus":"Marathon-specific, long run 30 km","weeklyHoursRange":{"low":6.5,"high":10.5},"keyWorkouts":["Long run with MP","MP blocks"]},
    {"name":"Taper","startWeek":22,"endWeek":24,"focus":"Cut volume, stay sharp, race","weeklyHoursRange":{"low":4,"high":7.5},"keyWorkouts":["Easy + strides","Race day"]}],
  "weeks":weeks_out,
  "raceStrategy":{"event":{"name":"Valencia Marathon 2026","date":RACE_DATE.isoformat(),"type":"Marathon","distance":42.2},
    "pacing":{"strategy":"Conservative negative split for a first marathon",
      "firstHalf":{"target":"7:00–7:05/km","notes":"DELIBERATELY hold back. The first 10 km should feel TOO easy — that's correct."},
      "secondHalf":{"target":"6:50–7:00/km if feeling good","notes":"Reach 30 km feeling fresh, then press slightly. Otherwise hold."},
      "targetHR":"150–162 bpm","lastTenK":"Whatever's left. Pass people from km 32 on.",
      "warnings":"Your easy pace is quick now, which will tempt you to start fast. Don't. Endurance, not speed, is the unknown in your first marathon."},
    "nutrition":{"preRace":"Night before: pasta + lean protein, nothing new. 3 hr before: 100g carbs (oatmeal+banana+honey, low fiber). 1 cup coffee 60 min before if usual.",
      "during":{"carbsPerHour":"60–80g","fluidPerHour":"500–750 ml","schedule":"Gel at km 8, then every 5 km (8/13/18/23/28/33/37). ~25g carbs each. Walk aid stations to drink cleanly.","products":"Only what you've practiced in long runs."},
      "rule":"Nothing new on race day. Lock your fuel protocol in long runs from week 15."},
    "raceMorning":{"wakeUp":"3:00 hrs before start","breakfast":"2:30–3:00 before — familiar carbs only","warmUp":"10 min easy + 4 strides 30 min before","gear":"Only what you've trained in. New = blisters."},
    "mentalCues":["Km 1–10: 'Easy. So easy. Supposed to feel slow.'","Km 11–21: 'Settle in. Rhythm. Drink and fuel.'","Km 22–32: 'Now the race begins. Stay relaxed.'","Km 33–42: 'Everyone hurts now. The training is in my legs. One km at a time.'"],
    "postRace":{"immediate":"Keep walking 10 min. Electrolytes. Eat within 30 min.","next72hrs":"Light walking only. No running. Sleep. Celebrate!","return":"First easy jog 5–7 days after. Two weeks unstructured before structure."}},
  "coachingNotes":[
    "📅 REVISION 2 (June 23): Rebuilt to 24 weeks from your current week. You skipped re-base and adapted well, so this starts in Base. Peak (30 km) & 3-week taper unchanged.",
    "📈 Your data: easy pace held at ~6:30/km while HR dropped from 159→139 over 3 weeks. That's real aerobic fitness. Paces recalibrated faster to match.",
    "🏃 THE LONG RUN IS THE JOB NOW. Your runs cluster at 4–6 km; the marathon is won on the Saturday long run. It grows ~1–2 km/week. Keep it SLOWER than your easy runs (7:00–7:30/km).",
    "💪 Strength is your weak link — you said 'occasionally.' Two real sessions a week (Mon + Fri). This is what keeps the knee quiet as long runs pass 15 km. Don't skip it.",
    "🦵 Knee is symptom-free — protect that. The cautious progression that built it still applies: any sharp or persistent pain = scale back immediately, see a physio. Achy/stiff is normal.",
    "😴 Recovery is your real limiter (1yo + work). The Wednesday run is OPTIONAL — skip it freely on bad-sleep weeks. 3 quality runs > 4 tired ones.",
    "🥗 As long runs grow, fuel them: ~250–350g carbs on long-run days. Practice race fuel from week 15.",
    "⌚ Keep exporting from your Watch every few weeks. The HR-at-pace trend is exactly how we'll know if the goal time can come down. Next check-in: after your first 18–20 km run.",
    "🧪 Around week 6, do a 5K time trial (all-out, flat) to validate your tempo/threshold zones — they're still estimated."]}

with open("plan.json","w") as f: json.dump(plan,f,indent=2,ensure_ascii=False)
lr=[w['days'][5]['workouts'][0].get('distanceKm') or 0 for w in plan['weeks']]
print(f"✓ {plan['meta']['totalWeeks']} weeks: {plan['meta']['planStartDate']} → {plan['meta']['eventDate']}")
print(f"✓ Long-run ramp: {lr}")
print(f"✓ Phases: " + ", ".join(f"{p['name']} W{p['startWeek']}-{p['endWeek']}" for p in plan['phases']))