import sys


def main() -> None:
    raw = sys.stdin.read()
    data = raw.split()
    if not data:
        return
    n = int(data[0])
    m = int(data[1])

    g = [
        [] for _ in range(n)
    ]
    pos = 2
    for _ in range(m):
        a = int(data[pos])
        b = int(data[pos+1])
        pos += 2
        g[a].append(b)
        g[b].append(a)

    for v in range(n):
        print(f"{v}: {g[v]}")


if __name__ == "__main__":
    main()
