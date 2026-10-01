import sys


def main() -> None:
    raw = sys.stdin.read()
    data = raw.split()
    if not data:
        return
    pos = 0
    n = int(data[pos])
    m = int(data[pos + 1])
    pos += 2

    adj = [
        [] for _ in range(n)
    ]
    for _ in range(m):
        u = int(data[pos])
        v = int(data[pos + 1])
        pos += 2
        adj[u].append(v)
        adj[v].append(u)

    seen = [False] * n
    par = [-1] * n
    order = [0]
    seen[0] = True
    st = [[0, 0]]

    while st:
        fr = st[-1]
        node = fr[0]
        idx = fr[1]
        deg = len(adj[node])
        if idx == deg:
            st.pop()
            continue
        nb = adj[node][idx]
        fr[1] = idx + 1
        if not seen[nb]:
            seen[nb] = True
            par[nb] = node
            order.append(nb)
            st.append([nb, 0])

    print("Preorder:", order)
    print("Parent:", par)


if __name__ == "__main__":
    main()
