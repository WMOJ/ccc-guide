def find(parent, x):
    """Find root with path halving."""
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def union(parent, size, a, b):
    """Merge groups; attach smaller tree under larger."""
    root_a = find(parent, a)
    root_b = find(parent, b)
    if root_a == root_b:
        return
    if size[root_a] < size[root_b]:
        parent[root_a] = root_b
        size[root_b] += size[root_a]
    else:
        parent[root_b] = root_a
        size[root_a] += size[root_b]


# Track 5 computers
n = 5
parent = list(range(n))
size = [1] * n

# Connect computers with cables
connections = [(0, 1), (1, 2), (3, 4)]
for u, v in connections:
    union(parent, size, u, v)

# Check connectivity
queries = [(0, 2), (0, 3), (1, 3)]
for a, b in queries:
    if find(parent, a) == find(parent, b):
        print("yes")
    else:
        print("no")
