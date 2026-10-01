import sys


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    m = int(data[1])
    codes = data[2:2 + n]
    index = {code: i for i, code in enumerate(codes)}

    adj = [[] for _ in range(n)]
    pos = 2 + n
    for _ in range(m):
        origin = index[data[pos]]
        dest = index[data[pos + 1]]
        pos += 2
        adj[origin].append(dest)

    for i in range(n):
        routes = [codes[j] for j in adj[i]]
        row = f"{codes[i]}: {routes}"
        print(row)


if __name__ == "__main__":
    main()
