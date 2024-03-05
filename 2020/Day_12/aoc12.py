"""
Create a ship class that holds the position and direction of the ship / waypoint.
Possibly for refactoring - try to see if there is a way to merge the two ship variants.
"""
import sys

Directions = {'N': (0, 1), 'S': (0, -1), 'W': (-1, 0), 'E': (1, 0)}
Actions = ('N', 'E', 'S', 'W', 'L', 'R', 'F')


class Ship:
    def __init__(self):
        self.xy = 0, 0
        self.direction = 'E'

    def perform_instruction(self, action: str, value: int) -> None:
        if action in ('L', 'R'):
            diridx = Actions.index(self.direction)
            if action == 'R':
                self.direction = Actions[(diridx + value // 90) % 4]
            else:
                self.direction = Actions[(diridx - value // 90) % 4]
            return
        direction = self.direction
        if action in ('N', 'E', 'S', 'W'):
            direction = action
        self.xy = (self.xy[0] + (Directions[direction][0] * value), self.xy[1] + (Directions[direction][1] * value))

    def get_distance(self) -> int:
        return abs(self.xy[0]) + abs(self.xy[1])


class ShipV2(Ship):
    def __init__(self):
        super().__init__()
        self.waypoint = (10, 1)

    def perform_instruction(self, action: str, value: int) -> None:
        if action in ('L', 'R'):
            match (value // 90) % 4:
                case 1:
                    if action == 'R':
                        self.waypoint = self.waypoint[1], -self.waypoint[0]
                    else:
                        self.waypoint = -self.waypoint[1], self.waypoint[0]
                case 2:
                    self.waypoint = -self.waypoint[0], -self.waypoint[1]
                case 3:
                    if action == 'L':
                        self.waypoint = self.waypoint[1], -self.waypoint[0]
                    else:
                        self.waypoint = -self.waypoint[1], self.waypoint[0]
        if action in ('N', 'E', 'S', 'W'):
            self.waypoint = (self.waypoint[0] + (Directions[action][0] * value),
                             self.waypoint[1] + (Directions[action][1] * value))
        if action == 'F':
            self.xy = self.xy[0] + (self.waypoint[0] * value), self.xy[1] + (self.waypoint[1] * value)


def main() -> int:
    myship = Ship()
    myshipv2 = ShipV2()
    with open('../Inputfiles/aoc12.txt', 'r') as file:
        for line in file.read().strip('\n').splitlines():
            myship.perform_instruction(line[0], int(line[1:]))
            myshipv2.perform_instruction(line[0], int(line[1:]))
    print("Part 1:", myship.get_distance())
    print("Part 2:", myshipv2.get_distance())
    return 0


if __name__ == "__main__":
    sys.exit(main())
