import sys


def main() -> None:
    rolls = sys.stdin.read().split()
    if not rolls:
        return

    freq = [0] * 7
    for roll in rolls:
        freq[int(roll)] += 1

    best = 1
    for face in range(2, 7):
        if freq[face] > freq[best]:
            best = face
    print(f"{best}: {freq[best]}")


if __name__ == "__main__":
    main()
