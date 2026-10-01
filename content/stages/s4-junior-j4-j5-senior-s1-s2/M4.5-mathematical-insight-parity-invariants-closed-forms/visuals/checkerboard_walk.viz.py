import vizrec as vz

ROWS = 6
COLS = 6


def colors():
    return [[(r + c) % 2 for c in range(COLS)] for r in range(ROWS)]


def board(cur_r, cur_c, end_r, end_c):
    states = [["none"] * COLS for _ in range(ROWS)]
    for r in range(ROWS):
        for c in range(COLS):
            if (r + c) % 2 == 1:
                states[r][c] = "wall"
    states[end_r][end_c] = "compare"
    states[cur_r][cur_c] = "current"
    rows = ["".join(vz.code(s) for s in row) for row in states]
    return vz.grid(rows, values=colors())


def moves_word(n):
    return "move" if n == 1 else "moves"


def shortest_path(start_r, start_c, end_r, end_c):
    """One step per row of difference, then one step per column of
    difference: a valid path of exactly distance grid moves."""
    path = []
    r, c = start_r, start_c
    row_step = 1 if end_r >= start_r else -1
    while r != end_r:
        r += row_step
        path.append((r, c))
    col_step = 1 if end_c >= start_c else -1
    while c != end_c:
        c += col_step
        path.append((r, c))
    return path


rec = vz.Recorder()
data = rec.stdin.split()
start_r, start_c = int(data[0]), int(data[1])
end_r, end_c = int(data[2]), int(data[3])
moves = int(data[4])

distance = abs(end_r - start_r) + abs(end_c - start_c)
surplus = moves - distance

rec.step(
    f"The shortest path from ({start_r}, {start_c}) to ({end_r}, {end_c}) takes {distance} moves. "
    f"There are {moves} moves to spend.",
    board=board(start_r, start_c, end_r, end_c),
)

if surplus < 0:
    rec.step(
        f"{moves} {moves_word(moves)} is fewer than the {distance} needed just to get there, so "
        "the answer is no, decided before taking a single step.",
        board=board(start_r, start_c, end_r, end_c),
    )
    rec.output("no\n")
else:
    path = shortest_path(start_r, start_c, end_r, end_c)
    cur_r, cur_c = start_r, start_c
    left = moves
    for step, (nr, nc) in enumerate(path, start=1):
        cur_r, cur_c = nr, nc
        left -= 1
        rec.step(
            f"Move {step}: step to ({cur_r}, {cur_c}), color {(cur_r + cur_c) % 2}. "
            f"{left} {moves_word(left)} left.",
            board=board(cur_r, cur_c, end_r, end_c),
        )

    # A neighbor to bounce against: one step in whichever direction stays
    # on the board.
    neighbor_r, neighbor_c = end_r, end_c
    if end_c > 0:
        neighbor_c = end_c - 1
    else:
        neighbor_c = end_c + 1

    pairs = surplus // 2
    for _ in range(pairs):
        cur_r, cur_c = neighbor_r, neighbor_c
        left -= 1
        rec.step(
            f"Spend a pair of spare moves: step out to ({cur_r}, {cur_c}), color "
            f"{(cur_r + cur_c) % 2}. {left} {moves_word(left)} left.",
            board=board(cur_r, cur_c, end_r, end_c),
        )
        cur_r, cur_c = end_r, end_c
        left -= 1
        rec.step(
            f"Step back to the target ({cur_r}, {cur_c}), color {(cur_r + cur_c) % 2}. "
            f"{left} {moves_word(left)} left.",
            board=board(cur_r, cur_c, end_r, end_c),
        )

    if surplus % 2 == 1:
        cur_r, cur_c = neighbor_r, neighbor_c
        left -= 1
        rec.step(
            f"One spare move is left over: step out to ({cur_r}, {cur_c}), color "
            f"{(cur_r + cur_c) % 2}, with no move left to step back. The token lands beside "
            "the target, not on it, so the answer is no.",
            board=board(cur_r, cur_c, end_r, end_c),
        )
        rec.output("no\n")
    else:
        rec.step(
            f"Every spare move was spent in a pair, so the token ends on the target "
            f"({cur_r}, {cur_c}) with 0 moves left. The answer is yes.",
            board=board(cur_r, cur_c, end_r, end_c),
        )
        rec.output("yes\n")
