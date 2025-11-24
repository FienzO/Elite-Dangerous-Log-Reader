import json
import os




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
            if uIn < 1 or uIn > i:
                print("Input outside of range!")
            else:
                break
        except:
            print("Retry")
    return os.path.join(path,logarr[uIn-1])



path = picklog()

with open(path, 'r') as file:
    for line in file:
        print(line)