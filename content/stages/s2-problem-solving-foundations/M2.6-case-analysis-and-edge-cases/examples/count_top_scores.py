n = int(input())
scores = [int(x) for x in input().split()]

best = max(scores)
count = 0
for score in scores:
    if score == best:
        count += 1

print(count)
