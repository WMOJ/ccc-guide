import sys


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    pos = 0
    query_count = int(input_data[pos])
    pos += 1

    answers = []
    for _ in range(query_count):
        start = int(input_data[pos])
        pos += 1
        target = int(input_data[pos])
        pos += 1

        # Every move is +4 or -6, both even, so the position's parity never
        # changes. Python's % is always in 0..1 here, even for a negative
        # difference, so this check is the same either direction.
        difference = target - start
        if difference % 2 != 0:
            answers.append("no")
            continue

        # Any even difference is reachable: repeat the block "+4, -6, +4"
        # (net +2) to close a positive gap, or "+4, -6" (net -2) to close
        # a negative one, as many times as needed.
        answers.append("yes")

    sys.stdout.write("\n".join(answers) + "\n")


if __name__ == "__main__":
    main()
