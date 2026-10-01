import vizrec as vz

rec = vz.Recorder()
n, q = map(int, rec.readline().split())
nxt = list(map(int, rec.readline().split()))
start, kmax = map(int, rec.readline().split())

LOG = max(1, kmax.bit_length())
up = [nxt]
for k in range(1, LOG):
    prev = up[k - 1]
    up.append([prev[prev[v]] for v in range(n)])

heads = [f"up[{k}]" for k in range(LOG)]
filled = [[False] * LOG for _ in range(n)]
for v in range(n):
    filled[v][0] = True


def frame(compare=(), current=None):
    cells = [[up[k][v] if filled[v][k] else "-" for k in range(LOG)] for v in range(n)]
    states = {}
    for v in range(n):
        for k in range(LOG):
            if filled[v][k]:
                states[(v, k)] = "done"
    for cell in compare:
        states[cell] = "compare"
    if current is not None:
        states[current] = "current"
    return vz.table(cells, states=states, row_heads=list(range(n)), col_heads=heads, row_title="v")


rec.step(
    "Column up[0] is the teleporter list itself: up[0][v] is the station one jump from v. "
    "Each row is one station v; the other columns are still empty (-).",
    table=frame(),
)
for k in range(1, LOG):
    half = 1 << (k - 1)
    for v in range(n):
        mid = up[k - 1][v]
        res = up[k][v]
        filled[v][k] = True
        rec.step(
            f"up[{k}][{v}] = up[{k - 1}][up[{k - 1}][{v}]] = up[{k - 1}][{mid}] = {res}. "
            f"From station {v}, "
            + (f"1 jump reaches station {mid}, and 1 more reaches" if half == 1
               else f"{half} jumps reach station {mid}, and {half} more reach")
            + f" station {res}.",
            table=frame(compare=[(v, k - 1), (mid, k - 1)], current=(v, k)),
        )
last = LOG - 1
rec.step(
    f"The table is full. Reading up[{last}][0] = {up[last][0]} says that {1 << last} jumps from "
    f"station 0 land on station {up[last][0]}.",
    table=frame(),
)
rec.output("".join(f"up[{k}] = {up[k]}\n" for k in range(LOG)))
