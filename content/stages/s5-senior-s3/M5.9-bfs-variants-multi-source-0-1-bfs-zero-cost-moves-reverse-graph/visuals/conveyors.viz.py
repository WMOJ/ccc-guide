from collections import deque

import vizrec as vz


def resolve_landing(conveyor, n):
    """The real node each node ends at after riding conveyors, or -1 if the ride never ends.

    Each node is added to a chain at most once, so this is O(n) total, not O(n) per node.
    """
    landing = list(range(n))
    state = [0] * n  # 0: unseen, 1: on the chain being built right now, 2: resolved
    for start in range(n):
        if state[start] != 0:
            continue
        chain = []
        u = start
        while conveyor[u] != -1 and state[u] == 0:
            state[u] = 1
            chain.append(u)
            u = conveyor[u]
        if conveyor[u] == -1:
            end = u
        elif state[u] == 1:
            end = -1
        else:
            end = landing[u]
        for node in chain:
            landing[node] = end
            state[node] = 2
    return landing


rec = vz.Recorder()
n, m, k = map(int, rec.readline().split())
edges = []
adj = [[] for _ in range(n)]
for _ in range(m):
    u, v = map(int, rec.readline().split())
    edges.append((str(u), str(v)))
    adj[u].append(v)
    adj[v].append(u)

conveyor = [-1] * n
conveyor_edges = []
for _ in range(k):
    a, b = map(int, rec.readline().split())
    conveyor[a] = b
    conveyor_edges.append((str(a), str(b)))

landing = resolve_landing(conveyor, n)

POS = {0: (0, 1), 1: (1.1, 0.3), 2: (2.2, 0), 3: (1.1, 1.7), 4: (2.2, 1.7), 5: (3.3, 0.6), 6: (4.4, 0.6)}
nodes = [(str(i), POS.get(i, (i, 0))[0], POS.get(i, (i, 0))[1]) for i in range(n)]
all_edges = edges + conveyor_edges

dist = [-1] * n
popped = set()
queue = deque()


def frame(current=None):
    node_states = {}
    for i in range(n):
        if i == current:
            node_states[str(i)] = "current"
        elif landing[i] == -1:
            node_states[str(i)] = "invalid"
        elif i in popped:
            node_states[str(i)] = "done"
        elif dist[i] != -1:
            node_states[str(i)] = "frontier"
    edge_states = {e: "wall" for e in conveyor_edges}
    values = {}
    for i in range(n):
        if dist[i] != -1:
            values[str(i)] = dist[i]
        elif landing[i] == -1:
            values[str(i)] = "×"
        else:
            values[str(i)] = "∞"
    items = [(str(node), "frontier") for node in queue]
    return {
        "g": vz.graph(nodes, all_edges, node_states=node_states, edge_states=edge_states,
                      values=values, value_label="distance"),
        "q": vz.queue(items),
    }


trapped = [str(i) for i in range(n) if landing[i] == -1]
if trapped:
    word = "Node" if len(trapped) == 1 else "Nodes"
    trap_text = (
        f"{word} {' and '.join(trapped)} ride conveyors that loop back on themselves, "
        "so they can never be a resting place."
    )
else:
    trap_text = "No conveyor here loops back on itself."
rec.step(
    "Every conveyor is followed first, marked as the highlighted edges. A node with an "
    "outgoing conveyor is never where the search actually stops. " + trap_text,
    **frame()
)

start = landing[0]
if start != -1:
    dist[start] = 0
    queue.append(start)
rec.step(
    f"Node 0's conveyor ride ends at node {start}, so the search starts there, at distance 0.",
    **frame()
)

while queue:
    u = queue.popleft()
    popped.add(u)
    rec.step(f"Node {u} leaves the front of the queue, at distance {dist[u]}.", **frame(current=u))
    added = []
    for v in adj[u]:
        lv = landing[v]
        if lv != -1 and dist[lv] == -1:
            dist[lv] = dist[u] + 1
            queue.append(lv)
            added.append(str(lv))
    if added:
        rec.step(
            f"From {u}, an edge reaches {', '.join(added)} (after riding any conveyor there). "
            f"Each joins the queue at distance {dist[u] + 1}.",
            **frame(current=u)
        )
    else:
        rec.step(
            f"Every edge from {u} leads to a node already reached or to a conveyor with no "
            "exit, so nothing new joins the queue.",
            **frame(current=u)
        )

swept = [str(i) for i in range(n) if landing[i] != i and landing[i] != -1]
tail = ""
if swept:
    word = "Node" if len(swept) == 1 else "Nodes"
    verb = "is" if len(swept) == 1 else "are"
    tail = (
        f" {word} {', '.join(swept)} {verb} swept onward by its own conveyor before the "
        "search can stand there, so its distance stays at ∞ too, for a different reason "
        "than the trapped nodes."
    )
rec.step(
    "The queue is empty. Every node that can be reached and rested on has its distance; "
    "the trapped nodes stay at ×." + tail,
    **frame()
)
rec.output(" ".join(str(x) for x in dist) + "\n")
