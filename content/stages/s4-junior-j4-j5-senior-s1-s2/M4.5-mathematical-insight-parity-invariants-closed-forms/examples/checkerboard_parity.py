import sys


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    # Parse input: start square as (row, col), end square, and moves
    start_r, start_c = int(input_data[0]), int(input_data[1])
    end_r, end_c = int(input_data[2]), int(input_data[3])
    moves = int(input_data[4])

    # Color of a square: (row + col) % 2
    start_color = (start_r + start_c) % 2
    end_color = (end_r + end_c) % 2

    # After an odd number of moves, color flips. After even, it stays.
    final_color = (start_color + moves) % 2

    if final_color == end_color:
        sys.stdout.write("yes\n")
    else:
        sys.stdout.write("no\n")


if __name__ == "__main__":
    main()
