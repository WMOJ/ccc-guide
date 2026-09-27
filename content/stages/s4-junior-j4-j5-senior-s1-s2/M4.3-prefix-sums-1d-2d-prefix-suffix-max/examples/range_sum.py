import sys


def main() -> None:
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    arr = list(map(int, input_data[1:n+1]))

    # Build prefix sum
    prefix = [0]
    for val in arr:
        prefix.append(prefix[-1] + val)

    # Process queries
    q = int(input_data[n+1])
    idx = n + 2
    for _ in range(q):
        i = int(input_data[idx])
        j = int(input_data[idx+1])
        result = prefix[j+1] - prefix[i]
        sys.stdout.write(str(result) + "\n")
        idx += 2


if __name__ == "__main__":
    main()
