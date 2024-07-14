"""
Oh boy, just when I assumed that day 15 was done dealt with, we get another one just like it...

--- Safety commit, NOT WORKING YET - and I have absolutely no idea why... ---

"""
import sys
from dataclasses import dataclass
from enum import Enum
import re
from copy import deepcopy


class Team(Enum):
    IMMUNESYSTEM = 'Immune System'
    INFECTION = 'Infection'

    def __repr__(self):
        return f"{self.name}"


class DmgType(Enum):
    COLD = 'cold'
    FIRE = 'fire'
    SLASHING = 'slashing'
    RADIATION = 'radiation'
    BLUDGEONING = 'bludgeoning'

    def __repr__(self):
        return f"{self.name}"


class TraitType(Enum):
    WEAK = 'weak'
    IMMUNE = 'immune'

    def __repr__(self):
        return f"{self.name}"


@dataclass(frozen=True)
class Trait:
    t: TraitType
    damagetype: DmgType


@dataclass
class Group:
    uid: int
    team: Team
    units: int
    hp: int
    attackpower: int
    attacktype: DmgType
    initiative: int
    traits: list[Trait]

    @property
    def effective_power(self):
        return self.units * self.attackpower

    def get_dmgtaken(self, power: int, atype: DmgType) -> int:
        for t in self.traits:
            if t.damagetype == atype:
                if t.t == TraitType.IMMUNE:
                    return 0
                elif t.t == TraitType.WEAK:
                    return 2 * power
        return power

    def receive_dmg(self, power: int, atype: DmgType) -> int:
        lostunits = min(self.get_dmgtaken(power, atype) // self.hp, self.units)
        self.units -= lostunits
        return lostunits


class ImmuneSystemSimulator:
    def __init__(self, rawstr: str) -> None:
        team = None
        uid = 1
        self.__groups: dict[int: Group] = {}
        for line in rawstr.splitlines():
            if len(line) > 0:
                if not line[0].isdigit():
                    team = Team(line.strip(':'))
                else:
                    units, hp, ap, init = list(map(int, re.findall(r"\d+", line)))
                    at = DmgType(re.findall(r"\d (\w+) damage at initiative", line)[0])
                    traits = []
                    traitstr = re.findall(r"\(([^)]+)", line)
                    if traitstr:
                        for part in traitstr[0].split('; '):
                            words = part.split()
                            for t in words[2:]:
                                traits.append(Trait(TraitType(words[0]), DmgType(t.strip(', '))))
                    self.__groups[uid] = Group(uid, team, units, hp, ap, at, init, traits)
                    uid += 1
        [print(g, self.__groups[g]) for g in self.__groups]

    def get_winning_units(self) -> int:
        groups = deepcopy(self.__groups)

        # While no winner
        while len(set([g.team for g in list(groups.values()) if g.units > 0])) > 1:
            # Target selection
            targets: dict[int: int] = {}
            attackerlist = sorted([g for g in groups.values() if g.units > 0],
                                  key=lambda x: (x.effective_power, x.initiative), reverse=True)
            for attacker in attackerlist:
                targetlist = sorted([t for t in attackerlist if t.team != attacker.team and t.units > 0
                                     and t.uid not in targets.values()],
                                    key=lambda x: (x.get_dmgtaken(attacker.effective_power, attacker.attacktype),
                                                   x.effective_power, x.initiative),
                                    reverse=True)
                if targetlist:
                    targets[attacker.uid] = targetlist[0].uid
            if not targets:
                return -1

            # Combat
            totaldmg = 0
            for attacker in sorted(list(groups.values()), key=lambda x: x.initiative, reverse=True):
                if attacker.units > 0 and attacker.uid in targets:
                    totaldmg += groups[targets[attacker.uid]].receive_dmg(attacker.effective_power, attacker.attacktype)
            if totaldmg == 0:
                # In case of deadlock of nothing mut immune dmg
                return -1
        return sum([g.units for g in groups.values() if g.units > 0])


def main() -> int:
    with open('../Inputfiles/aoc24.txt', 'r') as file:
        iss = ImmuneSystemSimulator(file.read().strip('\n'))
    print(f"Part 1: {iss.get_winning_units()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
