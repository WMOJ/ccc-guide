import sys


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    scores = list(map(int, input_data[1:n + 1]))

    # No score in this contest is negative, so 0 is a safe starting value:
    # it can never beat a real score.
    prefix_max = [0] * (n + 1)
    for i in range(n):
        prefix_max[i + 1] = max(prefix_max[i], scores[i])

    suffix_max = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix_max[i] = max(suffix_max[i + 1], scores[i])

    q = int(input_data[n + 1])
    idx = n + 2
    out_lines = []
    for _ in range(q):
        i = int(input_data[idx])
        idx += 1
        best_outside = max(prefix_max[i], suffix_max[i + 1])
        out_lines.append(str(best_outside))
    sys.stdout.write("\n".join(out_lines) + "\n")


if __name__ == "__main__":
    main()
