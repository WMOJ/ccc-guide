import vizrec as vz

rec = vz.Recorder()
rolls = rec.stdin.split()
n = len(rolls)

freq = [0] * 7


def rolls_frame(i):
    states = ["done" if j < i else "none" for j in range(n)]
    if i < n:
        states[i] = "current"
    return vz.array(rolls, states=states, pointers={"i": i} if i < n else None)


def freq_frame(current=None, best=None):
    states = ["none"] * 7
    if best is not None:
        states[best] = "done"
    if current is not None:
        states[current] = "current"
    pointers = [("best", best, "below")] if best is not None else None
    return vz.array(freq, states=states, pointers=pointers, index_base=0)


for i, roll in enumerate(rolls):
    face = int(roll)
    freq[face] += 1
    rec.step(
        f"Roll {roll} at position {i}: freq[{face}] becomes {freq[face]}.",
        rolls=rolls_frame(i),
        freq=freq_frame(current=face),
    )

best = 1
rec.step(
    "Counting is done. A second loop scans faces 2 to 6 for the largest count. "
    f"It starts with best = 1, so freq[1] = {freq[1]} is the count to beat.",
    rolls=rolls_frame(n),
    freq=freq_frame(best=best),
)

for face in range(2, 7):
    if freq[face] > freq[best]:
        old = best
        best = face
        rec.step(
            f"freq[{face}] is {freq[face]}, more than freq[{old}] = {freq[old]}, "
            f"so best becomes {face}.",
            rolls=rolls_frame(n),
            freq=freq_frame(current=face, best=best),
        )
    else:
        rec.step(
            f"freq[{face}] is {freq[face]}, not more than freq[{best}] = {freq[best]}, "
            f"so best stays {best}.",
            rolls=rolls_frame(n),
            freq=freq_frame(current=face, best=best),
        )

times = "time" if freq[best] == 1 else "times"
rec.step(
    f"The scan ends with best = {best}: face {best} came up {freq[best]} {times}, "
    "the most of any face.",
    rolls=rolls_frame(n),
    freq=freq_frame(best=best),
)

rec.output(f"{best}: {freq[best]}\n")
