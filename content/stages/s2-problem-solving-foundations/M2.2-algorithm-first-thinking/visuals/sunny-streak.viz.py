import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())
days = list(map(int, rec.readline().split()))

current_run = 0
best_run = 0


def frame(i, done):
    states = ["done" if j in done else "none" for j in range(n)]
    if i is not None:
        states[i] = "current"
    return vz.array(days, states=states, pointers={"day": i} if i is not None else None, index_base=1)


def counters():
    return vz.table(
        [[current_run, best_run]],
        col_heads=["current_run", "best_run"],
    )


rec.step(
    "Before day 1: the current run is 0 and the best run so far is 0.",
    arr=frame(None, set()),
    counters=counters(),
)
done = set()
for i, day in enumerate(days):
    if day == 1:
        current_run += 1
        best_run = max(best_run, current_run)
        rec.step(
            f"Day {i + 1} is sunny. The current run grows to {current_run}, and the best "
            f"run so far is {best_run}.",
            arr=frame(i, done),
            counters=counters(),
        )
    else:
        current_run = 0
        rec.step(
            f"Day {i + 1} is not sunny. The current run resets to 0. The best run so far "
            f"stays {best_run}.",
            arr=frame(i, done),
            counters=counters(),
        )
    done.add(i)

rec.step(
    f"After the last day, the best run seen was {best_run}.",
    arr=frame(None, done),
    counters=counters(),
)
rec.output(f"{best_run}\n")
