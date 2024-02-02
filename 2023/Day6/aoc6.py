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
    racelist_p1: list[Race] = []

    for idx in range(len(timelist)):
        racelist_p1.append(Race(timelist[idx], distancelist[idx]))
    result_p1 = 1
    for race in racelist_p1:
        result_p1 *= race.score

    print("Part1: ", result_p1)

    # ---- Part 2 ----
    racetime_p2 = ""
    distance_p2 = ""
    for race in racelist_p1:
        racetime_p2 += str(race.time)
        distance_p2 += str(race.distance)

    race_p2 = Race(int(racetime_p2), int(distance_p2))

    print("Part2: ", race_p2.score)

    return 0


if __name__ == "__main__":
    sys.exit(main())
