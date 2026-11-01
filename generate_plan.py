"""Valencia Marathon 2026 — REVISION 4 (Oct 11 check-in).
16 weeks: Mon 17 Aug 2026 -> race Sun 6 Dec 2026.

Rev 3 (Aug 16): goal pace 6:55 -> 6:20/km, peak long run 32 km, hills kept (dune terrain).
Rev 4 (Oct 11): week 8 (Oct 5-11) lost to a business trip + illness. The missed week takes the
place of the recovery week that was scheduled next; week 9 becomes a gentle return week, the
missed 26 km MP run moves to Oct 24, 30 km on Oct 31, 32 km peak and taper unchanged.
Goal pace 6:20 -> ~6:00/km on the evidence of the 24 km (last 4 km at 5:48-5:51, HR 154-160)
and MP sessions (5:15-5:35 at HR 152-161). Marathon-pace HR band lowered to 145-158.

Rev 5 (Nov 1): the 30 km is done (Oct 31). Goal pace ~6:00 -> ~6:10/km: holding 6:00 over
km 19-30 pushed HR 159 -> 166, above the 158 race ceiling. The 26 km (Oct 24) was missed and is
marked missed, not made up. Strength moves off Fridays; the 32 km stays easy with a stop rule.

Past weeks are history and keep the wording they were published with; the pace set (P) is
switched before each revision's first future week is built.
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
# Rev 5 wording (weeks 12-16), after the 30 km on Oct 31
P_REV5 = {"easy_hr":"HR 132–148","easy_pace":"~6:15–6:40/km",
          "long_easy":"HR 138–150, ~6:20–6:40/km","long_mp_easy":"HR 138–150, ~6:20–6:40/km",
          "mp":"~6:10/km, HR 145–158","tempo":"~5:00–5:20/km, HR 162–172",
          "long_min":6.5,"long_min_mp":6.4}
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
def missed(w,dn,planned,reason="trip / illness"):
    why = {"trip / illness":"Week lost to a business trip followed by illness. Not made up — the plan absorbs it (see Revision 4).",
           "ill":"Still ill. Not made up.",
           "":"Not run. Not made up — the plan absorbs it."}
    return {"id":mid(w,dn,"missed"),"sport":"missed","type":"missed","name":f"Missed — {reason}" if reason else "Missed",
            "description":f"Planned: {planned}","completed":False,"humanReadable":why.get(reason,why[""])}

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
          ("x","Easy Run — 40 min","ill"),
          ("m",None),("r",strides(45,4)),("s","A"),
          ("r",long(16,0,"Easy only, no MP. If HR sits above 150 at an easy pace, cut it to 12 km — you're not fully recovered yet.")),"rest"))
W.append(("Peak","Back on track — the missed 26 km",9.0,False,("s","B"),("r",easy(50,8)),("r",opt(40,6.5)),("x","Marathon Pace Block — 30 min @ MP",""),("s","A"),
          ("x","Long Run — 26 km (last 6 km @ MP)",""),"rest"))
W.append(("Peak","30 km — race-day dress rehearsal",10.0,False,("s","B"),("r",easy(55,8.5)),("r",opt(40,6.5)),("r",tempo(60,3,10)),("s","A"),
          ("r",long(30,6,"Full dress rehearsal: race breakfast, race kit, race shoes, race gels on the race schedule. Last 6 km at goal pace.")),"rest"))
# ---------- weeks 12-16: Rev 5 ----------
P.update(P_REV5)
W.append(("Peak","Recovery week — absorb the 30 km",6.5,True,"rest",("r",easy(45,7)),("s","A"),("r",strides(45,5)),("m",None),
          ("r",long(20,0,"Easy only. HR should settle around 145–150 at 6:20–6:40. If it's above 152 by km 8, cut to 16 km. Rehearse race fuelling: one gel every 30 min with water.")),"rest"))
W.append(("Peak","🏔️ PEAK — 32 km",10.0,False,("s","B"),("r",easy(50,8)),("s","A"),("r",mpblock(60,30)),("m",None),
          ("r",long(32,0,"🏔️ Peak long run, easy the whole way — no marathon-pace finish. First 20 km at HR ≤150. One gel every 30 min with water. If HR is above 155 at an easy pace by km 10, stop at 26–28 km: the run has done its job.")),"rest"))
W.append(("Taper","Taper begins — volume down, sharpness held",8.0,True,("s","B"),("r",easy(45,7)),("r",opt(35,5.5)),("r",mpblock(50,25)),"rest",("r",long(22)),"rest"))
W.append(("Taper","Legs fresh, mind sharp",6.0,True,("s","A"),("r",easy(40,6.5)),("m",None),("r",mpint(40,4,"1 km")),"rest",("r",long(14)),"rest"))
W.append(("Taper","🏁 RACE WEEK",4.0,True,"rest",("r",easy(30,4.8,"Easy shake-out. Legs should feel springy.")),("m",None),("r",strides(25,4)),"rest",
  ("r",{"name":"Pre-race shake-out — 15 min","description":"Fire the legs, nothing more.","durationMinutes":15,"primaryZone":"Z2 Easy","humanReadable":"10 min very easy + 4x 20s strides + 5 min walk.\nEat well, hydrate, sleep early. Lay out gear tonight."}),
  ("r",{"name":"🏁 VALENCIA MARATHON 42.2 km","description":"RACE DAY! See Race Strategy tab.","distanceKm":42.2,"durationMinutes":261,"primaryZone":"Z3 Marathon Pace","humanReadable":"Goal ~6:10/km (≈4:20). First 10 km at 6:15–6:20 — deliberately held back. Settle into 6:10 from km 10 with HR ≤158. From km 32, press only if HR is still ≤160. One gel just before each aid station (km 5, 10, 15, 20, 25, 30, 35), drink at the station. The training is in your legs."})))
assert len(W)==TOTAL_WEEKS, len(W)

def build(i,t):
    names=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    ws=PLAN_START+timedelta(weeks=i-1); days=[]; rh=rk=rn_=0
    for j,cell in enumerate(t[4:]):
        d=ws+timedelta(days=j)
        if cell=="rest": wos=[rest(i,names[j])]
        elif isinstance(cell,tuple) and cell[0]=="m": wos=[rest(i,names[j],True)]
        elif isinstance(cell,tuple) and cell[0]=="s": wos=[stg(i,names[j],cell[1])]
        elif isinstance(cell,tuple) and cell[0]=="x": wos=[missed(i,names[j],*cell[1:])]
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

plan={"version":"5.0","meta":{"id":"valencia-marathon-2026","athlete":"First-Time Marathoner","event":"Valencia Marathon 2026",
 "eventDate":RACE_DATE.isoformat(),"planStartDate":PLAN_START.isoformat(),"planEndDate":RACE_DATE.isoformat(),
 "createdAt":"2026-08-16T00:00:00Z","updatedAt":"2026-11-01T00:00:00Z","totalWeeks":TOTAL_WEEKS,"generatedBy":"Claude Coach",
 "tagline":"30 km in the legs. Five weeks to go: recover, one long easy run, then taper.",
 "overviewDeck":"16-week build from 15 km to race day, recalibrated on Nov 1 after the 30 km.",
 "zonesDeck":"Heart-rate targets drive every workout on the watch. Paces below are what those heart rates produced in Aug–Oct.",
 "revisionTitle":"Revision 5 · Nov 1 check-in",
 "revisionNote":"The 30 km on Oct 31 is done. Goal pace moves from ~6:00 to ~6:10/km (≈4:20): holding 6:00 over km 19–30 pushed heart rate from 159 to 166, above the 158 race ceiling, while 6:15–6:30 sat at 149–153. The 26 km on Oct 24 was missed and is not made up. This week stays a recovery week, strength moves off Fridays so it never lands the day before a long run, the 32 km on Nov 14 is easy the whole way with a stop-at-28 rule, and the taper is unchanged."},
 "preferences":{"swim":"meters","bike":"kilometers","run":"kilometers","firstDayOfWeek":"monday"},
 "assessment":{
  "foundation":{"raceHistory":["No prior races — first marathon"],"peakTrainingLoad":"50 km/week, longest run 30 km","foundationLevel":"novice","yearsInSport":10,
   "notes":"Consistent since June. One week lost to a business trip and illness (Oct 5–11); the 26 km on Oct 24 was also missed."},
  "currentForm":{"weeklyVolume":{"total":50,"run":50},"longestSessions":{"run":30},"consistency":"Good — two disrupted weeks in October, back on plan since Oct 26",
   "notes":"30 km on Oct 31 at 6:18/km average: km 1–15 at 6:15–6:30 (HR 147–153), km 19–30 at 5:49–6:17 (HR 159–166)."},
  "strengths":[{"sport":"run","evidence":"Finished 30 km with 12 km at ~6:00/km and no late collapse"},
   {"sport":"strength","evidence":"Strength now consistent: five sessions in the last two weeks"},
   {"sport":"run","evidence":"Pace-to-HR drift ≤4% on every long run of 15–24 km from August to early October"},
   {"sport":"run","evidence":"Cadence ~160–168 spm; ground contact time down from ~310 to ~265 ms since spring"}],
  "limiters":[{"sport":"run","evidence":"Holding 6:00/km cost HR 159 → 166 over km 19–30 — above the race ceiling with 12 km still to go"},
   {"sport":"run","evidence":"Fitness slightly down after the illness: tempo reps faded 4:58 → 5:16 → 5:39/km, versus three at ~5:00 in August"},
   {"sport":"general","evidence":"Long run jumped from 16 to 30 km after the 26 km was missed — this recovery week matters"}],
  "constraints":["3–4 running days/week","9-to-5 work, business travel + two children (1 yo & 11 yo)","Bodyweight strength only (home)","Rolling dune terrain near the coast — hillier than the flat Valencia course"]},
 "zones":{"run":{"hr":{"lthr":170,"maxEstimated":188,
   "notes":"Max HR 188 (observed 185 on strides). Tempo reps held 166–168 for 10 minutes, consistent with LTHR ~170. Marathon band lowered in Rev 4 to 145–158.",
   "zones":[{"zone":1,"name":"Recovery","hrLow":0,"hrHigh":132,"feels":"Very easy — chatty"},
     {"zone":2,"name":"Easy/Aerobic","hrLow":132,"hrHigh":148,"feels":"Conversational — where most runs live"},
     {"zone":3,"name":"Marathon","hrLow":145,"hrHigh":158,"feels":"Steady, full sentences — race HR until km 30"},
     {"zone":4,"name":"Tempo","hrLow":162,"hrHigh":172,"feels":"Hard — short phrases only"},
     {"zone":5,"name":"Threshold+","hrLow":172,"hrHigh":188,"feels":"Very hard — single words"}]},
  "pace":{"marathonGoalPace":"6:10/km","marathonGoalTime":"4:20","marathonGoalRange":"6:05–6:20/km (4:17–4:27 finish)",
   "easy":"6:15–6:40/km","longRun":"6:20–6:40/km","tempo":"5:00–5:20/km","threshold":"4:50–5:05/km",
   "notes":"Revised after the 30 km on Oct 31. Heart rate on the watch still drives every workout; these are the paces it produced in late October."}}},
 "phases":[
  {"name":"Build","startWeek":1,"endWeek":8,"focus":"Tempo + MP work, long run to 24 km","weeklyHoursRange":{"low":5.5,"high":9.5},"keyWorkouts":["Long run","Tempo","MP blocks","Hill repeats"]},
  {"name":"Peak","startWeek":9,"endWeek":13,"focus":"Return week, 30 km, recovery, 32 km easy","weeklyHoursRange":{"low":4,"high":11},"keyWorkouts":["Long run with MP finish","MP blocks","Tempo"]},
  {"name":"Taper","startWeek":14,"endWeek":16,"focus":"Cut volume, hold sharpness, race","weeklyHoursRange":{"low":4,"high":8},"keyWorkouts":["MP intervals","Easy + strides","Race day"]}],
 "weeks":weeks,
 "raceStrategy":{"event":{"name":"Valencia Marathon 2026","date":RACE_DATE.isoformat(),"type":"Marathon","distance":42.2},
  "pacing":{"strategy":"Controlled negative split — hold back early, press late",
   "firstHalf":{"target":"6:15–6:20/km for the first 10 km","notes":"Deliberately slower than goal. HR ~148–152. It will feel too easy — that is right."},
   "secondHalf":{"target":"6:10/km from km 10","notes":"Keep HR ≤158 through km 30. If it climbs, ease off 5–10 s/km — that is fine."},
   "segments":[{"km":"KM 1–10","pace":"6:15–6:20","cue":"Hold back. HR ~148–152. Too easy is correct."},
               {"km":"KM 11–21","pace":"6:10","cue":"Settle in. Half split ≈ 2:11–2:12."},
               {"km":"KM 22–32","pace":"6:10","cue":"HR ≤158. If it climbs, ease off 5–10 s/km. Gel before every station."},
               {"km":"KM 33–42","pace":"6:00–6:10","cue":"Press only if HR is still ≤160 and legs are good. Otherwise hold."}],
   "targetHR":"≤158 through km 30","lastTenK":"Press only if HR is still ≤160 at km 32. Otherwise hold 6:10.",
   "warnings":"On Oct 31, holding 6:00/km from km 19 pushed HR from 159 to 166 by km 26–30 — and race day has 12 more km after that. Starting at 6:15–6:20 costs you about a minute. Going out at 6:00 can cost you twenty after km 35."},
  "nutrition":{"preRace":"Night before: pasta + lean protein, nothing new. 3 hr before: ~100g carbs (oatmeal, banana, honey, low fibre). Coffee 60 min before if usual.",
   "during":{"carbsPerHour":"~60g","fluidPerHour":"~300–450 ml",
    "schedule":"One Upfront Gel (regular, ~30 g carbs) a few hundred metres before each aid station — km 5, 10, 15, 20, 25, 30, 35 — then drink half to two-thirds of the 33 cl water bottle at the station.",
    "gelKms":"5/10/15/20/25/30/35",
    "products":"Upfront Gel (regular, 50 g sachet) — as practised. Powerade and course gels only if tested in training."},
   "rule":"Nothing new on race day. The 20 km and the 32 km are your last two fuel rehearsals."},
  "raceMorning":{"wakeUp":"3:00 hrs before start","breakfast":"2:30–3:00 before — familiar carbs only","warmUp":"10 min easy + 4 strides, 30 min before","gear":"Only what you have trained in. New shoes = blisters."},
  "mentalCues":["Km 1–10: 'Too easy. Good. That's the plan.'","Km 11–21: 'Rhythm. Drink. Fuel. Relax the shoulders.'",
   "Km 22–32: 'Now the race starts. Quick feet, tall posture.'","Km 33–42: 'Everyone hurts now. The 32 km run is in my legs. One km at a time.'"],
  "postRace":{"immediate":"Keep walking 10 min. Electrolytes. Eat within 30 min.","next72hrs":"Light walking only. No running. Sleep.","return":"First easy jog 5–7 days after. Two unstructured weeks before any structure."}},
 "coachingNotes":[
  "📋 REVISION 5 (Nov 1): The 30 km is done. Goal pace moves from ~6:00 to ~6:10/km (≈4:20). Holding 6:00 over km 19–30 pushed HR from 159 to 166 — above the 158 race ceiling, with 12 km still to go on race day. At 6:15–6:30 your HR sat at 149–153. 6:10 on tapered, flat-course legs is the honest number.",
  "📉 Fitness dipped a little after the illness: the Oct 29 tempo reps faded 4:58 → 5:16 → 5:39/km at HR 163–170 (in August: three reps at ~5:00, HR 165–167). Five weeks is enough to win some of it back — by recovering well and completing the 32 km, not by adding work.",
  "🏃 The 30 km had 12 km at marathon pace, not the planned 6. The extra 6 km is where HR crept past 160. Run what's written — especially on the 32 km, which is easy the whole way.",
  "🧪 The 26 km on Oct 24 was missed and is not made up. You still got the key long run in.",
  "💪 Strength: five sessions in two weeks — finally consistent. Two changes: it moves off Fridays so it never lands the day before a long run (it was in the plan on Fridays — my mistake), and keep it moderate now: no new exercises, nothing that leaves you sore. Last session Mon Nov 23.",
  "⛽ Race fuelling: one Upfront Gel (~30 g) a few hundred metres before each aid station at km 5/10/15/20/25/30/35, washed down with the 33 cl water bottle — about 60 g of carbs an hour. Rehearse it exactly on the 20 km and the 32 km.",
  "🏔️ 32 km on Nov 14: easy the whole way, first 20 km at HR ≤150. If HR is above 155 at an easy pace by km 10, stop at 26–28 km — the run has done its job.",
  "⛰️ Valencia is flat; your long runs mostly aren't. Flat-course race pace should come out a little quicker than your training numbers.",
  "🧪 Next checkpoint: after the 32 km on Nov 14. Export then and we finalise race-day pacing."]}

with open("plan.json","w") as f: json.dump(plan,f,indent=2,ensure_ascii=False)
lr=[w['days'][5]['workouts'][0].get('distanceKm') or 0 for w in weeks]
print(f"✓ {TOTAL_WEEKS} weeks: {PLAN_START} → {RACE_DATE}")
print(f"✓ Long-run ramp: {lr}")
print(f"✓ Phases: " + ", ".join(f"{p['name']} W{p['startWeek']}-{p['endWeek']}" for p in plan['phases']))
print(f"✓ Goal: {plan['zones']['run']['pace']['marathonGoalPace']} → {plan['zones']['run']['pace']['marathonGoalRange']}")
