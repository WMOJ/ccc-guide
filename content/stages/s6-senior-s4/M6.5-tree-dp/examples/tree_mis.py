from sys import stdin


def main() -> None:
    data = stdin.read().split()
    if not data:
        return
    pos = 0
    n = int(data[pos])
    pos += 1
    adj = [[] for _ in range(n)]
    for _ in range(n - 1):
        a = int(data[pos])
        b = int(data[pos + 1])
        pos += 2
        adj[a].append(b)
        adj[b].append(a)

    parent = [-1] * n
    seen = [False] * n
    order = [0]
    seen[0] = True
    for u in order:
        for v in adj[u]:
            if not seen[v]:
                seen[v] = True
                parent[v] = u
                order.append(v)

    dp0 = [0] * n
    dp1 = [1] * n
    for i in range(n - 1, 0, -1):
        u = order[i]
        p = parent[u]
        dp0[p] += max(dp0[u], dp1[u])
        dp1[p] += dp0[u]

    print("Order:", order)
    print("dp0:", dp0)
    print("dp1:", dp1)
    print("Largest set:", max(dp0[0], dp1[0]))


if __name__ == "__main__":
    main()
