"""Valencia Marathon 2026 — REVISION 3 (Aug 16 check-in).
16 weeks: Mon 17 Aug 2026 -> race Sun 6 Dec 2026.
Athlete ahead of schedule: 15 km done at 6:28/km, HR 146, only +3bpm drift over 96 min.
EF +14% since June. Cadence 143 -> 165. Goal pace revised 6:55 -> 6:20/km.
"""
import json
from datetime import date, timedelta

PLAN_START = date(2026, 8, 17)
RACE_DATE  = date(2026, 12, 6)
TOTAL_WEEKS = 16

STRENGTH_A = {"name":"Strength A — Lower Body Foundation","description":"Knee insurance. Single-leg & glute work. Critical now that long runs pass 20 km.","durationMinutes":30,
 "humanReadable":("Warm-up (5 min): leg swings, hip circles, glute bridges 2x10\nMain (3 rounds, 60s rest):\n  • Bodyweight squats — 12 reps\n  • Reverse lunges — 8 each leg\n  • Single-leg glute bridges — 10 each leg\n  • Calf raises — 15 reps\n  • Side-lying clamshells — 12 each side\nCool-down (5 min): hip flexor & quad stretches")}
STRENGTH_B = {"name":"Strength B — Core & Stability","description":"Core + single-leg balance. Protects form when you fatigue late in long runs.","durationMinutes":25,
 "humanReadable":("Warm-up (5 min): cat-cow, bird-dog 2x8\nMain (3 rounds, 45s rest):\n  • Plank — 30–45s\n  • Side plank — 20–30s each side\n  • Dead bug — 8 each side\n  • Single-leg deadlift — 8 each leg\n  • Step-ups onto chair — 10 each leg\nCool-down (5 min): pigeon stretch, child's pose")}
MOB = {"name":"Mobility & Recovery","description":"Light movement — supports recovery.","durationMinutes":15,
 "humanReadable":("10–15 min:\n  • Foam roll quads, calves, glutes (5 min)\n  • Hip flexor stretch 60s each\n  • Hamstring stretch 60s each\n  • Ankle circles & calf stretch")}

def mid(w,d,s): return f"w{w}-{d.lower()[:3]}-{s}"
def rest(w,dn,mo=False):
    if mo:
        x=dict(MOB); x.update(id=mid(w,dn,"mob"),sport="mobility",type="recovery",primaryZone="Recovery",completed=False); return x
    return {"id":mid(w,dn,"rest"),"sport":"rest","type":"rest","name":"Rest Day","description":"Full recovery — adaptation happens now.","humanReadable":"Sleep, hydrate, eat well. Light walking is fine.","completed":False}
def stg(w,dn,v="A"):
    x=dict(STRENGTH_A if v=="A" else STRENGTH_B); x.update(id=mid(w,dn,"str"),sport="strength",type="strength",primaryZone="Z2",completed=False); return x
def rn(w,dn,**kw):
    x={"id":mid(w,dn,"run"),"sport":"run","type":"run","completed":False}; x.update(kw); return x

# ---- workout builders (paces updated to Aug fitness) ----
def easy(mins,km=None,note="Easy/conversational. HR 135–148. Let pace be whatever that allows."):
    return {"name":f"Easy Run — {mins} min","description":note,"durationMinutes":mins,"distanceKm":km,"primaryZone":"Z2 Easy",
        "humanReadable":f"Warm-up: 5 min very easy\nMain: {mins-10} min easy (HR 135–148, ~6:30–7:00/km)\nCool-down: 5 min easy + stretch"}
def opt(mins,km=None):
    return {"name":f"Easy Run — {mins} min (optional 4th run)","description":"Optional. Run only if recovery is good — skip freely on bad-sleep weeks.","durationMinutes":mins,"distanceKm":km,"primaryZone":"Z2 Easy",
        "humanReadable":f"OPTIONAL — only if you feel fresh.\nWarm-up: 5 min\nMain: {mins-10} min very easy (HR <145)\nCool-down: 5 min\n\nTired, poor sleep, or any knee signal? Do mobility instead."}
