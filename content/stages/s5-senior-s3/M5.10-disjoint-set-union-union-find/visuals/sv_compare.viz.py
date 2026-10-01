import vizrec as vz

rec = vz.Recorder()
n, m = map(int, rec.readline().split())

naive = list(range(n))
by_size = list(range(n))
size = [1] * n


def find(parent, x):
    while parent[x] != x:
        x = parent[x]
    return x


def depth_of(parent, i):
    d = 0
    while parent[i] != i:
        i = parent[i]
        d += 1
    return d


def height(parent):
    return max(depth_of(parent, i) for i in range(n))


def forest(parent, with_sizes=False, new_edge=None):
    nodes = [(i, i * (4.5 / max(n - 1, 1)), depth_of(parent, i) * 0.6) for i in range(n)]
    edges = [(i, parent[i]) for i in range(n) if parent[i] != i]
    edge_states = {new_edge: "frontier"} if new_edge else {}
    if with_sizes:
        values = {i: size[i] for i in range(n) if parent[i] == i}
        return vz.graph(nodes, edges, edge_states=edge_states, values=values, value_label="size")
    return vz.graph(nodes, edges, edge_states=edge_states)


rec.step(
    f"{n} elements sit in two forests, each element its own tree of height 0. Both forests will "
    "receive the same unions. Plain `find` is used, without path halving, so the shape stays visible.",
    naive=forest(naive),
    sized=forest(by_size, with_sizes=True),
)

for _ in range(m):
    a, b = map(int, rec.readline().split())
    edge_naive = None
    edge_sized = None
    text_naive = "Naive: already one group, no change."
    text_sized = "By size: already one group, no change."
    root_a, root_b = find(naive, a), find(naive, b)
    if root_a != root_b:
        naive[root_a] = root_b
        edge_naive = (root_a, root_b)
        text_naive = f"Naive hangs root {root_a} under root {root_b}."
    root_a, root_b = find(by_size, a), find(by_size, b)
    if root_a != root_b:
        sizes = f"sizes {size[root_a]} and {size[root_b]}"
        if size[root_a] < size[root_b]:
            by_size[root_a] = root_b
            size[root_b] += size[root_a]
            edge_sized = (root_a, root_b)
            text_sized = f"By size hangs root {root_a} under {root_b} ({sizes})."
        else:
            by_size[root_b] = root_a
            size[root_a] += size[root_b]
            edge_sized = (root_b, root_a)
            text_sized = f"By size hangs root {root_b} under {root_a} ({sizes})."
    rec.step(
        f"`union({a}, {b})`. {text_naive} {text_sized} Heights now: naive {height(naive)}, "
        f"by size {height(by_size)}.",
        naive=forest(naive, new_edge=edge_naive),
        sized=forest(by_size, with_sizes=True, new_edge=edge_sized),
    )

h_naive = height(naive)
h_sized = height(by_size)
if h_naive > h_sized:
    ending = (
        f"After {m} unions the naive forest has height {h_naive}, a chain, and the by-size forest "
        f"has height {h_sized}. Union by size never hangs a bigger tree under a smaller one, so "
        "the order of unions cannot build a chain."
    )
else:
    ending = (
        f"After {m} unions both forests have height {h_naive}. This order suits the naive rule, "
        "but its height depends on the order the unions arrive in. Union by size keeps the height "
        "low in every order."
    )
rec.step(
    ending,
    naive=forest(naive),
    sized=forest(by_size, with_sizes=True),
)

rec.output(f"Naive: {naive} height {h_naive}\nBy size: {by_size} height {h_sized}\n")
