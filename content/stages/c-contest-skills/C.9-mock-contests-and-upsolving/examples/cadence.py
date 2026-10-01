import sys


def main() -> None:
    tokens = sys.stdin.read().split()
    cycle = int(tokens[0])
    upsolve = int(tokens[1])
    wait = int(tokens[2])
    retry_day = upsolve + wait
    events = [
        (0, "day 0: mock contest"),
        (1, f"days 1 to {upsolve}: upsolve"),
        (retry_day, f"day {retry_day}: retry the problems you stalled on, from a blank file"),
        (cycle, f"day {cycle}: next mock contest"),
    ]
    events.sort(key=lambda e: e[0])
    lines = [text for _, text in events]
    if retry_day > cycle:
        lines.append("the retry falls after the next mock, so shorten the wait")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
