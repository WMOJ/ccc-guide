import sys


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    arr = list(map(int, data[1:n + 1]))

    # Build Fenwick tree (1-indexed)
    tree = [0] * (n + 1)

    def update(idx, val):
        # idx is 1-indexed
        while idx <= n:
            tree[idx] += val
            idx += idx & -idx

    # Initialize tree with array elements
    for i in range(n):
        update(i + 1, arr[i])

    def query(idx):
        # Sum from 0 to idx (0-indexed), converted to 1-indexed query
        idx += 1  # Convert to 1-indexed
        s = 0
        while idx > 0:
            s += tree[idx]
            idx -= idx & -idx
        return s

    # Query from 0 to 4 (should be 3+2+1+4+5=15)
    print(f"Sum [0, 4]: {query(4)}")

    # Query from 0 to 7 (should be 3+2+1+4+5+1+2+3=21)
    print(f"Sum [0, 7]: {query(7)}")

    # Update element at index 2 from 1 to 6 (add 5)
    update(3, 5)

    # Query again
    print(f"After update, sum [0, 4]: {query(4)}")
    print(f"After update, sum [0, 7]: {query(7)}")


if __name__ == "__main__":
    main()
