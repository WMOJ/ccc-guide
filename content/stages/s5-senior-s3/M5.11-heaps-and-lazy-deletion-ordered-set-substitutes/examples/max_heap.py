import heapq

h = []
heapq.heappush(h, -10)
heapq.heappush(h, -3)
heapq.heappush(h, -7)

print("Items in descending order:")
while h:
    print(-heapq.heappop(h), end=" ")
print()
