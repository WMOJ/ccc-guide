import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
idx = 0
n = int(data[idx])
idx += 1
values = list(map(int, data[idx:idx + n]))
idx += n

unique_values = sorted(set(values))
rank = {value: i for i, value in enumerate(unique_values)}
compressed = [None] * n


def values_frame(cur=None):
    states = ["done" if (cur is not None and pos < cur) else "none" for pos in range(n)]
    if cur is not None and cur < n:
        states[cur] = "current"
    pointers = [("i", cur)] if cur is not None and cur < n else None
    return vz.array(values, states=states, pointers=pointers)


def compressed_frame(cur=None):
    states = ["none" if v is None else "done" for v in compressed]
    if cur is not None and cur < n:
        states[cur] = "current"
    return vz.array(compressed, states=states)


rank_text = ", ".join(f"{v}: {r}" for v, r in sorted(rank.items(), key=lambda kv: kv[1]))
rec.step(
    f"{n} values arrive, some repeated. Sorting the {len(unique_values)} distinct ones and "
    f"numbering them from 0 gives rank = {{{rank_text}}}.",
    values=values_frame(),
    compressed=compressed_frame(),
)

for i in range(n):
    r = rank[values[i]]
    compressed[i] = r
    rec.step(
        f"values[{i}] is {values[i]}; rank[{values[i]}] is {r}, so compressed[{i}] = {r}.",
        values=values_frame(i),
        compressed=compressed_frame(i),
    )

rec.step(
    f"The compressed array only ever holds indices 0 through {len(unique_values) - 1}, "
    "however large the original values were.",
    values=values_frame(n),
    compressed=compressed_frame(),
)

rec.output(" ".join(map(str, compressed)) + "\n")
