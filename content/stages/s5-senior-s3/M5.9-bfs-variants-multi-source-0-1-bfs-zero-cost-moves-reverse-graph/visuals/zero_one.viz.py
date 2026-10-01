from collections import deque

import vizrec as vz

rec = vz.Recorder()
n, m, start = map(int, rec.readline().split())
edges = []
adj = [[] for _ in range(n)]
for _ in range(m):
    u, v, w = map(int, rec.readline().split())
    edges.append((str(u), str(v), w))
    adj[u].append((v, w))
    adj[v].append((u, w))

POS = {0: (0, 1), 1: (3, 0), 2: (1.5, 2), 3: (3, 2), 4: (4.5, 1)}
nodes = [(str(i), POS.get(i, (i, 0))[0], POS.get(i, (i, 0))[1]) for i in range(n)]

dist = [-1] * n
popped = set()
dq = deque()


def frame(current=None, edge=None, edge_state=None):
    node_states = {}
    for i in range(n):
        if i == current:
            node_states[str(i)] = "current"
        elif i in popped:
            node_states[str(i)] = "done"
        elif dist[i] != -1:
            node_states[str(i)] = "frontier"
    edge_states = {}
    if edge is not None:
        edge_states[edge] = edge_state
    values = {str(i): (dist[i] if dist[i] != -1 else "∞") for i in range(n)}
    items = [(str(node), "frontier") for node in dq]
    return {
        "g": vz.graph(nodes, edges, node_states=node_states, edge_states=edge_states,
                      values=values, value_label="distance"),
        "d": vz.struct("deque", items),
    }


dist[start] = 0
dq.append(start)
rec.step(
    f"Node {start} starts at distance 0 and goes into the deque. Every other node is at "
    "∞: no route to it is known yet.",
    **frame()
)

while dq:
    u = dq.popleft()
    popped.add(u)
    rec.step(
        f"Node {u} is at the front of the deque, at distance {dist[u]}.",
        **frame(current=u)
    )
    for v, w in adj[u]:
        nd = dist[u] + w
        edge = (str(u), str(v))
        if dist[v] == -1 or nd < dist[v]:
            before = "∞" if dist[v] == -1 else dist[v]
            dist[v] = nd
            if w == 0:
                dq.appendleft(v)
                where = "the front"
            else:
                dq.append(v)
                where = "the back"
            rec.step(
                f"Edge {u}-{v} has weight {w}. Through {u}, node {v} is {dist[u]} + {w} = "
                f"{nd} away, better than {before}. It goes into {where} of the deque.",
                **frame(current=u, edge=edge, edge_state="frontier")
            )
        else:
            rec.step(
                f"Edge {u}-{v} has weight {w}. Through {u}, node {v} would be {nd} away, "
                f"which does not beat {dist[v]}. Nothing changes.",
                **frame(current=u, edge=edge, edge_state="done")
            )

rec.step(
    "The deque is empty. Every reachable node holds its shortest distance from the start.",
    **frame()
)
rec.output(" ".join(str(x) for x in dist) + "\n")