def long(km,mp=0,note=""):
    if mp:
        return {"name":f"Long Run — {km} km (last {mp} km @ MP)","description":note or "Marathon-specific. Race-pace on tired legs + full fuel rehearsal.","distanceKm":km,"durationMinutes":int(km*6.6),"primaryZone":"Z2 + Z3 (MP)",
            "humanReadable":f"Warm-up: 1 km very easy\nMain:\n  • {km-mp} km easy (HR 138–150, ~6:40–7:00/km)\n  • {mp} km @ marathon pace (6:20/km, HR 152–162)\nCool-down: 5 min walk\nFuel: 30g carbs every 30 min after the first hour. Water every 15 min."}
    return {"name":f"Long Run — {km} km","description":note or "The engine of your marathon. Keep it genuinely easy — time on feet beats pace.","distanceKm":km,"durationMinutes":int(km*6.8),"primaryZone":"Z2 Easy",
        "humanReadable":f"Warm-up: 1 km very easy\nMain: {km-1} km easy (HR 138–150, ~6:40–7:05/km)\nCool-down: 5 min walk + stretches\nFuel: after 75 min take 30g carbs. Water every 15 min."}
def strides(mins,n):
    return {"name":f"Easy + {n} Strides — {mins} min","description":"Easy aerobic plus short pickups to hold leg speed and high cadence.","durationMinutes":mins,"primaryZone":"Z2 + Strides",
        "humanReadable":f"Warm-up: 15 min easy\nMain: {mins-25} min easy\nStrides: {n} x 20s acceleration to ~5K effort, 60s walk between\nCool-down: 5 min easy"}
def hills(mins,n):
    return {"name":f"Hill Repeats — {mins} min","description":"Dune hill strength. Builds power with less impact than flat speedwork.","durationMinutes":mins,"primaryZone":"Z4–Z5",
        "humanReadable":f"Warm-up: 15 min easy to your hill\nMain: {n} x 30s uphill hard (~5K effort, HR 168+), jog/walk down for full recovery (90s)\nCool-down: 10 min easy"}
def tempo(mins,n,blk):
    return {"name":f"Tempo — {n}x{blk} min","description":"Threshold work. Raises the ceiling your marathon pace sits under.","durationMinutes":mins,"primaryZone":"Z4 Tempo",
        "humanReadable":f"Warm-up: 15 min easy\nMain: {n} x {blk} min @ tempo (5:50–6:05/km, HR 162–172), 3 min jog recovery\nCool-down: 10 min easy"}
def mpint(mins,n,work):
    return {"name":f"MP Intervals — {n} x {work}","description":"Lock in goal marathon pace and rhythm.","durationMinutes":mins,"primaryZone":"Z3 Marathon Pace",
        "humanReadable":f"Warm-up: 15 min easy\nMain: {n} x {work} @ marathon pace (6:20/km, HR 152–162), 2 min jog recovery\nCool-down: 10 min easy"}
def mpblock(mins,mp):
    return {"name":f"Marathon Pace Block — {mp} min @ MP","description":"Sustained goal-pace work — the cornerstone session.","durationMinutes":mins,"primaryZone":"Z3 Marathon Pace",
        "humanReadable":f"Warm-up: 15 min easy\nMain: {mp} min continuous @ marathon pace (6:20/km, HR 152–162)\nCool-down: 10 min easy"}

