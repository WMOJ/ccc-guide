import vizrec as vz

rec = vz.Recorder()
n, target = map(int, rec.readline().split())
tickets = list(map(int, rec.readline().split()))

cells = [["-" for _ in range(n)] for _ in range(n)]
cell_states = {}
count = 0


def frame(current=None):
    states = dict(cell_states)
    if current is not None:
        states[current] = "current"
    return vz.table(
        cells, states=states, row_heads=tickets, col_heads=tickets,
        row_title="i", col_title="j"
    )


rec.step(
    f"Every pair (i, j) with i before j will be checked against the target, {target}.",
    t=frame()
)
for i in range(n):
    for j in range(i + 1, n):
        total = tickets[i] + tickets[j]
        cells[i][j] = total
        if total == target:
            count += 1
            cell_states[(i, j)] = "path"
            rec.step(
                f"The {tickets[i]}-dollar ticket plus the {tickets[j]}-dollar ticket is "
                f"{total}, which matches the target. Matches so far: {count}.",
                t=frame((i, j))
            )
        else:
            cell_states[(i, j)] = "done"
            rec.step(
                f"The {tickets[i]}-dollar ticket plus the {tickets[j]}-dollar ticket is "
                f"{total}, which does not match the target.",
                t=frame((i, j))
            )

pair_word = "pair" if count == 1 else "pairs"
rec.step(f"Every pair has been checked. {count} {pair_word} matched the target.", t=frame())
rec.output(f"{count}\n")
