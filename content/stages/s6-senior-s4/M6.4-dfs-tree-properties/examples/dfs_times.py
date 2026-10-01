import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    m = int(data[1])
    pos = 2
    adj = [[] for _ in range(n)]
    for _ in range(m):
        u = int(data[pos])
        v = int(data[pos + 1])
        pos += 2
        adj[u].append(v)

    disc = [-1] * n
    fin = [-1] * n
    clock = 0
    roots = 0
    for root in range(n):
        if disc[root] != -1:
            continue
        roots += 1
        disc[root] = clock
        clock += 1
        st = [[root, 0]]
        while st:
            fr = st[-1]
            node = fr[0]
            idx = fr[1]
            if idx == len(adj[node]):
                st.pop()
                fin[node] = clock
                clock += 1
                continue
            fr[1] = idx + 1
            nb = adj[node][idx]
            if disc[nb] == -1:
                disc[nb] = clock
                clock += 1
                st.append([nb, 0])

    lines = []
    for v in range(n):
        lines.append(f"{v} {disc[v]} {fin[v]}")
    lines.append(f"trees {roots}")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
