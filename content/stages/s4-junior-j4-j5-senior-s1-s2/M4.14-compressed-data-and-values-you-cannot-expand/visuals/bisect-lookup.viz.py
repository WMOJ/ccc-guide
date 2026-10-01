import vizrec as vz
from bisect import bisect_right

rec = vz.Recorder()
data = rec.stdin.split()
idx = 0
n = int(data[idx])
idx += 1
days = sorted(map(int, data[idx:idx + n]))
idx += n


def days_frame(found=None):
    values = days if days else ["-"]
    states = ["none"] * len(values)
    pointers = None
    if found is not None:
        pointers = [("found", found)]
    return vz.array(values, states=states, pointers=pointers, indices=True)


rec.step(
    f"{n} distinct days were recorded. bisect_right finds where a query day would sit among "
    "them, even one that was never recorded.",
    days=days_frame(),
)

q = int(data[idx])
idx += 1
counts = []
for _ in range(q):
    query_day = int(data[idx])
    idx += 1
    count = bisect_right(days, query_day)
    if count == 0:
        where = f"before every recorded day"
    elif count == n:
        where = f"after every recorded day"
    else:
        where = f"between day {days[count - 1]} and day {days[count]}"
    rec.step(
        f"Day {query_day} sits {where}. bisect_right returns {count}: that many recorded days "
        f"are on or before day {query_day}.",
        days=days_frame(found=count),
    )
    counts.append(count)

rec.output("\n".join(map(str, counts)) + "\n")
