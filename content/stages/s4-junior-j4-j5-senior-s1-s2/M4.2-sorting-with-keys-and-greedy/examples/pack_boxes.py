import sys


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    capacity = int(input_data[1])
    weights = list(map(int, input_data[2:2 + n]))

    weights.sort()

    total_weight = 0
    count = 0
    for weight in weights:
        if total_weight + weight <= capacity:
            total_weight += weight
            count += 1

    sys.stdout.write(str(count) + "\n")


if __name__ == "__main__":
    main()
