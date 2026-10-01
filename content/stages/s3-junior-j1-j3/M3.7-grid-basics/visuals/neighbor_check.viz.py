import vizrec as vz

rec = vz.Recorder()
r, c = map(int, rec.readline().split())
for _ in range(r):
    rec.readline()
qr, qc = map(int, rec.readline().split())

vr, vc = r + 2, c + 2
state = [["none"] * vc for _ in range(vr)]
values = [[None] * vc for _ in range(vr)]
for row in range(vr):
    for col in range(vc):
        if row in (0, vr - 1) or col in (0, vc - 1):
            state[row][col] = "invalid"
            values[row][col] = "x"
state[qr + 1][qc + 1] = "current"
count = 0
values[qr + 1][qc + 1] = str(count)


def frame():
    return vz.grid(state, values=values, indices=False)


rec.step(
    f"Row {qr}, column {qc} is current. The ring around the board is not part of it: it "
    "stands for every position the bounds check would reject. Check the four directions.",
    grid=frame(),
)

names = {(-1, 0): "up", (1, 0): "down", (0, -1): "left", (0, 1): "right"}
for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
    nr, nc = qr + dr, qc + dc
    direction = names[(dr, dc)]
    if 0 <= nr < r and 0 <= nc < c:
        count += 1
        state[nr + 1][nc + 1] = "compare"
        values[nr + 1][nc + 1] = "in"
        values[qr + 1][qc + 1] = str(count)
        rec.step(
            f"{direction.capitalize()}: row {nr}, column {nc} satisfies "
            f"0 <= {nr} < {r} and 0 <= {nc} < {c}. It counts as a neighbor ({count} so far).",
            grid=frame(),
        )
    else:
        rec.step(
            f"{direction.capitalize()}: row {nr}, column {nc} falls in the ring. It fails "
            f"0 <= {nr} < {r} and 0 <= {nc} < {c}, so it is not a neighbor.",
            grid=frame(),
        )

rec.step(
    f"All four directions are checked. Row {qr}, column {qc} has {count} neighbors inside the "
    "grid.",
    grid=frame(),
)
rec.output(f"{count}\n")
