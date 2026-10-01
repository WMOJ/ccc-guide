import sys


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return
    pos = 0
    n = int(data[pos])
    pos += 1
    piles = []
    for _ in range(n):
        piles.append(int(data[pos]))
        pos += 1

    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] + piles[i]

    dp = [[0] * n for _ in range(n)]
    opt = [[0] * n for _ in range(n)]
    for i in range(n):
        opt[i][i] = i

    tried = 0
    for size in range(2, n + 1):
        for i in range(n - size + 1):
            j = i + size - 1
            low = opt[i][j - 1]
            high = min(opt[i + 1][j], j - 1)
            best = pre[n] * n
            best_k = low
            for k in range(low, high + 1):
                tried += 1
                left = dp[i][k]
                right = dp[k + 1][j]
                total = left + right
                if total < best:
                    best = total
                    best_k = k
            span = pre[j + 1] - pre[i]
            dp[i][j] = best + span
            opt[i][j] = best_k

    print("Minimum cost:", dp[0][n - 1])
    print("Splits tried:", tried)
    print("Splits in the plain loop:", (n**3 - n) // 6)


if __name__ == "__main__":
    main()
