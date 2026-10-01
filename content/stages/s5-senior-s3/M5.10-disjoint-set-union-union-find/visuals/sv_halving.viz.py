import vizrec as vz

rec = vz.Recorder()
n, m = map(int, rec.readline().split())

parent = list(range(n))


def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]  # Skip one level
        x = parent[x]
    return x


def union(a, b):
    root_a = find(a)
    root_b = find(b)
    if root_a != root_b:
        parent[root_a] = root_b


def depth_of(i):
    x, d, seen = i, 0, set()
    while parent[x] != x and x not in seen:
        seen.add(x)
        x = parent[x]
        d += 1
    return d


def frame(current=None):
    nodes = [(i, i * (4.5 / max(n - 1, 1)), depth_of(i) * 0.6) for i in range(n)]
    edges = [(i, parent[i]) for i in range(n) if parent[i] != i]
    node_states = {current: "current"} if current is not None else {}
    pointers = [("x", current)] if current is not None else None
    return {
        "g": vz.graph(nodes, edges, node_states=node_states),
        "p": vz.array(parent, pointers=pointers),
    }


for _ in range(m):
    a, b = map(int, rec.readline().split())
    union(a, b)

parent_after_unions = list(parent)
rec.step(f"Naive unions build this forest. `parent` is {parent_after_unions}.", **frame())

x0 = int(rec.readline())
rec.step(
    f"`find({x0})` starts at {x0} and climbs toward the root, halving the path along the way.",
    **frame(current=x0)
)

x = x0
while parent[x] != x:
    before = parent[x]
    parent[x] = parent[parent[x]]
    after = parent[x]
    if after != before:
        caption = (
            f"`{x}` pointed to `{before}`, and `{before}` pointed on to `{after}`. Path halving "
            f"skips the middle link: `parent[{x}]` now points straight to `{after}`."
        )
    else:
        caption = f"`{x}` already points directly at `{after}`, one hop from where it started."
    rec.step(caption, **frame(current=x))
    x = after

result = x
rec.step(f"`parent[{x}]` is `{x}`: {x} is the root. `find({x0})` returns {result}.", **frame(current=x))
if parent == parent_after_unions:
    rec.step(
        f"The path from {x0} was already one hop long, so halving had nothing to skip. "
        f"`parent` is unchanged: {parent}.",
        **frame()
    )
else:
    rec.step(f"The path from {x0} is now much shorter. `parent` is {parent}.", **frame())

rec.output(
    f"Parent array after naive unions: {parent_after_unions}\n"
    f"find({x0}) with path halving: {result}\n"
    f"Parent array after find: {parent}\n"
)
