numbers = list(map(int, input().split()))
seen = set()
first_dup = -1

for num in numbers:
    if num in seen:
        first_dup = num
        break
    seen.add(num)

print(first_dup)
