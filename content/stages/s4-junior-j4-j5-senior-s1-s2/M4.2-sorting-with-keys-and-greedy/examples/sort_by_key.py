import sys


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    pos = 1
    tasks = []
    for _ in range(n):
        name = input_data[pos]
        duration = int(input_data[pos + 1])
        tasks.append((name, duration))
        pos += 2

    by_duration = sorted(tasks, key=lambda task: task[1])

    out_lines = []
    for name, duration in by_duration:
        out_lines.append(f"{name} {duration}")
    sys.stdout.write("\n".join(out_lines) + "\n")


if __name__ == "__main__":
    main()
