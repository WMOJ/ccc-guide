from collections import deque

import vizrec as vz

rec = vz.Recorder()
n, k = (int(x) for x in rec.readline().split())
scores = [int(x) for x in rec.readline().split()]

dp = [None] * n


def stones(dq, marks=None, new=None):
    marks = marks or {}
    items = []
    for j in dq:
        s = marks.get(j)
        if j == new:
            s = "current"
        items.append((str(j), f"{j}: {dp[j]}", s))
    return vz.struct("deque", items)


def window_range(i):
    lo = max(0, i - k)
    return [(lo, i - 1, "window")]


dp[0] = scores[0]
dq = deque([0])
rec.step(
    f"Stone 0 is the start, so `dp[0]` = {scores[0]}. The deque holds stone 0, written as "
    f"`index: dp`. A jump can cover at most {k} {'stone' if k == 1 else 'stones'}.",
    a=vz.array([dp[0]] + ["?"] * (n - 1), pointers=[("i", 0)], indices=True), d=stones(dq),
)

for i in range(1, n):
    expired = []
    while dq[0] < i - k:
        expired.append(dq.popleft())
    if expired:
        names = ", ".join(map(str, expired))
        reach = f"stone {i - 1}" if k == 1 else f"stones {i - k} to {i - 1}"
        rec.step(
            f"Stone {i} can only be reached from {reach}. Stone {names} is "
            f"older than that, so it leaves the front of the deque.",
            a=vz.array(["?" if v is None else v for v in dp], pointers=[("i", i)],
                       ranges=window_range(i), indices=True),
            d=stones(expired + list(dq), marks={e: "invalid" for e in expired}),
        )
    front = dq[0]
    dp[i] = scores[i] + dp[front]
    rec.step(
        f"The front of the deque is stone {front} with `dp[{front}]` = {dp[front]}, the best in "
        f"the window. Stone {i} scores {scores[i]}, so `dp[{i}]` = {scores[i]} + {dp[front]} "
        f"= {dp[i]}.",
        a=vz.array(["?" if v is None else v for v in dp], states={front: "current"},
                   pointers=[("i", i)], ranges=window_range(i), indices=True),
        d=stones(dq, marks={front: "compare"}),
    )
    popped = []
    while dq and dp[dq[-1]] <= dp[i]:
        popped.append(dq.pop())
    dq.append(i)
    vals = ["?" if v is None else v for v in dp]
    if popped:
        popped.reverse()
        names = ", ".join(map(str, popped))
        one = len(popped) == 1
        entries = "entry" if one else "entries"
        what = "stone" if one else "stones"
        they = "it" if one else "they"
        They = "It" if one else "They"
        rec.step(
            f"`dp[{i}]` = {dp[i]} is at least as large as the back {entries} for {what} {names}, "
            f"and stone {i} is newer, so {they} can never be the best predecessor again. "
            f"{They} leave{'s' if len(popped) == 1 else ''} the back, and stone {i} joins it.",
            a=vz.array(vals, pointers=[("i", i)], indices=True),
            d=stones(popped + list(dq), marks={p: "invalid" for p in popped}, new=i),
        )
    else:
        rec.step(
            f"The back entry is larger than `dp[{i}]` = {dp[i]}, so nothing leaves the back. "
            f"Stone {i} joins it, and the deque stays decreasing.",
            a=vz.array(vals, pointers=[("i", i)], indices=True),
            d=stones(dq, new=i),
        )

rec.step(
    f"Every stone is done. The route must end on stone {n - 1}, so the answer is "
    f"`dp[{n - 1}]` = {dp[n - 1]}.",
    a=vz.array(dp, states={n - 1: "path"}, pointers=[("i", n - 1)], indices=True),
    d=stones(dq),
)
rec.output(f"{dp[n - 1]}\n")
