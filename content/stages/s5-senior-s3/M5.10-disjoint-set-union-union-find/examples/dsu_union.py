def find(parent, x):
    """Find root with path halving."""
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def union(parent, size, a, b):
    """Merge groups containing a and b; attach smaller tree under larger."""
    root_a = find(parent, a)
    root_b = find(parent, b)
    if root_a == root_b:
        return
    # Attach smaller tree under larger
    if size[root_a] < size[root_b]:
        parent[root_a] = root_b
        size[root_b] += size[root_a]
    else:
        parent[root_b] = root_a
        size[root_a] += size[root_b]


# Start with 5 elements
n = 5
parent = list(range(n))
size = [1] * n

# Union 0 and 1
union(parent, size, 0, 1)
print("After union(0, 1):", parent)

# Union 2 and 3
union(parent, size, 2, 3)
print("After union(2, 3):", parent)

# Union the two groups
union(parent, size, 0, 2)
print("After union(0, 2):", parent)
print("Sizes:", size)
