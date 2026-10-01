from collections import deque

import vizrec as vz

rec = vz.Recorder()
n, m, target = map(int, rec.readline().split())
edges = []
rev_adj = [[] for _ in range(n)]
for _ in range(m):
    u, v = map(int, rec.readline().split())
    edges.append((str(u), str(v)))
    rev_adj[v].append(u)

POS = {0: (0, 0.5), 1: (1.5, 0), 2: (3, 0.5), 3: (4.5, 0.5), 4: (1.5, 1.5), 5: (0, 1.5), 6: (3, 1.7)}
nodes = [(str(i), POS.get(i, (i, 0))[0], POS.get(i, (i, 0))[1]) for i in range(n)]

dist = [-1] * n
popped = set()
queue = deque()


def frame(current=None):
    node_states = {}
    for i in range(n):
        if i == current:
            node_states[str(i)] = "current"
        elif i in popped:
            node_states[str(i)] = "done"
        elif dist[i] != -1:
            node_states[str(i)] = "frontier"
    values = {str(i): (dist[i] if dist[i] != -1 else "∞") for i in range(n)}
    items = [(str(node), "frontier") for node in queue]
    return {
        "g": vz.graph(nodes, edges, node_states=node_states, values=values,
                      value_label="to target", directed=True),
        "q": vz.queue(items),
    }


def moves(count):
    return "move" if count == 1 else "moves"


dist[target] = 0
queue.append(target)
rec.step(
    f"BFS runs on the reversed edges, starting at the target, node {target}. Distance 0 "
    "means the target is 0 moves from itself.",
    **frame()
)

while queue:
    u = queue.popleft()
    popped.add(u)
    rec.step(
        f"Node {u} leaves the front of the queue, {dist[u]} {moves(dist[u])} from the target.",
        **frame(current=u)
    )
    added = []
    for v in rev_adj[u]:
        if dist[v] == -1:
            dist[v] = dist[u] + 1
            queue.append(v)
            added.append(str(v))
    if added:
        nd = dist[u] + 1
        rec.step(
            f"A one-way edge in the original graph runs from each of {', '.join(added)} to "
            f"{u}, so reversed, it runs from {u} to them. Each joins the queue "
            f"{nd} {moves(nd)} from the target.",
            **frame(current=u)
        )
    else:
        rec.step(
            f"No one-way edge in the original graph points to {u} from a node not "
            "already reached, so nothing new joins the queue.",
            **frame(current=u)
        )

unreached = [str(i) for i in range(n) if dist[i] == -1]
if unreached:
    word = "Node" if len(unreached) == 1 else "Nodes"
    verb = "has" if len(unreached) == 1 else "have"
    pron = "it stays" if len(unreached) == 1 else "they stay"
    tail = f" {word} {', '.join(unreached)} {verb} no route to the target, so {pron} at ∞."
else:
    tail = ""
rec.step(
    "The queue is empty. Every node with a one-way route to the target now holds its "
    "distance." + tail,
    **frame()
)
rec.output(" ".join(str(x) for x in dist) + "\n")
