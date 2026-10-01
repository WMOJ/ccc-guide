import sys


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    arr = list(map(int, input_data[1:n + 1]))

    diff = [0] * n
    diff[0] = arr[0]
    for i in range(1, n):
        diff[i] = arr[i] - arr[i - 1]

    rebuilt = [0] * n
    rebuilt[0] = diff[0]
    for i in range(1, n):
        rebuilt[i] = rebuilt[i - 1] + diff[i]

    out_lines = [" ".join(map(str, diff)), " ".join(map(str, rebuilt))]
    sys.stdout.write("\n".join(out_lines) + "\n")


if __name__ == "__main__":
    main()
