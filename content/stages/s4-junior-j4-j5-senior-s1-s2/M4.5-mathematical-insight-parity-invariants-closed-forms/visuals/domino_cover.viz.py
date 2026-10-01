import vizrec as vz

rec = vz.Recorder()
data = rec.stdin.split()
n = int(data[0])
cut = int(data[1])

removed = set()
if cut:
    removed = {(0, 0), (n - 1, n - 1)}

covered = set()
current = set()
left_over = set()


def frame():
    rows = []
    for r in range(n):
        row = []
        for c in range(n):
            if (r, c) in removed:
                row.append("invalid")
            elif (r, c) in current:
                row.append("current")
            elif (r, c) in covered:
                row.append("done")
            elif (r, c) in left_over:
                row.append("compare")
            else:
                row.append("none")
        rows.append(row)
    values = [[(r + c) % 2 if (r, c) not in removed else None for c in range(n)] for r in range(n)]
    return vz.grid(rows, values=values)


def count_values(cells):
    zeros = sum(1 for (r, c) in cells if (r + c) % 2 == 0)
    return zeros, len(cells) - zeros


squares = [(r, c) for r in range(n) for c in range(n) if (r, c) not in removed]
zeros, ones = count_values(squares)
if cut:
    intro = (
        f"A {n} by {n} board with corners (0, 0) and ({n - 1}, {n - 1}) removed. Each square shows "
        f"(row + col) % 2. {len(squares)} squares remain: {zeros} show 0 and {ones} show 1."
    )
else:
    intro = (
        f"A {n} by {n} board, nothing removed. Each square shows (row + col) % 2. "
        f"{len(squares)} squares: {zeros} show 0 and {ones} show 1."
    )
rec.step(intro, grid=frame())

# Greedy placement, scanning rows: prefer a domino to the right, else one below.
dominoes = []
taken = set()
for r in range(n):
    for c in range(n):
        if (r, c) in removed or (r, c) in taken:
            continue
        for dr, dc in ((0, 1), (1, 0)):
            other = (r + dr, c + dc)
            if other[0] < n and other[1] < n and other not in removed and other not in taken:
                dominoes.append(((r, c), other))
                taken.add((r, c))
                taken.add(other)
                break
        else:
            left_over.add((r, c))

for k, (first, second) in enumerate(dominoes, start=1):
    current.clear()
    current.update((first, second))
    v1 = (first[0] + first[1]) % 2
    v2 = (second[0] + second[1]) % 2
    rec.step(
        f"Domino {k} covers {first} and {second}, which show {v1} and {v2}: one of each. "
        f"So far {k} square{'s' if k > 1 else ''} showing 0 and {k} showing 1 are covered.",
        grid=frame(),
    )
    covered.update((first, second))
    current.clear()

left_zero, left_one = count_values(left_over)
if not left_over:
    rec.step(
        f"All {len(squares)} squares are covered by {len(dominoes)} dominoes: "
        f"{zeros} squares showing 0 and {ones} showing 1, matched one to one.",
        grid=frame(),
    )
else:
    names = " and ".join(str(s) for s in sorted(left_over))
    rec.step(
        f"No domino fits any more, leaving {names} with no partner. Every domino covers one 0 and "
        f"one 1, but this board has {zeros} zeros and {ones} ones, so the surplus squares cannot be "
        "covered by any placement, not only this one.",
        grid=frame(),
    )

rec.output(f"{zeros} {ones}\n" + ("balanced\n" if zeros == ones else "no tiling\n"))
