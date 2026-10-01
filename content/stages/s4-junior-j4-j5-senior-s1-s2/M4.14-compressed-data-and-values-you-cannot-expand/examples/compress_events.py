import sys


def main() -> None:
    data = sys.stdin.read().split()
    pos = 0
    n = int(data[pos])
    pos += 1
    days = []
    types = []
    for _ in range(n):
        day = int(data[pos])
        pos += 1
        event_type = int(data[pos])
        pos += 1
        days.append(day)
        types.append(event_type)

    uniq = sorted(set(days))
    rank = {}
    for i, day in enumerate(uniq):
        rank[day] = i

    seen = []
    for day in uniq:
        seen.append(set())
    for k in range(n):
        d = days[k]
        t = types[k]
        r = rank[d]
        seen[r].add(t)

    counts = [len(s) for s in seen]
    print("\n".join(map(str, counts)))


if __name__ == "__main__":
    main()
