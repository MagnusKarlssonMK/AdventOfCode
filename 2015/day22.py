"""
Seems initially like a simple problem, but lots of tiny details to stumble on in the game rules.
It's also really tempting to create a giant class structure and almost build an entire basis for an RPG game,
similarly to the previous day, which here really just made it much harder to actually solve the problem.
Basically keep game data in a state class which recursively tries different sequences of spells and finds the
most mana efficient one.
"""
import time
from pathlib import Path
from dataclasses import dataclass
from enum import Enum, auto
from copy import deepcopy


class Spells(Enum):
    MAGIC_MISSILE = auto()
    DRAIN = auto()
    SHIELD = auto()
    POISON = auto()
    RECHARGE = auto()


@dataclass(frozen=True)
class SpellEffects:
    value: int
    time: int

    def countdown(self) -> "SpellEffects":
        return SpellEffects(self.value, self.time - 1)


class GameState:
    """Class for handling DFS-like recursive search through the possible wizard actions."""
    min_mana_spent = None
    SPELLS: dict[Spells, tuple[int, tuple[SpellEffects, ...]]] = \
        {Spells.MAGIC_MISSILE: (53, (SpellEffects(4, 0),)),
         Spells.DRAIN: (73, (SpellEffects(2, 0), SpellEffects(2, 0))),
         Spells.SHIELD: (113, (SpellEffects(7, 6),)),
         Spells.POISON: (173, (SpellEffects(3, 6),)),
         Spells.RECHARGE: (229, (SpellEffects(101, 5),))}

    def __init__(self, bhp: int, bdmg: int, whp: int, wmn: int, hardmode: bool):
        self.__boss_hp = bhp
        self.__boss_dmg = bdmg
        self.__wizard_hp = whp
        self.__wizard_mana = wmn
        self.__hardmode = hardmode
        self.__turncount = 0
        self.__manaspent = 0
        self.__active_effects: dict[Spells, SpellEffects] = {}

    def __effects_tick(self) -> None:
        """Updates stats for any active additive effects, decreases their time by 1 and removes them from the state
        if time goes to 0."""
        expired: list[Spells] = []
        for effect in self.__active_effects:
            match effect:
                case Spells.POISON:
                    self.__boss_hp -= self.__active_effects[effect].value
                case Spells.RECHARGE:
                    self.__wizard_mana += self.__active_effects[effect].value
                case _:
                    pass
            self.__active_effects[effect] = self.__active_effects[effect].countdown()
            if self.__active_effects[effect].time <= 0:
                expired.append(effect)
        for e in expired:
            self.__active_effects.pop(e)
            # Note - somewhat unclear from the rules if Shield should last the entire round, but it doesn't matter
            # since it will always expire on the wizard's turn.

    def __cast_spell(self, spell: Spells) -> None:
        """Performs the actions related to casting a spell, i.e. direct damage / heal, or adding effect to state."""
        manacost, effects = GameState.SPELLS[spell]
        self.__wizard_mana -= manacost
        self.__manaspent += manacost
        match spell:
            case Spells.MAGIC_MISSILE:
                self.__boss_hp -= effects[0].value
            case Spells.DRAIN:
                self.__boss_hp -= effects[0].value
                self.__wizard_hp += effects[1].value
            case Spells.RECHARGE | Spells.POISON | Spells.SHIELD:
                self.__active_effects[spell] = effects[0]

    def play_round(self) -> None:
        """Recursive function looking for solutions and records the best solution in MIN_MANA_SPENT."""
        # If hardmode, on wizards turn, reduce HP with 1
        if self.__hardmode and self.__turncount % 2 == 0:
            self.__wizard_hp -= 1
            if self.__wizard_hp <= 0:
                return
        if GameState.min_mana_spent and self.__manaspent >= GameState.min_mana_spent:
            return
        self.__effects_tick()
        if self.__boss_hp <= 0:
            if not GameState.min_mana_spent:
                GameState.min_mana_spent = self.__manaspent
            else:
                GameState.min_mana_spent = min(GameState.min_mana_spent, self.__manaspent)
            return
        if self.__turncount % 2 == 0:
            # Wizards turn
            self.__turncount += 1
            for spell in Spells:
                if spell in self.__active_effects or GameState.SPELLS[spell][0] > self.__wizard_mana:
                    continue
                ns = deepcopy(self)
                ns.__cast_spell(spell)
                if ns.__boss_hp <= 0:
                    if not GameState.min_mana_spent:
                        GameState.min_mana_spent = ns.__manaspent
                    else:
                        GameState.min_mana_spent = min(GameState.min_mana_spent, ns.__manaspent)
                    return
                ns.play_round()
        else:
            # Boss's turn
            self.__turncount += 1
            armor = 0 if Spells.SHIELD not in self.__active_effects else self.__active_effects[Spells.SHIELD].value
            self.__wizard_hp -= max(1, self.__boss_dmg - armor)
            if self.__wizard_hp > 0:
                self.play_round()


class WizardSim:
    """Wrapper class to interface between main and gamestate and hold the initial game data."""
    def __init__(self, rawstr: str, wizardhp: int = 50, wizardmana: int = 500) -> None:
        lines = rawstr.splitlines()
        self.__boss_hp = int(lines[0].split()[-1])
        self.__boss_dmg = int(lines[1].split()[-1])
        self.__wizard_hp = wizardhp
        self.__wizard_mana = wizardmana

    def get_cheapest_win(self, hardmode: bool = False) -> int:
        state = GameState(self.__boss_hp, self.__boss_dmg, self.__wizard_hp, self.__wizard_mana, hardmode)
        state.play_round()
        result = GameState.min_mana_spent
        GameState.min_mana_spent = None
        if not result:
            return -1  # Will never happen, just to keep linter happy
        return result


def main(aoc_input: str) -> None:
    game = WizardSim(aoc_input)
    print(f"Part 1: {game.get_cheapest_win()}")
    print(f"Part 2: {game.get_cheapest_win(True)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2015/day22.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
