import sys


def find(parent: list, x: int) -> int:
    """Find root with path halving; the root is the first free slot at or after x."""
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    k = int(data[1])

    # Slots 1..n, plus one sentinel slot at n + 1 that is never taken.
    parent = list(range(n + 2))

    out_lines = []
    for _ in range(k):
        slot = find(parent, 1)
        if slot == n + 1:
            out_lines.append("-1")
        else:
            out_lines.append(str(slot))
            parent[slot] = slot + 1

    print("\n".join(out_lines))


if __name__ == "__main__":
    main()
