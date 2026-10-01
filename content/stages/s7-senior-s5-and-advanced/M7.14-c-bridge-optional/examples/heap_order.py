import heapq
import sys


def main() -> None:
    raw = sys.stdin.read()
    tokens = raw.split()
    values = []
    for token in tokens:
        values.append(int(token))

    heap = []
    for v in values:
        heapq.heappush(heap, v)
    smallest_first = []
    while heap:
        smallest_first.append(heapq.heappop(heap))

    negated = []
    for v in values:
        heapq.heappush(negated, -v)
    largest_first = []
    while negated:
        largest_first.append(-heapq.heappop(negated))

    print("heapq", smallest_first)
    print("negated", largest_first)


if __name__ == "__main__":
    main()
