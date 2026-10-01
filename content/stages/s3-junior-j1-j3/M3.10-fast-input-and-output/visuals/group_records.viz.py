import vizrec as vz

rec = vz.Recorder()
tokens = rec.stdin.split()
n = len(tokens)


def frame(pos, group=None):
    states = ["done" if i < pos else ("current" if i == pos else "none") for i in range(n)]
    ranges = None
    if group is not None and group[1] > group[0]:
        ranges = [(group[0], group[1] - 1, f"group {group[2]} values")]
    return vz.array(tokens, states=states, pointers={"pos": pos}, ranges=ranges, indices=True)


def state_frame(group, k, total):
    return vz.table(
        cells=[[group], [k], [total]],
        row_heads=["group", "k", "sum so far"],
        col_heads=["value"],
    )


def noun(count):
    return f"{count} value{'s' if count != 1 else ''}"


pos = 0
groups = int(tokens[pos])
pos += 1
rec.step(
    f"tokens[0] is '{tokens[0]}', so there {'is' if groups == 1 else 'are'} {groups} group{'s' if groups != 1 else ''}. Each group starts with its own count, k. pos moves to {pos}.",
    tokens=frame(pos),
    state=state_frame(0, "?", 0),
)

results = []
for g in range(1, groups + 1):
    k = int(tokens[pos])
    start = pos + 1
    pos += 1
    if k == 0:
        rec.step(
            f"tokens[{start - 1}] is '{k}': group {g} holds no values, so its sum is 0. pos moves to {pos}.",
            tokens=frame(pos),
            state=state_frame(g, k, 0),
        )
        results.append(0)
        continue
    rec.step(
        f"tokens[{start - 1}] is '{k}': group {g} holds {noun(k)}. pos moves to {pos}.",
        tokens=frame(pos, (start, start + k, g)),
        state=state_frame(g, k, 0),
    )
    total = 0
    for j in range(k):
        val = int(tokens[pos])
        total += val
        pos += 1
        closing = f" The group is done: {total} is appended to results." if j == k - 1 else ""
        rec.step(
            f"tokens[{pos - 1}] is '{val}', so the sum so far is {total}. pos moves to {pos}.{closing}",
            tokens=frame(pos, (start, start + k, g)),
            state=state_frame(g, k, total),
        )
    results.append(total)

rec.step(
    f"Every group is read and pos is {pos}, one past the last token. The sum{'s' if groups != 1 else ''}: {', '.join(str(r) for r in results)}.",
    tokens=frame(pos),
    state=state_frame(groups, "-", results[-1]),
)

rec.output("\n".join(str(r) for r in results) + "\n")
