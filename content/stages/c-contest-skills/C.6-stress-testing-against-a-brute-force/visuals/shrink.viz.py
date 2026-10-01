import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
start = [int(t) for t in rec.readline().split()]


def brute(values):
    m = len(values)
    return max(
        sum(values[i:j + 1])
        for i in range(m)
        for j in range(i, m)
    )


def fast(values):
    m = len(values)
    total = 0
    prefix = [0]
    for v in values:
        total += v
        prefix.append(total)
    low = prefix[1]
    best = values[0]
    for j in range(m):
        end = prefix[j + 1]
        cand = end - low
        best = max(best, cand)
        low = min(low, end)
    return best


def current_frame(values, k=None):
    states = ["none"] * len(values)
    if k is not None:
        states[k] = "invalid"
    return vz.array(values, states=states, index_base=0)


def try_frame(values, fails):
    return vz.array(values, states=["done" if fails else "compare"] * len(values), index_base=0)


values = list(start)
rec.step(
    f"The test found {values}: the brute force says {brute(values)} and the fast function says "
    f"{fast(values)}. Shrinking tries to drop one element at a time and keeps any drop that still "
    f"fails.",
    current=current_frame(values),
    trial=try_frame(values, True),
)
changed = True
while changed:
    changed = False
    for k in range(len(values)):
        smaller = values[:k] + values[k + 1:]
        if not smaller:
            continue
        b, f = brute(smaller), fast(smaller)
        if b != f:
            rec.step(
                f"Drop values[{k}], which is {values[k]}: {smaller} gives brute {b} and fast {f}. "
                f"They still differ, so keep the smaller input and start again from its first "
                f"element.",
                current=current_frame(values, k),
                trial=try_frame(smaller, True),
            )
            values = smaller
            changed = True
            break
        rec.step(
            f"Drop values[{k}], which is {values[k]}: {smaller} gives brute {b} and fast {f}. "
            f"They agree, so this element is needed to show the bug. Put it back.",
            current=current_frame(values, k),
            trial=try_frame(smaller, False),
        )

rec.step(
    f"No single drop keeps the mismatch, so {values} is the smallest failing input: the brute force "
    f"says {brute(values)} and the fast function says {fast(values)}.",
    current=current_frame(values),
    trial=try_frame(values, True),
)
rec.output(
    f"start {start}\nshrunk {values}\nbrute {brute(values)}\nfast {fast(values)}\n"
)
