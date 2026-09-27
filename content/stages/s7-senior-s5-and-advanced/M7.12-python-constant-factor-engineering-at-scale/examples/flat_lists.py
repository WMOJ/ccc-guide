import sys

def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])

    # Read points into parallel lists
    x_coords = []
    y_coords = []
    for i in range(1, 2 * n + 1, 2):
        x_coords.append(int(data[i]))
        y_coords.append(int(data[i + 1]))

    # Process: find sum of all coordinates
    total = sum(x_coords) + sum(y_coords)
    sys.stdout.write(f"{total}\n")


if __name__ == "__main__":
    main()
