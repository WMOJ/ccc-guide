import sys


def main() -> None:
    data = sys.stdin.read().split()
    pos = 0
    m = int(data[pos])
    pos += 1
    segment_lengths = []
    segment_values = []
    for _ in range(m):
        length = int(data[pos])
        pos += 1
        value = data[pos]
        pos += 1
        segment_lengths.append(length)
        segment_values.append(value)

    cumulative = [0]
    for length in segment_lengths:
        cumulative.append(cumulative[-1] + length)

    q = int(data[pos])
    pos += 1
    answers = []
    for _ in range(q):
        query_pos = int(data[pos])
        pos += 1
        segment = 0
        while cumulative[segment + 1] <= query_pos:
            segment += 1
        answers.append(segment_values[segment])

    print("\n".join(answers))


if __name__ == "__main__":
    main()