# (phase, focus, hours, recovery, mon, tue, wed, thu, fri, sat, sun)
W=[]
W.append(("Build","Consolidate the 15 km jump",6.5,False,("s","B"),("r",strides(45,5)),("r",opt(35,5)),("r",easy(45,7)),("s","A"),("r",long(16)),"rest"))
W.append(("Build","Tempo returns + 18 km",7.5,False,("s","B"),("r",easy(50,7.5)),("r",opt(40,6)),("r",tempo(60,3,10)),("s","A"),("r",long(18)),"rest"))
W.append(("Build","Recovery week — absorb",5.5,True,"rest",("r",easy(40,6)),("m",None),("r",easy(45,7)),("s","A"),("r",long(13)),"rest"))
W.append(("Build","Marathon pace introduced",8.0,False,("s","B"),("r",easy(50,7.5)),("r",opt(40,6)),("r",mpint(55,4,"1.5 km")),("s","A"),("r",long(20)),"rest"))
W.append(("Build","First 22 km",8.5,False,("s","B"),("r",easy(50,7.5)),("r",opt(40,6)),("r",mpblock(60,25)),("s","A"),("r",long(22)),"rest"))
W.append(("Build","Recovery week",6.0,True,"rest",("r",easy(40,6)),("m",None),("r",strides(45,5)),("s","A"),("r",long(16)),"rest"))
W.append(("Build","Sharpen the top end",9.0,False,("s","B"),("r",easy(50,7.5)),("r",opt(40,6)),("r",hills(50,8)),("s","A"),("r",long(24,4,"Last 4 km at MP — first taste of race pace on tired legs.")),"rest"))
W.append(("Build","26 km with MP finish",9.5,False,("s","B"),("r",easy(55,8)),("r",opt(40,6)),("r",tempo(60,3,12)),("s","A"),("r",long(26,6,"Last 6 km at MP. Rehearse your fuel plan exactly.")),"rest"))
W.append(("Peak","Recovery week — don't skip",6.5,True,"rest",("r",easy(45,7)),("m",None),("r",easy(50,7.5)),("s","A"),("r",long(18)),"rest"))
W.append(("Peak","28 km — the confidence run",10.0,False,("s","B"),("r",easy(55,8)),("r",opt(40,6)),("r",mpblock(65,35)),("s","A"),("r",long(28,8,"Last 8 km at MP. Full dress rehearsal: gear, breakfast, gels.")),"rest"))
W.append(("Peak","30 km",10.5,False,("s","B"),("r",easy(55,8)),("r",opt(40,6)),("r",mpint(60,5,"2 km")),("s","A"),("r",long(30,6,"Steady, then 6 km at MP. This is the big one.")),"rest"))
W.append(("Peak","Recovery week",7.0,True,"rest",("r",easy(45,7)),("m",None),("r",easy(50,7.5)),("s","A"),("r",long(20)),"rest"))
W.append(("Peak","🏔️ PEAK — 32 km",11.0,False,("s","B"),("r",easy(50,7.5)),("r",opt(40,6)),("r",mpblock(60,30)),("s","A"),("r",long(32,0,"🏔️ Peak long run. Easy pace throughout. Your confidence bank for race day.")),"rest"))
W.append(("Taper","Taper begins — volume down, sharpness held",8.0,True,("s","B"),("r",easy(45,7)),("r",opt(35,5)),("r",mpblock(50,25)),"rest",("r",long(22)),"rest"))
W.append(("Taper","Legs fresh, mind sharp",6.0,True,("s","A"),("r",easy(40,6)),("m",None),("r",mpint(40,4,"1 km")),"rest",("r",long(14)),"rest"))
W.append(("Taper","🏁 RACE WEEK",4.0,True,"rest",("r",easy(30,4.5,"Easy shake-out. Legs should feel springy.")),("m",None),("r",strides(25,4)),"rest",
  ("r",{"name":"Pre-race shake-out — 15 min","description":"Fire the legs, nothing more.","durationMinutes":15,"primaryZone":"Z2 Easy","humanReadable":"10 min very easy + 4x 20s strides + 5 min walk.\nEat well, hydrate, sleep early. Lay out gear tonight."}),
  ("r",{"name":"🏁 VALENCIA MARATHON 42.2 km","description":"RACE DAY! See Race Strategy tab.","distanceKm":42.2,"durationMinutes":267,"primaryZone":"Z3 Marathon Pace","humanReadable":"Goal 6:20/km (~4:27). First 10 km at 6:30 — deliberately held back. Settle into 6:20 from km 10. Walk aid stations to fuel cleanly. 30g carbs every 30 min from km 8. The training is in your legs."})))
