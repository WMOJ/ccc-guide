import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    limit = int(data[1])
    heights = list(map(int, data[2:2 + n]))

    heights.sort()
    count = 0
    left = 0
    for right in range(n):
        while heights[right] - heights[left] > limit:
            left += 1
        count += right - left

    print(count)


if __name__ == "__main__":
    main()
