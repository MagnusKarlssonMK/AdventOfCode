"""
Uses the json module to load the data and then traverses it recursivly to count the content.
"""
import sys
from pathlib import Path
import json

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2015/day12.txt')


class JSON:
    def __init__(self, rawstr: str) -> None:
        self.__jsonstr = rawstr
        self.__json = json.loads(rawstr)

    def get_number_sum(self, ignored: str = None) -> int:
        return self.__json_object_count(self.__json, ignored)

    def __json_object_count(self, json_input, ignored: str = None) -> int:
        if isinstance(json_input, dict):
            if ignored and ignored in json_input.values():
                return 0
            else:
                return sum([self.__json_object_count(json_input[j], ignored) for j in json_input])
        if isinstance(json_input, list):
            return sum([self.__json_object_count(j, ignored) for j in json_input])
        if isinstance(json_input, int):
            return json_input
        return 0  # strings have no value


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        json_data = JSON(file.read().strip('\n'))
    print(f"Part 1: {json_data.get_number_sum()}")
    print(f"Part 2: {json_data.get_number_sum('red')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
