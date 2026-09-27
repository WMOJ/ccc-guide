import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
arrivals = list(map(int, rec.readline().split()))

queue_length = 0
max_length = 0


def arr_frame(i):
    states = ["done" if j < i else ("current" if j == i else "none") for j in range(n)]
    return vz.array(arrivals, states=states)


def q_frame():
    return vz.queue([f"patron {k + 1}" for k in range(queue_length)])


rec.step("Before minute 1: the line is empty.", arr=arr_frame(0), q=q_frame())
for i, minute_arrivals in enumerate(arrivals):
    queue_length += minute_arrivals
    max_length = max(max_length, queue_length)
    rec.step(
        f"Minute {i + 1}: {minute_arrivals} patrons join. The line is now {queue_length} long, "
        f"and the longest so far is {max_length}.",
        arr=arr_frame(i), q=q_frame()
    )
    if queue_length > 0:
        queue_length -= 1
        rec.step(
            f"Minute {i + 1}: one patron is served, leaving the line at {queue_length}.",
            arr=arr_frame(i), q=q_frame()
        )
    else:
        rec.step(
            f"Minute {i + 1}: no one is waiting, so no one is served.",
            arr=arr_frame(i), q=q_frame()
        )

rec.step(f"After minute {n}: the longest the line ever reached was {max_length}.", arr=arr_frame(n), q=q_frame())
rec.output(f"{max_length}\n")
