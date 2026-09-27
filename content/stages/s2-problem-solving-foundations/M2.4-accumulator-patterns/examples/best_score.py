scores = [7, 9, 9]
names = ["A", "B", "C"]

best_score = scores[0]
leader = names[0]
n = len(scores)
for i in range(1, n):
    cur = scores[i]
    if cur > best_score:
        best_score = cur
        leader = names[i]

print(leader, best_score)
