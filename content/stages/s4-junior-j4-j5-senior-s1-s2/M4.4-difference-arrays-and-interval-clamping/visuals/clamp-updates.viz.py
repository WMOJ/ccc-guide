import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
idx = 0
n = int(data[idx])
m = int(data[idx + 1])
idx += 2
updates = []
for _ in range(m):
    l, r, val = int(data[idx]), int(data[idx + 1]), int(data[idx + 2])
    updates.append((l, r, val))
    idx += 3

lo = min(0, min(u[0] for u in updates)) - 1
hi = max(n - 1, max(u[1] for u in updates)) + 1

shown = []
diff = [0] * (n + 1)

for row, (raw_l, raw_r, val) in enumerate(updates):
    shown.append((raw_l, raw_r, "raw", "invalid", row))
    rec.step(
        f"Update {row + 1} asks for [{raw_l}, {raw_r}]. Valid indices run 0 to {n - 1}.",
        line=vz.line(lo, hi, tick=1, intervals=list(shown)),
    )

    l = max(raw_l, 0)
    r = min(raw_r, n - 1)
    shown.pop()
    if l > r:
        shown.append((raw_l, raw_r, "raw", "invalid", row))
        rec.step(
            f"Clamped, l = max({raw_l}, 0) = {l} and r = min({raw_r}, {n - 1}) = {r}. Since l is "
            "past r, nothing of this range is inside the array: skip it.",
            line=vz.line(lo, hi, tick=1, intervals=list(shown)),
        )
    else:
        shown.append((l, r, "clamped", "done", row))
        rec.step(
            f"Clamped to [{l}, {r}]: l = max({raw_l}, 0) = {l}, r = min({raw_r}, {n - 1}) = {r}. "
            f"Apply diff[{l}] += {val}, diff[{r + 1}] -= {val}.",
            line=vz.line(lo, hi, tick=1, intervals=list(shown)),
        )
        diff[l] += val
        diff[r + 1] -= val

arr = []
current = 0
for i in range(n):
    current += diff[i]
    arr.append(current)

rec.step(
    f"Every update is clamped or skipped, and applied to diff. Rebuilding gives {arr}, matching "
    "examples/clamp_updates.py.",
    line=vz.line(lo, hi, tick=1, intervals=list(shown)),
)

rec.output(" ".join(map(str, arr)) + "\n")
