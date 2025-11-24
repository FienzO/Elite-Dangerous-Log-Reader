import json
import os


#####
EventWList = ["Commander", "Market", "MarketBuy", "MarketSell", "ColonisationContribution", "Cargo", "Undocked", "Docked", "FSDJump", "EjectCargo", "Ressurect", "Continued"]
#####



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



log = aquireLog(picklog())
for line in log:
    line = json.loads(line)
    if line['event'] == "Commander":
        cmdr = line['Name']
    elif line['event'] == "MarketBuy":
        print(line)
    elif line['event'] == "Undocked":
        print(line)
    elif line['event'] == "Docked":
        print(line)
    elif line['event'] == "MarketSell":
        print(line)



