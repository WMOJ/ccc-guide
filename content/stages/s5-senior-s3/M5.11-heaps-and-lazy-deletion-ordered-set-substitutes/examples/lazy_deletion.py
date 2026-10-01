import heapq
import sys

INF = 10 ** 9


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    m = int(data[1])
    pos = 2

    best = [INF] * n
    heap = []
    for _ in range(m):
        op = data[pos]
        pos += 1
        if op == "U":
            item = int(data[pos])
            priority = int(data[pos + 1])
            pos += 2
            best[item] = priority
            heapq.heappush(heap, (priority, item))
            print(f"Update job {item} to priority {priority}")
        else:
            priority, item = heapq.heappop(heap)
            while priority != best[item]:
                print(f"Skipping stale entry (priority {priority}, job {item})")
                priority, item = heapq.heappop(heap)
            print(f"Job {item} at priority {priority} is handed out")
            best[item] = -1


if __name__ == "__main__":
    main()
