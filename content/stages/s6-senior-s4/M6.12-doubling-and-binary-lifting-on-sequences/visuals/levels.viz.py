import math

import vizrec as vz

rec = vz.Recorder()
n, q = map(int, rec.readline().split())
nxt = list(map(int, rec.readline().split()))
start, kmax = map(int, rec.readline().split())

LOG = max(1, kmax.bit_length())
up = [nxt]
for k in range(1, LOG):
    prev = up[k - 1]
    up.append([prev[prev[v]] for v in range(n)])


def place(v):
    angle = -math.pi / 2 + 2 * math.pi * v / n
    return (round(2.2 + 2 * math.cos(angle), 2), round(2.2 + 2 * math.sin(angle), 2))


nodes = [(v, place(v)[0], place(v)[1]) for v in range(n)]


def frame(k):
    edges = []
    stay = {}
    for v in range(n):
        if up[k][v] == v:
            stay[v] = "stays"
        else:
            edges.append((v, up[k][v]))
    states = {v: "done" for v in stay}
    return vz.graph(nodes, edges, node_states=states, edge_states={e: "current" for e in edges},
                    values=stay, directed=True, value_label="self-jump")


def stays_text(k):
    count = sum(1 for v in range(n) if up[k][v] == v)
    if count == 0:
        return ""
    if count == n:
        return f" Every station lands back on itself, so the arrows collapse into the marks below the stations."
    if count == 1:
        return " One station lands on itself and shows a mark instead of an arrow."
    return f" {count} stations land on themselves and show a mark instead of an arrow."


rec.step(
    f"Level 0, up[0]: each arrow is one station's own teleporter, a jump of 1. From station {start} "
    f"it leads to station {up[0][start]}.",
    graph=frame(0),
)
for k in range(1, LOG):
    size = 1 << k
    half = 1 << (k - 1)
    mid = up[k - 1][start]
    rec.step(
        f"Level {k}, up[{k}]: each arrow is a jump of {size}. From station {start}, "
        + (f"1 jump reaches station {mid} and 1 more reaches" if half == 1
           else f"{half} jumps reach station {mid} and {half} more reach")
        + f" station {up[k][start]}, so up[{k}][{start}] = {up[k][start]}."
        + stays_text(k),
        graph=frame(k),
    )
rec.step(
    f"Levels 0 to {LOG - 1} give every station one pointer per level, for jump sizes "
    + ", ".join(str(1 << k) for k in range(LOG))
    + f". Any K up to {(1 << LOG) - 1} is a sum of these sizes.",
    graph=frame(LOG - 1),
)
rec.output("".join(f"up[{k}] = {up[k]}\n" for k in range(LOG)))
