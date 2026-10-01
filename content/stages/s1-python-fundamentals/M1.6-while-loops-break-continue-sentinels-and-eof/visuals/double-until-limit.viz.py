import vizrec as vz

rec = vz.Recorder()
limit = int(rec.readline())
value = 1
history = [value]


def frame():
    n = len(history)
    states = ["done"] * (n - 1) + ["current"]
    return vz.array(history, states=states, pointers=[("value", n - 1, None, True)], name=f"limit {limit}")


while value < limit:
    rec.step(
        f"Check value < limit: {value} < {limit} is True, so the block runs and value becomes {value * 2}.",
        a=frame(),
    )
    value *= 2
    history.append(value)

rec.step(
    f"Check value < limit: {value} < {limit} is False, so the loop ends and print(value) shows {value}.",
    a=frame(),
)

rec.output(f"{value}\n")
