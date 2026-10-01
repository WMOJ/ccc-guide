import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
s = data[0]
n = len(s)

is_pal = [[None] * n for _ in range(n)]


def table_frame(cur=None, arrow=None):
    cells = []
    states = []
    for i in range(n):
        row_cells = []
        row_states = []
        for j in range(n):
            if i > j:
                row_cells.append(None)
                row_states.append("none")
            elif is_pal[i][j] is None:
                row_cells.append(None)
                row_states.append("none")
            elif is_pal[i][j]:
                row_cells.append(j - i + 1)
                row_states.append("done")
            else:
                row_cells.append("-")
                row_states.append("invalid")
        cells.append(row_cells)
        states.append(row_states)
    if cur is not None:
        states[cur[0]][cur[1]] = "current"
    arrows = [arrow] if arrow else None
    return vz.table(
        cells,
        states=states,
        row_heads=list(s),
        col_heads=list(s),
        row_title="l",
        col_title="r",
        arrows=arrows,
    )


for i in range(n):
    is_pal[i][i] = True
rec.step(
    "Every single character is a palindrome: is_pal[i][i] is true for every i, the length-1 base case.",
    table=table_frame(),
)

count = n
for length in range(2, n + 1):
    for left in range(n - length + 1):
        right = left + length - 1
        if length == 2:
            result = s[left] == s[right]
            is_pal[left][right] = result
            verdict = "match" if result else "differ"
            rec.step(
                f"length {length}: is_pal[{left}][{right}] checks only '{s[left]}' vs '{s[right]}' "
                f"({verdict}): {'true' if result else 'false'}.",
                table=table_frame((left, right)),
            )
        else:
            inner = is_pal[left + 1][right - 1]
            result = s[left] == s[right] and inner
            is_pal[left][right] = result
            ends = "match" if s[left] == s[right] else "differ"
            rec.step(
                f"length {length}: is_pal[{left}][{right}] needs ends to {ends} and "
                f"is_pal[{left + 1}][{right - 1}] ({'true' if inner else 'false'}): "
                f"{'true' if result else 'false'}.",
                table=table_frame((left, right), ((left + 1, right - 1), (left, right))),
            )
        if result:
            count += 1

lines = [
    f"length {length}: '{s[left:left + length]}'"
    for length in range(2, n + 1)
    for left in range(n - length + 1)
    if is_pal[left][left + length - 1]
]
lines.append(f"total: {count}")
rec.output("\n".join(lines) + "\n")
