import sys


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    pos = 1
    runners = []
    for _ in range(n):
        name = input_data[pos]
        time = float(input_data[pos + 1])
        bib = int(input_data[pos + 2])
        runners.append((name, time, bib))
        pos += 3

    ranked = sorted(runners, key=lambda runner: (runner[1], runner[2]))

    out_lines = []
    for name, time, bib in ranked:
        out_lines.append(f"{name} {time} {bib}")
    sys.stdout.write("\n".join(out_lines) + "\n")


if __name__ == "__main__":
    main()
