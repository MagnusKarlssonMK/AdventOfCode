# Advent of code 2023 Day 21
# Not done - part 2 still not working

Vstate = {"Visited": 0, "Seen": 1, "Unseen": 2}
Vertex = tuple[int, int]  # row, col
Vproperties = list[str, int, Vertex]  # state


class Grid:
    def __init__(self):
        self.gridpoints = []
        self.height = 0
        self.width = 0

    def addrow(self, newrow: str) -> None:
        self.gridpoints.append(newrow)
        self.width = max(self.width, len(newrow))
        self.height += 1

    def getneighbors(self, invertex: Vertex) -> list[Vertex]:
        retlist = []
        if invertex[0] > 0:  # Up
            if self.gridpoints[invertex[0] - 1][invertex[1]] != "#":
                retlist.append((invertex[0] - 1, invertex[1]))
        if invertex[0] < self.height - 1:   # Down
            if self.gridpoints[invertex[0] + 1][invertex[1]] != "#":
                retlist.append((invertex[0] + 1, invertex[1]))
        if invertex[1] > 0:  # Left
            if self.gridpoints[invertex[0]][invertex[1] - 1] != "#":
                retlist.append((invertex[0], invertex[1] - 1))
        if invertex[1] < self.width - 1:   # Right
            if self.gridpoints[invertex[0]][invertex[1] + 1] != "#":
                retlist.append((invertex[0], invertex[1] + 1))
        return retlist

    def getreachablecells(self, vstart: Vertex, nbrsteps: int) -> int:
        vertexlist: dict[Vertex: Vproperties] = {}
        bfs_queue = [vstart]
        vertexlist[vstart] = [Vstate["Seen"], 0, None]
        while len(bfs_queue) > 0:
            u = bfs_queue.pop(0)
            neighbors = self.getneighbors(u)
            for v in neighbors:
                try:
                    if vertexlist[v][0] != Vstate["Unseen"]:
                        continue
                except KeyError:
                    pass
                vertexlist[v] = [Vstate["Seen"], vertexlist[u][1] + 1, u]
                bfs_queue.append(v)
            vertexlist[u][0] = Vstate["Visited"]
        count = 0
        offset = sum(vstart) % 2
        for vkey in list(vertexlist.keys()):
            if vertexlist[vkey][1] <= nbrsteps and (vertexlist[vkey][1] % 2 == (nbrsteps + offset) % 2):
                count += 1
        return count


grid = Grid()
start: Vertex = -1, -1

with open("aoc21.txt", "r") as file:
    for line in file.readlines():
        if len(line) > 1:
            grid.addrow(line.strip("\n"))
            if (startidx := line.find("S")) >= 0:
                start = grid.height - 1, startidx

print("Part1: ", grid.getreachablecells(start, 64))

D = 26501365
w = grid.width
h = w
s = (w - 1) // 2, (h - 1) // 2
N = (D - s[0]) // w
E = grid.getreachablecells(s, 3 * w)
O = grid.getreachablecells(s, (3 * w) + 1)
print(f"N={N} E={E} O= {O}")
sa = w + D - (N * w) - 1
sb = D - (N * w)
st = w - 1

a1 = grid.getreachablecells((0, 0), sa)
a2 = grid.getreachablecells((0, h - 1), sa)
a3 = grid.getreachablecells((w - 1, 0), sa)
a4 = grid.getreachablecells((w - 1, h - 1), sa)
a_tot = a1 + a2 + a3 + a4
b1 = grid.getreachablecells((0, 0), sb)
b2 = grid.getreachablecells((0, h - 1), sb)
b3 = grid.getreachablecells((w - 1, 0), sb)
b4 = grid.getreachablecells((w - 1, h - 1), sb)
b_tot = b1 + b2 + b3 + b4
t1 = grid.getreachablecells((0, s[1]), st)
t2 = grid.getreachablecells((s[0], 0), st)
t3 = grid.getreachablecells((w - 1, s[1]), st)
t4 = grid.getreachablecells((s[0], h - 1), st)
t_tot = t1 + t2 + t3 + t4

print(f"A={a_tot} B={b_tot} T={t_tot}")

F = (O * ((N - 1) ** 2)) + (E * (N ** 2)) + (a_tot * (N - 1)) + (N * b_tot) + t_tot

print("F=", F)
# 610158222359995

# Correct answer: 610158187362102
