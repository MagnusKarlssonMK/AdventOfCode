"""
Step 1: Determine the loop size from the public card key
Step 2: Use the loop size to transform the public door key into the encryption key
"""
import time
from pathlib import Path


class HotelDoor:
    __MOD = 20201227
    __SEED = 7

    def __init__(self, rawstr: str) -> None:
        self.__card_pub_key, self.__door_pub_key = list(map(int, rawstr.splitlines()))

    def get_encryption_key(self) -> int:
        # Get the loop size
        loop_size = 0
        value = 1
        while self.__card_pub_key != value:
            loop_size += 1
            value = (HotelDoor.__SEED * value) % HotelDoor.__MOD
        # Get the key from transforming the door key
        value = 1
        for _ in range(loop_size):
            value = (self.__door_pub_key * value) % HotelDoor.__MOD
        return value


def main(aoc_input: str) -> None:
    door = HotelDoor(aoc_input)
    print(f"Part 1: {door.get_encryption_key()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2020/day25.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
