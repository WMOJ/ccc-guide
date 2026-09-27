orders = ['pizza', 'burger', 'salad', 'pasta']
queue = list(orders)

print("Processing orders in order:")
while queue:
    order = queue.pop(0)
    print(f"Served: {order}")
