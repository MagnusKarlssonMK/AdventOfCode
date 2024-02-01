import sys


def main() -> int:
    with open('aoc1.txt', 'r') as file:
        numbers = list(map(int, file.read().strip('\n').split('\n')))
    inc_count_p1 = 0
    for n in range(1, len(numbers)):
        if numbers[n] > numbers[n-1]:
            inc_count_p1 += 1
    print("Part 1: ", inc_count_p1)

    window_buffer = []
    previous = 999999
    inc_count_p2 = 0
    for n in range(len(numbers)):
        window_buffer.append(numbers[n])
        if len(window_buffer) > 3:
            window_buffer.pop(0)
            if sum(window_buffer) > previous:
                inc_count_p2 += 1
            previous = sum(window_buffer)
    print("Part 2: ", inc_count_p2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
