n = int(input())
passing_count = 0

for i in range(n):
    mark = int(input())
    if mark >= 50:
        passing_count += 1

print(passing_count)
