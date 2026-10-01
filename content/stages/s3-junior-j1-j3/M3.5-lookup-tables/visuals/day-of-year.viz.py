import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
pos = 0
q = int(data[pos])
pos += 1
queries = []
for _ in range(q):
    month = int(data[pos])
    day = int(data[pos + 1])
    pos += 2
    queries.append((month, day))

days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
days_before = [0] * 13
WINDOW = 6


def window(k):
    lo = max(0, k - WINDOW + 1)
    return lo, k


def month_frame(m):
    lo, hi = window(m)
    vals = days_in_month[lo:hi + 1]
    states = ["current" if lo + i == m else "none" for i in range(len(vals))]
    return vz.array(vals, states=states, index_base=lo)


def before_frame(m, built):
    lo, hi = window(m)
    vals = days_before[lo:hi + 1]
    states = []
    for i in range(len(vals)):
        idx = lo + i
        if idx == m:
            states.append("current")
        elif idx <= built:
            states.append("done")
        else:
            states.append("none")
    return vz.array(vals, states=states, index_base=lo)


rec.step(
    "days_before[0] is 0: no days come before month 1.",
    month=month_frame(0),
    before=before_frame(0, 0),
)

for m in range(1, 13):
    days_before[m] = days_before[m - 1] + days_in_month[m]
    rec.step(
        f"days_before[{m}] is days_before[{m - 1}] plus "
        f"days_in_month[{m}]: {days_before[m - 1]} + "
        f"{days_in_month[m]} = {days_before[m]}.",
        month=month_frame(m),
        before=before_frame(m, m),
    )

for month, day in queries:
    total = days_before[month - 1] + day
    rec.step(
        f"Day {day} of month {month}: days_before[{month - 1}] "
        f"is {days_before[month - 1]}, plus {day} is {total}, "
        f"the day of the year.",
        month=month_frame(month),
        before=before_frame(month - 1, 12),
    )

rec.output("\n".join(str(days_before[m - 1] + d) for m, d in queries) + "\n")
