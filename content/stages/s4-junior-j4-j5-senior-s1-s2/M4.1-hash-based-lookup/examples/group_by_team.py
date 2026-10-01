import sys


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    pos = 1
    by_team = {}
    for _ in range(n):
        team = input_data[pos]
        score = int(input_data[pos + 1])
        pos += 2
        by_team.setdefault(team, []).append(score)

    lines = []
    for team in sorted(by_team):
        lines.append(f"{team}: {max(by_team[team])}")
    sys.stdout.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
