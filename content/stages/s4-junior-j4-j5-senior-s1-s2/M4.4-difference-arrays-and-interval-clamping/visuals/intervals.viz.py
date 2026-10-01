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

shown = []
ordinals = ["first", "second", "third", "fourth", "fifth", "sixth"]
for row, (l, r, val) in enumerate(updates):
    shown.append((l, r, f"+{val}", "current" if row == len(updates) - 1 else "done", row))
    word = ordinals[row] if row < len(ordinals) else f"update {row + 1}"
    rec.step(
        f"The {word} range runs from index {l} through index {r} and adds {val}. Drawing it on "
        f"row {row} keeps it clear of the rows above.",
        line=vz.line(0, n, tick=1, intervals=shown),
    )
    shown[-1] = (l, r, f"+{val}", "done", row)

rec.step(
    f"All {m} ranges sit on the line together now. Any index covered by more than one row picks "
    "up every one of those additions once diff is rebuilt.",
    line=vz.line(0, n, tick=1, intervals=shown),
)

diff = [0] * (n + 1)
for l, r, val in updates:
    diff[l] += val
    diff[r + 1] -= val
built = []
current = 0
for i in range(n):
    current += diff[i]
    built.append(current)

rec.output(" ".join(map(str, built)) + "\n")
