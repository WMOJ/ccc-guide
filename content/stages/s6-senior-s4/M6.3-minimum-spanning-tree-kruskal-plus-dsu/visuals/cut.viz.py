import vizrec as vz

rec = vz.Recorder()
n, m = map(int, rec.readline().split())
raw = []
for _ in range(m):
    u, v, w = map(int, rec.readline().split())
    raw.append((w, u, v))
edges = sorted(raw)

POS = [(0.5, 2), (2.5, 3.6), (2, 2), (2.5, 0.4), (4.6, 2), (4.6, 0.4)]
nodes = [(i, POS[i][0], POS[i][1]) for i in range(n)]
graph_edges = [(u, v, w) for w, u, v in raw]

parent = list(range(n))
size = [1] * n


def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


done = []


def frame(side=(), crossing=(), best=None):
    edge_states = {(u, v): "done" for u, v in done}
    for w, u, v in crossing:
        edge_states[(u, v)] = "frontier"
    if best is not None:
        edge_states[(best[1], best[2])] = "path"
    node_states = {i: "compare" for i in side}
    return {"g": vz.graph(nodes, graph_edges, node_states=node_states, edge_states=edge_states)}


rec.step(
    f"The same {n} cities and {m} costed edges as before. A cut splits the cities into two sides; "
    "an edge crosses the cut when its ends are on different sides. Kruskal's algorithm accepts "
    "an edge only when it is the cheapest edge across some cut.",
    **frame()
)

total = 0
chosen = []
for w, u, v in edges:
    ru, rv = find(u), find(v)
    if ru == rv:
        continue
    side = [i for i in range(n) if find(i) == ru]
    inside = set(side)
    crossing = [e for e in edges if (e[1] in inside) != (e[2] in inside)]
    best = min(crossing)
    label = "{" + ", ".join(str(i) for i in side) + "}"
    lines = ", ".join(f"{a}-{b} ({c})" for c, a, b in crossing)
    rec.step(
        f"Cut: the group {label} on one side, every other city on the other. The edges across it "
        f"are {lines}. The cheapest, {best[1]}-{best[2]} at {best[0]}, is the edge Kruskal accepts, "
        "so it is safe.",
        **frame(side=side, crossing=crossing, best=best)
    )
    if size[ru] < size[rv]:
        parent[ru] = rv
        size[rv] += size[ru]
    else:
        parent[rv] = ru
        size[ru] += size[rv]
    total += w
    chosen.append(f"{u}-{v}")
    done.append((u, v))
    if len(chosen) == n - 1:
        break

if len(chosen) == n - 1:
    rec.step(
        f"Every accepted edge was the cheapest across some cut, so together they form a minimum "
        f"spanning tree of cost {total}.",
        **frame()
    )
    rec.output(f"{total}\n{' '.join(chosen)}\n")
else:
    rec.step(
        f"The {len(chosen)} accepted edges were each the cheapest across a cut, but they do not "
        "reach every city: no spanning tree exists, so the answer is -1.",
        **frame()
    )
    rec.output("-1\n")
