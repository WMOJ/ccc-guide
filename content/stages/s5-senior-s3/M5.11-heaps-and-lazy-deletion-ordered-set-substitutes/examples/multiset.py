import heapq
import sys


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return
    m = int(data[0])
    pos = 1

    heap = []
    pending = {}
    count = 0
    for _ in range(m):
        op = data[pos]
        value = int(data[pos + 1])
        pos += 2
        if op == "A":
            heapq.heappush(heap, -value)
            count += 1
            print(f"Added {value}, count = {count}")
        else:
            pending[value] = pending.get(value, 0) + 1
            count -= 1
            print(f"Removed {value}, count = {count}")

    while heap:
        value = -heap[0]
        if pending.get(value, 0) > 0:
            pending[value] -= 1
            heapq.heappop(heap)
            continue
        print(f"Maximum: {value}, remaining count: {count}")
        break


if __name__ == "__main__":
    main()
