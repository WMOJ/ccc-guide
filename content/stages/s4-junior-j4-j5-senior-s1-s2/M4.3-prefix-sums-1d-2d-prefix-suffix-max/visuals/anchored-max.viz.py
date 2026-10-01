import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
idx = 0
n = int(data[idx])
idx += 1
scores = list(map(int, data[idx:idx + n]))
idx += n
q = int(data[idx])
idx += 1
positions = [int(data[idx + k]) for k in range(q)]
idx += q

ROW_SCORES, ROW_PREFIX, ROW_SUFFIX = 0, 1, 2
prefix_max = [None] * (n + 1)
suffix_max = [None] * (n + 1)


def cells():
    return [scores + [None], list(prefix_max), list(suffix_max)]


def frame(extra_states=None, arrows=None):
    states = {}
    for c in range(n + 1):
        if prefix_max[c] is not None:
            states[(ROW_PREFIX, c)] = "done"
        if suffix_max[c] is not None:
            states[(ROW_SUFFIX, c)] = "done"
    if extra_states:
        states.update(extra_states)
    return vz.table(
        cells(),
        states=states,
        row_heads=["scores", "prefix_max", "suffix_max"],
        col_heads=list(range(n + 1)),
        col_title="i",
        arrows=arrows,
    )


rec.step(
    "Six submissions come in, with scores in columns 0 to 5. prefix_max and suffix_max each get "
    "one more column, 0 to 6: one entry longer than scores.",
    t=frame(),
)

prefix_max[0] = 0
for i in range(n):
    prefix_max[i + 1] = max(prefix_max[i], scores[i])
    rec.step(
        f"prefix_max[{i + 1}] is max(prefix_max[{i}], scores[{i}]) = "
        f"max({prefix_max[i]}, {scores[i]}) = {prefix_max[i + 1]}.",
        t=frame(
            extra_states={(ROW_PREFIX, i + 1): "current"},
            arrows=[
                ((ROW_PREFIX, i), (ROW_PREFIX, i + 1)),
                ((ROW_SCORES, i), (ROW_PREFIX, i + 1)),
            ],
        ),
    )

suffix_max[n] = 0
for i in range(n - 1, -1, -1):
    suffix_max[i] = max(suffix_max[i + 1], scores[i])
    rec.step(
        f"suffix_max[{i}] is max(suffix_max[{i + 1}], scores[{i}]) = "
        f"max({suffix_max[i + 1]}, {scores[i]}) = {suffix_max[i]}.",
        t=frame(
            extra_states={(ROW_SUFFIX, i): "current"},
            arrows=[
                ((ROW_SUFFIX, i + 1), (ROW_SUFFIX, i)),
                ((ROW_SCORES, i), (ROW_SUFFIX, i)),
            ],
        ),
    )

for i in positions:
    result = max(prefix_max[i], suffix_max[i + 1])
    rec.step(
        f"With submission {i} set aside: prefix_max[{i}] = {prefix_max[i]}, "
        f"suffix_max[{i + 1}] = {suffix_max[i + 1]}. max({prefix_max[i]}, {suffix_max[i + 1]}) "
        f"= {result}, the best score outside position {i}.",
        t=frame(extra_states={
            (ROW_SCORES, i): "current",
            (ROW_PREFIX, i): "compare",
            (ROW_SUFFIX, i + 1): "compare",
        }),
    )

rec.output("\n".join(str(max(prefix_max[i], suffix_max[i + 1])) for i in positions) + "\n")
