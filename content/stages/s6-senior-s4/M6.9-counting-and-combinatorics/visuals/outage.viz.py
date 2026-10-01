import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
n = int(data[0])
readings = list(map(int, data[1:1 + n]))

total = n * (n + 1) // 2
clean = 0
run = 0
runs = []


def readings_frame(i, run):
    states = []
    for j in range(n):
        if readings[j] == 0 and j <= i:
            states.append("invalid")
        elif j == i:
            states.append("current")
        elif j < i and j > i - run:
            states.append("done")
        else:
            states.append("none")
    ranges = [(i - run + 1, i, "clean run")] if run > 0 else None
    return vz.array(readings, states=states, ranges=ranges, indices=True)


def run_frame(i):
    vals = [runs[j] if j <= i else "-" for j in range(n)]
    states = ["done" if j <= i else "none" for j in range(n)]
    return vz.array(vals, states=states, indices=True)


for i, v in enumerate(readings):
    if v == 0:
        run = 0
    else:
        run += 1
    clean += run
    runs.append(run)
    if v == 0:
        caption = (
            f"Day {i} reads 0, an outage, so `run` resets to 0: no range ending on day {i} is "
            f"clean. `clean` stays {clean}."
        )
    else:
        caption = (
            f"Day {i} reads {v}, so `run` becomes {run}: {run} "
            f"{'range ends' if run == 1 else 'ranges end'} on day {i} without containing an outage. "
            f"`clean` grows to {clean}."
        )
    rec.step(caption, a=readings_frame(i, run), r=run_frame(i))

answer = total - clean
rec.step(
    f"All {n} days are read. There are {n} * {n + 1} / 2 = {total} ranges in all and {clean} "
    f"of them are clean, so {total} - {clean} = {answer} ranges contain at least one outage.",
    a=readings_frame(n, 0), r=run_frame(n),
)
rec.output(f"{answer}\n")
