import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
idx = 0
n = int(data[idx])
idx += 1
values = list(map(int, data[idx:idx + n]))
idx += n
q = int(data[idx])
idx += 1
queries = []
for _ in range(q):
    i, j = int(data[idx]), int(data[idx + 1])
    idx += 2
    queries.append((i, j))

prefix = [0]


def values_frame(cur=None, rng=None):
    states = ["done" if (cur is not None and pos < cur) else "none" for pos in range(n)]
    if cur is not None and cur < n:
        states[cur] = "current"
    return vz.array(values, states=states, ranges=[rng] if rng else None)


def prefix_frame(pointers=None, compare=None):
    return vz.array(prefix, states=["done"] * len(prefix), index_base=0, pointers=pointers, compare=compare)


rec.step(
    "Before any day is added, prefix holds one entry, 0: the rainfall total for zero days.",
    values=values_frame(0),
    prefix=prefix_frame(),
)

for k in range(n):
    prefix.append(prefix[-1] + values[k])
    rec.step(
        f"prefix[{k + 1}] is prefix[{k}] plus values[{k}]: {prefix[k]} + {values[k]} = {prefix[k + 1]}.",
        values=values_frame(k),
        prefix=prefix_frame(pointers={"k": k + 1}),
    )

rec.step(
    "The prefix array is complete, one entry longer than values, with prefix[0] equal to 0.",
    values=values_frame(n),
    prefix=prefix_frame(),
)

for i, j in queries:
    rec.step(
        f"To total the rainfall from day {i} to day {j}, mark that range on values.",
        values=values_frame(n, rng=(i, j, f"day {i}-{j}")),
        prefix=prefix_frame(pointers=[("i", i), ("j+1", j + 1)]),
    )
    total = prefix[j + 1] - prefix[i]
    rec.step(
        f"prefix[{j + 1}] - prefix[{i}] = {prefix[j + 1]} - {prefix[i]} = {total}. "
        f"That is the total rainfall from day {i} to day {j}.",
        values=values_frame(n, rng=(i, j, f"day {i}-{j}")),
        prefix=prefix_frame(
            pointers=[("i", i), ("j+1", j + 1)],
            compare=(i, j + 1, f"={total}"),
        ),
    )

rec.output("\n".join(str(prefix[j + 1] - prefix[i]) for i, j in queries) + "\n")
