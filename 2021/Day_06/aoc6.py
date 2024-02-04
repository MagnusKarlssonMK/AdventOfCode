"""
Solution - rather than storing each and every lantern fish individually, simply store a list of internal timer states
0 - 8 and how many fish are in each state. When stepping a day, simply pop the first element in the list corresponding
to state-0 and add that number to state-6 and also append that number to state-8.
"""
import sys


def main() -> int:
    fish_states = [0 for _ in range(9)]
    with open('../Inputfiles/aoc6.txt', 'r') as file:
        for nbr in list(map(int, file.read().strip('\n').split(','))):
            fish_states[nbr] += 1

    # 80 days:
    p1 = 0
    for n in range(256):
        state_0 = fish_states.pop(0)
        fish_states[6] += state_0
        fish_states.append(state_0)
        if n == 79:
            p1 = sum(fish_states)
    print("Part 1: ", p1)
    print("Part 2: ", sum(fish_states))
    return 0


if __name__ == "__main__":
    sys.exit(main())
