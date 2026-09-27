import sys
from collections import deque


def main() -> None:
    input_data = sys.stdin.read().split()
    n = int(input_data[0])
    k = int(input_data[1])
    values = list(map(int, input_data[2:2 + n]))

    # dp[i] = max value reachable from any position within distance k
    dp = [0] * n
    dq = deque()

    for i in range(n):
        # Remove indices outside the window
        while dq and dq[0][1] < i - k:
            dq.popleft()

        # Add current value to the deque
        while dq and dq[-1][0] <= values[i]:
            dq.pop()
        dq.append((values[i], i))

        # The best predecessor within distance k
        if dq:
            dp[i] = dq[0][0] + values[i]
        else:
            dp[i] = values[i]

    print(max(dp) if dp else 0)


if __name__ == "__main__":
    main()
