import heapq

h = []
valid = {}

# Add item 0 with priority 8
heapq.heappush(h, (8, 0))
valid[(8, 0)] = False

# Update item 0 to priority 2
heapq.heappush(h, (2, 0))
valid[(2, 0)] = True

# Pop items, skipping invalid ones
print("Popping from heap:")
while h:
    priority, item = heapq.heappop(h)
    if valid.get((priority, item), False):
        print(f"Item {item} with priority {priority}")
    else:
        print(f"Skipping stale entry ({priority}, {item})")
