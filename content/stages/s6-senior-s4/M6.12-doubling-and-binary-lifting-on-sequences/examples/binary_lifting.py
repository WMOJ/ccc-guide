import sys


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    start = int(data[1])
    target_jump = int(data[2])

    # Build a simple linked list: node i -> node i+1
    # lift[node][k] = node reached after 2^k steps

    # Determine table size needed
    LOG = 20
    lift = [[-1] * LOG for _ in range(n)]

    # Base case: lift[i][0] = i+1 (one step ahead)
    for i in range(n - 1):
        lift[i][0] = i + 1

    # Fill the table: lift[i][k] = where you reach from lift[i][k-1] after 2^(k-1) steps
    for k in range(1, LOG):
        for i in range(n):
            if lift[i][k - 1] != -1:
                lift[i][k] = lift[lift[i][k - 1]][k - 1]

    # Query: jump target_jump steps from start
    current = start
    remaining = target_jump

    for k in range(LOG - 1, -1, -1):
        if remaining >= (1 << k):
            if lift[current][k] == -1:
                break
            current = lift[current][k]
            remaining -= (1 << k)

    if remaining == 0:
        print(f"After jumping {target_jump} steps from {start}, reach node {current}")
    else:
        print(f"Cannot jump {target_jump} steps from {start} (only {target_jump - remaining} steps possible)")


if __name__ == "__main__":
    main()
