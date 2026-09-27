from collections import deque

rows, cols = map(int, input().split())
grid = [input() for _ in range(rows)]

seen = [[False] * cols for _ in range(rows)]
sizes = []
for r in range(rows):
    for c in range(cols):
        if grid[r][c] != "L" or seen[r][c]:
            continue
        # (r, c) is land that no earlier search reached: a new region starts here.
        seen[r][c] = True
        queue = deque([(r, c)])
        size = 0
        while queue:
            cr, cc = queue.popleft()
            size += 1
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = cr + dr, cc + dc
                if (
                    0 <= nr < rows
                    and 0 <= nc < cols
                    and grid[nr][nc] == "L"
                    and not seen[nr][nc]
                ):
                    seen[nr][nc] = True
                    queue.append((nr, nc))
        sizes.append(size)

print(len(sizes))
print(*sorted(sizes))
