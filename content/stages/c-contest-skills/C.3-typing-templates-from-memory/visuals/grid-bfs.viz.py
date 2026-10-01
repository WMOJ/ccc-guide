from collections import deque

import vizrec as vz

rec = vz.Recorder()
rows, cols = map(int, rec.readline().split())
grid = [rec.readline() for _ in range(rows)]
start = (0, 0)
for r in range(rows):
    for c in range(cols):
        if grid[r][c] == "S":
            start = (r, c)

dist = [[-1] * cols for _ in range(rows)]
dist[start[0]][start[1]] = 0
state = [["#" if grid[r][c] == "#" else "." for c in range(cols)] for r in range(rows)]


def frame():
    values = []
    for r in range(rows):
        row = []
        for c in range(cols):
            if dist[r][c] >= 0:
                row.append(dist[r][c])
            elif grid[r][c] == "#":
                row.append("#")
            else:
                row.append(grid[r][c] if grid[r][c] in "SE" else ".")
        values.append(row)
    return {"grid": vz.grid(["".join(row) for row in state], values=values)}


def name(cell):
    return f"({cell[0]}, {cell[1]})"


queue = deque([start])
state[start[0]][start[1]] = "q"
rec.step(
    "The template starts with dist[start] = 0 and the start cell in the queue. Every other cell still has "
    "distance -1, meaning not reached. Walls are hatched, and the number in a cell is its distance.",
    **frame(),
)
answer = -1
while queue:
    r, c = queue.popleft()
    state[r][c] = "c"
    if grid[r][c] == "E":
        answer = dist[r][c]
        rec.step(
            f"Cell {name((r, c))} comes off the queue and is E, with distance {answer}. The template stores "
            f"{answer} and breaks out of the loop.",
            **frame(),
        )
        break
    parts = []
    for label, dr, dc in (("down", 1, 0), ("up", -1, 0), ("right", 0, 1), ("left", 0, -1)):
        nr, nc = r + dr, c + dc
        if not (0 <= nr < rows and 0 <= nc < cols):
            parts.append(f"{label} is off the grid")
        elif grid[nr][nc] == "#":
            parts.append(f"{label} is a wall")
        elif dist[nr][nc] != -1:
            parts.append(f"{label} already has distance {dist[nr][nc]}")
        else:
            dist[nr][nc] = dist[r][c] + 1
            state[nr][nc] = "q"
            queue.append((nr, nc))
            parts.append(f"{label} is new, so it gets distance {dist[nr][nc]}")
    rec.step(
        f"Cell {name((r, c))} comes off the queue (distance {dist[r][c]}). The four neighbors, in the "
        f"template's order: " + "; ".join(parts) + ".",
        **frame(),
    )
    state[r][c] = "d"
if answer == -1:
    rec.step(
        "The queue is empty and E was never taken out of it, so the loop ends with answer = -1.",
        **frame(),
    )
rec.output(f"{answer}\n")
