import sys


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return

    days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    days_before = [0] * 13
    for m in range(1, 13):
        days_before[m] = days_before[m - 1] + days_in_month[m]

    pos = 0
    q = int(data[pos])
    pos += 1

    lines = []
    for _ in range(q):
        month = int(data[pos])
        day = int(data[pos + 1])
        pos += 2
        lines.append(str(days_before[month - 1] + day))

    sys.stdout.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
