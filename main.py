import time
import asyncio
import random
import os
import sys

gravAccel = 9.80665


# Starship V2 parameters

superHeavyDryMass = 281000
starshipDryMass = 161000 #+-3600
superHeavyFuelCapacity = 3250000
starshipFuelCapacity = 1500000

raptorSLThrust = 2260000 #Raptor 2 SL
raptorVacThrust = 2530000 #Raptor 2 Vac

raptorSLISP = 327 # vacuum
raptorVacISP = 380 # vacuum

RSLstartupSuccessRate = 0.9

boostTWR = (33*raptorSLThrust) / ((superHeavyDryMass + superHeavyFuelCapacity + starshipDryMass + starshipFuelCapacity)*gravAccel)
shipTWR = (3*raptorSLThrust + 3*raptorVacThrust) / ((starshipDryMass + starshipFuelCapacity)*gravAccel)

raptorStatus = {}
for i in range(1,34):
  raptorStatus[f"E{i}"] = {"Active": False, "Throttle": 0, "CH4": False, "LOX": False, "Temp": False}

# print(raptorStatus)
# print(boostTWR)
# print(shipTWR)

launchStatus = {
  "weatherGO": {"name": "Weather","status": False},
  "rangeGO": {"name": "Range","status": False},
  "shMethaneLoadGO": {"name": "Superheavy Methane","status": False},
  "shLOXLoadGO": {"name": "Superheavy LOX","status": False},
  "shipMethaneLoadGO": {"name": "Starship Methane","status": False},
  "shipLOXLoadGO": {"name": "Starship LOX","status": False}
}


GoforLaunch = False

# functions

async def launchCountdown(t):
  print(" ")
  # start = time.perf_counter()
  while t >= 0:
    sys.stdout.write("\033[A\033[K")
    sys.stdout.flush() 
    print(t)
    if t<2:
      print("Engine Ignition")
      for engine in raptorStatus:
        raptorStatus[engine]["Throttle"] = 0.4
        rand = random.uniform(0,1)
        if rand < RSLstartupSuccessRate: raptorStatus[engine]["Active"] = True
        else: raptorStatus[engine]["Active"] = False

    await asyncio.sleep(1)
    t = t-1

def clear_screen():
    # 'nt' is for Windows, 'posix' is for Linux/macOS
    os.system('cls' if os.name == 'nt' else 'clear')


while GoforLaunch == False:
  clear_screen()
  flag = False
  for key in launchStatus:
    print(str(launchStatus[key]["name"]) + ": " + str(launchStatus[key]["status"]))
    if launchStatus[key]["status"] == False:
      flag = True

  if flag: GoforLaunch = False
  elif (not flag): GoforLaunch = True

  # fix the issues (randomly)
  for key in launchStatus:
    rand = random.uniform(0,1)
    if launchStatus[key]["status"] == False:
      if rand > 0.1: launchStatus[key]["status"] = True

  asyncio.run(asyncio.sleep(1))


print("\nVEHICLE IS GO FOR LAUNCH\n")
asyncio.run(asyncio.sleep(1))

payloadMass = input("Payload Mass (kg): ")

asyncio.run(launchCountdown(3))


print(raptorStatus)

activeEngines = 0
for engine in raptorStatus:
  if raptorStatus[engine]["Active"] == False:
    print("Engine " + str(engine) + " failed to start")
  elif (raptorStatus[engine]["Active"] == True) and (raptorStatus[engine]["Throttle"] == 0.4):
    activeEngines += 1

if activeEngines >= 28:
  print("LiftOff")
else:
  print("Insufficient Thrust\nLiftOff Abort")