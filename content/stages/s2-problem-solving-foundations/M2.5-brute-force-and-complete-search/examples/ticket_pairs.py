n, target = map(int, input().split())
tickets = [int(x) for x in input().split()]

count = 0
for i in range(n):
    for j in range(i + 1, n):
        if tickets[i] + tickets[j] == target:
            count += 1

print(count)
