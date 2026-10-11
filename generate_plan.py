"""Valencia Marathon 2026 — REVISION 4 (Oct 11 check-in).
16 weeks: Mon 17 Aug 2026 -> race Sun 6 Dec 2026.

Rev 3 (Aug 16): goal pace 6:55 -> 6:20/km, peak long run 32 km, hills kept (dune terrain).
Rev 4 (Oct 11): week 8 (Oct 5-11) lost to a business trip + illness. The missed week takes the
place of the recovery week that was scheduled next; week 9 becomes a gentle return week, the
missed 26 km MP run moves to Oct 24, 30 km on Oct 31, 32 km peak and taper unchanged.
Goal pace 6:20 -> ~6:00/km on the evidence of the 24 km (last 4 km at 5:48-5:51, HR 154-160)
and MP sessions (5:15-5:35 at HR 152-161). Marathon-pace HR band lowered to 145-158.

Weeks 1-7 are history and keep their Rev 3 wording; paces are switched to the Rev 4 set
before week 9 is built.
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

# ---- pace/HR wording used inside workout descriptions ----
# Rev 3 wording (weeks 1-7, kept as history)
P_REV3 = {"easy_hr":"HR 135–148","easy_pace":"~6:30–7:00/km",
          "long_easy":"HR 138–150, ~6:40–7:05/km","long_mp_easy":"HR 138–150, ~6:40–7:00/km",
          "mp":"6:20/km, HR 152–162","tempo":"5:50–6:05/km, HR 162–172",
          "long_min":6.8,"long_min_mp":6.6}
# Rev 4 wording (weeks 9-16), from the Aug-Oct data
P_REV4 = {"easy_hr":"HR 132–148","easy_pace":"~6:00–6:30/km",
          "long_easy":"HR 138–148, ~6:10–6:40/km","long_mp_easy":"HR 138–148, ~6:10–6:30/km",
          "mp":"~6:00/km, HR 145–158","tempo":"~5:05–5:20/km, HR 162–172",
          "long_min":6.4,"long_min_mp":6.3}
P = dict(P_REV3)

def mid(w,d,s): return f"w{w}-{d.lower()[:3]}-{s}"
def rest(w,dn,mo=False):
    if mo:
        x=dict(MOB); x.update(id=mid(w,dn,"mob"),sport="mobility",type="recovery",primaryZone="Recovery",completed=False); return x
    return {"id":mid(w,dn,"rest"),"sport":"rest","type":"rest","name":"Rest Day","description":"Full recovery — adaptation happens now.","humanReadable":"Sleep, hydrate, eat well. Light walking is fine.","completed":False}
def stg(w,dn,v="A"):
    x=dict(STRENGTH_A if v=="A" else STRENGTH_B); x.update(id=mid(w,dn,"str"),sport="strength",type="strength",primaryZone="Z2",completed=False); return x
def rn(w,dn,**kw):
    x={"id":mid(w,dn,"run"),"sport":"run","type":"run","completed":False}; x.update(kw); return x
def missed(w,dn,planned):
    return {"id":mid(w,dn,"missed"),"sport":"missed","type":"missed","name":"Missed — trip / illness",
            "description":f"Planned: {planned}","completed":False,
            "humanReadable":"Week lost to a business trip followed by illness. Not made up — the plan absorbs it (see Revision 4)."}

# ---- workout builders (read the current wording from P at call time) ----
def easy(mins,km=None,note=None):
    return {"name":f"Easy Run — {mins} min","description":note or f"Easy/conversational. {P['easy_hr']}. Let pace be whatever that allows.","durationMinutes":mins,"distanceKm":km,"primaryZone":"Z2 Easy",
        "humanReadable":f"Warm-up: 5 min very easy\nMain: {mins-10} min easy ({P['easy_hr']}, {P['easy_pace']})\nCool-down: 5 min easy + stretch"}
def opt(mins,km=None):
    return {"name":f"Easy Run — {mins} min (optional 4th run)","description":"Optional. Run only if recovery is good — skip freely on bad-sleep weeks.","durationMinutes":mins,"distanceKm":km,"primaryZone":"Z2 Easy",
        "humanReadable":f"OPTIONAL — only if you feel fresh.\nWarm-up: 5 min\nMain: {mins-10} min very easy (HR <145)\nCool-down: 5 min\n\nTired, poor sleep, or any knee signal? Do mobility instead."}
def long(km,mp=0,note=""):
    if mp:
        return {"name":f"Long Run — {km} km (last {mp} km @ MP)","description":note or "Marathon-specific. Race-pace on tired legs + full fuel rehearsal.","distanceKm":km,"durationMinutes":int(km*P['long_min_mp']),"primaryZone":"Z2 + Z3 (MP)",
            "humanReadable":f"Warm-up: 1 km very easy\nMain:\n  • {km-mp} km easy ({P['long_mp_easy']})\n  • {mp} km @ marathon pace ({P['mp']})\nCool-down: 5 min walk\nFuel: 30g carbs every 30 min after the first hour. Water every 15 min."}
    return {"name":f"Long Run — {km} km","description":note or "The engine of your marathon. Keep it genuinely easy — time on feet beats pace.","distanceKm":km,"durationMinutes":int(km*P['long_min']),"primaryZone":"Z2 Easy",
        "humanReadable":f"Warm-up: 1 km very easy\nMain: {km-1} km easy ({P['long_easy']})\nCool-down: 5 min walk + stretches\nFuel: after 75 min take 30g carbs. Water every 15 min."}
def strides(mins,n):
    return {"name":f"Easy + {n} Strides — {mins} min","description":"Easy aerobic plus short pickups to hold leg speed and high cadence.","durationMinutes":mins,"primaryZone":"Z2 + Strides",
        "humanReadable":f"Warm-up: 15 min easy\nMain: {mins-25} min easy\nStrides: {n} x 20s acceleration to ~5K effort, 60s walk between\nCool-down: 5 min easy"}
def hills(mins,n):
    return {"name":f"Hill Repeats — {mins} min","description":"Dune hill strength. Builds power with less impact than flat speedwork.","durationMinutes":mins,"primaryZone":"Z4–Z5",
        "humanReadable":f"Warm-up: 15 min easy to your hill\nMain: {n} x 30s uphill hard (~5K effort, HR 168+), jog/walk down for full recovery (90s)\nCool-down: 10 min easy"}
def tempo(mins,n,blk):
    return {"name":f"Tempo — {n}x{blk} min","description":"Threshold work. Raises the ceiling your marathon pace sits under.","durationMinutes":mins,"primaryZone":"Z4 Tempo",
        "humanReadable":f"Warm-up: 15 min easy\nMain: {n} x {blk} min @ tempo ({P['tempo']}), 3 min jog recovery\nCool-down: 10 min easy"}
def mpint(mins,n,work):
    return {"name":f"MP Intervals — {n} x {work}","description":"Lock in goal marathon pace and rhythm.","durationMinutes":mins,"primaryZone":"Z3 Marathon Pace",
        "humanReadable":f"Warm-up: 15 min easy\nMain: {n} x {work} @ marathon pace ({P['mp']}), 2 min jog recovery\nCool-down: 10 min easy"}
def mpblock(mins,mp):
    return {"name":f"Marathon Pace Block — {mp} min @ MP","description":"Sustained goal-pace work — the cornerstone session.","durationMinutes":mins,"primaryZone":"Z3 Marathon Pace",
        "humanReadable":f"Warm-up: 15 min easy\nMain: {mp} min continuous @ marathon pace ({P['mp']})\nCool-down: 10 min easy"}

# (phase, focus, hours, recovery, mon, tue, wed, thu, fri, sat, sun)
W=[]
# ---------- weeks 1-7: history (Rev 3 wording) ----------
W.append(("Build","Consolidate the 15 km jump",6.5,False,("s","B"),("r",strides(45,5)),("r",opt(35,5)),("r",easy(45,7)),("s","A"),("r",long(16)),"rest"))
W.append(("Build","Tempo returns + 18 km",7.5,False,("s","B"),("r",easy(50,7.5)),("r",opt(40,6)),("r",tempo(60,3,10)),("s","A"),("r",long(18)),"rest"))
W.append(("Build","Recovery week — absorb",5.5,True,"rest",("r",easy(40,6)),("m",None),("r",easy(45,7)),("s","A"),("r",long(13)),"rest"))
W.append(("Build","Marathon pace introduced",8.0,False,("s","B"),("r",easy(50,7.5)),("r",opt(40,6)),("r",mpint(55,4,"1.5 km")),("s","A"),("r",long(20)),"rest"))
W.append(("Build","First 22 km",8.5,False,("s","B"),("r",easy(50,7.5)),("r",opt(40,6)),("r",mpblock(60,25)),("s","A"),("r",long(22)),"rest"))
W.append(("Build","Recovery week",6.0,True,"rest",("r",easy(40,6)),("m",None),("r",strides(45,5)),("s","A"),("r",long(16)),"rest"))
W.append(("Build","Sharpen the top end",9.0,False,("s","B"),("r",easy(50,7.5)),("r",opt(40,6)),("r",hills(50,8)),("s","A"),("r",long(24,4,"Last 4 km at MP — first taste of race pace on tired legs.")),"rest"))
# ---------- week 8: missed (business trip, then ill) ----------
W.append(("Build","Missed — business trip, then ill",0.0,False,
          ("x","Strength B — Core & Stability"),("x","Easy Run — 55 min"),("x","Easy Run — 40 min (optional)"),
          ("x","Tempo — 3x12 min"),("x","Strength A — Lower Body Foundation"),("x","Long Run — 26 km (last 6 km @ MP)"),("x","Rest Day")))
# ---------- weeks 9-16: Rev 4 ----------
P.update(P_REV4)
W.append(("Peak","Return week — ease back in after illness",4.0,True,("m",None),
          ("r",easy(40,6.5,"First run back. Fever gone and only above-the-neck symptoms? Run it easy. Fever, chest symptoms or aches = another rest day.")),
          ("m",None),("r",strides(45,4)),("s","A"),
          ("r",long(16,0,"Easy only, no MP. If HR sits above 150 at an easy pace, cut it to 12 km — you're not fully recovered yet.")),"rest"))
W.append(("Peak","Back on track — the missed 26 km",9.0,False,("s","B"),("r",easy(50,8)),("r",opt(40,6.5)),("r",mpblock(60,30)),("s","A"),
          ("r",long(26,6,"The session you missed. Last 6 km at goal pace (~6:00/km, HR ≤158). First gel at 40–45 min, then every 30 min.")),"rest"))
W.append(("Peak","30 km — race-day dress rehearsal",10.0,False,("s","B"),("r",easy(55,8.5)),("r",opt(40,6.5)),("r",tempo(60,3,10)),("s","A"),
          ("r",long(30,6,"Full dress rehearsal: race breakfast, race kit, race shoes, race gels on the race schedule. Last 6 km at goal pace.")),"rest"))
W.append(("Peak","Recovery week",7.0,True,"rest",("r",easy(45,7)),("m",None),("r",strides(45,5)),("s","A"),("r",long(20)),"rest"))
W.append(("Peak","🏔️ PEAK — 32 km",11.0,False,("s","B"),("r",easy(50,8)),("r",opt(40,6.5)),("r",mpblock(60,30)),("s","A"),
          ("r",long(32,0,"🏔️ Peak long run. Easy pace throughout. Your confidence bank for race day.")),"rest"))
W.append(("Taper","Taper begins — volume down, sharpness held",8.0,True,("s","B"),("r",easy(45,7)),("r",opt(35,5.5)),("r",mpblock(50,25)),"rest",("r",long(22)),"rest"))
W.append(("Taper","Legs fresh, mind sharp",6.0,True,("s","A"),("r",easy(40,6.5)),("m",None),("r",mpint(40,4,"1 km")),"rest",("r",long(14)),"rest"))
W.append(("Taper","🏁 RACE WEEK",4.0,True,"rest",("r",easy(30,4.8,"Easy shake-out. Legs should feel springy.")),("m",None),("r",strides(25,4)),"rest",
  ("r",{"name":"Pre-race shake-out — 15 min","description":"Fire the legs, nothing more.","durationMinutes":15,"primaryZone":"Z2 Easy","humanReadable":"10 min very easy + 4x 20s strides + 5 min walk.\nEat well, hydrate, sleep early. Lay out gear tonight."}),
  ("r",{"name":"🏁 VALENCIA MARATHON 42.2 km","description":"RACE DAY! See Race Strategy tab.","distanceKm":42.2,"durationMinutes":254,"primaryZone":"Z3 Marathon Pace","humanReadable":"Goal ~6:00/km (≈4:13). First 10 km at 6:05–6:10 — deliberately held back. Settle into 6:00 from km 10 with HR ≤158. From km 32, press only if HR is still ≤160. Walk aid stations to fuel cleanly. Gel at km 7, then every 5 km. The training is in your legs."})))
assert len(W)==TOTAL_WEEKS, len(W)

def build(i,t):
    names=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    ws=PLAN_START+timedelta(weeks=i-1); days=[]; rh=rk=rn_=0
    for j,cell in enumerate(t[4:]):
        d=ws+timedelta(days=j)
        if cell=="rest": wos=[rest(i,names[j])]
        elif isinstance(cell,tuple) and cell[0]=="m": wos=[rest(i,names[j],True)]
        elif isinstance(cell,tuple) and cell[0]=="s": wos=[stg(i,names[j],cell[1])]
        elif isinstance(cell,tuple) and cell[0]=="x": wos=[missed(i,names[j],cell[1])]
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

plan={"version":"4.0","meta":{"id":"valencia-marathon-2026","athlete":"First-Time Marathoner","event":"Valencia Marathon 2026",
 "eventDate":RACE_DATE.isoformat(),"planStartDate":PLAN_START.isoformat(),"planEndDate":RACE_DATE.isoformat(),
 "createdAt":"2026-08-16T00:00:00Z","updatedAt":"2026-10-11T00:00:00Z","totalWeeks":TOTAL_WEEKS,"generatedBy":"Claude Coach",
 "tagline":"One week lost, nothing broken. Eight weeks to go — the long runs that matter are still ahead.",
 "overviewDeck":"16-week build from 15 km to race day, recalibrated on Oct 11 from the Aug–Oct watch data.",
 "zonesDeck":"Heart-rate targets drive every workout on the watch. Paces below are what those heart rates produced in Aug–Oct.",
 "revisionTitle":"Revision 4 · Oct 11 check-in",
 "revisionNote":"Week 8 (Oct 5–11) was lost to a business trip and illness. It takes the place of the recovery week that was scheduled next, so week 9 becomes an easy return week, the missed 26 km with a marathon-pace finish moves to Oct 24, the 30 km follows on Oct 31, and the 32 km peak and 3-week taper stay where they were. Goal pace moves from 6:20 to ~6:00/km (≈4:13): the last 4 km of the 24 km ran 5:48–5:51/km. The marathon-pace heart-rate band drops to 145–158 so Thursday sessions line up with that pace."},
 "preferences":{"swim":"meters","bike":"kilometers","run":"kilometers","firstDayOfWeek":"monday"},
 "assessment":{
  "foundation":{"raceHistory":["No prior races — first marathon"],"peakTrainingLoad":"46 km/week, longest run 24 km","foundationLevel":"novice","yearsInSport":10,
   "notes":"Consistent training since June 1. One week lost (Oct 5–11) to a business trip and illness."},
  "currentForm":{"weeklyVolume":{"total":39,"run":39},"longestSessions":{"run":24},"consistency":"Very good — one missed week in nineteen",
   "notes":"24 km on Oct 3 at 6:14/km average, HR ~150; last 4 km at 5:48–5:51/km (HR 154–160). Pace-to-heart-rate drift stayed at or under ~4% on all seven long runs of 15–24 km since mid-August."},
  "strengths":[{"sport":"run","evidence":"Aerobic durability: pace-to-HR drift ≤4% on every long run from 15 to 24 km"},
   {"sport":"run","evidence":"Finished the 24 km with 4 km at 5:48–5:51/km — about 30 s/km faster than the Rev 3 goal pace"},
   {"sport":"run","evidence":"Tempo reps at ~5:05/km and MP reps at 5:15–5:35/km, all inside their heart-rate bands"},
   {"sport":"run","evidence":"Easy-run efficiency up ~8% from June to September; ground contact time down from ~310 to ~265 ms"}],
  "limiters":[{"sport":"strength","evidence":"Four strength sessions logged since June — still the main injury risk as the long run goes to 32 km"},
   {"sport":"run","evidence":"Never beyond 24 km. At km 17–19 of the 24 km, HR rose to 153–159 while pace slipped to 6:29–6:35 — fuelling and durability to test at 26 and 30 km"},
   {"sport":"general","evidence":"Returning from 8 days off (travel + illness); the first week back has to be easy"}],
  "constraints":["3–4 running days/week","9-to-5 work, business travel + two children (1 yo & 11 yo)","Bodyweight strength only (home)","Rolling dune terrain near the coast — hillier than the flat Valencia course"]},
 "zones":{"run":{"hr":{"lthr":170,"maxEstimated":188,
   "notes":"Max HR 188 (observed 185 on strides). Tempo reps held 166–168 for 10 minutes, consistent with LTHR ~170. Marathon band lowered in Rev 4 to 145–158.",
   "zones":[{"zone":1,"name":"Recovery","hrLow":0,"hrHigh":132,"feels":"Very easy — chatty"},
     {"zone":2,"name":"Easy/Aerobic","hrLow":132,"hrHigh":148,"feels":"Conversational — where most runs live"},
     {"zone":3,"name":"Marathon","hrLow":145,"hrHigh":158,"feels":"Steady, full sentences — race HR until km 30"},
     {"zone":4,"name":"Tempo","hrLow":162,"hrHigh":172,"feels":"Hard — short phrases only"},
     {"zone":5,"name":"Threshold+","hrLow":172,"hrHigh":188,"feels":"Very hard — single words"}]},
  "pace":{"marathonGoalPace":"6:00/km","marathonGoalTime":"4:13","marathonGoalRange":"5:50–6:10/km (4:06–4:20 finish)",
   "easy":"6:00–6:30/km","longRun":"6:10–6:40/km","tempo":"5:05–5:20/km","threshold":"4:50–5:05/km",
   "notes":"From Aug–Oct runs at the stated heart rates. Goal pace is confirmed by the marathon-pace finishes of the 26 km (Oct 24) and 30 km (Oct 31)."}}},
 "phases":[
  {"name":"Build","startWeek":1,"endWeek":8,"focus":"Tempo + MP work, long run to 24 km","weeklyHoursRange":{"low":5.5,"high":9.5},"keyWorkouts":["Long run","Tempo","MP blocks","Hill repeats"]},
  {"name":"Peak","startWeek":9,"endWeek":13,"focus":"Return week, then 26 → 30 → 32 km","weeklyHoursRange":{"low":4,"high":11},"keyWorkouts":["Long run with MP finish","MP blocks","Tempo"]},
  {"name":"Taper","startWeek":14,"endWeek":16,"focus":"Cut volume, hold sharpness, race","weeklyHoursRange":{"low":4,"high":8},"keyWorkouts":["MP intervals","Easy + strides","Race day"]}],
 "weeks":weeks,
 "raceStrategy":{"event":{"name":"Valencia Marathon 2026","date":RACE_DATE.isoformat(),"type":"Marathon","distance":42.2},
  "pacing":{"strategy":"Controlled negative split — hold back early, press late",
   "firstHalf":{"target":"6:05–6:10/km for the first 10 km","notes":"Deliberately slower than goal. HR ~145–150. It will feel too easy — that is right."},
   "secondHalf":{"target":"6:00/km from km 10","notes":"Keep HR ≤158 until km 30. If it climbs, ease off 5–10 s/km — that is fine."},
   "segments":[{"km":"KM 1–10","pace":"6:05–6:10","cue":"Hold back. HR ~145–150. Too easy is correct."},
               {"km":"KM 11–21","pace":"6:00","cue":"Settle in. Half split ≈ 2:08."},
               {"km":"KM 22–32","pace":"6:00","cue":"HR ≤158. Fuel on schedule even if you don't feel like it."},
               {"km":"KM 33–42","pace":"5:50–6:00","cue":"Press only if HR is still ≤160 and legs are good. Otherwise hold."}],
   "targetHR":"≤158 until km 30","lastTenK":"Press only if HR is still ≤160 at km 32. Otherwise hold 6:00.",
   "warnings":"Your long runs already average ~6:10 at HR ~148, so 6:00 will feel easy early. That feeling is the trap: a 6:08 first 10 km costs you about a minute; a 5:45 first 10 km can cost you fifteen after km 35."},
  "nutrition":{"preRace":"Night before: pasta + lean protein, nothing new. 3 hr before: ~100g carbs (oatmeal, banana, honey, low fibre). Coffee 60 min before if usual.",
   "during":{"carbsPerHour":"60–80g","fluidPerHour":"500–750 ml",
    "schedule":"Gel at km 7 (~40 min), then every 5 km: 7/12/17/22/27/32/37. ~25 g each, always with water. Walk the aid stations to drink properly.",
    "gelKms":"7/12/17/22/27/32/37",
    "products":"Only what you have practised in long runs."},
   "rule":"Nothing new on race day. The 26 km and 30 km are your last two full fuel rehearsals."},
  "raceMorning":{"wakeUp":"3:00 hrs before start","breakfast":"2:30–3:00 before — familiar carbs only","warmUp":"10 min easy + 4 strides, 30 min before","gear":"Only what you have trained in. New shoes = blisters."},
  "mentalCues":["Km 1–10: 'Too easy. Good. That's the plan.'","Km 11–21: 'Rhythm. Drink. Fuel. Relax the shoulders.'",
   "Km 22–32: 'Now the race starts. Quick feet, tall posture.'","Km 33–42: 'Everyone hurts now. The 32 km run is in my legs. One km at a time.'"],
  "postRace":{"immediate":"Keep walking 10 min. Electrolytes. Eat within 30 min.","next72hrs":"Light walking only. No running. Sleep.","return":"First easy jog 5–7 days after. Two unstructured weeks before any structure."}},
 "coachingNotes":[
  "📋 REVISION 4 (Oct 11): One week lost to a business trip and illness. It replaces the recovery week that was due next, so the cost is one session — the 26 km with a marathon-pace finish — which moves to Oct 24. The 32 km peak (Nov 14) and the 3-week taper are unchanged. Don't try to make up the missed miles.",
  "🤒 Return rule for week 9: run only if the fever is gone and any symptoms are above the neck (stuffy nose, mild sore throat). Chest symptoms, fever or body aches mean another rest day. If HR on an easy pace sits 5+ beats above normal, shorten the run.",
  "🎯 Goal pace moves 6:20 → ~6:00/km (≈4:13). The last 4 km of the 24 km ran 5:48–5:51/km at HR 154–160, and MP sessions on fresh legs ran 5:15–5:35/km. It stays provisional: the MP finishes of the 26 km and 30 km decide between ~5:50 (4:06) and ~6:10 (4:20).",
  "❤️ Marathon-pace HR band lowered to 145–158 (was 152–162). With the old band, Thursday MP work came out at 5:15–5:35/km — race effort, but well faster than race pace. The new band lines up with ~6:00/km.",
  "⛽ On the 24 km, HR crept to 153–159 at km 17–19 while pace slipped to 6:29–6:35, then km 20 was slow and the finish was strong. That pattern often means carbs ran low. On the 26 and 30 km: first gel at 40–45 min, then every 30 min, no skipping.",
  "💪 STRENGTH IS STILL THE GAP. Four sessions logged since June. The long run is about to go from 24 to 32 km. Monday and Friday, 25–30 minutes — the single-leg work is what keeps the knee quiet under that load.",
  "🏃 Long runs average HR 146–150, at the top of the easy band. Keep the first half at 148 or below; the drift in the second half is where the training effect is.",
  "📈 Fitness since May: easy-run efficiency up ~8% (June → September), ground contact time down from ~310 to ~265 ms, pace-to-HR drift ≤4% on every long run.",
  "⛰️ Valencia is flat; your long runs are not (the 18 km on Aug 29 had ~200 flights of climbing). Flat-course race pace should come out a little quicker than your training numbers.",
  "⌚ The duplicate 'Indoor Run' records stopped after Sep 12, so training load is no longer double-counted.",
  "🧪 Next checkpoint: after the 30 km on Oct 31. Export then and we lock race pace."]}

with open("plan.json","w") as f: json.dump(plan,f,indent=2,ensure_ascii=False)
lr=[w['days'][5]['workouts'][0].get('distanceKm') or 0 for w in weeks]
print(f"✓ {TOTAL_WEEKS} weeks: {PLAN_START} → {RACE_DATE}")
print(f"✓ Long-run ramp: {lr}")
print(f"✓ Phases: " + ", ".join(f"{p['name']} W{p['startWeek']}-{p['endWeek']}" for p in plan['phases']))
print(f"✓ Goal: {plan['zones']['run']['pace']['marathonGoalPace']} → {plan['zones']['run']['pace']['marathonGoalRange']}")
