def find(parent, x):
    """Follow parent pointers to the root."""
    while parent[x] != x:
        x = parent[x]
    return x


def union(parent, a, b):
    """Merge the groups containing a and b."""
    root_a = find(parent, a)
    root_b = find(parent, b)
    if root_a != root_b:
        parent[root_a] = root_b


# Start with 5 independent elements
parent = [0, 1, 2, 3, 4]

# Union 0 and 1
union(parent, 0, 1)
print("After union(0, 1):", parent)

# Union 2 and 3
union(parent, 2, 3)
print("After union(2, 3):", parent)

# Check connectivity
print("find(0):", find(parent, 0))
print("find(1):", find(parent, 1))
print("find(2):", find(parent, 2))
print("find(3):", find(parent, 3))
