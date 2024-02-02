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


def main() -> int:
    sensors: dict[tuple[int, int]: tuple[int, int]] = {}
    p1_rangelist: list[list[int]] = []  # Start, stop
    y_value = 2000000
    with open('../Inputfiles/aoc15.txt', 'r') as file:
        for line in file.read().strip('\n').split('\n'):
            s_x, s_y, b_x, b_y = list(map(int, re.findall(r"-?\d+", line)))
            sensors[(s_x, s_y)] = (b_x, b_y)
            manhattan = abs(s_x - b_x) + abs(s_y - b_y)
            x_at_y = manhattan - abs(y_value - s_y)
            if x_at_y > 0:
                p1_rangelist.append([s_x - x_at_y, s_x + x_at_y])
    # Merge overlapping ranges
    filtered_rangelist: list[list[int]] = []
    for r in mergeintervals(p1_rangelist):
        filtered_rangelist.append(r)

    # Total number of tiles covered:
    totalcount = sum([1 + x[1] - x[0] for x in filtered_rangelist])
    # Subtract 1 for every beacon inside those ranges
    for beacon in list(filter(lambda x: x[1] == y_value, set(sensors.values()))):
        for r in filtered_rangelist:
            if r[0] <= beacon[0] <= r[1]:
                totalcount -= 1
                break
    print("Part1: ", totalcount)
    return 0


if __name__ == "__main__":
    sys.exit(main())

# P1: 5394423
# P2: 11840879211051
