import heapq

heap = []
heapq.heappush(heap, (4, "B"))
heapq.heappush(heap, (1, "C"))
heapq.heappush(heap, (3, "B"))
print(heapq.heappop(heap))
print(heapq.heappop(heap))
