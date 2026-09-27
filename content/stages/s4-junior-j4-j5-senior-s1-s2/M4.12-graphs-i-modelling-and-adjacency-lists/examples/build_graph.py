n, m = map(int, input().split())
graph = {i: [] for i in range(n)}

for _ in range(m):
    a, b = map(int, input().split())
    graph[a].append(b)
    graph[b].append(a)

for vertex in range(n):
    print(f"{vertex}: {graph[vertex]}")
