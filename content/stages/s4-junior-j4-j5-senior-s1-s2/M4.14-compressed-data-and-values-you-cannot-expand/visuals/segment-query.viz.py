import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
idx = 0
m = int(data[idx])
idx += 1
segment_lengths = []
segment_values = []
for _ in range(m):
    length = int(data[idx])
    idx += 1
    value = data[idx]
    idx += 1
    segment_lengths.append(length)
    segment_values.append(value)

cumulative = [0]


def segments_frame(cur=None):
    states = ["done" if cur is not None and pos < cur else "none" for pos in range(m)]
    if cur is not None and cur < m:
        states[cur] = "current"
    return vz.array(segment_values, states=states)


def cumulative_frame(pointers=None):
    return vz.array(cumulative, states=["done"] * len(cumulative), index_base=0, pointers=pointers)


rec.step(
    f"{m} runs make up the sequence, each far too long to store one slot per position. "
    f"cumulative starts with one entry, 0, before any run is counted.",
    segments=segments_frame(),
    cumulative=cumulative_frame(),
)

for k in range(m):
    cumulative.append(cumulative[-1] + segment_lengths[k])
    rec.step(
        f"cumulative[{k + 1}] is cumulative[{k}] plus the length of run {k} "
        f"({segment_values[k]}, length {segment_lengths[k]}): {cumulative[k]} + {segment_lengths[k]} = {cumulative[k + 1]}.",
        segments=segments_frame(k),
        cumulative=cumulative_frame(pointers={f"k": k + 1}),
    )

q = int(data[idx])
idx += 1
answers = []
for _ in range(q):
    query_pos = int(data[idx])
    idx += 1
    segment = 0
    while cumulative[segment + 1] <= query_pos:
        rec.step(
            f"Position {query_pos}: cumulative[{segment + 1}] = {cumulative[segment + 1]} is at or "
            f"before it, so run {segment} ({segment_values[segment]}) ends too early. Move to run {segment + 1}.",
            segments=segments_frame(segment),
            cumulative=cumulative_frame(pointers={"boundary": segment + 1}),
        )
        segment += 1
    rec.step(
        f"cumulative[{segment}] = {cumulative[segment]} is at or before {query_pos}, and "
        f"cumulative[{segment + 1}] = {cumulative[segment + 1]} is past it: position {query_pos} "
        f"falls inside run {segment}, so the answer is {segment_values[segment]}.",
        segments=segments_frame(segment),
        cumulative=cumulative_frame(pointers=[("start", segment), ("end", segment + 1)]),
    )
    answers.append(segment_values[segment])

rec.output("\n".join(answers) + "\n")
