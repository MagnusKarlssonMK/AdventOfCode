"""
Use regex to split the IP addresses in segments based on the brackets; the first segment and every other segment after
that will be a supernet, while the second segment and every other after that will be a hypernet.
From there on it's mostly just string parsing, with a sliding window over the strings to scan them for the patterns.
"""
import sys
from pathlib import Path
import re

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2016/day07.txt')


def contains_abba(word: str) -> bool:
    for i in range(len(word) - 3):
        if word[i] == word[i + 3] and word[i] != word[i + 1] and word[i + 1] == word[i + 2]:
            return True
    return False


def get_aba(word: str) -> iter:
    for i in range(len(word) - 2):
        if word[i] == word[i + 2] and word[i] != word[i + 1]:
            yield word[i: i + 3]


def get_bab(word: str) -> iter:
    for i in range(len(word) - 2):
        if word[i] == word[i + 2] and word[i] != word[i + 1]:
            yield word[i + 1] + word[i] + word[i + 1]


class IpAddress:
    def __init__(self, ip: str) -> None:
        self.__supernets = []
        self.__hypernets = []
        for i, s in enumerate(re.split(r"\[([^]]+)]", ip)):
            if i % 2 == 0:
                self.__supernets.append(s)
            else:
                self.__hypernets.append(s)

    def supports_tls(self) -> bool:
        for word in self.__hypernets:
            if contains_abba(word):
                return False
        for word in self.__supernets:
            if contains_abba(word):
                return True
        return False

    def supports_ssl(self) -> bool:
        aba = set()
        bab = set()
        for word in self.__supernets:
            for a in get_aba(word):
                aba.add(a)
        for word in self.__hypernets:
            for a in get_bab(word):
                bab.add(a)
        return len(aba & bab) > 0


class IpDatabase:
    def __init__(self, rawstr: str) -> None:
        self.__ipaddr = [IpAddress(line) for line in rawstr.splitlines()]

    def get_tls_support_count(self) -> int:
        return sum([1 if ip.supports_tls() else 0 for ip in self.__ipaddr])

    def get_ssl_support_count(self) -> int:
        return sum([1 if ip.supports_ssl() else 0 for ip in self.__ipaddr])


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        iplist = IpDatabase(file.read().strip('\n'))
    print(f"Part 1: {iplist.get_tls_support_count()}")
    print(f"Part 2: {iplist.get_ssl_support_count()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
