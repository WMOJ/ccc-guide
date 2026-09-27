import heapq

heap = []
heapq.heappush(heap, (4, "B"))
heapq.heappush(heap, (3, "B"))
done = {"B": False}
while heap:
    d, u = heapq.heappop(heap)
    if done[u]:
        print("skip", d, u)
        continue  # an out-of-date entry: u was done earlier
    done[u] = True
    print("done", d, u)
