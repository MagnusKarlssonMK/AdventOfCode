"""
Part 1: Note that the question is which particle will be closest *in the long term*, not the closest ever over the
entire trajectory. In the long term (i.e. t->inf), the closest will be the one with the lowest acceleration. However,
with my input, there's multiple particles sharing the same lowest acceleration, and making a secondary sorting on
initial velocity is not safe since it depends on the relative direction between velocity and acceleration.
So in lack of better ideas at the moment, I'll just stick with a bit of trial and error to try to find an estimate
of number of steps to run the simulation before it seems to stabilize.
"""
import sys
from pathlib import Path
import re
from dataclasses import dataclass
from copy import deepcopy

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2017/day20.txt')


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    def get_distance(self, other: "Point") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)


@dataclass(frozen=True)
class Particle:
    point: Point
    vel: Point
    acc: Point

    def step(self) -> "Particle":
        vel = self.vel + self.acc
        point = self.point + vel
        return Particle(point, vel, self.acc)


class GPU:
    def __init__(self, rawstr: str) -> None:
        self.__particles: list[Particle] = \
            [Particle(Point(*nbrs[0:3]), Point(*nbrs[3:6]), Point(*nbrs[6:])) for nbrs in
             [list(map(int, re.findall(r"-?\d+", line))) for line in rawstr.splitlines()]]

    def get_closest_particle(self) -> int:
        particles = deepcopy(self.__particles)
        for _ in range(1000):
            for p, part in enumerate(particles):
                particles[p] = part.step()
        distances = [p.point.get_distance(Point(0, 0, 0)) for p in particles]
        return distances.index(min(distances))

    def get_remaining_particle_count(self) -> int:
        particles = deepcopy(self.__particles)
        for _ in range(1000):
            seen_points = set()
            collided_points = set()
            for p, part in enumerate(particles):
                particles[p] = part.step()
                if particles[p].point in seen_points:
                    collided_points.add(particles[p].point)
                else:
                    seen_points.add(particles[p].point)

            collided_particles = []
            for cp in collided_points:
                for p in particles:
                    if p.point == cp:
                        collided_particles.append(p)
            for p in collided_particles:
                particles.remove(p)
        return len(particles)


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        gpu = GPU(file.read().strip('\n'))
    print(f"Part 1: {gpu.get_closest_particle()}")
    print(f"Part 2: {gpu.get_remaining_particle_count()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
