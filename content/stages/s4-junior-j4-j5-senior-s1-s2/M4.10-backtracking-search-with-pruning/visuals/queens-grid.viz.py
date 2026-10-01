import vizrec as vz

rec = vz.Recorder()
n = int(rec.readline())

board = [["."] * n for _ in range(n)]
solutions = 0
noted_empty_start = False


def frame():
    cells = ["".join(row) for row in board]
    values = [[("Q" if board[r][c] == "p" else None) for c in range(n)] for r in range(n)]
    return vz.grid(cells, values=values)


def place(row, columns, diagonals_down, diagonals_up):
    global solutions, noted_empty_start
    if row == n:
        solutions += 1
        rec.step(
            f"Every row holds a queen and none attacks another: solution {solutions} is complete.",
            grid=frame(),
        )
        return
    tried_and_skipped = []
    for col in range(n):
        if col in columns or (row - col) in diagonals_down or (row + col) in diagonals_up:
            tried_and_skipped.append(col)
            continue
        board[row][col] = "p"
        columns.add(col)
        diagonals_down.add(row - col)
        diagonals_up.add(row + col)
        if tried_and_skipped:
            cols_text = ", ".join(str(c) for c in tried_and_skipped)
            skip_note = f" Column{'s' if len(tried_and_skipped) > 1 else ''} {cols_text} in this row are already attacked."
        else:
            skip_note = ""
        start_note = ""
        if not noted_empty_start:
            start_note = " The board starts empty."
            noted_empty_start = True
        rec.step(
            f"Row {row}: place a queen at column {col}.{start_note}{skip_note}",
            grid=frame(),
        )
        place(row + 1, columns, diagonals_down, diagonals_up)
        board[row][col] = "."
        columns.remove(col)
        diagonals_down.remove(row - col)
        diagonals_up.remove(row + col)
        rec.step(
            f"Backtrack: the queen at row {row}, column {col} is removed so the next column can be tried.",
            grid=frame(),
        )
    if row == 0:
        rec.step(
            "Every column has been tried for row 0: the search of this board size is complete.",
            grid=frame(),
        )


place(0, set(), set(), set())
rec.output(f"{solutions}\n")
