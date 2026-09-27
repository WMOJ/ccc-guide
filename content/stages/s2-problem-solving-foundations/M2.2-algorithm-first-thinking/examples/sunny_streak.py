days = [1, 1, 0, 1, 1, 1, 0]

current_run = 0
best_run = 0
for day in days:
    if day == 1:
        current_run += 1
        best_run = max(best_run, current_run)
    else:
        current_run = 0

print(best_run)
