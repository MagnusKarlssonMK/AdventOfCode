"""

"""
import sys
from dataclasses import dataclass


@dataclass
class Coordinate:
    x: int
    y: int
    z: int

    def get_distance(self, other: "Coordinate") -> int:
        return (self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2

    def __repr__(self):
        return f"{self.x}, {self.y}, {self.z}"


class Scanner:
    def __init__(self, rawstr: str) -> None:
        lines = rawstr.splitlines()
        self.id = int(lines[0].split()[2])  # TBD - Need to store the scanner id?
        self.__beacons = [Coordinate(*list(map(int, lines[i].split(',')))) for i in range(1, len(lines))]
        self.__distancematrix = [[0 for _ in range(len(self.__beacons))] for _ in range(len(self.__beacons))]
        for i in range(len(self.__beacons) - 1):
            for j in range(i + 1, len(self.__beacons)):
                self.__distancematrix[i][j] = self.__beacons[i].get_distance(self.__beacons[j])
                self.__distancematrix[j][i] = self.__distancematrix[i][j]


class Probe:
    NBR_OF_BEACONS = 12

    def __init__(self, rawstr: str) -> None:
        self.__scanners = [Scanner(s) for s in rawstr.split('\n\n')]

    def placeholder(self) -> int:
        return -1


def main() -> int:
    with open('../Inputfiles/aoc19_example.txt', 'r') as file:
        myprobe = Probe(file.read().strip('\n'))
    print(f"Part 1: {myprobe.placeholder()}")
    a = {1, 4, 3, 2, 8}
    b = {4, 8, 3, 1, 2}
    print(a == b)
    return 0


if __name__ == "__main__":
    sys.exit(main())
