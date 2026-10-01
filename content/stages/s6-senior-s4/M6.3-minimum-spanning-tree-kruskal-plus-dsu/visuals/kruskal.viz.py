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


accepted = {}
skipped = {}


def frame(current=None):
    edge_states = {}
    for e in accepted:
        edge_states[e] = "path"
    for e in skipped:
        edge_states[e] = "invalid"
    node_states = {}
    if current is not None:
        node_states = {current[0]: "compare", current[1]: "compare"}
    roots = {i: find(i) for i in range(n)}
    return {
        "g": vz.graph(nodes, graph_edges, node_states=node_states, edge_states=edge_states,
                      values=roots, value_label="root"),
        "p": vz.array(parent, pointers=None),
    }


order = ", ".join(f"{u}-{v} ({w})" for w, u, v in edges)
rec.step(
    f"{n} cities start in {n} separate groups. Each edge is labeled with its cost. Kruskal's "
    f"algorithm looks at them cheapest first: {order}. `parent` lists each city's parent, and "
    "the number under a city is its group's root.",
    **frame()
)

total = 0
count = 0
for w, u, v in edges:
    ru, rv = find(u), find(v)
    if ru == rv:
        skipped[(u, v)] = w
        rec.step(
            f"Edge {u}-{v} costs {w}. `find({u})` and `find({v})` both return {ru}, so the "
            f"cities are already connected and this edge would close a cycle. Skip it.",
            **frame(current=(u, v))
        )
        continue
    before = list(parent)
    if size[ru] < size[rv]:
        parent[ru] = rv
        size[rv] += size[ru]
        attached, under = ru, rv
    else:
        parent[rv] = ru
        size[ru] += size[rv]
        attached, under = rv, ru
    total += w
    count += 1
    accepted[(u, v)] = w
    sum_text = f"total {total}" if count == 1 else f"total {total - w} + {w} = {total}"
    rec.step(
        f"Edge {u}-{v} costs {w}. `find({u})` is {ru} and `find({v})` is {rv}: different groups, "
        f"so accept it. Root {attached} goes under root {under}, `parent[{attached}]` is now "
        f"{under}; {sum_text}.",
        **frame(current=(u, v))
    )
    if count == n - 1:
        break

skipped_left = len(edges) - len(accepted) - len(skipped)
if count == n - 1:
    chosen = " ".join(f"{u}-{v}" for u, v in accepted)
    extra = (f" The other {skipped_left} edge{'s' if skipped_left != 1 else ''} are never "
             "looked at.") if skipped_left > 1 else (
        " The last remaining edge is never looked at." if skipped_left == 1 else "")
    rest = edges[len(accepted) + len(skipped):]
    if rest and rest[0][0] == w:
        extra += (f" Edge {rest[0][1]}-{rest[0][2]} costs {w}, the same as the last accepted edge, "
                  "so a different tie order would leave out another edge but give the same total.")
    rec.step(
        f"{count} edges connect {n} cities, so the tree is finished.{extra} Total cost {total}.",
        **frame()
    )
    rec.output(f"{total}\n{chosen}\n")
else:
    groups = len({find(i) for i in range(n)})
    rec.step(
        f"The edges ran out after {count} accepted, and the cities still form {groups} groups. "
        f"No tree of {n - 1} edges exists, so the answer is -1.",
        **frame()
    )
    rec.output("-1\n")
