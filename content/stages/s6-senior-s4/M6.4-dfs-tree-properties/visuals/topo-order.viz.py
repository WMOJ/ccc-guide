import vizrec as vz

rec = vz.Recorder()
n, m = map(int, rec.readline().split())
edges = []
adj = [[] for _ in range(n)]
for _ in range(m):
    u, v = map(int, rec.readline().split())
    edges.append((u, v))
    adj[u].append(v)
POS = {0: (0, 1), 1: (1.3, 0), 2: (1.3, 2), 3: (2.6, 1), 4: (4, 1), 5: (2.6, 3)}
nodes = [(r, POS[r][0], POS[r][1]) for r in range(n)]

disc = [-1] * n
fin = [-1] * n
order = []
back_edges = []
seen_edges = {}


def frame(final=None):
    node_states = {}
    for v in range(n):
        if fin[v] != -1:
            node_states[v] = "done"
        elif disc[v] != -1:
            node_states[v] = "current"
    edge_states = dict(seen_edges)
    shown = final if final is not None else order
    values = list(shown) + ["·"] * (n - len(shown))
    states = ["done"] * len(shown) + [None] * (n - len(shown))
    return {
        "g": vz.graph(nodes, edges, node_states=node_states, edge_states=edge_states, directed=True),
        "a": vz.array(values, states=states, indices=False),
    }


def stack_text(st):
    return ", ".join(str(f[0]) for f in st) if st else "empty"


rec.step(
    f"A directed graph of {n} tasks, where an edge from a to b means a must come before b. The row "
    "will collect tasks in the order they finish.",
    **frame()
)
clock = 0
for root in range(n):
    if disc[root] != -1:
        continue
    disc[root] = clock
    clock += 1
    st = [[root, 0]]
    rec.step(f"Node {root} has not been reached, so the search starts there. Stack: {stack_text(st)}.",
             **frame())
    while st:
        fr = st[-1]
        node = fr[0]
        idx = fr[1]
        if idx == len(adj[node]):
            st.pop()
            fin[node] = clock
            clock += 1
            order.append(node)
            rec.step(
                f"Node {node} has tried every edge, so it finishes and joins the row: every task "
                f"that must come after it is already in the row. Stack: {stack_text(st)}.",
                **frame()
            )
            continue
        fr[1] = idx + 1
        nb = adj[node][idx]
        if disc[nb] == -1:
            disc[nb] = clock
            clock += 1
            st.append([nb, 0])
            seen_edges[(node, nb)] = "path"
            rec.step(f"Edge {node} to {nb} leads to a new node, so the search goes down it. "
                     f"Stack: {stack_text(st)}.", **frame())
        elif fin[nb] == -1:
            seen_edges[(node, nb)] = "invalid"
            rec.step(
                f"Edge {node} to {nb} leads to node {nb}, which is still on the stack: a back edge. "
                f"Node {nb} must come before node {node} through the tree path, and node {node} "
                f"before node {nb} through this edge, so no order exists.",
                **frame()
            )
            rec.step(
                "A back edge means a cycle, so there is no valid order. The program prints `cycle` "
                "and stops looking.",
                **frame()
            )
            rec.output("cycle\n")
            raise SystemExit
        else:
            seen_edges[(node, nb)] = "done"
            rec.step(f"Edge {node} to {nb} leads to node {nb}, which is already finished and already "
                     f"in the row. Nothing to do.", **frame())

final = list(reversed(order))
rec.step(
    "The search is over and no back edge appeared. The row is now reversed, so the last task to "
    "finish comes first. Read left to right, every task comes before the tasks that depend on it.",
    **frame(final=final)
)
rec.output(" ".join(str(v) for v in final) + "\n")
