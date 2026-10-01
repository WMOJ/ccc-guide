import random
import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
n = int(data[0])
k = int(data[1])
seed = int(data[2])
values = list(map(int, data[3:3 + n]))

random.seed(seed)
rank = k - 1

# Run the algorithm once, keeping what each round did, then replay it as steps.
rounds = []
while True:
    idx = random.randrange(len(values))
    pivot = values[idx]
    smaller = [v for v in values if v < pivot]
    larger = [v for v in values if v > pivot]
    equal = len(values) - len(smaller) - len(larger)
    if rank < len(smaller):
        keep = "smaller"
    elif rank < len(smaller) + equal:
        keep = "equal"
    else:
        keep = "larger"
    rounds.append({
        "values": values, "idx": idx, "pivot": pivot, "smaller": smaller, "larger": larger,
        "equal": equal, "keep": keep, "rank": rank,
    })
    if keep == "equal":
        answer = pivot
        break
    if keep == "smaller":
        values = smaller
    else:
        rank -= len(smaller) + equal
        values = larger

total = len(rounds)
col_heads = ["pivot", "smaller", "equal", "larger"]


def table(upto, show_split):
    cells = []
    states = {}
    for r in range(total):
        info = rounds[r]
        row = [None] * 4
        if r <= upto:
            row[0] = info["pivot"]
        if r < upto or (r == upto and show_split):
            row[1] = len(info["smaller"])
            row[2] = info["equal"]
            row[3] = len(info["larger"])
        cells.append(row)
        for c in range(4):
            if r < upto:
                states[(r, c)] = "done"
            elif r == upto and c == 0:
                states[(r, c)] = "current"
            elif r == upto and show_split:
                states[(r, c)] = "current"
    return vz.table(
        cells, states=states, row_heads=[f"round {r + 1}" for r in range(total)],
        col_heads=col_heads,
    )


for r, info in enumerate(rounds):
    vals = info["values"]
    size = len(vals)
    states = ["none"] * size
    states[info["idx"]] = "current"
    rec.step(
        f"Round {r + 1}: `random.randrange({size})` picks position {info['idx']}, so the pivot is "
        f"{info['pivot']}. The wanted value is number {info['rank'] + 1} in sorted order among "
        f"these {size} candidates.",
        a=vz.array(vals, states=states, pointers=[("pivot", info["idx"])], indices=True),
        t=table(r, False),
    )
    s = len(info["smaller"])
    e = info["equal"]
    lg = len(info["larger"])
    split = info["smaller"] + [info["pivot"]] * e + info["larger"]
    keep = info["keep"]
    groups = {"smaller": (0, s - 1), "equal": (s, s + e - 1), "larger": (s + e, size - 1)}
    states = []
    ranges = []
    for name, (a, b) in groups.items():
        if b < a:
            continue
        if name == keep:
            ranges.append((a, b, name))
        elif name == "equal":
            ranges.append((a, b, "equal"))
        for _ in range(a, b + 1):
            states.append("current" if keep == "equal" and name == "equal" else
                          "frontier" if name == keep else "done")
    if keep == "equal":
        tail = (
            f"Number {info['rank'] + 1} in sorted order falls in the equal group, so the "
            f"answer is the pivot, {info['pivot']}."
        )
    else:
        gone = size - (s if keep == "smaller" else lg)
        tail = (
            f"Number {info['rank'] + 1} in sorted order falls in the {keep} group, so the other "
            f"{gone} {'candidate is' if gone == 1 else 'candidates are'} discarded."
        )
    rec.step(
        f"Comparing every candidate with {info['pivot']} gives {s} smaller, {e} equal and {lg} "
        f"larger. {tail}",
        a=vz.array(split, states=states, ranges=ranges, indices=True),
        t=table(r, True),
    )

word = "round" if total == 1 else "rounds"
rec.output(f"smallest number {k}: {answer}, found in {total} {word}\n")
