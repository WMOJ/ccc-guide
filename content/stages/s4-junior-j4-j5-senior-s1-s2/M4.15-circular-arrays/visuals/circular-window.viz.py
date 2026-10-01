import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
n = int(data[0])
k = int(data[1])
values = [int(x) for x in data[2:2 + n]]


def window_indices(start):
    return [(start + off) % n for off in range(k)]


def frame(start, best_start=None):
    states = ["none"] * n
    for i in window_indices(start):
        states[i] = "current"
    if best_start is not None and best_start != start:
        for i in window_indices(best_start):
            if states[i] == "none":
                states[i] = "done"
    return vz.array(values, states=states, circular=True, indices=True)


window_sum = sum(values[0:k])
best = window_sum
best_start = 0

rec.step(
    f"Start with the window at position 0: values[0] through values[{k - 1}], summing to {window_sum}.",
    ring=frame(0),
)

for start in range(1, n):
    leaving_index = (start - 1) % n
    leaving = values[leaving_index]
    entering_index = (start + k - 1) % n
    entering = values[entering_index]
    window_sum = window_sum - leaving + entering
    wrapped = entering_index < leaving_index
    note = " The window has wrapped past the last index." if wrapped else ""
    if window_sum > best:
        best = window_sum
        best_start = start
        note += f" That beats the best sum so far, now {best}."
    rec.step(
        f"Slide to position {start}: drop values[{leaving_index}] = {leaving}, add "
        f"values[{entering_index}] = {entering}. New sum: {window_sum}.{note}",
        ring=frame(start, best_start),
    )

rec.step(
    f"Every one of the {n} starting positions is checked, wrapped ones included. "
    f"The best window starts at position {best_start} with sum {best}.",
    ring=frame(best_start, best_start),
)

rec.output(f"{best}\n")
