import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
marks = [int(rec.readline()) for _ in range(n)]

count = 0
states = ["_"] * n


def arr(i):
    pointers = [("i", i, None, True)] if i is not None else None
    return vz.array(marks, states=states, pointers=pointers, indices=True)


def tab(i, states_map=None):
    return vz.table([[i if i is not None else "-"], [count]], states=states_map, row_heads=["i", "count"])


for i in range(n):
    states[i] = "c"
    rec.step(
        f"Position {i}: mark {marks[i]}. Is it 50 or higher? count is still {count}.",
        array=arr(i),
        table=tab(i, {(0, 0): "current"}),
    )
    if marks[i] >= 50:
        count += 1
        states[i] = "d"
        rec.step(
            f"{marks[i]} >= 50 is True, so count += 1 makes count {count}.",
            array=arr(i),
            table=tab(i, {(1, 0): "path"}),
        )
    else:
        states[i] = "x"
        rec.step(
            f"{marks[i]} >= 50 is False, so count stays {count}. Only i moves on.",
            array=arr(i),
            table=tab(i, {(0, 0): "done"}),
        )

rec.step(
    f"The loop is over. i went through all {n} positions, but count is {count}: "
    f"{count} of the {n} marks passed.",
    array=vz.array(marks, states=states, indices=True),
    table=tab(None, {(1, 0): "path"}),
)

rec.output(f"{count}\n")
