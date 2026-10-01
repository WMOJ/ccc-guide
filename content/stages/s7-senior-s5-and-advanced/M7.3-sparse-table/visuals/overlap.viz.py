from functools import reduce
from math import gcd
from operator import add

import vizrec as vz

rec = vz.Recorder()
tokens = rec.stdin.split()
name = tokens[0]
n = int(tokens[1])
a = [int(t) for t in tokens[2:2 + n]]
left = int(tokens[2 + n])
last = int(tokens[3 + n])

op = {"min": min, "gcd": gcd, "sum": add}[name]
word = {"min": "minimum", "gcd": "gcd", "sum": "sum"}[name]

size = 1
while size * 2 <= last - left + 1:
    size *= 2
second = last - size + 1
first = reduce(op, a[left:left + size])
other = reduce(op, a[second:last + 1])
two = op(first, other)
truth = reduce(op, a[left:last + 1])
shared = list(range(second, left + size))


def frame(blocks=0, overlap=False):
    st = {i: "queued" for i in range(left, last + 1)}
    ranges = []
    if blocks >= 1:
        for i in range(left, left + size):
            st[i] = "done"
        ranges.append((left, left + size - 1, f"block 1: {first}", "above"))
    if blocks >= 2:
        for i in range(second, last + 1):
            st[i] = "done"
        ranges.append((second, last, f"block 2: {other}", "below"))
    if overlap:
        for i in shared:
            st[i] = "compare"
    return vz.array(a, states=st, ranges=ranges or None, name="a")


rec.step(
    f"The query asks for the {word} of a[{left}..{last}], length {last - left + 1}. "
    f"Two blocks of length {size} will cover it, one from each end.",
    array=frame(),
)
rec.step(f"Block 1 covers a[{left}..{left + size - 1}]. Its {word} is {first}.", array=frame(1))
rec.step(f"Block 2 covers a[{second}..{last}]. Its {word} is {other}.", array=frame(2, overlap=True))
shared_vals = ", ".join(str(a[i]) for i in shared)
rec.step(
    f"a[{shared[0]}..{shared[-1]}] ({shared_vals}) lies in both blocks, so it was counted twice.",
    array=frame(2, overlap=True),
)
if name == "sum":
    rec.step(
        f"Combining the blocks gives {first} + {other} = {two}, but the true {word} of the range is {truth}. "
        f"The shared cells were added twice, so a sum cannot use overlapping blocks.",
        array=frame(2, overlap=True),
    )
else:
    rec.step(
        f"Combining the blocks gives {name}({first}, {other}) = {two}, and the true {word} of the range is "
        f"{truth}. Counting the shared cells twice changes nothing for a {word}.",
        array=frame(2, overlap=True),
    )
rec.output(f"two blocks: {two}, true answer: {truth}\n")
