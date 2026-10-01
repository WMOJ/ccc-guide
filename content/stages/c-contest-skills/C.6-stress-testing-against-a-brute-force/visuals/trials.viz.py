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
    low = prefix[1]
    best = values[0]
    for j in range(n):
        end = prefix[j + 1]
        cand = end - low
        best = max(best, cand)
        low = min(low, end)
    return best


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
failed = None
for trial in range(1, 1001):
    values = new_case()
    want = brute(values)
    got = fast(values)
    shown = " ".join(str(v) for v in values)
    if want == got:
        rows.append((shown, want, got, "ok"))
        states.append("ddd")
        rec.step(
            f"Trial {trial}: the input is {values}. The brute force says {want} and the fast "
            f"function says {got}. They agree, so the loop goes on to the next trial.",
            table=frame(),
        )
    else:
        rows.append((shown, want, got, "DIFF"))
        states.append("xxx")
        rec.step(
            f"Trial {trial}: the input is {values}. The brute force says {want} but the fast "
            f"function says {got}. They differ, so the loop stops and prints this input.",
            table=frame(),
        )
        failed = trial
        break

if failed is None:
    rec.output("no mismatch\n")
else:
    rec.output(f"trial {failed}\ninput {values}\nbrute {want}\nfast {got}\n")
