import vizrec as vz

rec = vz.Recorder()
target = int(rec.readline())

memo_values = [None] * target


def frame(current):
    states = ["done" if v is not None else "unvisited" for v in memo_values]
    states[current] = "current"
    return {"memo": vz.array(memo_values, states=states, name="memo")}


def count_ways(stair):
    if stair >= target:
        return 1
    if memo_values[stair] is not None:
        rec.step(
            f"`ways({stair})` is needed again. `memo[{stair}]` already holds "
            f"{memo_values[stair]}, so it is looked up instead of recomputed.",
            **frame(stair),
        )
        return memo_values[stair]
    result = count_ways(stair + 1) + count_ways(stair + 2)
    memo_values[stair] = result
    rec.step(
        f"`ways({stair})` is computed for the first time and stored: `memo[{stair}] = {result}`.",
        **frame(stair),
    )
    return result


answer = count_ways(0)
rec.output(f"{answer}\n")
