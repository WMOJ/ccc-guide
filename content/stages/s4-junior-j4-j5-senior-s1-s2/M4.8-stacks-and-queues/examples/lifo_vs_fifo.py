import sys
from collections import deque


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    values = input_data

    stack = list(values)
    stack_order = []
    while stack:
        stack_order.append(stack.pop())

    queue = deque(values)
    queue_order = []
    while queue:
        queue_order.append(queue.popleft())

    sys.stdout.write(f"stack: {' '.join(stack_order)}\n")
    sys.stdout.write(f"queue: {' '.join(queue_order)}\n")


if __name__ == "__main__":
    main()
