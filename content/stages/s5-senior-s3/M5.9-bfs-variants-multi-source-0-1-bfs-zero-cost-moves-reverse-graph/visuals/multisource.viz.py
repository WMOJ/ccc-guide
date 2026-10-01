from collections import deque

import vizrec as vz

rec = vz.Recorder()
rows, cols = map(int, rec.readline().split())
grid = [rec.readline() for _ in range(rows)]

dist = [[-1] * cols for _ in range(rows)]
state = [["#" if grid[r][c] == "#" else "." for c in range(cols)] for r in range(rows)]
sources = []
for r in range(rows):
    for c in range(cols):
        if grid[r][c] == "D":
            sources.append((r, c))


def name(cell):
    return f"{cell[0]},{cell[1]}"


def frame(queue):
    values = []
    for r in range(rows):
        row = []
        for c in range(cols):
            row.append(dist[r][c] if dist[r][c] >= 0 else None)
        values.append(row)
    items = [(name(cell), name(cell), "frontier") for cell in queue]
    return {
        "grid": vz.grid(["".join(row) for row in state], values=values),
        "queue": vz.queue(items),
    }


queue = deque()
for r, c in sources:
    dist[r][c] = 0
    state[r][c] = "q"
    queue.append((r, c))

label = " and ".join(name(s) for s in sources) if len(sources) > 1 else name(sources[0])
rec.step(
    f"Every source starts in the queue at distance 0: {label}. Plain BFS pushes one start "
    "cell; multi-source BFS pushes all of them before the search takes its first step.",
    **frame(queue)
)

while queue:
    r, c = queue.popleft()
    state[r][c] = "c"
    added = []
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#" and dist[nr][nc] == -1:
            dist[nr][nc] = dist[r][c] + 1
            queue.append((nr, nc))
            state[nr][nc] = "q"
            added.append(name((nr, nc)))
    if added:
        joined = " and ".join(added) if len(added) <= 2 else ", ".join(added[:-1]) + " and " + added[-1]
        what = f"{joined} join{'s' if len(added) == 1 else ''} the queue at distance {dist[r][c] + 1}."
    else:
        what = "It has no open neighbor still unseen, so nothing joins the queue."
    rec.step(
        f"Cell {name((r, c))} leaves the queue at distance {dist[r][c]}, its distance to "
        f"the nearest source. {what}",
        **frame(queue)
    )
    state[r][c] = "d"

out_lines = []
for r in range(rows):
    out_lines.append(" ".join(str(dist[r][c]) for c in range(cols)))
rec.step(
    "The queue is empty. Every open cell now holds its distance to the nearest source; a "
    "cell no source could reach, cut off by walls, is never assigned one.",
    **frame(queue)
)
rec.output("\n".join(out_lines) + "\n")
