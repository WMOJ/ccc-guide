from collections import deque

import vizrec as vz

rec = vz.Recorder()
n, root = map(int, rec.readline().split())
adj = [[] for _ in range(n)]
for _ in range(n - 1):
    a, b = map(int, rec.readline().split())
    adj[a].append(b)
    adj[b].append(a)

parent = [None] * n
depth = [None] * n
found_at = [None] * n
order = []


def build(node, current):
    kids = [build(c, current) for c in range(n) if parent[c] == node and depth[c] is not None]
    if node == current:
        state = "current"
    elif node in queue_ids:
        state = "frontier"
    else:
        state = "done"
    return vz.node(node, str(node), children=kids, state=state,
                    note=f"d{depth[node]}" if depth[node] is not None else None)


def frame(current=None):
    return {
        "t": vz.tree(build(root, current)),
        "arr": vz.table(
            [
                [(-1 if i == root else parent[i]) for i in range(n)],
                [depth[i] for i in range(n)],
                [found_at[i] for i in range(n)],
            ],
            row_heads=["parent", "depth", "order"],
            col_heads=[f"r{i}" for i in range(n)],
        ),
    }


depth[root] = 0
found_at[root] = 0
order.append(root)
queue = deque([root])
queue_ids = set(queue)
rec.step(
    f"Rooting starts at room {root}: its depth is 0 and it is the only room in the queue.",
    **frame()
)
while queue:
    node = queue.popleft()
    queue_ids = set(queue)
    joined = []
    for neighbor in adj[node]:
        if depth[neighbor] is None:
            depth[neighbor] = depth[node] + 1
            parent[neighbor] = node
            found_at[neighbor] = len(order)
            order.append(neighbor)
            queue.append(neighbor)
            joined.append(neighbor)
    queue_ids = set(queue)
    if joined:
        names = ", ".join(f"Room {r}" for r in joined)
        what = f"{names} had no depth yet, so {'it becomes' if len(joined) == 1 else 'they become'} room {node}'s child{'ren' if len(joined) > 1 else ''} at depth {depth[node] + 1}."
    else:
        what = "Every neighbor of this room already has a depth, so nothing new joins the queue."
    rec.step(
        f"Room {node} leaves the queue and becomes current, at depth {depth[node]}. {what}",
        **frame(current=node)
    )

rec.step(
    "The queue is empty: every room has a parent and a depth. The order row is the sequence "
    "rooms were discovered in, the same order the next figure walks in reverse.",
    **frame()
)
parent_out = [(-1 if i == root else parent[i]) for i in range(n)]
rec.output(f"Parent: {parent_out}\nDepth: {depth}\nOrder: {order}\n")
