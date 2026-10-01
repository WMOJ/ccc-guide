import sys


def cut(dp, pre, i, j):
    best = pre[-1] * len(dp)
    for k in range(i, j):
        left = dp[i][k]
        right = dp[k + 1][j]
        total = left + right
        best = min(best, total)
    span = pre[j + 1] - pre[i]
    return best + span


def main() -> None:
    raw = sys.stdin.read()
    data = raw.split()
    if not data:
        return
    nums = list(map(int, data))
    n = nums[0]
    piles = nums[1:]

    pre = [0]
    for x in piles:
        pre.append(pre[-1] + x)

    dp = []
    for _ in range(n):
        dp.append([0] * n)
    for size in range(2, n + 1):
        m = n - size + 1
        for i in range(m):
            j = i + size - 1
            c = cut(dp, pre, i, j)
            dp[i][j] = c

    ans = dp[0][n - 1]
    print("Minimum cost:", ans)


if __name__ == "__main__":
    main()
