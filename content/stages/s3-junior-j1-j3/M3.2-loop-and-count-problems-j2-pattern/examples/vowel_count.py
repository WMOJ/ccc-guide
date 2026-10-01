import sys


def main() -> None:
    raw = sys.stdin.read()
    lines = raw.split("\n")
    n = int(lines[0])

    vowel_count = 0
    for i in range(n):
        word = lines[1 + i]
        if word[0] in "aeiouAEIOU":
            vowel_count += 1

    print(vowel_count)


if __name__ == "__main__":
    main()
