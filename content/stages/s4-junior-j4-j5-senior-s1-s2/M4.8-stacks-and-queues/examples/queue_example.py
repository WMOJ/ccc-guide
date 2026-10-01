import sys
from collections import deque


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    orders = deque(input_data)
    served = []
    while orders:
        served.append(f"Served: {orders.popleft()}")

    sys.stdout.write("\n".join(served) + "\n")


if __name__ == "__main__":
    main()
