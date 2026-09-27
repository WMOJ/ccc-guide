input()
arrivals = [int(x) for x in input().split()]

queue_length = 0
max_length = 0
for minute_arrivals in arrivals:
    queue_length += minute_arrivals
    max_length = max(max_length, queue_length)
    if queue_length > 0:
        queue_length -= 1

print(max_length)
