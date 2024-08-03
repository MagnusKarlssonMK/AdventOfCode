"""
Represent the grid with a set of infected points, and store non-clean points in a dict with its state. While performing
the bursts, add the point or update its state if the point the virus is on is no longer clean, or remove it from the
dict if it becomes clean.
"""
import sys
from dataclasses import dataclass
from enum import Enum
from copy import deepcopy


class NodeState(Enum):
    CLEAN = 0
    WEAKENED = 1
    INFECTED = 2
    FLAGGED = 3


@dataclass(frozen=True)
class Point:
    row: int
    col: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.row + other.row, self.col + other.col)

    def turn_left(self) -> "Point":
        return Point(-self.col, self.row)

    def turn_right(self) -> "Point":
        return Point(self.col, -self.row)

    def turn_back(self) -> "Point":
        return Point(-self.row, -self.col)


class Cluster:
    def __init__(self, rawstr: str) -> None:
        self.__infected: dict[Point: NodeState] = {}
        lines = rawstr.splitlines()
        for row, line in enumerate(lines):
            for col, c in enumerate(line):
                if c == '#':
                    self.__infected[Point(row, col)] = NodeState.INFECTED
        self.__virus_pos = Point(len(lines) // 2, len(lines[0]) // 2)
        self.__virus_dir = Point(-1, 0)
        self.__startvalues = (deepcopy(self.__infected), deepcopy(self.__virus_pos), deepcopy(self.__virus_dir))

    def __reset(self):
        self.__infected = deepcopy(self.__startvalues[0])
        self.__virus_pos = deepcopy(self.__startvalues[1])
        self.__virus_dir = deepcopy(self.__startvalues[2])

    def __perform_burst(self) -> bool:
        current_infected = self.__virus_pos in self.__infected
        if current_infected:
            self.__virus_dir = self.__virus_dir.turn_right()
            self.__infected.pop(self.__virus_pos)
        else:
            self.__virus_dir = self.__virus_dir.turn_left()
            self.__infected[self.__virus_pos] = NodeState.INFECTED
        self.__virus_pos += self.__virus_dir
        return not current_infected

    def __perform_evolved_burst(self) -> bool:
        current_state = NodeState.CLEAN if self.__virus_pos not in self.__infected \
            else self.__infected[self.__virus_pos]
        newstate = None
        match current_state:
            case NodeState.CLEAN:
                self.__virus_dir = self.__virus_dir.turn_left()
                newstate = NodeState.WEAKENED
            case NodeState.WEAKENED:
                newstate = NodeState.INFECTED
            case NodeState.INFECTED:
                self.__virus_dir = self.__virus_dir.turn_right()
                newstate = NodeState.FLAGGED
            case NodeState.FLAGGED:
                self.__virus_dir = self.__virus_dir.turn_back()
                newstate = NodeState.CLEAN
        if newstate != NodeState.CLEAN:
            self.__infected[self.__virus_pos] = newstate
        else:
            self.__infected.pop(self.__virus_pos)
        self.__virus_pos += self.__virus_dir
        return newstate == NodeState.INFECTED

    def get_infected_count(self, bursts: int, evolved: bool = False) -> int:
        if not evolved:
            result = sum([1 for _ in range(bursts) if self.__perform_burst()])
        else:
            result = sum([1 for _ in range(bursts) if self.__perform_evolved_burst()])
        self.__reset()
        return result


def main() -> int:
    with open('../Inputfiles/aoc22.txt', 'r') as file:
        cluster = Cluster(file.read().strip('\n'))
    print(f"Part 1: {cluster.get_infected_count(10_000)}")
    print(f"Part 2: {cluster.get_infected_count(10_000_000, True)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
