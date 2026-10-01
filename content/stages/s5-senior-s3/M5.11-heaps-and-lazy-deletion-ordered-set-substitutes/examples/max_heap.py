import heapq
import sys


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    values = [int(x) for x in data[1:1 + n]]

    heap = []
    for value in values:
        heapq.heappush(heap, -value)

    print("Stored as negatives:", heap)

    print("Items in descending order:")
    while heap:
        print(-heapq.heappop(heap), end=" ")
    print()


if __name__ == "__main__":
    main()
