import sys


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])

    # Compute sum of floor(n / d) for d = 1 to n, using O(sqrt(n)) blocks
    # instead of an O(n) loop over every divisor d.
    total = 0
    d = 1

    while d <= n:
        q = n // d  # the quotient shared by this whole block of divisors

        # Every d' in this block satisfies n // d' == q. The largest such d'
        # is n // q (when q > 0); beyond it the quotient drops below q.
        next_d = n // q if q > 0 else n

        count = next_d - d + 1
        total += q * count

        d = next_d + 1

    print(f"Sum of floor({n}/d) for d=1 to {n}: {total}")


if __name__ == "__main__":
    main()
