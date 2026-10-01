import sys


def build_counts(word: str) -> list:
    counts = [0] * 26
    for char in word:
        counts[ord(char) - ord("a")] += 1
    return counts


def main() -> None:
    tokens = sys.stdin.read().split()
    if len(tokens) < 2:
        return
    word_a = tokens[0]
    word_b = tokens[1]

    counts_a = build_counts(word_a)
    counts_b = build_counts(word_b)

    if counts_a == counts_b:
        print("Anagram")
    else:
        print("Not anagram")


if __name__ == "__main__":
    main()
