import sys


def dfs(node, adj, state, discovery, finish, time_counter):
    state[node] = 'gray'
    discovery[node] = time_counter[0]
    time_counter[0] += 1

    for neighbor in adj[node]:
        if state[neighbor] == 'white':
            dfs(neighbor, adj, state, discovery, finish, time_counter)

    state[node] = 'black'
    finish[node] = time_counter[0]
    time_counter[0] += 1


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    idx = 0
    n = int(input_data[idx])
    m = int(input_data[idx + 1])
    idx += 2

    adj = [[] for _ in range(n)]
    for _ in range(m):
        u = int(input_data[idx])
        v = int(input_data[idx + 1])
        idx += 2
        adj[u].append(v)

    state = ['white'] * n
    discovery = [-1] * n
    finish = [-1] * n
    time_counter = [0]

    for i in range(n):
        if state[i] == 'white':
            dfs(i, adj, state, discovery, finish, time_counter)

    result = []
    for i in range(n):
        result.append(str(i) + " " + str(discovery[i]) + " " + str(finish[i]))

    sys.stdout.write("\n".join(result) + "\n")


if __name__ == "__main__":
    main()
