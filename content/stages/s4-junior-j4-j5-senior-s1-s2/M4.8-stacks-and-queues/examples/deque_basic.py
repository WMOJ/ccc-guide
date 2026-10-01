import sys
from collections import deque


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    values = [int(x) for x in input_data]

    d = deque()
    for i, val in enumerate(values):
        if i % 2 == 0:
            d.append(val)
        else:
            d.appendleft(val)

    sys.stdout.write(" ".join(str(x) for x in d) + "\n")


if __name__ == "__main__":
    main()