assert len(W)==TOTAL_WEEKS, len(W)

def build(i,t):
    order=["mon","tue","wed","thu","fri","sat","sun"]
    names=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    ws=PLAN_START+timedelta(weeks=i-1); days=[]; rh=rk=rn_=0
    for j,cell in enumerate(t[4:]):
        d=ws+timedelta(days=j)
        if cell=="rest": wos=[rest(i,names[j])]
        elif isinstance(cell,tuple) and cell[0]=="m": wos=[rest(i,names[j],True)]
        elif isinstance(cell,tuple) and cell[0]=="s": wos=[stg(i,names[j],cell[1])]
        elif isinstance(cell,tuple) and cell[0]=="r":
            wos=[rn(i,names[j],**cell[1])]
            mm=cell[1].get("durationMinutes",0) or 0; rh+=mm/60
            if cell[1].get("distanceKm"): rk+=cell[1]["distanceKm"]
            rn_+=1
        else: wos=[]
        days.append({"date":d.isoformat(),"dayOfWeek":names[j],"workouts":wos})
    return days,{"totalHours":round(rh,1),"bySport":{"run":{"sessions":rn_,"hours":round(rh,1),"km":round(rk,1)}}}

weeks=[]
for i,t in enumerate(W,1):
    days,summ=build(i,t); ws=PLAN_START+timedelta(weeks=i-1)
    weeks.append({"weekNumber":i,"startDate":ws.isoformat(),"endDate":(ws+timedelta(days=6)).isoformat(),
        "phase":t[0],"focus":t[1],"targetHours":t[2],"isRecoveryWeek":t[3],"days":days,"summary":summ})

