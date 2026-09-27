import sys


def main() -> None:
    input_data = sys.stdin.read().split()
    n = int(input_data[0])

    events = []
    for i in range(n):
        start = int(input_data[1 + i * 2])
        end = int(input_data[1 + i * 2 + 1])
        events.append((start, 1))
        events.append((end, -1))

    events.sort()

    total_coverage = 0
    active_count = 0
    prev_pos = events[0][0]

    for pos, delta in events:
        if active_count > 0 and pos > prev_pos:
            total_coverage += (pos - prev_pos) * active_count

        active_count += delta
        prev_pos = pos

    print(total_coverage)


if __name__ == "__main__":
    main()
