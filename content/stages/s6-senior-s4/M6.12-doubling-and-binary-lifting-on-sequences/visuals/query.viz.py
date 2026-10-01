import math

import vizrec as vz

rec = vz.Recorder()
n, q = map(int, rec.readline().split())
nxt = list(map(int, rec.readline().split()))
start, K = map(int, rec.readline().split())

LOG = max(1, K.bit_length())
up = [nxt]
for k in range(1, LOG):
    prev = up[k - 1]
    up.append([prev[prev[v]] for v in range(n)])


def place(v):
    angle = -math.pi / 2 + 2 * math.pi * v / n
    return (round(2.2 + 2 * math.cos(angle), 2), round(2.2 + 2 * math.sin(angle), 2))


nodes = [(v, place(v)[0], place(v)[1]) for v in range(n)]
base = [(v, nxt[v]) for v in range(n)]
bits = [(K >> k) & 1 for k in range(LOG)]
binary = format(K, "b")

hops = []
visited = [start]
here_col = ["-"] * LOG
state_col = [("queued" if bits[k] else "none") for k in range(LOG)]


def frame(here, cur_k=None, latest=None):
    edges = list(base)
    estates = {}
    weights = {}
    for a, b, size in hops:
        if (a, b) not in edges:
            edges.append((a, b))
        estates[(a, b)] = "path"
        weights[(a, b)] = f"+{size}"
    if latest is not None:
        estates[(latest[0], latest[1])] = "current"
    gedges = [(a, b, weights[(a, b)]) if (a, b) in weights else (a, b) for a, b in edges]
    nstates = {v: "done" for v in visited}
    nstates[here] = "current"
    graph = vz.graph(nodes, gedges, node_states=nstates, edge_states=estates, directed=True)
    cells = [[1 << k, bits[k], here_col[k]] for k in range(LOG)]
    tstates = []
    for k in range(LOG):
        if k == cur_k:
            tstates.append("ccc")
        elif here_col[k] != "-":
            tstates.append("ddd")
        elif bits[k]:
            tstates.append("qqq")
        else:
            tstates.append("___")
    table = vz.table(cells, states=tstates, row_heads=list(range(LOG)), col_heads=["jump", "bit", "here"],
                     row_title="k")
    return {"graph": graph, "table": table}


here = start
set_bits = [k for k in range(LOG) if bits[k]]
rec.step(
    f"K = {K} is {binary} in binary, so "
    + (f"bit{'s' if len(set_bits) > 1 else ''} " + ", ".join(str(k) for k in set_bits) + " "
       + ("are" if len(set_bits) > 1 else "is") + " set. " if set_bits else "no bit is set. ")
    + f"The rider starts at station {start}.",
    **frame(here),
)
for k in range(LOG):
    if bits[k]:
        there = up[k][here]
        hops.append((here, there, 1 << k))
        visited.append(there)
        here_col[k] = there
        rec.step(
            f"Bit {k} is set: use up[{k}][{here}] = {there}, a hop of {1 << k} "
            f"{'jump' if k == 0 else 'jumps'}. The rider moves from station {here} to station {there}.",
            **frame(there, k, (here, there)),
        )
        here = there
    else:
        here_col[k] = here
        rec.step(
            f"Bit {k} is clear, so there is no hop of {1 << k}. The rider stays at station {here}.",
            **frame(here, k),
        )
if K == 0:
    final = f"Every bit is used: the rider is still at station {here}, with no lookups at all."
else:
    final = (f"Every bit is used: the rider is at station {here} after {K} jumps, with "
             f"{len(set_bits)} table {'lookup' if len(set_bits) == 1 else 'lookups'} instead of {K} hops.")
rec.step(final, **frame(here))
rec.output(f"{here}\n")
