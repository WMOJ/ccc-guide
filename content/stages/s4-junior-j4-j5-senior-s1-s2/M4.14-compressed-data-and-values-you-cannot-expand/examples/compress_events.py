n = int(input())
events = {}
days = []

for _ in range(n):
    day, event_type = map(int, input().split())
    if day not in events:
        events[day] = set()
        days.append(day)
    events[day].add(event_type)

days.sort()
day_to_compressed = {day: i for i, day in enumerate(days)}

result = []
for day in days:
    count = len(events[day])
    result.append(str(count))

print("\n".join(result))
