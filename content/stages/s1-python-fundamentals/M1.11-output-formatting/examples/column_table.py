n = int(input())
for _ in range(n):
    name, score = input().split()
    print(f"{name:<10}{score:>5}")
