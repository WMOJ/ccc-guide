import vizrec as vz


def plural(word, n):
    return word if n == 1 else word + "s"


def checkerboard_row(r, m):
    row = []
    for c in range(m):
        if (r + c) % 2 == 0:
            row.append("a")
        else:
            row.append("b")
    return row


def frame(letters, filled, state):
    cells = []
    values = []
    for i, row in enumerate(letters):
        if i < filled:
            cells.append(state * len(row))
            values.append(row)
        else:
            cells.append("_" * len(row))
            values.append([None] * len(row))
    return vz.grid(cells, values=values)


rec = vz.Recorder()
data = rec.stdin.split()
n = int(data[0])
m = int(data[1])

letters = []
for r in range(n):
    letters.append(checkerboard_row(r, m))

if n % 2 != 0 or m % 2 != 0:
    row_vowels = m // 2
    total_vowels = n * row_vowels
    rec.step(
        f"Try splitting every row evenly: {row_vowels} {plural('vowel', row_vowels)} "
        f"and {row_vowels} {plural('consonant', row_vowels)} each, {total_vowels} "
        f"{plural('vowel', total_vowels)} across all {n} rows.",
        board=frame(letters, n, "c"),
    )
    quotient = total_vowels / m
    rec.step(
        f"Spread evenly over {m} columns, each needs {total_vowels} / {m} = "
        f"{quotient:g} vowels, not a whole number. Impossible.",
        board=frame(letters, n, "x"),
    )
    rec.output("Impossible\n")
else:
    for r in range(1, n + 1):
        half = m // 2
        rec.step(
            f"Row {r - 1}: (row + col) % 2 decides vowel or consonant, "
            f"{half} {plural('vowel', half)} and {half} {plural('consonant', half)}.",
            board=frame(letters, r, "d"),
        )
    lines = []
    for row in letters:
        lines.append("".join(row))
    rec.output("\n".join(lines) + "\n")

rec.done()
