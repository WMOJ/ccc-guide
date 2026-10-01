import sys


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    m = int(data[1])

    adj = [[] for _ in range(n)]
    pos = 2
    for _ in range(m):
        a = int(data[pos])
        b = int(data[pos + 1])
        pos += 2
        adj[a].append(b)

    for v in range(n):
        row = f"{v}: {adj[v]}"
        print(row)


if __name__ == "__main__":
    main()
