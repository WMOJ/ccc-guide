def find(parent, x):
    """Find root with path halving."""
    while parent[x] != x:
        parent[x] = parent[parent[x]]  # Skip one level
        x = parent[x]
    return x


def union(parent, a, b):
    """Merge the groups containing a and b."""
    root_a = find(parent, a)
    root_b = find(parent, b)
    if root_a != root_b:
        parent[root_a] = root_b


# Build a chain by naive unions: 0 <- 1 <- 2 <- 3 <- 4
parent = list(range(5))
for i in range(4):
    union(parent, i, i + 1)

print("Parent array after naive unions:", parent)

# First find on 0: takes 4 steps without halving
print("find(0) with path halving:", find(parent, 0))

# After halving, the path is shorter
print("Parent array after find:", parent)
