import sys


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    m = int(input_data[1])

    diff = [0] * (n + 1)

    idx = 2
    for _ in range(m):
        l = int(input_data[idx])
        r = int(input_data[idx + 1])
        val = int(input_data[idx + 2])
        diff[l] += val
        diff[r + 1] -= val
        idx += 3

    # Reconstruct
    arr = []
    current = 0
    for i in range(n):
        current += diff[i]
        arr.append(current)

    sys.stdout.write(" ".join(map(str, arr)) + "\n")


if __name__ == "__main__":
    main()
