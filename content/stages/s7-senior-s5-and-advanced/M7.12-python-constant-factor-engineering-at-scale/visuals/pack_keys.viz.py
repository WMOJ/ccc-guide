import vizrec as vz

BASE = 1000
rec = vz.Recorder()
n = int(rec.readline())
pairs = []
for _ in range(n):
    a, b = map(int, rec.readline().split())
    pairs.append((a, b))


def label(pair):
    return f"{pair[0]},{pair[1]}"


labels = [label(p) for p in pairs]
keys = []
for i in range(n):
    a, b = pairs[i]
    keys.append(a * BASE + b)
    shown = keys + ["?"] * (n - len(keys))
    st = {j: "done" for j in range(i)}
    st[i] = "current"
    rec.step(
        f"Pair {i} is ({a}, {b}). Its key is {a} * {BASE} + {b} = {keys[i]}: `a` moves up by "
        f"{BASE}, so `b` only fills the low digits."
        + (f" {b} is the largest `b` that fits below {BASE}." if b == BASE - 1 else ""),
        p=vz.array(labels, states=st, indices=True),
        k=vz.array(shown, states=st, indices=True),
    )

keys.sort()
rec.step(
    f"`keys.sort()` orders plain integers: {keys}. Keys with a smaller `a` come first, and keys "
    f"with equal `a` are ordered by `b`.",
    p=vz.array(labels, name="unsorted", indices=True),
    k=vz.array(keys, states="m" * n, name="sorted", indices=True),
)

out = []
shown = ["?"] * n
for i in range(n):
    a, b = divmod(keys[i], BASE)
    shown[i] = f"{a},{b}"
    out.append(f"{a} {b}")
    st = {j: "done" for j in range(i)}
    st[i] = "current"
    rec.step(
        f"`divmod({keys[i]}, {BASE})` is ({a}, {b}): the quotient is `a` and the remainder is `b`.",
        p=vz.array(shown, states=st, name="unpacked", indices=True),
        k=vz.array(keys, states=st, name="sorted", indices=True),
    )
rec.output("\n".join(out) + "\n")
