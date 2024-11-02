"""
Basically a BFS solution, where the most important realization to get decent speed is that the isotope names are not
important in terms of state space, so instead we throw away the names and store the isotopes as pairs of current
floor of its microchip and its generator. (Not doing this abstraction causes the state space to explode with
different permutations of isotopes in the same overall state, just different names on the corresponding positions).
For part 2, simply add 2 isotopes with both generators and microchips on the first floor and run again.
"""
import time
from pathlib import Path
import re
from dataclasses import dataclass
from itertools import combinations
from copy import deepcopy


@dataclass(frozen=True)
class Isotope:
    microchip_floor: int
    generator_floor: int

    def __lt__(self, other: "Isotope") -> bool:
        # The actual order is not important, we just need to get a deterministic sorting of a list of isotopes, so that
        # we can identify identical states.
        if self.microchip_floor != other.microchip_floor:
            return self.microchip_floor < other.microchip_floor
        return self.generator_floor < other.generator_floor


@dataclass(frozen=True)
class State:
    elevator_floor: int
    isotopes: tuple[Isotope, ...]

    def get_next_states(self, topfloor: int) -> iter:
        # Make a list of (index, 'm'/'g') of all items on current elevator floor
        current_floor_items = []
        for i, iso in enumerate(self.isotopes):
            if iso.microchip_floor == self.elevator_floor:
                current_floor_items.append((i, 'm'))
            if iso.generator_floor == self.elevator_floor:
                current_floor_items.append((i, 'g'))
        move_combos = [(item,) for item in current_floor_items]  # Only take one item
        for pair in combinations(current_floor_items, 2):     # Combinations of two items
            move_combos.append(pair)
        for items in move_combos:
            if len(items) == 2 and items[0][1] != items[1][1] and items[0][0] != items[1][0]:
                continue  # We can't take a generator and a microchip of different items together on the elevator
            for elevator_direction in (-1, 1):
                newfloor = self.elevator_floor + elevator_direction
                if not 0 <= newfloor <= topfloor:
                    continue
                # rebuild the moved isotopes
                newisotopes = list(self.isotopes)
                for idx, t in items:
                    if t == 'm':
                        newisotopes[idx] = Isotope(newfloor, newisotopes[idx].generator_floor)
                    else:
                        newisotopes[idx] = Isotope(newisotopes[idx].microchip_floor, newfloor)
                newstate = State(newfloor, tuple(sorted(newisotopes)))
                if newstate.__is_valid_move():
                    yield newstate

    def __is_valid_move(self) -> bool:
        floors_w_gens = {i.generator_floor for i in self.isotopes}
        for i in self.isotopes:
            if i.microchip_floor != i.generator_floor and i.microchip_floor in floors_w_gens:
                # A chip without its generator buddy will get fried if it's on a floor with other generators.
                return False
        return True

    def is_complete(self, topfloor: int) -> bool:
        for i in self.isotopes:
            if i.microchip_floor != topfloor or i.generator_floor != topfloor:
                return False
        return True


class Facility:
    def __init__(self, rawstr: str) -> None:
        self.__topfloor = 0
        items = {}
        for floor, line in enumerate(rawstr.splitlines()):
            self.__topfloor = floor
            for i in re.findall(r" (\w+) generator", line):
                items[i] = [floor]
            for i in re.findall(r" (\w+)-compatible microchip", line):
                items[i].append(floor)
        self.__isotopes = [Isotope(m, g) for g, m in items.values()]
        # Note: the actual item names are not important (in terms of state space, the item pairs are interchangeable)

    def get_min_steps(self, extra_parts: bool = False) -> int:
        parts: list[Isotope] = deepcopy(self.__isotopes)
        if extra_parts:
            parts.append(Isotope(0, 0))
            parts.append(Isotope(0, 0))
        state = State(0, tuple(sorted(parts)))
        seen = set()
        queue = [(0, state)]
        while queue:
            steps, state = queue.pop(0)
            if state.is_complete(self.__topfloor):
                return steps
            if state in seen:
                continue
            seen.add(state)
            for newstate in state.get_next_states(self.__topfloor):
                if newstate not in seen:
                    queue.append((steps + 1, newstate))
        return -1


def main(aoc_input: str) -> None:
    facility = Facility(aoc_input)
    print(f"Part 1: {facility.get_min_steps()}")
    print(f"Part 2: {facility.get_min_steps(True)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2016/day11.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
