import sys


def main() -> None:
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    word = tokens[0]

    freq = [0] * 26
    for char in word:
        if "a" <= char <= "z":
            index = ord(char) - ord("a")
            freq[index] += 1

    lines = []
    for i in range(26):
        if freq[i] > 0:
            letter = chr(ord("a") + i)
            lines.append(f"{letter}: {freq[i]}")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
