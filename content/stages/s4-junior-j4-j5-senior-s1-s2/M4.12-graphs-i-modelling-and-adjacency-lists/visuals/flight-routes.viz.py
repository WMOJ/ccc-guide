import math

import vizrec as vz

rec = vz.Recorder()
n, m = map(int, rec.readline().split())
codes = rec.readline().split()
index = {code: i for i, code in enumerate(codes)}
edges = []
for _ in range(m):
    origin, dest = rec.readline().split()
    edges.append((index[origin], index[dest]))

adj = [[] for _ in range(n)]


def positions(count):
    cx, cy, r = 2.5, 2.5, 2.3
    if count == 1:
        return {0: (cx, cy)}
    pts = {}
    for i in range(count):
        angle = -math.pi / 2 + 2 * math.pi * i / count
        pts[i] = (round(cx + r * math.cos(angle), 2), round(cy + r * math.sin(angle), 2))
    return pts


pos = positions(n)


def frame(current_edge=None, done_edges=None):
    done_edges = done_edges or []
    nodes = [(codes[v], pos[v][0], pos[v][1]) for v in range(n)]
    node_states = {}
    for v in range(n):
        if current_edge and v in current_edge:
            node_states[codes[v]] = "current"
        elif adj[v]:
            node_states[codes[v]] = "done"
    edge_states = {}
    for a, b in done_edges:
        edge_states[(codes[a], codes[b])] = "done"
    shown_edges = [(codes[a], codes[b]) for a, b in done_edges]
    if current_edge:
        a, b = current_edge
        edge_states[(codes[a], codes[b])] = "current"
        shown_edges = shown_edges + [(codes[a], codes[b])]
    rows = [[str([codes[j] for j in adj[v]])] for v in range(n)]
    return {
        "graph": vz.graph(
            nodes, shown_edges, node_states=node_states, edge_states=edge_states, directed=True
        ),
        "table": vz.table(
            rows,
            row_heads=[codes[v] for v in range(n)],
            col_heads=["routes to"],
        ),
    }


rec.step(
    f"The {n} airports are read as text codes, not numbers, so each one is mapped to an index "
    "first. A dict from code to index is the vertex numbering.",
    **frame()
)

done_edges = []
for a, b in edges:
    adj[a].append(b)
    rec.step(
        f"The flight {codes[a]} to {codes[b]} adds {codes[b]} to {codes[a]}'s route list. A "
        f"flight only goes one way, so {codes[b]}'s list is untouched.",
        **frame(current_edge=(a, b), done_edges=list(done_edges))
    )
    done_edges.append((a, b))

rec.step(
    "Every route is read. An airport that is only ever a destination, never an origin, keeps "
    "an empty route list.",
    **frame(done_edges=list(done_edges))
)

lines = [f"{codes[v]}: {[codes[j] for j in adj[v]]}" for v in range(n)]
rec.output("\n".join(lines) + "\n")
