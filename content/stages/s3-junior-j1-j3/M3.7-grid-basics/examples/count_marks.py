r, c = map(int, input().split())
grid = []
for i in range(r):
    row = input()
    grid.append(row)

count = 0
for row in range(r):
    for col in range(c):
        if grid[row][col] == '#':
            count += 1

print(count)
