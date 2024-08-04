"""
Part 1:
Algebraic approach - if we start at y-position 0 with velocity V, then the position of 'y' as function over number of
steps 'n' can be derived as:
y(0) = 0
y(1) = 0 + V
y(2) = 0 + V + V - 1
y(3) = 0 + V + V - 1 + V - 2
...
y(n) = n*V - sum(1...(n-1)) = n*V - n*(n-1)/2
Or:
a)  y(n) = n*(V - (n-1)/2)
From this we can see that except at n=0, y will again cross 0 at V = (n-1)/2, or n = 2*V+1.
Assuming that the target y area is below zero, then to reach as high as possible would correspond to where in the step
after again reaching zero we immediately get to the y_min from the input, and we know that the velocity at that point
will be -V-1, so the best initial velocity will be
    V = abs(y_min) - 1
To find the maximum y-value in between these zero points, we can also express function 'a' as:
b)  y(n+1) = y(n) + V - (n-1)
The turning point will be when the y position is no longer increasing, meaning y(n+1) == y(n), i.e. V - (n-1) = 0.
Putting n = V + 1 into a) gives us:
Y-max = y(V+1) = Y(V) = (V+1)*V/2
We also assume that the X-axis does not impose any restrictions, since it caps off at 0 and thus it should always be
possible to find a starting x-velocity such that we hit the target range. This would only be an issue if the target
range is small and the number of steps low, but since we are effectively trying to use as many steps as possible in
to maximize the y-axis, this shouldn't be any issue at all.

Part 2:
In short: find the range of possible x-values and the number of steps 'n' for each value that would hit the target in
the x-axis, then do the same for the y-axis and combine the results - any x- and y-combination that has at least
one common 'n' value will be able to hit the target.
X-axis:
    We know that the maximum initial velocity is X-max of the target - any value greater than that will overshoot.
    The range for a certain initial velocity V is V*(V+1)/2, so to reach X-min we need at least minimum initial
    velocity V = ceil((-1+sqrt(1+8*Xmin))/2).
    We could be fancy and try to calculate the max and min n value for each initial x-velocity as well, but it's a bit
    more complicated, so try to just loop from n=0 and calculate x-position until either velocity is zero or we pass
    X-max.
Y-axis:
    We already know the maximum initial y-velocity from part 1. And the minimum will be Y-min, since smaller values
    than that will overshoot in the y-axis.
    Get the n-values for each valid y-value the same way as for x, however for positive initial velocities we already
    know how to calculate the number of steps to get back to y=0, so we can simply take the step counter from when
    evaluating the corresponding negative value -1 and just add that extra offset.
"""
import sys
from pathlib import Path
import re
import math

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2021/day17.txt')


class Steps:
    def __init__(self, minsteps: float) -> None:
        # Note: store values as float to be able to handle infinity values for when x-axis stops inside the range
        self.max = minsteps
        self.min = minsteps

    def __eq__(self, other: "Steps") -> bool:
        o_min = max(self.min, other.min)
        o_max = min(self.max, other.max)
        if o_min <= o_max:
            return True
        else:
            return False


class ProbeLauncer:
    def __init__(self, rawstr: str) -> None:
        nbrs = list(map(int, re.findall(r"-?\d+", rawstr)))
        self.__x_min = min(nbrs[0:2])
        self.__x_max = max(nbrs[0:2])
        self.__y_min = min(nbrs[2:4])
        self.__y_max = max(nbrs[2:4])

    def get_max_height(self) -> int:
        y = abs(self.__y_min) - 1
        return y * (y + 1) // 2

    def get_combination_count(self) -> int:
        # Get the x-axis ranges
        xmax_v = self.__x_max
        xmin_v = math.ceil((-1+math.sqrt(1+8*self.__x_min))/2)
        xv_val: dict[int: Steps] = {}
        for xv in range(xmin_v, xmax_v + 1):
            vel = xv
            x = 0
            n = 0
            while vel > 0 and x <= self.__x_max:
                n += 1
                x += vel
                vel -= 1
                if self.__x_min <= x <= self.__x_max:
                    if xv in xv_val:
                        xv_val[xv].max = n
                    else:
                        xv_val[xv] = Steps(n)
                    if vel == 0:
                        xv_val[xv].max = math.inf
        # Get the y-axis ranges
        ymin_v = self.__y_min
        yv_val: dict[int: Steps] = {}
        for yv in range(-1, ymin_v - 1, -1):
            vel = yv
            y = 0
            n = 0
            while y >= self.__y_min:
                n += 1
                y += vel
                vel -= 1
                if self.__y_min <= y <= self.__y_max:
                    if yv in yv_val:
                        yv_val[yv].max = n
                    else:
                        yv_val[yv] = Steps(n)
                    yv_up = abs(yv) - 1
                    if yv_up in yv_val:
                        yv_val[yv_up].max = n + (2 * yv_up) + 1
                    else:
                        yv_val[yv_up] = Steps(n + (2 * yv_up) + 1)
        # Crosscheck possible combinations
        combinations: set[tuple[int, int]] = set()
        for y in yv_val:
            for x in xv_val:
                if yv_val[y] == xv_val[x]:
                    combinations.add((x, y))
        return len(combinations)


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        mylauncher = ProbeLauncer(file.read().strip('\n'))
    print(f"Part 1: {mylauncher.get_max_height()}")
    print(f"Part 2: {mylauncher.get_combination_count()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
