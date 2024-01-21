# Change "aocpart" to select part (A or B)
# Could do with some cleanup, and possibly some optimizations (part 2 is really slow)
# Consider adding a classs function in Grid to do the bulk of the work in what would be "main", and use a class
# attribute to select p1 or p2 (A / B)

RowCol = tuple[int, int]
Directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
OppositeChar = ["^", "<", "v", ">"]


class Grid:
    def __init__(self):
        self.grid = []
        self.width = 0
        self.height = 0

    def addrow(self, rawstring: str):
        self.grid.append(rawstring)
        self.width = max(len(rawstring), self.width)
        self.height += 1

    def findneighbors(self, incoord: RowCol) -> list[RowCol]:
        retval = []
        for dR, dC in Directions:
            if (0 <= incoord[0] + dR < self.height and 0 <= incoord[1] + dC < self.width and
                    self.grid[incoord[0] + dR][incoord[1] + dC] != "#"):
                retval.append((incoord[0] + dR, incoord[1] + dC))
        return retval


class AdjacencyList:
    def __init__(self):
        self.adj: dict[RowCol: list[tuple[RowCol, int]]] = {}  # vertexXY: list(neighborXY, cost)

    def dfs(self, start: RowCol, end: RowCol, seen=None) -> list:
        if start == end:
            return [0]
        if seen is None:
            seen = set()
        seen.add(start)
        lengthlist = []
        for nextvertex, distance in self.adj[start]:
            if nextvertex not in seen:
                for length in self.dfs(nextvertex, end, seen):
                    lengthlist.append(length + distance)
        seen.remove(start)
        return lengthlist


mygrid = Grid()
startnode = None
exitnode = None
alist = AdjacencyList()

with open("aoc23.txt", "r") as file:
    [mygrid.addrow(line.strip("\n")) for line in file.readlines() if len(line) > 1]

# Step 1: find vertices = tiles that have more than 2 neighbors
# a) Find start node
for idx, tile in enumerate(mygrid.grid[0]):
    if tile != "#":
        alist.adj[0, idx] = []
        startnode = (0, idx)
        break
# b) Find tiles with more than 2 neighbors
for rowidx in range(1, mygrid.height - 1):
    for colidx in range(1, mygrid.width - 1):
        if mygrid.grid[rowidx][colidx] != "#" and len(mygrid.findneighbors((rowidx, colidx))) > 2:
            alist.adj[rowidx, colidx] = []

# c) Find exit tile
for idx, tile in enumerate(mygrid.grid[mygrid.height - 1]):
    if tile != "#":
        alist.adj[mygrid.height - 1, idx] = []
        exitnode = (mygrid.height - 1, idx)
        break
aocpart = "B"
# Step 2: Find the edges and their "costs"
for vertex in list(alist.adj.keys()):
    vq: list[tuple[RowCol, int]] = [(vertex, 0)]
    visited = set()
    while len(vq) > 0:
        currentV = vq.pop(0)
        if currentV[0] not in visited:
            visited.add(currentV[0])
            for neighbor in mygrid.findneighbors(currentV[0]):
                if neighbor in alist.adj and neighbor != vertex:
                    alist.adj[vertex].append((neighbor, currentV[1] + 1))
                    continue
                neighborchar = mygrid.grid[neighbor[0]][neighbor[1]]
                drow, dcol = neighbor[0] - currentV[0][0], neighbor[1] - currentV[0][1]
                if neighborchar != OppositeChar[Directions.index((drow, dcol))] or aocpart != "A":
                    vq.append((neighbor, currentV[1] + 1))

# Step 3: Calculate the longest path with DFS
print("Part2:", aocpart, ": ", max(alist.dfs(startnode, exitnode)))
