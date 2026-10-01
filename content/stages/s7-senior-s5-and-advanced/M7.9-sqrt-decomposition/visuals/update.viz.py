import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
a = [int(x) for x in rec.readline().split()]
rec.readline()
kind, p, v = map(int, rec.readline().split())
kind2, l2, r2 = map(int, rec.readline().split())

b = 1
while b * b < n:
    b += 1
blocks = (n + b - 1) // b
sums = [sum(a[k * b:k * b + b]) for k in range(blocks)]
k = p // b


def frame(vals, sm, pos=None, blk=None, fresh=False):
    states = ["_"] * n
    if pos is not None:
        states[pos] = "d" if fresh else "c"
    tstates = ["_"] * blocks
    if blk is not None:
        tstates[blk] = "d" if fresh else "c"
    return {
        "a": vz.array(vals, states=states, name="values"),
        "s": vz.table([sm], states=["".join(tstates)],
                      col_heads=[f"block {j}" for j in range(blocks)]),
    }


old = a[p]
rec.step(
    f"Set position {p} to {v}. Position {p} is in block {p} // {b} = {k}, and it holds {old} now. "
    f"`sums[{k}]` is {sums[k]}.",
    **frame(list(a), list(sums), p, k)
)
delta = v - old
old_sum = sums[k]
new_sum = old_sum + delta
sign = "+" if delta >= 0 else "-"
a[p] = v
sums[k] = new_sum
rec.step(
    f"The value changes by {v} - {old} = {delta}. Write `a[{p}] = {v}`, and add the same {delta} "
    f"to `sums[{k}]`: {old_sum} {sign} {abs(delta)} = {new_sum}. No other value or block is read "
    "or written.",
    **frame(list(a), list(sums), p, k, fresh=True)
)
total = 0
lo = l2
while lo < r2 and lo % b != 0:
    total += a[lo]
    lo += 1
while lo + b <= r2:
    total += sums[lo // b]
    lo += b
while lo < r2:
    total += a[lo]
    lo += 1
rec.step(
    f"A later query for positions {l2} up to, but not including, {r2} reads the new numbers and "
    f"answers {total}.",
    **frame(list(a), list(sums))
)
rec.output(f"{total}\n")
