period = int(input())
offset = int(input())
days = int(input())

count = 0
for d in range(days):
    if d % period == offset % period:
        count += 1

print(count)
