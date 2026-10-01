import sys


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    pos = 0
    start_r = int(input_data[pos])
    pos += 1
    start_c = int(input_data[pos])
    pos += 1
    end_r = int(input_data[pos])
    pos += 1
    end_c = int(input_data[pos])
    pos += 1
    moves = int(input_data[pos])
    pos += 1

    # The fewest moves that can reach the target: one per row and one per
    # column of difference. Any extra moves have to come in pairs, spent
    # stepping away and back, so they can only make up an even surplus.
    distance = abs(end_r - start_r) + abs(end_c - start_c)
    surplus = moves - distance

    if surplus >= 0 and surplus % 2 == 0:
        sys.stdout.write("yes\n")
    else:
        sys.stdout.write("no\n")


if __name__ == "__main__":
    main()
