import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
values = list(map(int, rec.readline().split()))

total = 0
copied = 0
for i in range(n):
    rest = values[i:]
    total += rest[0]
    now = len(rest) - 1
    copied += now
    left = {0: "current"}
    for j in range(1, len(rest)):
        left[j] = "compare"
    right = {j: "done" for j in range(i)}
    right[i] = "current"
    if now == 0:
        text = (
            f"`rest[0]` is {rest[0]}, so `total` is {total}. `rest[1:]` would be empty, nothing is "
            f"copied, and `copied` stays {copied}. The index version reads `values[{i}]` in place."
        )
    else:
        text = (
            f"`rest[0]` is {rest[0]}, so `total` is {total}. `rest[1:]` builds a new list and copies "
            f"the other {now} item{'s' if now != 1 else ''}, so `copied` is {copied}. The index version reads `values[{i}]` "
            f"in place and copies nothing."
        )
    rec.step(
        text,
        s=vz.array(rest, states=left, pointers={"rest": 0}),
        i=vz.array(values, states=right, pointers={"i": i}),
    )

rec.step(
    f"Both versions reach a total of {total}. Slicing copied {copied} items along the way, "
    f"which is {n} * {n - 1} / 2, and the index version copied none. `rest` ended as an empty list.",
    s=vz.array(values[-1:], states="d", name="last rest"),
    i=vz.array(values, states="d" * n),
)
rec.output(f"{total} {copied} {total}\n")
