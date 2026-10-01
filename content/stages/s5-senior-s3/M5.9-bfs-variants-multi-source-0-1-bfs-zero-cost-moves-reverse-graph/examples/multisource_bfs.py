import sys
from collections import deque


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return
    rows = int(data[0])
    cols = int(data[1])
    grid = data[2:2 + rows]

    dist = [[-1] * cols for _ in range(rows)]
    queue = deque()
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "D":
                dist[r][c] = 0
                queue.append((r, c))

    while queue:
        r, c = queue.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if (
                0 <= nr < rows
                and 0 <= nc < cols
                and grid[nr][nc] != "#"
                and dist[nr][nc] == -1
            ):
                dist[nr][nc] = dist[r][c] + 1
                queue.append((nr, nc))

    out_lines = []
    for r in range(rows):
        out_lines.append(" ".join(str(dist[r][c]) for c in range(cols)))
    print("\n".join(out_lines))


if __name__ == "__main__":
    main()
