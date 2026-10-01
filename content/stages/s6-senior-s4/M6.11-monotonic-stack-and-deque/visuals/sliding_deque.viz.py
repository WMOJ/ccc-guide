from collections import deque

import vizrec as vz

rec = vz.Recorder()
n, k = (int(x) for x in rec.readline().split())
values = [int(x) for x in rec.readline().split()]

dq = deque()
maximums = []


def array(i, front=None):
    lo = max(0, i - k + 1)
    st = {front: "current"} if front is not None else None
    return vz.array(values, states=st, pointers=[("i", i)], ranges=[(lo, i, "window" if i >= k - 1 else "window so far")],
                    indices=True)


def items(entries, marks=None, new=None):
    marks = marks or {}
    out = []
    for j in entries:
        s = marks.get(j)
        if j == new:
            s = "current"
        out.append((str(j), f"{j}: {values[j]}", s))
    return vz.struct("deque", out)


for i in range(n):
    expired = []
    while dq and dq[0] <= i - k:
        expired.append(dq.popleft())
    if expired:
        rec.step(
            f"The window is now indices {i - k + 1} to {i}. Index {expired[0]} is older than "
            "that, so it leaves the front of the deque.",
            a=array(i), d=items(expired + list(dq), marks={expired[0]: "invalid"}),
        )
    popped = []
    while dq and values[dq[-1]] <= values[i]:
        popped.append(dq.pop())
    dq.append(i)
    if popped:
        popped.reverse()
        one = len(popped) == 1
        if one:
            names = f"index {popped[0]}"
        else:
            names = "indices " + ", ".join(map(str, popped[:-1])) + f" and {popped[-1]}"
        rec.step(
            f"Index {i} holds {values[i]}, at least as large as the back "
            f"{'entry' if one else 'entries'} for {names}. "
            f"{'That index is' if one else 'Those indices are'} older and no larger, so "
            f"{'it' if one else 'they'} can never be a window's maximum again and "
            f"{'leaves' if one else 'leave'} the back. Index {i} joins the deque.",
            a=array(i), d=items(popped + list(dq), marks={p: "invalid" for p in popped}, new=i),
        )
    else:
        tail = f" The back entry is larger than {values[i]}, so nothing leaves the back." if len(dq) > 1 else ""
        rec.step(
            f"Index {i} holds {values[i]} and joins the back of the deque.{tail}",
            a=array(i), d=items(dq, new=i),
        )
    if i >= k - 1:
        f = dq[0]
        maximums.append(values[f])
        rec.step(
            f"The window holds indices {i - k + 1} to {i}. The front of the deque is index {f}, "
            f"so the window's maximum is {values[f]}.",
            a=array(i, front=f), d=items(dq, marks={f: "compare"}),
        )

rec.step(
    f"The last window is done. The maximums, in order, are {' '.join(str(x) for x in maximums)}.",
    a=array(n - 1, front=dq[0]), d=items(dq, marks={dq[0]: "compare"}),
)
rec.output(" ".join(str(x) for x in maximums) + "\n")
