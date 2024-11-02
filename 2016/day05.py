"""
Iterate with an increasing index value and use hashlib to calculate the md5 checksums to generate the passwords.
Takes a lot of iterations, i.e. doorbreaking is NOT fast.
"""
import time
from pathlib import Path
import hashlib


class Door:
    __PASSWORD_LEN = 8

    def __init__(self, rawstr: str) -> None:
        self.__door_id = rawstr

    def get_password(self) -> str:
        pwd = ''
        index = 0
        while len(pwd) < Door.__PASSWORD_LEN:
            hashed = hashlib.md5((self.__door_id + str(index)).encode()).hexdigest()
            if hashed.startswith('00000'):
                pwd += hashed[5]
            index += 1
        return pwd

    def get_advanced_password(self) -> str:
        pwd = ['_' for _ in range(Door.__PASSWORD_LEN)]
        index = 0
        while '_' in pwd:
            hashed = hashlib.md5((self.__door_id + str(index)).encode()).hexdigest()
            if hashed.startswith('00000') and hashed[5].isdigit():
                pos = int(hashed[5])
                if pos < Door.__PASSWORD_LEN:
                    if pwd[int(pos)] == '_':
                        pwd[int(pos)] = hashed[6]
            index += 1
        return ''.join(pwd)


def main(aoc_input: str) -> None:
    door = Door(aoc_input)
    print(f"Part 1: {door.get_password()}")
    print(f"Part 2: {door.get_advanced_password()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2016/day05.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
