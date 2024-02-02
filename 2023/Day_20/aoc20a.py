# Advent of code 2023 Day 20 part A
import re
import math


Pulse = {"Low": 0, "High": 1}
Message = (str, str, Pulse)  # To, From, pulse


class Module:
    def __init__(self, mtype: str, outputs: list[str]) -> None:
        self.type = mtype
        self.inputs: dict[str: Pulse] = {}
        self.outputs = outputs
        self.onoffstate = 0

    def addinput(self, newinput: str) -> None:
        self.inputs[newinput] = Pulse["Low"]

    def processsignal(self, inmsg: Message) -> list[Message]:
        return [(to, inmsg[0], Pulse["Low"]) for to in self.outputs]

    def __str__(self):
        return f"Type: {self.type} Outputs: {self.outputs}"


class Flipflop(Module):
    def processsignal(self, inmsg: Message) -> list[Message]:
        if inmsg[2] == Pulse["High"]:
            return []
        else:
            if self.onoffstate > 0:  # On
                self.onoffstate = 0
                return [(to, inmsg[0], Pulse["Low"]) for to in self.outputs]
            else:
                self.onoffstate = 1  # Off
                return [(to, inmsg[0], Pulse["High"]) for to in self.outputs]


class Conjunction(Module):
    def processsignal(self, inmsg: Message) -> list[Message]:
        self.inputs[inmsg[1]] = inmsg[2]
        if any(instate != Pulse["High"] for instate in list(self.inputs.values())):
            return [(to, inmsg[0], Pulse["High"]) for to in self.outputs]
        else:
            return [(to, inmsg[0], Pulse["Low"]) for to in self.outputs]


modulelist: dict[str: Module] = {}
conjugatebuffer = []

with open("../Inputfiles/aoc20.txt", "r") as file:
    for line in file.readlines():
        if len(line) > 1:
            name, out = line.strip("\n").split(" -> ")
            out = re.findall(r"\w+", out)
            if name[0] == "%":
                modulelist[re.findall(r"\w+", name)[0]] = Flipflop("Flipflop", out)
            elif name[0] == "&":
                tmp = re.findall(r"\w+", name)[0]
                modulelist[tmp] = Conjunction("Conjunction", out)
                conjugatebuffer.append(tmp)
            else:
                modulelist[re.findall(r"\w+", name)[0]] = Module("Broadcaster", out)

# Initialize all inputs for conjunctions
while len(conjugatebuffer) > 0:
    current = conjugatebuffer.pop(0)
    for mod in list(modulelist.keys()):
        if current in modulelist[mod].outputs:
            modulelist[current].addinput(mod)

pulsecount = [0, 0]

for pushcount in range(0, 1000):
    msgqueue = [("broadcaster", "button", Pulse["Low"])]
    while len(msgqueue) > 0:
        newmsg = msgqueue.pop(0)
        # print(newmsg[1], " -> ", newmsg[0], " : ", newmsg[2])
        pulsecount[newmsg[2]] += 1
        try:
            outmsgs = modulelist[newmsg[0]].processsignal(newmsg)
            for m in outmsgs:
                msgqueue.append(m)
        except KeyError:
            pass

print("Part1: ", math.prod(pulsecount))
