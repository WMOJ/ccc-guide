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


tree = []
weight = {}


def tree_path(a, b):
    adj = {i: [] for i in range(n)}
    for u, v in tree:
        adj[u].append(v)
        adj[v].append(u)
    prev = {a: None}
    todo = [a]
    for x in todo:
        for y in adj[x]:
            if y not in prev:
                prev[y] = x
                todo.append(y)
    path = [b]
    while prev[path[-1]] is not None:
        path.append(prev[path[-1]])
    return path[::-1]


def frame(skipped=None, path=()):
    states = {e: "done" for e in tree}
    for i in range(len(path) - 1):
        states[(path[i], path[i + 1])] = "path"
    if skipped:
        states[skipped] = "invalid"
    node_states = {i: "compare" for i in skipped} if skipped else {}
    return {"g": vz.graph(nodes, graph_edges, node_states=node_states, edge_states=states)}


rec.step(
    "Kruskal's algorithm builds the tree edge by edge. Each step below stops at an edge it "
    "skips, with the tree built so far marked. A skipped edge's ends are already joined by "
    "accepted edges, so it would close a cycle.",
    **frame()
)
chosen = []
for w, u, v in edges:
    ru, rv = find(u), find(v)
    if ru == rv:
        path = tree_path(u, v)
        steps = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        costs = [weight.get((a, b), weight.get((b, a))) for a, b in steps]
        text = ", ".join(f"{a}-{b} ({c})" for (a, b), c in zip(steps, costs))
        rec.step(
            f"Edge {u}-{v} costs {w}, but the tree already joins {u} to {v} through {text}. Every "
            f"one of those edges costs at most {w}, so {u}-{v} would only add a dearer way round "
            "a loop. Skip it.",
            **frame(skipped=(u, v), path=path)
        )
        continue
    if size[ru] < size[rv]:
        parent[ru] = rv
        size[rv] += size[ru]
    else:
        parent[rv] = ru
        size[ru] += size[rv]
    tree.append((u, v))
    weight[(u, v)] = w
    chosen.append((w, u, v))
    if len(chosen) == n - 1:
        break

total = sum(c[0] for c in chosen)
if len(chosen) == n - 1:
    rec.step(
        f"The finished tree costs {total}. Each skipped edge lost to a path of cheaper or equal "
        "edges, so nothing cheaper was thrown away.",
        **frame()
    )
    rec.output(f"{total}\n{' '.join(f'{u}-{v}' for _, u, v in chosen)}\n")
else:
    rec.step(
        f"The forest has {len(chosen)} edges and cannot be completed: some cities are cut off, so "
        "there is no spanning tree and the answer is -1.",
        **frame()
    )
    rec.output("-1\n")
