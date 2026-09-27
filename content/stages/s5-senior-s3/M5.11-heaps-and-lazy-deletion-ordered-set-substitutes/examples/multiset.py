import heapq

h = []
removed = set()
count = 0

# Add items
for val in [3, 7, 2, 9, 5]:
    heapq.heappush(h, -val)
    count += 1

print(f"Added 5 items, count = {count}")

# Remove item with value 9
removed.add(9)
count -= 1

# Find maximum
while h:
    val = -heapq.heappop(h)
    if val not in removed:
        print(f"Maximum: {val}, remaining count: {count}")
        break
    else:
        count -= 1
