import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
a = [int(x) for x in rec.readline().split()]
rec.readline()
kind, x, y = map(int, rec.readline().split())

b = 1
while b * b < n:
    b += 1
blocks = (n + b - 1) // b
sums = [sum(a[k * b:k * b + b]) for k in range(blocks)]

lo = x
hi = y
total = 0
added = set()
taken = set()
touched = 0


def frame(pointer=True):
    states = []
    for i in range(n):
        if i in added:
            states.append("d")
        elif x <= i < y:
            states.append("q")
        else:
            states.append("_")
    tstates = []
    for k in range(blocks):
        tstates.append("d" if k in taken else "_")
    tstates.append("c")
    ptrs = {"lo": cur_lo} if pointer and cur_lo < n else None
    return {
        "a": vz.array(a, states=states, pointers=ptrs, name="values"),
        "s": vz.table(
            [sums + [total]],
            states=["".join(tstates)],
            col_heads=[f"block {k}" for k in range(blocks)] + ["total"],
        ),
    }


cur_lo = lo
rec.step(
    f"Sum positions {x} up to, but not including, {y}. The block size is {b}, so blocks start at "
    f"multiples of {b}. `lo` = {lo}, and the range is marked. `total` starts at 0.",
    **frame()
)
while lo < hi and lo % b != 0:
    total += a[lo]
    added.add(lo)
    touched += 1
    lo += 1
    cur_lo = lo
    if lo % b == 0 or lo >= hi:
        more = f" `lo` = {lo} is {'a block start' if lo % b == 0 else 'the end of the range'}."
    else:
        more = f" `lo` = {lo} is still inside a block."
    rec.step(
        f"`lo` was not at a block start, so add the single value `a[{lo - 1}]` = {a[lo - 1]}. "
        f"`total` is {total}.{more}",
        **frame()
    )
while lo + b <= hi:
    k = lo // b
    total += sums[k]
    taken.add(k)
    for i in range(lo, lo + b):
        added.add(i)
    touched += 1
    lo += b
    cur_lo = lo
    rec.step(
        f"Positions {lo - b} to {lo - 1} are a whole block inside the range, so add the stored "
        f"`sums[{k}]` = {sums[k]} instead of {b} values. `total` is {total}, and `lo` = {lo}.",
        **frame()
    )
if lo < hi:
    lead = "No whole block fits." if not taken else "No more whole blocks fit."
    rec.step(
        f"{lead} A block of {b} from position {lo} would end at position {lo + b - 1}, but the "
        f"range stops after position {hi - 1}. The rest is added one value at a time.",
        **frame()
    )
while lo < hi:
    total += a[lo]
    added.add(lo)
    touched += 1
    lo += 1
    cur_lo = lo
    rec.step(
        f"Add the single value `a[{lo - 1}]` = {a[lo - 1]}. `total` is {total}, and "
        f"`lo` = {lo}.",
        **frame()
    )
if touched < y - x:
    saving = f"It took {touched} additions instead of {y - x}."
else:
    saving = f"All {touched} additions were single values: the range is shorter than a block."
rec.step(
    f"`lo` has reached `hi`, so the answer is {total}. {saving}",
    **frame(pointer=False)
)
rec.output(f"{total}\n")
