def find(parent, x):
    """Find root with path halving; returns first free slot at or after x."""
    if parent[x] == x:
        return x
    parent[x] = find(parent, x + 1)
    return parent[x]


def main() -> None:
    n = 5
    parent = list(range(n + 1))

    results = []
    for _ in range(3):
        # Find next free slot
        slot = find(parent, 1)
        results.append(str(slot))
        # Mark it occupied by pointing it to the next slot
        if slot < n:
            parent[slot] = slot + 1

    print("\n".join(results))


if __name__ == "__main__":
    main()
