"""
Uses classes and inheritance to implement the different module types, and an overall system class to hold them all
and provide an interface for pushing the button.
Possible improvement: add method to reset the system to avoid needing two separate copies for P1 and P2.
"""
import sys
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

    def add_input(self, newinput: str) -> None:
        self.inputs[newinput] = Pulse["Low"]

    def process_signal(self, inmsg: Message) -> list[Message]:
        return [(to, inmsg[0], Pulse["Low"]) for to in self.outputs]

    def __str__(self):
        return f"Type: {self.type} Outputs: {self.outputs}"


class Flipflop(Module):
    def process_signal(self, inmsg: Message) -> list[Message]:
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
    def process_signal(self, inmsg: Message) -> list[Message]:
        self.inputs[inmsg[1]] = inmsg[2]
        if any(instate != Pulse["High"] for instate in list(self.inputs.values())):
            return [(to, inmsg[0], Pulse["High"]) for to in self.outputs]
        else:
            return [(to, inmsg[0], Pulse["Low"]) for to in self.outputs]


class CommunicationSystem:
    def __init__(self):
        self.modulelist: dict[str: Module] = {}
        self.__conjugatebuffer = []
        self.rxcon = ""
        self.rxcon_inputs = {}

    def add_module(self, rawstr: str) -> None:
        name, out = rawstr.split(" -> ")
        out = re.findall(r"\w+", out)
        if name[0] == "%":
            self.modulelist[re.findall(r"\w+", name)[0]] = Flipflop("Flipflop", out)
        elif name[0] == "&":
            tmp = re.findall(r"\w+", name)[0]
            self.modulelist[tmp] = Conjunction("Conjunction", out)
            self.__conjugatebuffer.append(tmp)
        else:
            self.modulelist[re.findall(r"\w+", name)[0]] = Module("Broadcaster", out)

    def initialize_conj(self) -> None:
        while len(self.__conjugatebuffer) > 0:
            current = self.__conjugatebuffer.pop(0)
            for mod in list(self.modulelist.keys()):
                if current in self.modulelist[mod].outputs:
                    self.modulelist[current].add_input(mod)
                if self.rxcon == "":
                    if "rx" in self.modulelist[mod].outputs:
                        self.rxcon = mod
                else:
                    if self.rxcon in self.modulelist[mod].outputs:
                        self.rxcon_inputs[mod] = 0

    def push_button(self, count: int) -> dict[Pulse: int]:
        pulsecount: dict[Pulse: int] = {Pulse["Low"]: 0, Pulse["High"]: 0}
        for pushcount in range(count):
            msgqueue = [("broadcaster", "button", Pulse["Low"])]
            while len(msgqueue) > 0:
                newmsg = msgqueue.pop(0)
                pulsecount[newmsg[2]] += 1
                if newmsg[0] in self.modulelist:
                    outmsgs = self.modulelist[newmsg[0]].process_signal(newmsg)
                    [msgqueue.append(m) for m in outmsgs]
        return pulsecount

    def get_rx_lowcount(self) -> int:
        pushcount = 0
        while any(count == 0 for count in list(self.rxcon_inputs.values())):
            pushcount += 1
            msgqueue = [("broadcaster", "button", Pulse["Low"])]
            while len(msgqueue) > 0:
                newmsg = msgqueue.pop(0)
                if newmsg[0] in self.modulelist:
                    outmsgs = self.modulelist[newmsg[0]].process_signal(newmsg)
                    for m in outmsgs:
                        msgqueue.append(m)
                        if (newmsg[0] in self.rxcon_inputs and m[2] == Pulse["High"] and
                                self.rxcon_inputs[newmsg[0]] == 0):
                            self.rxcon_inputs[newmsg[0]] = pushcount
        return math.lcm(*list(self.rxcon_inputs.values()))


def main() -> int:
    comsys = CommunicationSystem()
    comsys2 = CommunicationSystem()
    with open("../Inputfiles/aoc20.txt", "r") as file:
        for line in file.read().strip('\n').splitlines():
            comsys.add_module(line)
            comsys2.add_module(line)
    comsys.initialize_conj()
    pulsecount = comsys.push_button(1000)
    print("Part 1:", math.prod(pulsecount.values()))

    comsys2.initialize_conj()
    print("Part 2:", comsys2.get_rx_lowcount())
    return 0


if __name__ == "__main__":
    sys.exit(main())
