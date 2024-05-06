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
From this we can see that except at n=0, y will again cross 0 at V = (n-1)/2, or n = 2*V+1 (of course, assuming that
the target y_min is < 0).
To reach as high as possible would correspond to the step after againg reaching zero we immediately get to the y_min
from the input, and we know that the velocity at that point will be -V-1, so the best initial velocity will be
V = abs(y_min)-1
To find the Y-max in between these zero points, we can also express the function as:
b)  y(n+1) = y(n) + V - (n-1)
The turning point will be when the y position is no longer increasing, meaning y(n+1) == y(n), i.e. V - (n-1) = 0.
Putting n = V + 1 into a) gives us:
Y-max = y(V+1) = Y(V) = (V+1)*V/2
We also assume that the X-axis does not impose any restrictions, and since it caps off at 0, it should always be
possible to find a starting velocity such that we hit the target range. This would only be an issue if the target
range is small and the number of steps low, but since we are effectively trying to use as many steps as possible in
to maximize the y-axis, this shouldn't be any issue at all.

"""
import sys
import re


class ProbeLauncer:
    def __init__(self, rawstr: str) -> None:
        nbrs = list(map(int, re.findall(r"-?\d+", rawstr)))
        self.__x_range = nbrs[0:2]
        self.__y_range = nbrs[2:4]

    def get_max_height(self) -> int:
        y = abs(min(self.__y_range)) - 1
        return y * (y + 1) // 2


def main() -> int:
    with open('../Inputfiles/aoc17.txt', 'r') as file:
        mylauncher = ProbeLauncer(file.read().strip('\n'))
    print(f"Part 1: {mylauncher.get_max_height()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
