import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
n = int(data[0])
m = int(data[1])
rows = data[2:2 + n]

row_counts = []
for row in rows:
    vowels = 0
    for ch in row:
        if ch == "a":
            vowels += 1
    row_counts.append(vowels)

col_counts = []
for c in range(m):
    vowels = 0
    for row in rows:
        if row[c] == "a":
            vowels += 1
    col_counts.append(vowels)


def table(row_head_count, col_head_count, cur_row, cur_col):
    row_heads = []
    for i in range(n):
        if i < row_head_count:
            row_heads.append(row_counts[i])
        else:
            row_heads.append("?")
    col_heads = []
    for c in range(m):
        if c < col_head_count:
            col_heads.append(col_counts[c])
        else:
            col_heads.append("?")
    states = []
    for i in range(n):
        state_row = []
        for c in range(m):
            if i == cur_row or c == cur_col:
                state_row.append("current")
            elif i < row_head_count or c < col_head_count:
                state_row.append("done")
            else:
                state_row.append("none")
        states.append(state_row)
    cells = [list(row) for row in rows]
    return vz.table(cells, states=states, row_heads=row_heads, col_heads=col_heads)


for i in range(n):
    rec.step(
        f"Row {i}: count the a's, {row_counts[i]} of them.",
        counts=table(i + 1, 0, i, -1),
    )

for c in range(m):
    rec.step(
        f"Column {c}: count the a's, {col_counts[c]} of them.",
        counts=table(n, c + 1, -1, c),
    )

rows_ok = min(row_counts) == max(row_counts)
cols_ok = min(col_counts) == max(col_counts)
halves_ok = True
for count in row_counts:
    if count * 2 != m:
        halves_ok = False

if rows_ok and cols_ok and halves_ok:
    rec.step(
        "Every row count matches, every column count matches, and each row splits "
        "exactly in half: valid.",
        counts=table(n, m, -1, -1),
    )
    rec.output("valid\n")
else:
    reason = "the row counts" if not rows_ok else "the column counts"
    if rows_ok and cols_ok and not halves_ok:
        reason = "a row's vowel count"
    rec.step(
        f"{reason.capitalize()} do not all match: invalid.",
        counts=table(n, m, -1, -1),
    )
    rec.output("invalid\n")

rec.done()