plan={"version":"3.0","meta":{"id":"valencia-marathon-2026","athlete":"First-Time Marathoner","event":"Valencia Marathon 2026",
 "eventDate":RACE_DATE.isoformat(),"planStartDate":PLAN_START.isoformat(),"planEndDate":RACE_DATE.isoformat(),
 "createdAt":"2026-08-16T00:00:00Z","updatedAt":"2026-08-16T00:00:00Z","totalWeeks":TOTAL_WEEKS,"generatedBy":"Claude Coach",
 "revisionNote":"Revision 3 (Aug 16). 15 km at 6:28/km over ~378 m climbing, HR 146, +3bpm drift over 96 min. EF +14% since June, cadence 143->165. Goal pace revised 6:55 -> 6:20/km. Peak long run raised to 32 km. Hill repeats retained (dune terrain)."},
 "preferences":{"swim":"meters","bike":"kilometers","run":"kilometers","firstDayOfWeek":"monday"},
 "assessment":{
  "foundation":{"raceHistory":["No prior races — first marathon"],"peakTrainingLoad":"36 km/week, longest run 15 km","foundationLevel":"novice","yearsInSport":10,
   "notes":"8 weeks of consistent training with zero missed weeks. Handling 4 runs/week comfortably."},
  "currentForm":{"weeklyVolume":{"total":36,"run":36},"longestSessions":{"run":15},"consistency":"Excellent — no gaps since June 1",
   "notes":"15 km at 6:28/km over ~378 m of climbing, mean HR 146, peak 157, only +3 bpm drift over 96 min. Even 5 km splits (6:24/6:35/6:24). Efficiency factor up 14% since June."},
  "strengths":[{"sport":"run","evidence":"Only +3 bpm cardiac drift over 96 min on hilly terrain — exceptional aerobic control"},
   {"sport":"run","evidence":"Cadence improved 143 -> 165 spm, reducing impact load per step"},
   {"sport":"run","evidence":"Efficiency factor +14% in 8 weeks (same HR, 1:10/km faster)"},
   {"sport":"general","evidence":"Zero missed training weeks; knee has stayed symptom-free"}],
  "limiters":[{"sport":"strength","evidence":"Only 2 strength sessions logged since June — the main injury risk as volume climbs"},
   {"sport":"run","evidence":"Untested beyond 15 km; the 25–42 km range is entirely unknown territory"},
   {"sport":"run","evidence":"Long runs carry ~25 m/km of climbing — great training, but means flat-ground race pace is still unmeasured"}],
  "constraints":["3–4 running days/week","9-to-5 work + two children (1 yo & 11 yo)","Bodyweight strength only (home)","Rolling dune terrain near the coast — hillier than the flat Valencia course"]},
 "zones":{"run":{"hr":{"lthr":170,"maxEstimated":188,
   "notes":"Observed max 183 in hard sessions. Zones validated against 8 weeks of data — easy runs sit correctly at 142–147.",
   "zones":[{"zone":1,"name":"Recovery","hrLow":0,"hrHigh":132,"feels":"Very easy — chatty"},
     {"zone":2,"name":"Easy/Aerobic","hrLow":132,"hrHigh":150,"feels":"Conversational — where most runs live"},
     {"zone":3,"name":"Marathon Pace","hrLow":150,"hrHigh":162,"feels":"Comfortably hard, full sentences"},
     {"zone":4,"name":"Tempo","hrLow":162,"hrHigh":172,"feels":"Hard — short phrases only"},
     {"zone":5,"name":"Threshold","hrLow":172,"hrHigh":185,"feels":"Very hard — single words"}]},
  "pace":{"marathonGoalPace":"6:20/km","marathonGoalRange":"6:10–6:35/km (4:20–4:38 finish)",
   "easy":"6:30–7:00/km","longRun":"6:40–7:05/km","tempo":"5:50–6:05/km","threshold":"5:30–5:45/km",
   "notes":"Revised UP from 6:55/km after the 15 km at 6:28 with negligible drift. Final goal confirmed after the 26–28 km runs in October."}}},
 "phases":[
  {"name":"Build","startWeek":1,"endWeek":8,"focus":"Tempo + MP work, long run to 26 km","weeklyHoursRange":{"low":5.5,"high":9.5},"keyWorkouts":["Long run","Tempo","MP blocks","Hill repeats"]},
  {"name":"Peak","startWeek":9,"endWeek":13,"focus":"Marathon-specific, long run to 32 km","weeklyHoursRange":{"low":6.5,"high":11},"keyWorkouts":["Long run with MP finish","MP blocks"]},
  {"name":"Taper","startWeek":14,"endWeek":16,"focus":"Cut volume, hold sharpness, race","weeklyHoursRange":{"low":4,"high":8},"keyWorkouts":["MP intervals","Easy + strides","Race day"]}],
 "weeks":weeks,
 "raceStrategy":{"event":{"name":"Valencia Marathon 2026","date":RACE_DATE.isoformat(),"type":"Marathon","distance":42.2},
  "pacing":{"strategy":"Controlled negative split — hold back early, press late",
   "firstHalf":{"target":"6:30/km for the first 10 km","notes":"DELIBERATELY slower than goal. It will feel far too easy — that is exactly right."},
   "secondHalf":{"target":"6:20/km from km 10","notes":"If you reach 32 km still strong, press to 6:10. Otherwise hold."},
   "targetHR":"152–162 bpm","lastTenK":"Whatever remains. Aim to pass people from km 32 on.",
   "warnings":"Your easy pace is now ~6:25, so 6:20 will feel deceptively comfortable at the start. The marathon punishes that feeling at km 32. Hold the leash for 10 km."},
  "nutrition":{"preRace":"Night before: pasta + lean protein, nothing new. 3 hr before: ~100g carbs (oatmeal, banana, honey, low fibre). Coffee 60 min before if usual.",
   "during":{"carbsPerHour":"60–80g","fluidPerHour":"500–750 ml",
    "schedule":"Gel at km 8, then every 5 km (8/13/18/23/28/33/37). ~25g each. Walk aid stations to drink properly.",
    "products":"Only what you have practised in long runs."},
   "rule":"Nothing new on race day. Lock the fuel protocol in from the 24 km run onward."},
  "raceMorning":{"wakeUp":"3:00 hrs before start","breakfast":"2:30–3:00 before — familiar carbs only","warmUp":"10 min easy + 4 strides, 30 min before","gear":"Only what you have trained in. New shoes = blisters."},
  "mentalCues":["Km 1–10: 'Too easy. Good. That's the plan.'","Km 11–21: 'Rhythm. Drink. Fuel. Relax the shoulders.'",
   "Km 22–32: 'Now the race starts. Quick feet, tall posture.'","Km 33–42: 'Everyone hurts now. The 32 km run is in my legs. One km at a time.'"],
  "postRace":{"immediate":"Keep walking 10 min. Electrolytes. Eat within 30 min.","next72hrs":"Light walking only. No running. Sleep.","return":"First easy jog 5–7 days after. Two unstructured weeks before any structure."}},
 "coachingNotes":[
  "📈 REVISION 3 (Aug 16): Your 15 km at 6:28/km with mean HR 146 and only +3 bpm drift over 96 minutes is a genuinely strong aerobic performance. Efficiency factor is up 14% since June at identical heart rate. Goal pace moves from 6:55 to 6:20/km (~4:27 finish).",
  "🎯 The new goal is provisional. It is built on a 15 km effort — the 26 km and 28 km runs in October are what actually confirm it. If those go well, 6:10 is on the table. If they hurt, we move back toward 6:35. No ego either way.",
  "👟 Cadence went 143 → 165 spm. That is a real, meaningful change: shorter stride, less impact per footfall, and very likely part of why the knee has stayed quiet. Keep it there — the strides sessions exist partly to maintain it.",
  "💪 STRENGTH IS THE GAP. Two sessions logged since June. You are about to double your long run from 15 to 32 km. Single-leg and glute work is what keeps a quiet knee quiet under that load. Monday and Friday, 25–30 minutes. This is the one thing in the plan I would not negotiate on.",
  "⛰️ Your runs carry real climbing — the 15 km had ~378 m of ascent (124 flights), the 12 km on Aug 2 had ~418 m. The Elevation Ascended field exports blank, but Flights Climbed captures it. Hill repeats stay in the plan. Valencia is pancake-flat, so your flat-ground pace is very likely 10–20 sec/km quicker than these numbers suggest — the 6:20 goal has margin.",
  "🏃 Long runs are now the whole game: 16 → 18 → 20 → 22 → 24 → 26 → 28 → 30 → 32 km. Keep them at HR 138–150 (~6:40–7:05/km) — slower than your easy runs. Time on feet builds the durability that pace cannot.",
  "😴 Recovery is your real limiter (work + a 1-year-old). The Wednesday run stays OPTIONAL. Three quality runs beat four tired ones, every time.",
  "🥗 From the 24 km run onward, practise race fuelling exactly: 30g carbs every 30 min. Your gut needs training as much as your legs.",
  "⌚ Duplicate 'Indoor Run' entries appeared alongside outdoor runs in July–early August (Watchletic recording without GPS). They stopped after Aug 4 — worth confirming your recording setup is clean so training load isn't double-counted.",
  "🧪 Next checkpoint: after the 26 km run (week 8, early October). Export then and we will finalise race pace."]}

with open("plan.json","w") as f: json.dump(plan,f,indent=2,ensure_ascii=False)
lr=[w['days'][5]['workouts'][0].get('distanceKm') or 0 for w in weeks]
print(f"✓ {TOTAL_WEEKS} weeks: {PLAN_START} → {RACE_DATE}")
print(f"✓ Long-run ramp: {lr}")
print(f"✓ Phases: " + ", ".join(f"{p['name']} W{p['startWeek']}-{p['endWeek']}" for p in plan['phases']))
print(f"✓ Goal: {plan['zones']['run']['pace']['marathonGoalPace']} → {plan['zones']['run']['pace']['marathonGoalRange']}")
