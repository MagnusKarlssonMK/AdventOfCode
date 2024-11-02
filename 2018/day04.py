"""
Parsing, parsing, parsing... and then some sorting.
Not much else to say, just some dict trickery to extract the corresponding values / keys from the records.
"""
import time
from pathlib import Path
import re
from dataclasses import dataclass
from enum import Enum


class Event(Enum):
    BEGIN_SHIFT = 0
    FALLS_ASLEEP = 1
    WAKES_UP = 2


@dataclass(frozen=True)
class Timestamp:
    year: int
    month: int
    day: int
    hour: int
    minute: int

    def __lt__(self, other: "Timestamp") -> bool:
        if self.year != other.year:
            return self.year < other.year
        if self.month != other.month:
            return self.month < other.month
        if self.day != other.day:
            return self.day < other.day
        if self.hour != other.hour:
            return self.hour < other.hour
        return self.minute < other.minute


class Record:
    def __init__(self, rawstr: str) -> None:
        self.__records = []
        for line in rawstr.splitlines():
            left, right = line.split('] ')
            right = right.split()
            event = None
            guard = -1
            if right[0] == "Guard":
                guard = int(right[1].strip('#'))
                event = Event.BEGIN_SHIFT
            elif right[0] == "falls":
                event = Event.FALLS_ASLEEP
            elif right[0] == "wakes":
                event = Event.WAKES_UP
            self.__records.append((Timestamp(*list(map(int, re.findall(r"\d+", left)))), guard, event))
        self.__records.sort(key=lambda x: x[0])

    def get_guard_id(self) -> tuple[int, int]:
        guards = {g: {} for _, g, _ in self.__records if g != -1}  # guardid: (asleepminutes: count))
        asleepminute = -1
        guard = -1
        for timestamp, g, event in self.__records:
            match event:
                case Event.BEGIN_SHIFT:
                    guard = g
                case Event.FALLS_ASLEEP:
                    asleepminute = timestamp.minute
                case Event.WAKES_UP:
                    for t in range(asleepminute, timestamp.minute):
                        if t not in guards[guard]:
                            guards[guard][t] = 1
                        else:
                            guards[guard][t] += 1

        maxasleep = 0, 0, 0
        maxminute = 0, 0, 0
        for g in guards:
            if (m := sum(guards[g].values())) > maxasleep[1]:
                maxasleep = g, m, max(guards[g], key=guards[g].get)
            if guards[g] and (n := max(guards[g].values())) > maxminute[1]:
                maxminute = g, n, max(guards[g], key=guards[g].get)
        return maxasleep[0] * maxasleep[2], maxminute[0] * maxminute[2]


def main(aoc_input: str) -> None:
    record = Record(aoc_input)
    p1, p2 = record.get_guard_id()
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2018/day04.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
