import math

import vizrec as vz

rec = vz.Recorder()
n, m = map(int, rec.readline().split())
edges = []
for _ in range(m):
    a, b = map(int, rec.readline().split())
    edges.append((a, b))

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
    nodes = [(v, pos[v][0], pos[v][1]) for v in range(n)]
    node_states = {}
    for v in range(n):
        if current_edge and v in current_edge:
            node_states[v] = "current"
        elif adj[v]:
            node_states[v] = "done"
    edge_states = {}
    for e in done_edges:
        edge_states[e] = "done"
    shown_edges = list(done_edges)
    if current_edge:
        edge_states[current_edge] = "current"
        shown_edges = shown_edges + [current_edge]
    rows = [[str(adj[v])] for v in range(n)]
    return {
        "graph": vz.graph(
            nodes, shown_edges, node_states=node_states, edge_states=edge_states, directed=True
        ),
        "table": vz.table(
            rows,
            row_heads=[str(v) for v in range(n)],
            col_heads=["neighbors"],
        ),
    }


rec.step(
    f"{n} vertices and {m} directed edges: unlike the undirected version, each edge only "
    "points one way, from the first vertex named to the second.",
    **frame()
)

done_edges = []
for a, b in edges:
    adj[a].append(b)
    rec.step(
        f"Reading {a}-{b} as a directed edge appends {b} to vertex {a}'s list only. Vertex "
        f"{b} does not get {a} added back.",
        **frame(current_edge=(a, b), done_edges=list(done_edges))
    )
    done_edges.append((a, b))

rec.step(
    "A vertex with no outgoing arrow, such as the last one here, still has an empty list: it "
    "is a dead end in this direction, even though edges point into it.",
    **frame(done_edges=list(done_edges))
)

lines = [f"{v}: {adj[v]}" for v in range(n)]
rec.output("\n".join(lines) + "\n")
