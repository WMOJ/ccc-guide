import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
values = list(map(int, rec.readline().split()))[:n]

# The program from examples/longest_run.py, one comparison per step.
best = 1
run = 1
best_span = (0, 0)
run_start = 0


def true_longest():
    start = 0
    top = (0, 0)
    for i in range(1, n + 1):
        if i == n or values[i] != values[i - 1]:
            if i - start > top[1] - top[0] + 1:
                top = (start, i - 1)
            start = i
    return top


def frame(i, upto, final=False):
    states = []
    for k in range(n):
        if final:
            top = true_longest()
            inside = top[0] <= k <= top[1]
            states.append("path" if inside and best != top[1] - top[0] + 1 else "done")
        elif k == i:
            states.append("current")
        elif k == i - 1 and i > 0:
            states.append("compare")
        elif k < i:
            states.append("done")
        else:
            states.append("none")
    ranges = [(run_start, upto, f"run {run}", "above")]
    if best_span != (run_start, upto) or best != run:
        ranges.append((best_span[0], best_span[1], f"best {best}", "below"))
    return vz.array(
        values,
        states=states,
        pointers=None if final else [("i", i, "below", True)] if i < n else None,
        ranges=ranges[:2],
        indices=True,
    )


rec.step(
    f"The program starts with best = 1 and run = 1: the first value, {values[0]}, is a run of length 1.",
    arr=frame(0, 0),
)
for i in range(1, n):
    if values[i] == values[i - 1]:
        run += 1
        caption = (
            f"i = {i}: values[{i}] is {values[i]}, the same as values[{i - 1}]. "
            f"The run grows, so run = {run}."
        )
    else:
        old = run
        if run > best:
            best = run
            best_span = (run_start, i - 1)
        caption = (
            f"i = {i}: values[{i}] is {values[i]}, not {values[i - 1]}. The run of {old} ends, "
            f"so best = max(best, {old}) = {best}, and run starts over at 1."
        )
        run = 1
        run_start = i
    rec.step(caption, arr=frame(i, i))

top = true_longest()
expected = top[1] - top[0] + 1
verdict = "matches the expected output" if best == expected else "is wrong answer"
if best == expected:
    tail = f"The loop ends and the program prints best = {best}, the longest run, so it {verdict}."
else:
    tail = (
        f"The loop ends with run = {run}, and nothing copies it into best. "
        f"The program prints {best}, but the longest run has length {expected}: it {verdict}."
    )
rec.step(tail, arr=frame(n, n - 1, final=True))
rec.output(f"{best}\n")
