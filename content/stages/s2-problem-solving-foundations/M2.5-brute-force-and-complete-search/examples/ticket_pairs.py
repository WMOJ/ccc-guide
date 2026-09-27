tickets = [3, 5, 2, 8]
target = 10

count = 0
for i in range(len(tickets)):
    for j in range(i + 1, len(tickets)):
        if tickets[i] + tickets[j] == target:
            count += 1

print(count)
