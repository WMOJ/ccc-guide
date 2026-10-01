n = int(input())
visited = set()
for _ in range(n):
    row, col = map(int, input().split())
    if (row, col) in visited:
        print("again", row, col)
    else:
        visited.add((row, col))
print(len(visited))
