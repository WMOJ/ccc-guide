scores = [7, 9, 9]
names = ["A", "B", "C"]

best_score = scores[0]
best_name = names[0]
for i in range(1, len(scores)):
    if scores[i] > best_score:
        best_score = scores[i]
        best_name = names[i]

print(best_name, best_score)
