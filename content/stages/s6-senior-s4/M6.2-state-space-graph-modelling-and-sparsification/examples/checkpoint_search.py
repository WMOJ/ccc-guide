import sys
import heapq


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    idx = 0
    n_rooms = int(input_data[idx])
    n_edges = int(input_data[idx + 1])
    n_checkpoints = int(input_data[idx + 2])
    idx += 3

    # Build adjacency list
    adj = [[] for _ in range(n_rooms)]
    for _ in range(n_edges):
        u = int(input_data[idx])
        v = int(input_data[idx + 1])
        cost = int(input_data[idx + 2])
        idx += 3
        adj[u].append((v, cost))
        adj[v].append((u, cost))

    # Read checkpoints to collect
    checkpoints = []
    for _ in range(n_checkpoints):
        checkpoints.append(int(input_data[idx]))
        idx += 1

    checkpoint_set = frozenset(checkpoints)
    start_state = (0, frozenset())
    best = {}

    pq = [(0, start_state)]
    while pq:
        dist, state = heapq.heappop(pq)
        room, collected = state

        if state in best:
            continue
        best[state] = dist

        if collected == checkpoint_set:
            sys.stdout.write(str(dist) + "\n")
            return

        for next_room, cost in adj[room]:
            new_collected = collected | (
                frozenset([next_room])
                if next_room in checkpoints
                else frozenset()
            )
            next_state = (next_room, new_collected)
            next_dist = dist + cost

            if next_state not in best:
                heapq.heappush(pq, (next_dist, next_state))

    sys.stdout.write("-1\n")


if __name__ == "__main__":
    main()
