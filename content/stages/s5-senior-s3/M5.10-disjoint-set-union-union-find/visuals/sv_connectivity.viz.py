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


def union(a, b):
    root_a, root_b = find(a), find(b)
    if root_a == root_b:
        return
    if size[root_a] < size[root_b]:
        parent[root_a] = root_b
        size[root_b] += size[root_a]
    else:
        parent[root_b] = root_a
        size[root_a] += size[root_b]


def depth_of(i):
    x, d, seen = i, 0, set()
    while parent[x] != x and x not in seen:
        seen.add(x)
        x = parent[x]
        d += 1
    return d


def frame(edge=None, compare=None):
    nodes = [(i, i * (4.5 / max(n - 1, 1)), depth_of(i) * 0.6) for i in range(n)]
    edges = [(i, parent[i]) for i in range(n) if parent[i] != i]
    node_states = {c: "compare" for c in (compare or ())}
    edge_states = {edge: "frontier"} if edge else {}
    return {
        "g": vz.graph(nodes, edges, node_states=node_states, edge_states=edge_states),
        "p": vz.array(parent),
    }


rec.step(f"{n} computers start with no cables between them: each is its own component.", **frame())

for _ in range(m):
    u, v = map(int, rec.readline().split())
    union(u, v)
    rec.step(f"Cable {u}-{v} is processed: `union({u}, {v})` merges their components.", **frame(edge=(u, v)))

q = int(rec.readline())
out_lines = []
for _ in range(q):
    a, b = map(int, rec.readline().split())
    root_a, root_b = find(a), find(b)
    same = root_a == root_b
    if same:
        caption = f"Query {a}, {b}: `find({a})` and `find({b})` both return {root_a}. Answer: yes."
    else:
        caption = f"Query {a}, {b}: `find({a})` returns {root_a}, `find({b})` returns {root_b}. Answer: no."
    rec.step(caption, **frame(compare=(a, b)))
    out_lines.append("yes" if same else "no")

rec.output("\n".join(out_lines) + "\n")
