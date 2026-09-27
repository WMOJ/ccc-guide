import sys


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    capacity = int(input_data[1])

    boxes = []
    idx = 2
    for _ in range(n):
        weight = int(input_data[idx])
        value = int(input_data[idx + 1])
        boxes.append((weight, value))
        idx += 2

    # Sort by value per weight, descending
    boxes.sort(key=lambda b: b[1] / b[0], reverse=True)

    total_weight = 0
    total_value = 0
    for weight, value in boxes:
        if total_weight + weight <= capacity:
            total_weight += weight
            total_value += value

    sys.stdout.write(str(total_value) + "\n")


if __name__ == "__main__":
    main()
