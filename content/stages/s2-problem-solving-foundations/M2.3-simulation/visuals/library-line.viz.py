import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
arrivals = list(map(int, rec.readline().split()))

queue = []  # persistent patron ids currently waiting, front (served next) at index 0
max_length = 0
next_id = 1


def arr_frame(i):
    states = ["done" if (i is not None and j < i) else ("current" if j == i else "none") for j in range(n)]
    return vz.array(arrivals, states=states, index_base=1)


def q_frame():
    return vz.queue([f"patron {pid}" for pid in queue])


rec.step("Before minute 1: the line is empty.", arr=arr_frame(None), q=q_frame())
for i, minute_arrivals in enumerate(arrivals):
    for _ in range(minute_arrivals):
        queue.append(next_id)
        next_id += 1
    max_length = max(max_length, len(queue))
    if minute_arrivals == 0:
        join_clause = f"no one joins, so the line stays {len(queue)} long"
    elif minute_arrivals == 1:
        join_clause = f"1 patron joins. The line is now {len(queue)} long"
    else:
        join_clause = f"{minute_arrivals} patrons join. The line is now {len(queue)} long"
    rec.step(
        f"Minute {i + 1}: {join_clause}, and the longest so far is {max_length}.",
        arr=arr_frame(i), q=q_frame()
    )
    if queue:
        queue.pop(0)
        rec.step(
            f"Minute {i + 1}: one patron is served, leaving the line at {len(queue)}.",
            arr=arr_frame(i), q=q_frame()
        )
    else:
        rec.step(
            f"Minute {i + 1}: no one is waiting, so no one is served.",
            arr=arr_frame(i), q=q_frame()
        )

rec.step(f"After minute {n}: the longest the line ever reached was {max_length}.", arr=arr_frame(n), q=q_frame())
rec.output(f"{max_length}\n")
