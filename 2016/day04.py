"""
Do most of the heavy lifting in a Room class, which will hold the input values and provides functions for validating
the checksum and decodes the string.
"""
import sys
import re


class Room:
    def __init__(self, words: list[str], sectorid: int, checksum: str) -> None:
        self.__words = tuple(words)
        self.__sector_id = sectorid
        self.__checksum = checksum

    def __validate_checksum(self) -> bool:
        """Generates the checksum for the words, and returns whether it matches the stored checksum from the input."""
        letters = ''.join(self.__words)
        lettercount = {}
        for c in letters:
            if c not in lettercount:
                lettercount[c] = 1
            else:
                lettercount[c] += 1
        if len(lettercount) < 5:  # Safety measure, just in case there's less than 5 unique characters in the string
            return False
        # Sort by number of occurrences first, alphabetically second, and extract the top 5
        chksum = ''.join([i[0] for i in sorted(list(lettercount.items()), key=lambda x: (-x[1], x[0]))[:5]])
        return chksum == self.__checksum

    def get_real_sectorid(self) -> int:
        """Returns the sector-id of the room if it is valid, otherwise 0."""
        if self.__validate_checksum():
            return self.__sector_id
        return 0

    def decode_room(self) -> str:
        """Returns the decoded name of the room."""
        decoded_name = ''
        for word in self.__words:
            for c in word:
                nbr = (ord(c) - ord('a') + self.__sector_id) % (1 + ord('z') - ord('a')) + ord('a')
                decoded_name += chr(nbr)
            decoded_name += ' '
        return decoded_name.strip()  # A bit ugly, but a strip just to remove the last added space at the end...


class Kiosk:
    def __init__(self, rawstr: str) -> None:
        self.__rooms = []
        for line in rawstr.splitlines():
            *words, sec_id, chksm = re.findall(r"\w+", line)
            self.__rooms.append(Room(words, int(sec_id), chksm))
        self.__decoded_rooms: dict[str: int] = {}

    def get_real_rooms_sector_sum(self) -> int:
        total = 0
        for room in self.__rooms:
            if (secid := room.get_real_sectorid()) > 0:
                total += secid
                self.__decoded_rooms[room.decode_room()] = secid
        return sum([room.get_real_sectorid() for room in self.__rooms])

    def get_north_pole_sectorid(self) -> int:
        for room in self.__decoded_rooms:
            if room == 'northpole object storage':
                return self.__decoded_rooms[room]
        return -1


def main() -> int:
    with open('../Inputfiles/aoc4.txt', 'r') as file:
        kiosk = Kiosk(file.read().strip('\n'))
    print(f"Part 1: {kiosk.get_real_rooms_sector_sum()}")
    print(f"Part 2: {kiosk.get_north_pole_sectorid()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
