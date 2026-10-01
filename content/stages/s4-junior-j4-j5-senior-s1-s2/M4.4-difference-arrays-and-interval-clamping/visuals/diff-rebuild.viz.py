import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
idx = 0
n = int(data[idx])
m = int(data[idx + 1])
idx += 2
updates = []
for _ in range(m):
    l, r, val = int(data[idx]), int(data[idx + 1]), int(data[idx + 2])
    updates.append((l, r, val))
    idx += 3

diff = [0] * (n + 1)


def diff_frame(pointers=None):
    return vz.array(diff, pointers=pointers, index_base=0)


def arr_frame(built, cur=None):
    values = built + [None] * (n - len(built))
    states = ["done"] * len(built) + ["none"] * (n - len(built))
    if cur is not None:
        states[cur] = "current"
    return vz.array(values, states=states)


rec.step(
    f"diff starts as {n + 1} zeros, one entry longer than the array so diff[r + 1] always has "
    "room to write.",
    diff=diff_frame(),
    arr=arr_frame([]),
)

for l, r, val in updates:
    diff[l] += val
    diff[r + 1] -= val
    rec.step(
        f"Update [{l}, {r}] by {val}: diff[{l}] += {val} starts it, diff[{r + 1}] -= {val} stops "
        "it right after the range.",
        diff=diff_frame(pointers=[("l", l, "above", True), ("r+1", r + 1, "above")]),
        arr=arr_frame([]),
    )

rec.step(
    "Every update is recorded. Now rebuild the array the same way M4.3's prefix sum runs over "
    "any array: a running total, left to right.",
    diff=diff_frame(),
    arr=arr_frame([]),
)

built = []
current = 0
for i in range(n):
    current += diff[i]
    built.append(current)
    rec.step(
        f"arr[{i}] = the running total after diff[{i}]: {current - diff[i]} + {diff[i]} = "
        f"{current}.",
        diff=diff_frame(pointers=[("i", i, "above", True)]),
        arr=arr_frame(built, cur=i),
    )

rec.step(
    f"The running sum of diff is the final array: {built}, every range update applied.",
    diff=diff_frame(),
    arr=arr_frame(built),
)

rec.output(" ".join(map(str, built)) + "\n")
