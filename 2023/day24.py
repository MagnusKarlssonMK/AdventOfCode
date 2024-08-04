"""
Part 1: Iterates over all combinations of intersections using itertools, and finds the intersection (if any) for
all combinations using x0, y0 = (b1*c2-b2*c1)/(a1*b2-a2*b1) , (c1*a2-c2*a1)/(a1*b2-a2*b1). y = x*dy/dx + c, so
a=dy, b=-dx, c can be found based on the given coordinate.
Part 2: Uses the sympy equation solver to find the answer. I may have borrowed the basis for this solution from
people smarter than me...
"""
import sys
from pathlib import Path
from itertools import combinations
import sympy as sp

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2023/day24.txt')


class Hailstone:
    def __init__(self, rawstr: str) -> None:
        left, right = rawstr.split(' @ ')
        self.x, self.y, self.z = list(map(int, left.split(', ')))
        self.dx, self.dy, self.dz = list(map(int, right.split(', ')))

    def get_2d_intersection(self, other: 'Hailstone') -> tuple[bool, float, float]:  # Intersects, x, y
        """Calculates the intersection point (if any) of two hailstones in the XY plane. Also checks whether
        the intersection happens in the future. Returns a boolean to indicate whether any future intersection
        was found, and the X,Y coordinates for it."""
        a1, a2 = self.dy, other.dy
        b1, b2 = -self.dx, -other.dx
        if (d := (a1 * b2) - (a2 * b1)) == 0:
            return False, 0, 0
        c1 = -((self.x * self.dy) - (self.y * self.dx))
        c2 = -((other.x * other.dy) - (other.y * other.dx))
        x0 = ((b1 * c2) - (b2 * c1)) / d
        y0 = ((c1 * a2) - (c2 * a1)) / d
        if (((x0 > self.x and self.dx > 0) or (x0 < self.x and self.dx < 0)) and
                ((x0 > other.x and other.dx > 0) or (x0 < other.x and other.dx < 0))):
            return True, x0, y0
        return False, x0, y0

    def get_datapoints(self) -> tuple[int, int, int, int, int, int]:
        return self.x, self.y, self.z, self.dx, self.dy, self.dz

    def __str__(self):
        return f"({self.x},{self.y},{self.z}) - ({self.dx},{self.dy},{self.dz})"


class Air:
    def __init__(self) -> None:
        self.hailstones: list[Hailstone] = []
        self.xy_intersection_range = (200000000000000, 400000000000000)

    def add_hailstone(self, rawstr: str) -> None:
        self.hailstones.append(Hailstone(rawstr))

    def get_2d_intersectioncount(self) -> int:
        intersections = 0
        for h1, h2 in combinations(self.hailstones, 2):
            intersects, x, y = h1.get_2d_intersection(h2)
            if (intersects and self.xy_intersection_range[0] <= x <= self.xy_intersection_range[1] and
                    self.xy_intersection_range[0] <= y <= self.xy_intersection_range[1]):
                intersections += 1
        return intersections

    def get_3d_silverbullet(self) -> int:
        """Calculates and returns the score for part 2."""
        unknowns = sp.symbols('x y z dx dy dz t1 t2 t3')
        x, y, z, dx, dy, dz, *time = unknowns
        equations = []
        # Note: 3 stones is enough datapoints to find the solution, no need to go through the entire list
        for t, h in zip(time, [self.hailstones[stone].get_datapoints() for stone in range(3)]):
            equations.append(sp.Eq(x + t * dx, h[0] + t * h[3]))
            equations.append(sp.Eq(y + t * dy, h[1] + t * h[4]))
            equations.append(sp.Eq(z + t * dz, h[2] + t * h[5]))
        solution = sp.solve(equations, unknowns).pop()
        return sum(solution[:3])


def main() -> int:
    myair = Air()
    with open(INPUT_FILE, 'r') as file:
        for line in file.read().strip('\n').splitlines():
            myair.add_hailstone(line)
    print(f"Part 1: {myair.get_2d_intersectioncount()}")
    print(f"Part 2: {myair.get_3d_silverbullet()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
