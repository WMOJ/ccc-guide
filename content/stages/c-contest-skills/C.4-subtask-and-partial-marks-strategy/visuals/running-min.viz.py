import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
values = [int(t) for t in rec.readline().split()]

prefix = [0]
for v in values:
    prefix.append(prefix[-1] + v)


def paren(x):
    return f"({x})" if x < 0 else str(x)


def values_frame(j=None, rng=None):
    states = ["none"] * n
    if j is not None:
        states[j] = "current"
    return vz.array(values, states=states, ranges=[rng] if rng else None, index_base=0)


def prefix_frame(low_at, end=None):
    states = ["none"] * (n + 1)
    states[low_at] = "compare"
    pointers = [("low", low_at, "below")]
    if end is not None and end != low_at:
        states[end] = "current"
        pointers.append(("end", end))
    return vz.array(prefix, states=states, pointers=pointers, index_base=0)


low_at = 0
low = prefix[0]
best = values[0]
rec.step(
    f"prefix is {prefix}, built in one pass. low starts at prefix[0], which is {low}, and best "
    f"starts at values[0], which is {best}.",
    values=values_frame(),
    prefix=prefix_frame(low_at),
)
for j in range(n):
    end = prefix[j + 1]
    cand = end - low
    text = (
        f"j = {j}: cand is prefix[{j + 1}] - low = {end} - {paren(low)} = {cand}, the sum of "
        f"values[{low_at}:{j + 1}]."
    )
    if cand > best:
        best = cand
        text += f" It beats best, so best becomes {best}."
    else:
        text += f" It does not beat best, which stays {best}."
    rec.step(
        text,
        values=values_frame(j, (low_at, j, f"sum {cand}")),
        prefix=prefix_frame(low_at, j + 1),
    )
    if end < low:
        low = end
        low_at = j + 1
        rec.step(
            f"prefix[{j + 1}] is smaller than low, so low moves there and becomes {low}. A run "
            f"starting at values[{j + 1}] would subtract this smaller entry.",
            values=values_frame(j),
            prefix=prefix_frame(low_at),
        )

rec.step(
    f"Every end has been tried against the smallest prefix before it. best is {best}, the "
    f"largest sum of any run of consecutive values.",
    values=values_frame(),
    prefix=prefix_frame(low_at),
)
rec.output(f"{best}\n")
