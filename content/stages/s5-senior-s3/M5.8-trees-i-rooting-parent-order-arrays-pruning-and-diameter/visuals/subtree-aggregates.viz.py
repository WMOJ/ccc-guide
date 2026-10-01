from collections import deque

import vizrec as vz

rec = vz.Recorder()
n, root = map(int, rec.readline().split())
adj = [[] for _ in range(n)]
for _ in range(n - 1):
    a, b = map(int, rec.readline().split())
    adj[a].append(b)
    adj[b].append(a)
items = list(map(int, rec.readline().split()))

parent = [None] * n
depth = [None] * n
order = []
depth[root] = 0
queue = deque([root])
while queue:
    node = queue.popleft()
    order.append(node)
    for neighbor in adj[node]:
        if depth[neighbor] is None:
            depth[neighbor] = depth[node] + 1
            parent[neighbor] = node
            queue.append(neighbor)

size = [1] * n
total = list(items)
folded = [False] * n


def build(node, current):
    kids = [build(c, current) for c in range(n) if parent[c] == node]
    if node == current:
        state = "current"
    elif folded[node]:
        state = "done"
    else:
        state = None
    return vz.node(node, str(node), children=kids, state=state, edge=state,
                    note=f"{size[node]}, {total[node]}")


def frame(current=None):
    return {
        "t": vz.tree(build(root, current)),
        "arr": vz.table(
            [size, total],
            row_heads=["size", "total"],
            col_heads=[f"r{i}" for i in range(n)],
        ),
    }


rec.step(
    "Every room starts with size 1 (itself) and its own item total. The order from rooting, "
    f"{order}, is walked back to front, so a room's children are folded in before the room "
    "itself is.",
    **frame()
)
for node in reversed(order):
    above = parent[node]
    if above is None:
        rec.step(
            f"Room {root} is last: it has no parent to fold into. Its size, {size[root]}, "
            f"covers the whole floor, and its item total, {total[root]}, sums every room.",
            **frame(current=root)
        )
        break
    before_size = size[above]
    before_total = total[above]
    size[above] += size[node]
    total[above] += total[node]
    folded[node] = True
    rec.step(
        f"Room {node} (size {size[node]}, item total {total[node]}) folds into its parent, "
        f"room {above}: the parent's size grows from {before_size} to {size[above]}, and its "
        f"item total from {before_total} to {total[above]}.",
        **frame(current=node)
    )

rec.output(f"Room count: {size}\nItem total: {total}\n")
