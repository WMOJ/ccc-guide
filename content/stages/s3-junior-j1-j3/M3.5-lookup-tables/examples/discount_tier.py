import sys


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return

    discount = [20, 15, 10, 5, 0]
    tier = data[0]
    index = ord(tier) - ord("A")
    sys.stdout.write(f"{discount[index]}\n")


if __name__ == "__main__":
    main()
