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

    order = sorted(range(n), key=lambda i: boxes[i][1] / boxes[i][0], reverse=True)
    greedy_weight = 0
    greedy_value = 0
    for i in order:
        weight, value = boxes[i]
        if greedy_weight + weight <= capacity:
            greedy_weight += weight
            greedy_value += value

    best_value = 0
    for mask in range(1 << n):
        weight = 0
        value = 0
        for i in range(n):
            if mask & (1 << i):
                weight += boxes[i][0]
                value += boxes[i][1]
        if weight <= capacity:
            best_value = max(best_value, value)

    out_lines = [str(greedy_value), str(best_value)]
    sys.stdout.write("\n".join(out_lines) + "\n")


if __name__ == "__main__":
    main()
