import random

import vizrec as vz

rec = vz.Recorder()
seed = int(rec.readline())


def new_case():
    n = random.randint(1, 3)
    return [random.randint(-3, 3) for _ in range(n)]


def brute(values):
    n = len(values)
    return max(
        sum(values[i:j + 1])
        for i in range(n)
        for j in range(i, n)
    )


def fast(values):
    n = len(values)
    total = 0
    prefix = [0]
    for v in values:
        total += v
        prefix.append(total)
    low = prefix[0]
    best = values[0]
    for j in range(n):
        end = prefix[j + 1]
        cand = end - low
        best = max(best, cand)
        low = min(low, end)
    return best


SHOWN = 6
rows = []
states = []


def frame():
    return vz.table(
        cells=[list(r[:3]) for r in rows],
        states=list(states),
        row_heads=[f"{k} {r[3]}" for k, r in enumerate(rows, start=1)],
        col_heads=["input", "brute", "fast"],
        row_title="trial",
    )


random.seed(seed)
mismatch = None
for trial in range(1, 1001):
    values = new_case()
    want = brute(values)
    got = fast(values)
    if want != got:
        mismatch = trial
        break
    if trial <= SHOWN:
        shown = " ".join(str(v) for v in values)
        rows.append((shown, want, got, "ok"))
        states.append("ddd")
        rec.step(
            f"Trial {trial}: the input is {values}. The brute force says {want} and the fixed "
            f"function says {got}. They agree.",
            table=frame(),
        )
    if trial == SHOWN:
        rec.skip(
            "The loop keeps going through trial 1000, and every trial agrees.",
            1000 - SHOWN,
            table=frame(),
        )

if mismatch is None:
    rec.step(
        "After 1000 trials the two functions never disagreed, so the loop prints no mismatch.",
        table=frame(),
    )
    rec.output("no mismatch\n")
else:
    rec.step(f"Trial {mismatch} differs: the fix did not cure this input.", table=frame())
    rec.output(f"trial {mismatch}\n")
