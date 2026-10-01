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
        "graph": vz.graph(nodes, shown_edges, node_states=node_states, edge_states=edge_states),
        "table": vz.table(
            rows,
            row_heads=[str(v) for v in range(n)],
            col_heads=["neighbors"],
        ),
    }


if m == 0:
    rec.step(
        f"{n} vertices start with an empty neighbor list, and no edges are given: every vertex "
        "stays on its own.",
        **frame()
    )
else:
    rec.step(
        f"{n} vertices start with an empty neighbor list, and {m} edges are waiting to be read.",
        **frame()
    )

done_edges = []
for a, b in edges:
    adj[a].append(b)
    adj[b].append(a)
    rec.step(
        f"Reading the edge {a}-{b} appends {b} to vertex {a}'s list and {a} to vertex {b}'s "
        "list, since the graph is undirected.",
        **frame(current_edge=(a, b), done_edges=list(done_edges))
    )
    done_edges.append((a, b))

rec.step(
    "Every edge has been read. The table on the right is exactly what the program prints, one "
    "line per vertex.",
    **frame(done_edges=list(done_edges))
)

lines = [f"{v}: {adj[v]}" for v in range(n)]
rec.output("\n".join(lines) + "\n")
