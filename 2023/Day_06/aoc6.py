"""
Uses quadratic formula to calculate the two points where the score intersects the old record. One of the surprising
challenges was to round them off in the right direction, to also account for the few cases where the solution was
exactly the same value as the old record.
As it turned out, perhaps not super useful to create a class for storing the races.
"""
import sys
import math
import re


class Race:
    def __init__(self, t: int, d: int):
        self.time = t
        self.distance = d
        self.minvelocity = math.floor((self.time - math.sqrt(self.time**2 - (4 * self.distance))) / 2) + 1
        self.maxvelocity = math.ceil((self.time + math.sqrt(self.time**2 - (4 * self.distance))) / 2) - 1
        self.score = 1 + self.maxvelocity - self.minvelocity

    def __str__(self):
        return (f"Time: {self.time}, Distance: {self.distance}, MinVel: {self.minvelocity},\\"
                f" MaxVel: {self.maxvelocity}, Score: {self.score}")


def main() -> int:
    with open("../Inputfiles/aoc6.txt", "r") as file:
        timelist = list(map(int, re.findall(r"\d+", file.readline())))
        distancelist = list(map(int, re.findall(r"\d+", file.readline())))

    # ---- Part 1 ----
    racelist_p1: list[Race] = [Race(timelist[idx], distancelist[idx]) for idx in range(len(timelist))]
    result_p1 = math.prod([race.score for race in racelist_p1])
    print("Part1:", result_p1)

    # ---- Part 2 ----
    racetime_p2 = int(''.join([str(race.time) for race in racelist_p1]))
    distance_p2 = int(''.join([str(race.distance) for race in racelist_p1]))

    race_p2 = Race(racetime_p2, distance_p2)
    print("Part2:", race_p2.score)
    return 0


if __name__ == "__main__":
    sys.exit(main())
