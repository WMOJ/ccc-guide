import sys


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    passes = int(data[1])

    current_player = 0
    for _ in range(passes):
        current_player = (current_player + 1) % n

    print(current_player)


if __name__ == "__main__":
    main()
