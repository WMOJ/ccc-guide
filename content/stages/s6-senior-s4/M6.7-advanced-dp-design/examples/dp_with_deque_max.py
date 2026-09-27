import sys
from collections import deque


def main() -> None:
    input_data = sys.stdin.read().split()
    n = int(input_data[0])
    k = int(input_data[1])
    values = list(map(int, input_data[2:2 + n]))

    # dp[i] = the best total you can reach by ending your chosen positions at i.
    # Every earlier chosen position j in [i - k, i - 1] is a legal predecessor.
    dp = [0] * n
    dq = deque()  # indices j, kept so dp[j] is decreasing front to back

    for i in range(n):
        # Drop predecessors that fall outside the window before reading the front.
        while dq and dq[0] < i - k:
            dq.popleft()

        best_predecessor = dp[dq[0]] if dq else 0
        dp[i] = values[i] + best_predecessor

        # dp[i] is now a candidate predecessor for later positions. Pop any
        # weaker entries at the back before adding it, so the deque stays
        # decreasing and the front is always the current window's best.
        while dq and dp[dq[-1]] <= dp[i]:
            dq.pop()
        dq.append(i)

    print(max(dp) if dp else 0)


if __name__ == "__main__":
    main()
