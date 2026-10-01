import vizrec as vz

rec = vz.Recorder()
n, m = map(int, rec.readline().split())
listed = []
for _ in range(m):
    u, v, w = map(int, rec.readline().split())
    listed.append((w, u, v))

POS = [(0.5, 2), (2.5, 3.6), (2, 2), (2.5, 0.4), (4.6, 2), (4.6, 0.4)]
nodes = [(i, POS[i][0], POS[i][1]) for i in range(n)]
graph_edges = [(u, v, w) for w, u, v in listed]


def build(order):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    tree = []
    total = 0
    for w, u, v in order:
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[rv] = ru
            tree.append((u, v))
            total += w
    return tree, total


def panel(tree):
    states = {e: "path" for e in tree}
    return vz.graph(nodes, graph_edges, edge_states=states)


tree_a, total_a = build(listed)
tree_b, total_b = build(sorted(listed))
edges_b = " ".join(f"{u}-{v}" for u, v in tree_b[:n - 1])

rec.step(
    f"Both trees use the same cycle check and connect all {n} cities. Taking the edges in the "
    f"order they were listed costs {total_a}. Taking them cheapest first costs {total_b}, the "
    "minimum: sorting is what makes the greedy choice optimal.",
    a=panel(tree_a),
    b=panel(tree_b),
)
rec.output(f"{total_b}\n{edges_b}\n")
