"""
Generate md5 hashes one-by-one, and for each
- check if it has 5 repeated characters, and if so, validate any pending previously found index with 3 repetitions of
that same character
- then check if it has 3 repeated characters, and if so, add its index to a dict of pending keys for validation. Only
add it to the first found character, in case there's more than one triple.

Use a hasher with a cache for at least some chance of reducing time for the ridiculous number of hashings required for
Part 2. It's still really quite slow though, Part 2 takes around a minute to complete.
"""
import sys
from pathlib import Path
import hashlib
import re
from functools import lru_cache

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2016/day14.txt')


@lru_cache(None)
def get_md5(inputstr: str, stretch: int = 0) -> str:
    result = inputstr
    for _ in range(stretch + 1):
        result = hashlib.md5(result.encode()).hexdigest()
    return result


class KeyGenerator:
    def __init__(self, salt: str) -> None:
        self.__salt = salt

    def get_64th_index(self, stretch: int = 0) -> int:
        nbr = 64
        index = 0
        keys = set()
        triples: dict[str: set[int]] = {}
        while len(keys) < nbr:
            h = get_md5(self.__salt + str(index), stretch)
            # Find any 5-repetitions (check the 5's first to avoid having a hash validate itself,
            # since it will also b a 3)
            for c in re.findall(r"(.)\1{4}", h):
                if c in triples:
                    for t in triples.pop(c):
                        if (index - t) < 1001:
                            keys.add(t)
            # Find any 3-repetitions, only consider the first match
            if c := re.findall(r"(.)\1{2}", h):
                if c[0] not in triples:
                    triples[c[0]] = {index}
                else:
                    triples[c[0]].add(index)
            index += 1
        # Note: the key validation probably validates more than one key, so there's likely more than 64 keys in the set.
        # I.e. we can't just take the max value of the set, we need to sort it and get the answer by index.
        return sorted(keys)[nbr - 1]


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        keygen = KeyGenerator(file.read().strip('\n'))
    print(f"Part 1: {keygen.get_64th_index()}")
    print(f"Part 2: {keygen.get_64th_index(2016)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
