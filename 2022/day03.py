import sys


def main() -> int:
    rangelist = ((range(ord('a'), ord('z') + 1), 1),
                 (range(ord('A'), ord('Z') + 1), 27))
    totalprio_p1 = 0
    totalprio_p2 = 0
    with open('../Inputfiles/aoc3.txt', 'r') as file:
        linebuffer = []
        for line in file.read().strip('\n').splitlines():
            linebuffer.append(line)
            left, right = line[:len(line) // 2], line[len(line) // 2:]
            shared_p1 = ''.join(set(left).intersection(right))
            if len(shared_p1) > 0:
                totalprio_p1 += sum([ord(shared_p1[0]) - r[0].start + r[1] for r in rangelist
                                     if ord(shared_p1[0]) in r[0]])
            if len(linebuffer) >= 3:
                shared_p2 = ''.join(set(linebuffer[0]).intersection(linebuffer[1]).intersection(linebuffer[2]))
                linebuffer.clear()
                if len(shared_p2) > 0:
                    totalprio_p2 += sum([ord(shared_p2[0]) - r[0].start + r[1] for r in rangelist
                                         if ord(shared_p2[0]) in r[0]])
    print("Part1:", totalprio_p1)
    print("Part2:", totalprio_p2)

    return 0


if __name__ == "__main__":
    sys.exit(main())
