import sys
from collections import deque


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    k = int(data[1])
    values = [int(x) for x in data[2:2 + n]]

    dq = deque()  # indices, values[j] decreasing from front to back
    maximums = []
    for i in range(n):
        while dq and dq[0] <= i - k:
            dq.popleft()
        while dq and values[dq[-1]] <= values[i]:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            maximums.append(values[dq[0]])

    print(" ".join(str(x) for x in maximums))


if __name__ == "__main__":
    main()
