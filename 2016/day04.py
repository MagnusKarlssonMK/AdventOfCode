"""
2016 day 4 - Security Through Obscurity
"""
import time
from pathlib import Path


class Room:
    def __init__(self, s: str) -> None:
        self.__sector_id = 0
        self.__checksum = ""
        parts = s.split('-')
        words = [p for p in parts if ']' not in p]
        left, right = parts[-1].split('[')
        self.__sector_id = int(left)
        self.__checksum = right.strip(']')
        self.__words = tuple(words)

    def validate(self) -> int:
        """Generates the checksum for the words, and returns the sector id if it 
        matches the stored checksum from the input, otherwise zero."""
        letters = ''.join(self.__words)
        lettercount: dict[str, int] = {}
        for c in letters:
            if c not in lettercount:
                lettercount[c] = 1
            else:
                lettercount[c] += 1
        if len(lettercount) >= len(self.__checksum):
            # Sort by number of occurrences first, alphabetically second, and extract the top 5
            candidate = ''.join([i[0] for i in sorted(list(lettercount.items()), key=lambda x: (-x[1], x[0]))[:len(self.__checksum)]])
            if candidate == self.__checksum:
                return self.__sector_id
        return 0

    def decode_check(self, target: list[str]) -> bool:
        """Returns whether the decoded name of the room matches the target."""
        # 1. Check number of words
        if len(self.__words) != len(target):
            return False
        # 2. Check number of letters in each word
        for left, right in zip(self.__words, target):
            if len(left) != len(right):
                return False
        # 3. Decode the words and compare to target
        decoded_name = [''.join([chr((ord(c) - ord('a') + self.__sector_id) % (1 + ord('z') - ord('a')) + ord('a')) for c in word]) for word in self.__words]
        return decoded_name == target


class InputData:
    def __init__(self, s: str) -> None:
        self.__rooms: list[Room] = [Room(line) for line in s.splitlines()]

    def solve(self) -> tuple[int, int]:
        p1 = 0
        p2 = 0
        TARGET = ["northpole", "object", "storage"]
        for room in self.__rooms:
            s_id = room.validate()
            p1 += s_id
            if room.decode_check(TARGET):
                p2 = s_id
        return p1, p2


def main(aoc_input: str) -> None:
    kiosk = InputData(aoc_input)
    p1, p2 = kiosk.solve()
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2016/day04.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
