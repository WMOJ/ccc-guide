import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])

    # Slow: concatenating strings
    # result = ""
    # for i in range(1, n + 1):
    #     result += data[i] + " "

    # Fast: appending to list and joining once
    output = []
    for i in range(1, n + 1):
        output.append(data[i])

    sys.stdout.write(" ".join(output) + "\n")


if __name__ == "__main__":
    main()
