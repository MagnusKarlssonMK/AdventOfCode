import sys

"""
Rock:     0
Paper:    1
Scissors: 2
"""

handtonum = {'A': 0, 'B': 1, 'C': 2, 'X': 0, 'Y': 1, 'Z': 2}
numtohand = {0: 'A', 1: 'B', 2: 'C'}
scoretable = {0: 1, 1: 2, 2: 3}


def getscore(left: int, right: int) -> int:
    retval = scoretable[right]
    if left == right:  # Draw
        retval += 3
    elif (left + 1) % 3 == right:  # right wins
        retval += 6
    # else - left wins
    return retval


def determinehand(left: str, right: str) -> str:
    match right:
        case 'Y':  # Draw
            return left
        case 'X':  # Lose
            return numtohand[(handtonum[left] + 2) % 3]
        case 'Z':  # Win
            return numtohand[(handtonum[left] + 1) % 3]
    return ""


def main() -> int:
    result_p1 = 0
    result_p2 = 0
    with open('aoc2.txt', 'r') as file:
        for line in file.readlines():
            if len(line) > 1:
                left, right = line.strip('\n').split()
                result_p1 += getscore(handtonum[left], handtonum[right])
                result_p2 += getscore(handtonum[left], handtonum[determinehand(left, right)])
    print("Part1: ", result_p1)
    print("Part2: ", result_p2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
