from math import isqrt

import vizrec as vz

rec = vz.Recorder()
limit = int(rec.readline())

distinct = []
for n in range(1, limit + 1):
    values = set()
    for d in range(1, n + 1):
        values.add(n // d)
    distinct.append(len(values))

ticks = [0, limit // 2, limit]
xs = (0, limit, "n", ticks)
ys = (0, limit, "count", ticks)
terms = [(n, n) for n in range(1, limit + 1)]
counts = [(n, distinct[n - 1]) for n in range(1, limit + 1)]
bound = [(n, 2 * n ** 0.5) for n in range(1, limit + 1)]
last = distinct[-1]

rec.step(
    f"For each n from 1 to {limit} there are n terms `n // d`: that is the straight line. The "
    f"lower curve counts how many different values those terms take. At n = {limit} there are "
    f"{last} values among the {limit} terms.",
    p=vz.plot(xs, ys, [("n", "terms n", terms, 1), ("k", "distinct", counts, 0)],
              markers=[(limit, last, f"{last} values", "current")])
)
rec.step(
    f"The count follows 2 * sqrt(n) closely; with a whole-number root, 2 * isqrt({limit}) is "
    f"{2 * isqrt(limit)}. So the number of blocks grows like sqrt(n), not like n.",
    p=vz.plot(xs, ys, [("n", "terms n", terms, 1), ("k", "distinct", counts, 0),
                       ("s", "2 * sqrt(n)", bound, 2)],
              markers=[(limit, last, f"{last} values", "current")])
)
rec.output(f"{last}\n{2 * isqrt(limit)}\n")
