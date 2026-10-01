import sys
from collections import deque


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    k = int(data[1])
    scores = [int(x) for x in data[2:2 + n]]

    # dp[i] = best total for a route that starts on stone 0 and ends on stone i.
    # The previous stone j is any stone from i - k to i - 1.
    dp = [0] * n
    dp[0] = scores[0]
    dq = deque([0])  # stone indices, dp[j] decreasing from front to back

    for i in range(1, n):
        while dq[0] < i - k:
            dq.popleft()
        dp[i] = scores[i] + dp[dq[0]]
        while dq and dp[dq[-1]] <= dp[i]:
            dq.pop()
        dq.append(i)

    print(dp[n - 1])


if __name__ == "__main__":
    main()
