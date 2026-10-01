import sys


def main() -> None:
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    word = "a" * n

    freq_ops = 0
    freq = [0] * 26
    for char in word:
        freq_ops += 1
        freq[ord(char) - ord("a")] += 1

    count_ops = 0
    matches = 0
    for letter_index in range(26):
        letter = chr(ord("a") + letter_index)
        for char in word:
            count_ops += 1
            if char == letter:
                matches += 1
        # this inner loop is the work word.count(letter) does: a full scan every call

    print(freq_ops, count_ops)


if __name__ == "__main__":
    main()
