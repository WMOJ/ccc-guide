import sys


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return

    grades = {"A": 90, "B": 80, "C": 70, "D": 60, "F": 0}
    letter = data[0]
    sys.stdout.write(f"{grades[letter]}\n")


if __name__ == "__main__":
    main()
