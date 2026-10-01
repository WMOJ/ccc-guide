import heapq
import sys


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    k = int(data[1])
    values = [int(x) for x in data[2:2 + n]]

    heap = []
    minimums = []
    for i in range(n):
        heapq.heappush(heap, (values[i], i))
        while heap[0][1] <= i - k:
            heapq.heappop(heap)
        if i >= k - 1:
            minimums.append(heap[0][0])

    print(" ".join(str(x) for x in minimums))


if __name__ == "__main__":
    main()
