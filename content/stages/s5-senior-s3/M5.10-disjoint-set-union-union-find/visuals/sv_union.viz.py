import vizrec as vz

rec = vz.Recorder()
n, m = map(int, rec.readline().split())

parent = list(range(n))
size = [1] * n


def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def depth_of(i):
    x, d = i, 0
    while parent[x] != x:
        x = parent[x]
        d += 1
    return d


def frame(compare=None, new_edge=None):
    nodes = [(i, i * (4.5 / max(n - 1, 1)), depth_of(i) * 0.6) for i in range(n)]
    edges = [(i, parent[i]) for i in range(n) if parent[i] != i]
    node_states = {r: "compare" for r in (compare or ())}
    edge_states = {new_edge: "frontier"} if new_edge else {}
    values = {i: size[i] for i in range(n) if parent[i] == i}
    return {
        "g": vz.graph(nodes, edges, node_states=node_states, edge_states=edge_states,
                      values=values, value_label="size"),
        "p": vz.array(parent),
    }


rec.step(
    f"{n} elements start as {n} one-node trees. Each is its own root, so `parent[i]` is `i` "
    "and every tree has size 1.",
    **frame()
)

out_lines = []
for _ in range(m):
    a, b = map(int, rec.readline().split())
    root_a, root_b = find(a), find(b)
    if root_a == root_b:
        rec.step(
            f"`union({a}, {b})`: {a} and {b} share root {root_a}. They are already one group, "
            "so nothing changes.",
            **frame(compare=(root_a,))
        )
        out_lines.append(f"After union({a}, {b}): {parent}")
        continue
    rec.step(
        f"`union({a}, {b})`: root {root_a} has size {size[root_a]}, root {root_b} has size "
        f"{size[root_b]}. The smaller tree will attach under the larger one.",
        **frame(compare=(root_a, root_b))
    )
    if size[root_a] < size[root_b]:
        parent[root_a] = root_b
        size[root_b] += size[root_a]
        winner, edge = root_b, (root_a, root_b)
    else:
        parent[root_b] = root_a
        size[root_a] += size[root_b]
        winner, edge = root_a, (root_b, root_a)
    rec.step(
        f"Root {winner} stays the root. Its size grows to {size[winner]}, and the other root "
        "becomes its child.",
        **frame(new_edge=edge)
    )
    out_lines.append(f"After union({a}, {b}): {parent}")

rec.output("\n".join(out_lines) + f"\nSizes: {size}\n")
