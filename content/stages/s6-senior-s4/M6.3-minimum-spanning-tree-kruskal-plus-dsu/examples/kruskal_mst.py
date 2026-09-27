import sys


def find(parent, x):
    if parent[x] != x:
        parent[x] = find(parent, parent[x])
    return parent[x]


def union(parent, rank, x, y):
    root_x = find(parent, x)
    root_y = find(parent, y)

    if root_x == root_y:
        return False

    if rank[root_x] < rank[root_y]:
        parent[root_x] = root_y
    elif rank[root_x] > rank[root_y]:
        parent[root_y] = root_x
    else:
        parent[root_y] = root_x
        rank[root_x] += 1

    return True


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    idx = 0
    n = int(input_data[idx])
    m = int(input_data[idx + 1])
    idx += 2

    edges = []
    for _ in range(m):
        u = int(input_data[idx])
        v = int(input_data[idx + 1])
        w = int(input_data[idx + 2])
        idx += 3
        edges.append((w, u, v))

    edges.sort()

    parent = list(range(n))
    rank = [0] * n
    total_weight = 0
    edges_used = 0

    for w, u, v in edges:
        if union(parent, rank, u, v):
            total_weight += w
            edges_used += 1
            if edges_used == n - 1:
                break

    if edges_used == n - 1:
        sys.stdout.write(str(total_weight) + "\n")
    else:
        sys.stdout.write("-1\n")


if __name__ == "__main__":
    main()
