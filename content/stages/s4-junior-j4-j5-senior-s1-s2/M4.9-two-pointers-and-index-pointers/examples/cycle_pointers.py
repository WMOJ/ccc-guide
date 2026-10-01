"""Fast/slow pointers: detect a cycle in a sequence of next-indices, and report its length."""

import sys


def solve() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    nxt = [int(x) for x in input_data[1 : n + 1]]
    start = int(input_data[n + 1])

    slow = start
    fast = start
    found = False
    while True:
        if fast == -1 or nxt[fast] == -1:
            break
        slow = nxt[slow]
        fast = nxt[nxt[fast]]
        if slow == fast:
            found = True
            break

    if not found:
        print("no cycle")
        return

    length = 1
    cur = nxt[slow]
    while cur != slow:
        cur = nxt[cur]
        length += 1
    print(f"cycle length {length}")


def main() -> None:
    solve()


if __name__ == "__main__":
    main()
