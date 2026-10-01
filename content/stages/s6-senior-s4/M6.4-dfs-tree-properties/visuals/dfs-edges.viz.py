import vizrec as vz

rec = vz.Recorder()
n, m = map(int, rec.readline().split())
edges = []
adj = [[] for _ in range(n)]
for _ in range(m):
    u, v = map(int, rec.readline().split())
    edges.append((u, v))
    adj[u].append(v)
POS = {0: (0, 1), 1: (2, 0), 2: (4, 0), 3: (4, 2), 4: (1, 3)}
nodes = [(r, POS[r][0], POS[r][1]) for r in range(n)]

disc = [-1] * n
fin = [-1] * n
kind_of = {}
KIND_STATE = {"tree": "path", "back": "invalid", "forward": "compare", "cross": "frontier"}
clock = 0
out_edges = []


def frame(current_edge=None, stack=()):
    node_states = {}
    for v in range(n):
        if fin[v] != -1:
            node_states[v] = "done"
        elif disc[v] != -1:
            node_states[v] = "current"
    edge_states = {e: KIND_STATE[k] for e, k in kind_of.items()}
    cells = [[disc[v] if disc[v] != -1 else "–", fin[v] if fin[v] != -1 else "–"] for v in range(n)]
    states = []
    for v in range(n):
        states.append([
            "done" if disc[v] != -1 else None,
            "done" if fin[v] != -1 else None,
        ])
    return {
        "g": vz.graph(nodes, edges, node_states=node_states, edge_states=edge_states, directed=True),
        "t": vz.table(cells, states=states, row_heads=list(range(n)), col_heads=["disc", "fin"],
                      row_title="node"),
    }


def stack_text(st):
    return ", ".join(str(f[0]) for f in st) if st else "empty"


rec.step(
    f"A directed graph with {n} nodes and {m} edges. Nothing is discovered yet, so every time in the "
    "table is a dash. The clock starts at 0 and ticks once at every discovery and every finish.",
    **frame()
)
roots = 0
for root in range(n):
    if disc[root] != -1:
        continue
    roots += 1
    disc[root] = clock
    clock += 1
    st = [[root, 0]]
    rec.step(
        f"Node {root} has no discovery time and no earlier tree reached it, so it starts a new tree. "
        f"It is discovered at time {disc[root]}. Stack: {stack_text(st)}.",
        **frame()
    )
    while st:
        fr = st[-1]
        node = fr[0]
        idx = fr[1]
        if idx == len(adj[node]):
            st.pop()
            fin[node] = clock
            clock += 1
            rec.step(
                f"Node {node} has tried all its edges, so it finishes at time {fin[node]} and leaves "
                f"the stack. Stack: {stack_text(st)}.",
                **frame()
            )
            continue
        fr[1] = idx + 1
        nb = adj[node][idx]
        if disc[nb] == -1:
            kind = "tree"
            disc[nb] = clock
            clock += 1
            st.append([nb, 0])
            text = (f"Edge {node} to {nb}: node {nb} has no discovery time, so this is a tree edge. "
                    f"Node {nb} is discovered at time {disc[nb]}. Stack: {stack_text(st)}.")
        elif fin[nb] == -1:
            kind = "back"
            text = (f"Edge {node} to {nb}: node {nb} is discovered but not finished, so it is on the "
                    f"stack, an ancestor of node {node}. This is a back edge.")
        elif disc[node] < disc[nb]:
            kind = "forward"
            text = (f"Edge {node} to {nb}: node {nb} is finished and was discovered after node {node}, "
                    f"so it is a descendant reached another way. This is a forward edge.")
        else:
            kind = "cross"
            text = (f"Edge {node} to {nb}: node {nb} is finished and was discovered before node "
                    f"{node}, in a branch that closed earlier. This is a cross edge.")
        kind_of[(node, nb)] = kind
        out_edges.append(f"{node} {nb} {kind}")
        rec.step(text, **frame())

rec.step(
    f"Every node has both times, and every edge has a kind. The search started {roots} "
    f"tree{'' if roots == 1 else 's'}; the clock ended at {clock}, two ticks per node.",
    **frame()
)
lines = out_edges + [f"{v} {disc[v]} {fin[v]}" for v in range(n)]
rec.output("\n".join(lines) + "\n")
