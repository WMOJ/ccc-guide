import vizrec as vz

rec = vz.Recorder()
values = [int(x) for x in rec.stdin.split()]

d = []
for i, val in enumerate(values):
    if i % 2 == 0:
        d.append(val)
        method, side = "append", "the back"
    else:
        d.insert(0, val)
        method, side = "appendleft", "the front"
    rec.step(
        f"{method}({val}) adds {val} to {side}. Deque is now {d}.",
        deque=vz.struct("deque", [(x, "done") for x in d]),
    )

rec.output(" ".join(str(x) for x in d) + "\n")
