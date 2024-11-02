"""
Similar to day 9.
Rather than going through all the permutations, try to reduce the space by using a BFS queue based on first and last
positions of the people seated so far, and only add an expansion of that combination to the queue if the score of the
people in the middle (who will not be affected by any further additions) yields a better result.

This works quite well and blazingly fast compared to brute-forcing with permutations, but the code is NASTY, definitely
would benefit from some restructuring.
"""
import time
from pathlib import Path


class SeatPlanner:
    __MYSELF = 'YOU'

    def __init__(self, rawstr: str) -> None:
        self.__people: set[str] = set()
        self.__happyness: dict[str: dict[str: int]] = {}
        for line in rawstr.splitlines():
            person1, _, lg, value, _, _, _, _, _, _, person2 = line.strip('.').split()
            self.__people.add(person1)
            if lg == 'lose':
                value = -int(value)
            else:
                value = int(value)
            if person1 not in self.__happyness:
                self.__happyness[person1] = {person2: value}
            else:
                self.__happyness[person1][person2] = value
        # Add yourself for part 2
        self.__happyness[SeatPlanner.__MYSELF] = {}
        for neighbor in self.__people:
            self.__happyness[SeatPlanner.__MYSELF][neighbor] = 0
            self.__happyness[neighbor][SeatPlanner.__MYSELF] = 0

    def get_max_happiness(self, addself: bool = False) -> int:
        people = set(self.__people)
        if addself:
            people.add(SeatPlanner.__MYSELF)
        first = people.pop()
        best_seen: dict[tuple[str, str]: list[list[set[str], int]]] = {}  # (first, last): (middle, value)
        queue: list[tuple[str, tuple[str], int]] = []
        for p in people:
            queue.append((p, tuple(), self.__get_happiness(list((first, p)))))
        while queue:
            last, middle, happy = queue.pop(0)
            best = True
            # Check if something better has been discovered since adding this entry to the queue
            if (first, last) in best_seen:
                for i, (oldset, oldhappy) in enumerate(best_seen[(first, last)]):
                    if oldset == set(middle) and oldhappy > happy:
                        best = False
                        break
            if not best:
                continue
            for new_last in people:
                if new_last != last and new_last not in middle:
                    new_middle: tuple[str] = (*middle, last)
                    new_happiness = self.__get_happiness(list((first, *new_middle, new_last)))
                    best = True
                    # Check if the new seating with this addition is worth pursuing
                    if (first, new_last) in best_seen:
                        for i, (oldset, oldhappy) in enumerate(best_seen[(first, new_last)]):
                            if oldset == set(new_middle):
                                if oldhappy >= new_happiness:
                                    best = False  # No use continuing this branch
                                else:
                                    best_seen[(first, new_last)][i][1] = new_happiness
                                break
                        else:
                            # No match was found - this was the first time we found this middle combo
                            best_seen[(first, new_last)].append([set(new_middle), new_happiness])
                    else:
                        # First time we try this combination of first and last
                        best_seen[(first, new_last)] = [[set(new_middle), new_happiness]]
                    if best:
                        queue.append((new_last, new_middle, new_happiness))
        maxhappy = 0
        # Go through the 'seen' data and find the max happiness where everyone is seated
        for pair in best_seen:
            for middle, happy in best_seen[pair]:
                if len(middle) == len(people) - 1:
                    maxhappy = max(maxhappy, happy)
        return maxhappy

    def __get_happiness(self, seating: list[str]) -> int:
        length = len(seating)
        return sum([self.__happyness[p][seating[(i + 1) % length]] + self.__happyness[p][seating[(i - 1) % length]]
                    for i, p in enumerate(seating)])


def main(aoc_input: str) -> None:
    planner = SeatPlanner(aoc_input)
    print(f"Part 1: {planner.get_max_happiness()}")
    print(f"Part 2: {planner.get_max_happiness(True)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2015/day13.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
