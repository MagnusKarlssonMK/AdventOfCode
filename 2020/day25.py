"""
Step 1: Determine the loop size from the public card key
Step 2: Use the loop size to transform the public door key into the encryption key
"""
import sys


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


def main() -> int:
    with open('../Inputfiles/aoc25.txt', 'r') as file:
        door = HotelDoor(file.read().strip('\n'))
    print(f"Part 1: {door.get_encryption_key()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
