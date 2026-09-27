n = int(input())
readings = [tuple(map(int, input().split())) for _ in range(n)]

unique_days = sorted(set(day for day, _ in readings))
day_to_compressed = {day: i for i, day in enumerate(unique_days)}

event_types = [set() for _ in unique_days]
for day, event_type in readings:
    event_types[day_to_compressed[day]].add(event_type)

print("\n".join(str(len(s)) for s in event_types))
