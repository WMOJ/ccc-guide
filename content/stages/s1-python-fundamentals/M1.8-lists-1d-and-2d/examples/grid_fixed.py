rows = int(input())
cols = int(input())
grid = [[0] * cols for _ in range(rows)]
grid[0][1] = 5
print(grid)
