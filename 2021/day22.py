"""
Stores the cuboids as base point and 'delta' vector. I didn't end up using that format as much as I might have though.
(There's probably some more clever and less verbose ways to calculate the intersections for example.)
Basically run through the cuboids and find intersections and create 'negative' cuboids for the intersecting areas,
and then calculate the total volume from that.
"""
import sys
from dataclasses import dataclass
import re


@dataclass
class Coord:
    x: int
    y: int
    z: int

    def in_range(self, val: int) -> bool:
        return -val <= self.x <= val and -val <= self.y <= val and -val <= self.z <= val

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.x + other.x, self.y + other.y, self.z + other.z)


class Cuboid:
    def __init__(self, onoff: int, x1: int, x2: int, y1: int, y2: int, z1: int, z2: int) -> None:
        self.ison = onoff
        self.__basepoint = Coord(x1, y1, z1)
        self.__dvec = Coord(x2 - x1, y2 - y1, z2 - z1)
        # Assume that all inputs start from the 'lowest' point, i.e. all values in dvec are positive

    def is_inrange(self, limit: int) -> bool:
        return self.__basepoint.in_range(limit) and (self.__basepoint + self.__dvec).in_range(limit)

    def get_volume(self) -> int:
        return self.ison * (self.__dvec.x + 1) * (self.__dvec.y + 1) * (self.__dvec.z + 1)

    def get_intersection(self, other: "Cuboid") -> list["Cuboid"]:
        if any([self.__basepoint.x > other.__basepoint.x + other.__dvec.x,
                self.__basepoint.x + self.__dvec.x < other.__basepoint.x,
                self.__basepoint.y > other.__basepoint.y + other.__dvec.y,
                self.__basepoint.y + self.__dvec.y < other.__basepoint.y,
                self.__basepoint.z > other.__basepoint.z + other.__dvec.z,
                self.__basepoint.z + self.__dvec.z < other.__basepoint.z,]):
            return []
        x1 = max(self.__basepoint.x, other.__basepoint.x)
        y1 = max(self.__basepoint.y, other.__basepoint.y)
        z1 = max(self.__basepoint.z, other.__basepoint.z)
        x2 = min(self.__basepoint.x + self.__dvec.x, other.__basepoint.x + other.__dvec.x)
        y2 = min(self.__basepoint.y + self.__dvec.y, other.__basepoint.y + other.__dvec.y)
        z2 = min(self.__basepoint.z + self.__dvec.z, other.__basepoint.z + other.__dvec.z)
        return [Cuboid(other.ison, x1, x2, y1, y2, z1, z2)]

    def __repr__(self):
        return f"On: {self.ison} - {self.__basepoint} - {self.__dvec}"


class Reactor:
    def __init__(self, rawstr: str) -> None:
        self.__reboot_steps: list[Cuboid] = []
        for line in rawstr.splitlines():
            state, right = line.split()
            coords = list(map(int, re.findall(r"-?\d+", right)))
            self.__reboot_steps.append(Cuboid(1 if state == "on" else -1, *coords))

    def get_reboot_cubes(self, regionlimited: bool = True) -> int:
        processed_cuboids: list[Cuboid] = []
        for cuboid in self.__reboot_steps:
            if regionlimited and not cuboid.is_inrange(50):
                continue
            new_intersections = []
            for old_c in processed_cuboids:
                intersection = cuboid.get_intersection(old_c)
                if intersection:
                    intersection[0].ison *= -1
                    new_intersections.append(intersection[0])
            [processed_cuboids.append(i) for i in new_intersections]
            if cuboid.ison == 1:
                processed_cuboids.append(cuboid)
        return sum([c.get_volume() for c in processed_cuboids])


def main() -> int:
    with open('../Inputfiles/aoc22.txt', 'r') as file:
        myreactor = Reactor(file.read().strip('\n'))
    print(f"Part 1: {myreactor.get_reboot_cubes()}")
    print(f"Part 2: {myreactor.get_reboot_cubes(False)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
