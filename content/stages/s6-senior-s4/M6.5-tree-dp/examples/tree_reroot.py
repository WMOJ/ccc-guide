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

    size = [1] * n
    down = [0] * n
    for i in range(n - 1, 0, -1):
        u = order[i]
        p = parent[u]
        s = size[u]
        size[p] += s
        down[p] += down[u] + s

    ans = [0] * n
    ans[0] = down[0]
    for c in order[1:]:
        p = parent[c]
        s = size[c]
        far = n - s
        ans[c] = ans[p] - s + far

    print("Size:", size)
    print("Down:", down)
    print("Answer:", ans)


if __name__ == "__main__":
    main()
