import json
import os
from datetime import datetime

#####
EventWList = ["Commander", "Market", "MarketBuy", "MarketSell", "ColonisationContribution", "Cargo", "Undocked", "Docked", "FSDJump", "EjectCargo", "Ressurect", "Continued"]
#####

global cargo, sumtps, totalCargo


def tsConvert(ts):
    dtObj = datetime.fromisoformat(ts.replace('Z', '+00:00'))
    return dtObj.timestamp()

def tpsCalc(t1, t2 ,cargoCount):
    sumTime = t2-t1
    tps = cargoCount/sumTime

    return tps

def picklog():
    path = "~//..//log-depot"
    logarr = sorted(os.listdir(path))
    
    for i, log in enumerate(logarr):
        log = log[8:]
        log, _ = os.path.splitext(log)
        print(f"{i+1})\t{log}")

    while True:
        try:
            uIn = int(input(": "))
            if uIn < 1 or uIn > (i+1):
                print("Input outside of range!")
            else:
                break
        except ValueError:
            print("Retry")
    return os.path.join(path,logarr[uIn-1])

def aquireLog(path):

    with open(path, 'r') as file:
        log = []
        for line in file:
            #print(line, type(line))
            pLine = json.loads(line)
            if pLine["event"] in EventWList:
                log.append(line)
    return log

def addCargo(cargoType,count):
    cargoType = cargoType.lower()
    if cargoType not in cargo:
        cargo[cargoType] = count
        totalCargo[cargoType] = count
    else:
        cargo[cargoType] += count
        totalCargo[cargoType] += count
    #print(f"Bought {count} {cargoType}")
    #print(cargo)

def remCargo(cargoType, count):
    cargoType = cargoType.lower()
    if cargoType not in cargo:
        print("Err, subtracting from noneexistent cargo", cargoType)
    else:
        if cargo[cargoType] < count:
            print("Err, subtracting from noneexistent cargo", cargoType, cargo[cargoType], count)
        else:
            cargo[cargoType] -= count
    #print(f"sold {count} {cargoType}")
    #print(cargo)

haulcount = -1
tps = []
t1, t2 = 0,0

cargo = {}
totalCargo = {}



log = aquireLog(picklog())
for line in log:
    line = json.loads(line)
    if line['event'] == "Commander":
        cmdr = line['Name']
    elif line['event'] == "MarketBuy":
        cargoType = line['Type']
        count = line['Count']

        addCargo(cargoType, count)

        haulcount += 1
        tps.append(0)

        print(line)
    elif line['event'] == "Undocked":
        #print(line)
        t1 = tsConvert(line['timestamp'])
        pass
    elif line['event'] == "Docked":
        #print(line)
        pass
    elif line['event'] == "MarketSell":
        cargoType = line['Type']
        count = line['Count']
        remCargo(cargoType, count)

        t2 = tsConvert(line['timestamp'])
        tps[haulcount] += tpsCalc(t1,t2,count)
        #print(tps)

        #print(line)
    elif line['event'] == "ColonisationContribution":
        contributions = line['Contributions']
        contriCount = 0
        for contri in contributions:
            cargoType = contri['Name_Localised']
            count = contri['Amount']
            remCargo(cargoType, count)
            contriCount += count

        t2 = tsConvert(line['timestamp'])
        tps[haulcount] += tpsCalc(t1,t2,contriCount)

        #print(tps)
    

avtps = 0
for i in tps:
    avtps += i
avtps /= haulcount
tonnes = 0
print("Total tonnage:")
for item in totalCargo.keys():
    tonnes += totalCargo[item]
    print(f"    {totalCargo[item]} {item}")
print(f"Average Tonnes per Second: {round(avtps,3)}")
payrate = int(input("Payment per tonne: "))
print(f"Estimated Payment: {"{:,}".format(payrate * tonnes)}")




