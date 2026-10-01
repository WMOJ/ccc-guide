import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
n = int(data[0])
a = list(map(int, data[1:n + 1]))
target = int(data[n + 1])

prefixes = [0]
for x in a:
    prefixes.append(prefixes[-1] + x - target)
SLOTS = 6

best = {0: 0}
order = [0]
dps = [0]


def top(cur=None, state="current"):
    row_p = [prefixes[i] if i < len(dps) else None for i in range(n + 1)]
    row_d = [dps[i] if i < len(dps) else None for i in range(n + 1)]
    states = {}
    if cur is not None:
        states[(0, cur)] = state
        states[(1, cur)] = state
    return vz.table([row_p, row_d], states=states, row_heads=["prefix", "dp"],
                    col_heads=list(range(n + 1)), col_title="j")


def dict_frame(hl=None, state="current"):
    keys = order + [None] * (SLOTS - len(order))
    vals = [best[k] if k is not None else None for k in keys]
    states = {}
    if hl is not None:
        states[(0, order.index(hl))] = state
        states[(1, order.index(hl))] = state
    return vz.table([keys, vals], states=states, row_heads=["key", "best"])


rec.step(
    f"dp[j] is the most disjoint stretches with average {target} in the first j elements. "
    "Start with dp[0] = 0 and best[0] = 0: the empty prefix, with no stretch yet.",
    top=top(0, "done"),
    best=dict_frame(0, "done"),
)
for j in range(1, n + 1):
    p = prefixes[j]
    x = a[j - 1]
    prev = dps[-1]
    if p in best:
        cand = best[p] + 1
        new = max(prev, cand)
        if cand > prev:
            why = (f"best[{p}] + 1 = {cand} beats dp[{j - 1}] = {prev}: end a new stretch here, "
                   f"one that starts at an earlier prefix equal to {p}.")
        else:
            why = (f"best[{p}] + 1 = {cand} does not beat dp[{j - 1}] = {prev}, so dp[{j}] "
                   f"stays {new}.")
        dps.append(new)
        rec.step(
            f"prefix[{j}] = {p} (after {x} - {target}). The key {p} is in the dictionary. {why}",
            top=top(j, "compare"),
            best=dict_frame(p, "compare"),
        )
    else:
        dps.append(prev)
        rec.step(
            f"prefix[{j}] = {p} (after {x} - {target}). The key {p} is new, so no stretch ends "
            f"here and dp[{j}] stays {prev}.",
            top=top(j),
            best=dict_frame(),
        )
    if p not in best:
        order.append(p)
    best[p] = dps[-1]
    rec.step(
        f"Store best[{p}] = {dps[-1]}, the most stretches found by the time this prefix appeared.",
        top=top(j),
        best=dict_frame(p, "done"),
    )
rec.step(
    f"dp[{n}] = {dps[-1]}: the most disjoint stretches with average {target}.",
    top=top(n, "done"),
    best=dict_frame(),
)
rec.output(f"{dps[-1]}\n")
