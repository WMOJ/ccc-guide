from collections import deque

arr = [3, 1, 4, 1, 5, 9, 2, 6]
k = 3

dq = deque()
results = []

for i, val in enumerate(arr):
    # Remove indices outside the window
    while dq and dq[0] < i - k + 1:
        dq.popleft()

    # Remove larger values from the back
    while dq and arr[dq[-1]] > val:
        dq.pop()

    dq.append(i)

    # Window is complete
    if i >= k - 1:
        results.append(arr[dq[0]])

print("Sliding window minima:", results)
