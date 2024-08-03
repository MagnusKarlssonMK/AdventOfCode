import sys
import re


def mergeintervals(intervallist: list[list[int]]) -> iter:
    intervallist.sort()
    intqueue = [intervallist[0]]
    for i in intervallist[1:]:
        if intqueue[-1][0] <= i[0] <= intqueue[-1][-1]:
            intqueue[-1][-1] = max(intqueue[-1][-1], i[-1])
        else:
            intqueue.append(i)

    for i in range(len(intqueue)):
        yield intqueue[i]


class Sensor:
    def __init__(self, s_x: int, s_y: int, b_x: int, b_y: int):
        self.position: tuple[int, int] = s_x, s_y
        self.beacon: tuple[int, int] = b_x, b_y
        self.range: int = abs(s_x - b_x) + abs(s_y - b_y)

    def is_inrange(self, position: tuple[int, int]) -> bool:
        return self.range >= abs(self.position[0] - position[0]) + abs(self.position[1] - position[1])


class Zone:
    def __init__(self, rawstr: str):
        self.sensors: list[Sensor] = [Sensor(*list(map(int, re.findall(r"-?\d+", line))))
                                      for line in rawstr.splitlines()]

    def get_coverage(self, row: int) -> int:
        p1_rangelist: list[list[int]] = []  # Start, stop
        for sensor in self.sensors:
            if (x_at_y := sensor.range - abs(row - sensor.position[1])) > 0:
                p1_rangelist.append([sensor.position[0] - x_at_y, sensor.position[0] + x_at_y])
        # Merge overlapping ranges
        filtered_rangelist: list[list[int]] = [r for r in mergeintervals(p1_rangelist)]
        # Total number of tiles covered:
        totalcount = sum([1 + x[1] - x[0] for x in filtered_rangelist])
        # Subtract 1 for every beacon inside those ranges
        for beacon in list(filter(lambda x: x[1] == row, set([s.beacon for s in self.sensors]))):
            for r in filtered_rangelist:
                if r[0] <= beacon[0] <= r[1]:
                    totalcount -= 1
                    break
        return totalcount

    def get_darkpointfreq(self, maxsize: int) -> int:
        lines: dict[tuple[int, int]: int] = {}
        for sensor in self.sensors:
            # Create 4 lines representing the outsides of the sensor's area, y = ax + b, a = [1, -1]
            # Tuple values (a, b)
            upper_left = (1, sensor.position[1] - sensor.range - 1 - sensor.position[0])
            upper_right = (-1, sensor.position[1] - sensor.range - 1 + sensor.position[0])
            lower_left = (-1, sensor.position[1] + sensor.range + 1 + sensor.position[0])
            lower_right = (1, sensor.position[1] + sensor.range + 1 - sensor.position[0])
            for line in (upper_left, upper_right, lower_left, lower_right):
                if line in lines:
                    lines[line] += 1
                else:
                    lines[line] = 1
        # Filter out and keep only the lines that appear at least twice
        ascending: list[int] = []
        descending: list[int] = []
        for line, nbr in lines.items():
            if nbr > 1:
                if line[0] == 1:
                    ascending.append(line[1])
                else:
                    descending.append(line[1])

        positions: list[tuple[int, int]] = []
        for asc_b in ascending:
            for des_b in descending:
                x = (des_b - asc_b) // 2
                positions.append((x, x + asc_b))

        for p in positions:
            if 0 <= p[0] <= maxsize and 0 <= p[1] <= maxsize and self.__is_positiondark(p):
                return p[0] * 4000000 + p[1]
        return -1

    def __is_positiondark(self, position: tuple[int, int]) -> bool:
        for sensor in self.sensors:
            if sensor.is_inrange(position):
                return False
        return True


def main() -> int:
    with open('../Inputfiles/aoc15.txt', 'r') as file:
        myzone = Zone(file.read().strip('\n'))
    print("Part 1:", myzone.get_coverage(2000000))
    print("Part 2:", myzone.get_darkpointfreq(4000000))
    return 0


if __name__ == "__main__":
    sys.exit(main())
