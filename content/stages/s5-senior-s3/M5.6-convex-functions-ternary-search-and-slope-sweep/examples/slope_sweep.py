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

    breakpoints = sorted(zip(positions, weights))
    total_weight = sum(weights)

    left_weight = 0
    best_loc = breakpoints[-1][0]
    for p, w in breakpoints:
        left_weight += w
        slope = 2 * left_weight - total_weight
        if slope >= 0:
            best_loc = p
            break

    best_cost = 0
    for p, w in zip(positions, weights):
        best_cost += w * abs(p - best_loc)

    print(f"{best_loc} {best_cost}")


if __name__ == "__main__":
    main()
