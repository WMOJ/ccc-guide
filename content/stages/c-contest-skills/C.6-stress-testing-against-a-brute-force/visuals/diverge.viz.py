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


def buggy(values):
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


def shrink(values):
    changed = True
    while changed:
        changed = False
        for k in range(len(values)):
            smaller = values[:k] + values[k + 1:]
            if smaller and brute(smaller) != buggy(smaller):
                values = smaller
                changed = True
                break
    return values


values = shrink(start)
m = len(values)
prefix = [0]
for v in values:
    prefix.append(prefix[-1] + v)
want = brute(values)


def paren(x):
    return f"({x})" if x < 0 else str(x)


def values_frame(j=None, rng=None):
    states = ["none"] * m
    if j is not None:
        states[j] = "current"
    return vz.array(values, states=states, ranges=[rng] if rng else None, index_base=0)


def prefix_frame(low_at, end=None):
    states = ["none"] * (m + 1)
    states[low_at] = "compare"
    pointers = [("low", low_at, "below")]
    if end is not None and end != low_at:
        states[end] = "current"
        pointers.append(("end", end))
    return vz.array(prefix, states=states, pointers=pointers, index_base=0)


low_at = 1
low = prefix[low_at]
best = values[0]
rec.step(
    f"The shrunk input is {values}, so prefix is {prefix}. The buggy function starts low at "
    f"prefix[1], which is {low}, and best at values[0], which is {best}.",
    values=values_frame(),
    prefix=prefix_frame(low_at),
)
for j in range(m):
    end = prefix[j + 1]
    cand = end - low
    text = f"cand is prefix[{j + 1}] - prefix[{low_at}] = {end} - {paren(low)} = {cand}."
    rng = None
    if low_at > j:
        text += " Both come from the same entry, so this is an empty range, not a subarray."
    else:
        rng = (low_at, j, f"sum {cand}")
        text += f" That is the sum of values[{low_at}..{j}]."
    if cand > best:
        best = cand
        text += f" It beats best, so best becomes {best}."
    else:
        text += f" It does not beat best, which stays {best}."
    rec.step(text, values=values_frame(j, rng), prefix=prefix_frame(low_at, j + 1))
    if end < low:
        low = end
        low_at = j + 1
        rec.step(
            f"prefix[{j + 1}] is below low, so low moves there and becomes {low}.",
            values=values_frame(j),
            prefix=prefix_frame(low_at),
        )

if best > want:
    closing = (
        f"The function returns {best}, but the brute force says {want}. No subarray sums to "
        f"{best}: that value came from subtracting prefix[1] from itself."
    )
else:
    closing = (
        f"The function returns {best}, but the brute force says {want}. The best subarray starts "
        f"at values[0], and prefix[0] was never available to subtract."
    )
rec.step(closing, values=values_frame(), prefix=prefix_frame(low_at))
rec.output(f"start {start}\nshrunk {values}\nbrute {want}\nfast {best}\n")
