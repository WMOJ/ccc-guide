from collections import deque

orders = ['pizza', 'burger', 'salad', 'pasta']
queue = deque(orders)

print("Processing orders in order:")
while queue:
    order = queue.popleft()
    print(f"Served: {order}")
