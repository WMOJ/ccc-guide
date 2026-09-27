import heapq

h = []
heapq.heappush(h, 5)
heapq.heappush(h, 2)
heapq.heappush(h, 8)
heapq.heappush(h, 1)

print("Heap:", h)

while h:
    print(heapq.heappop(h), end=" ")
print()
