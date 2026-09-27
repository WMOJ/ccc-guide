import sys
from collections import deque


def main() -> None:
    input_data = sys.stdin.read().split()
    n = int(input_data[0])
    k = int(input_data[1])
    arr = list(map(int, input_data[2:2 + n]))

    dq = deque()
    result = []

    for i in range(n):
        # Remove indices outside the window
        while dq and dq[0] < i - k + 1:
            dq.popleft()

        # Remove indices of elements smaller than current
        while dq and arr[dq[-1]] <= arr[i]:
            dq.pop()

        dq.append(i)

        # The maximum in the current window is at the front
        if i >= k - 1:
            result.append(arr[dq[0]])

    print("\n".join(map(str, result)))


if __name__ == "__main__":
    main()
