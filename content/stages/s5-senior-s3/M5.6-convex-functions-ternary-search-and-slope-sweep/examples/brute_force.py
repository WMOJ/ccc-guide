import sys


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    pos = 0
    n = int(input_data[pos])
    pos += 1
    positions = [int(x) for x in input_data[pos : pos + n]]
    pos += n
    weights = [int(x) for x in input_data[pos : pos + n]]
    pos += n
    lo = int(input_data[pos])
    hi = int(input_data[pos + 1])

    def cost(c: int) -> int:
        total = 0
        for p, w in zip(positions, weights):
            total += w * abs(p - c)
        return total

    best_loc = lo
    best_cost = cost(lo)
    for c in range(lo + 1, hi + 1):
        c_cost = cost(c)
        if c_cost < best_cost:
            best_loc = c
            best_cost = c_cost

    print(f"{best_loc} {best_cost}")


if __name__ == "__main__":
    main()
