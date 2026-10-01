rows = int(input())
cols = int(input())
grid = [list(map(int, input().split())) for _ in range(rows)]

total = 0
for r in range(rows):
    for c in range(cols):
        total += grid[r][c]
print(total)
