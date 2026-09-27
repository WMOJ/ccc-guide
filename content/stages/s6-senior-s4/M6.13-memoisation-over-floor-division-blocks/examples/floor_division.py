import sys


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    d = int(data[1])

    # Compute sum of floor(i / d) for i = 1 to n
    # Naive: O(n), but we'll use floor-division blocks for O(sqrt(n))

    total = 0
    i = 1

    while i <= n:
        q = i // d  # quotient at position i
        # Find the last position in this block with the same quotient
        # floor(i / d) = q means q*d <= i < (q+1)*d
        # The last i with quotient q is (q+1)*d - 1, but capped at n
        next_boundary = min((q + 1) * d - 1, n)

        # All integers from i to next_boundary have quotient q
        count = next_boundary - i + 1
        total += q * count

        i = next_boundary + 1

    print(f"Sum of floor(i/{d}) for i=1 to {n}: {total}")


if __name__ == "__main__":
    main()
