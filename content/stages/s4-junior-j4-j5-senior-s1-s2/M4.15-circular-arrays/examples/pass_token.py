n, passes = map(int, input().split())
current_player = 0

for _ in range(passes):
    current_player = (current_player + 1) % n

print(current_player)
