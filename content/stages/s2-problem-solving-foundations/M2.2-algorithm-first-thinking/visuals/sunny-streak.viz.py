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
    return vz.array(days, states=states, pointers={"day": i} if i is not None else None)


rec.step(
    f"Before day 1: the current run is 0 and the best run so far is 0.",
    arr=frame(None, set())
)
done = set()
for i, day in enumerate(days):
    if day == 1:
        current_run += 1
        best_run = max(best_run, current_run)
        rec.step(
            f"Day {i + 1} is sunny. The current run grows to {current_run}, and the best "
            f"run so far is {best_run}.",
            arr=frame(i, done)
        )
    else:
        current_run = 0
        rec.step(
            f"Day {i + 1} is not sunny. The current run resets to 0. The best run so far "
            f"stays {best_run}.",
            arr=frame(i, done)
        )
    done.add(i)

rec.step(
    f"After the last day, the best run seen was {best_run}.",
    arr=frame(None, done)
)
rec.output(f"{best_run}\n")
