import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    heights = [int(x) for x in data[1:1 + n]]
    heights.append(0)  # a bar of height 0 at the end pops everything

    best = 0
    stack = []  # bars whose right edge is still open, heights rising
    for i in range(n + 1):
        while stack and heights[stack[-1]] >= heights[i]:
            top = stack.pop()
            left = stack[-1] if stack else -1
            width = i - left - 1
            best = max(best, heights[top] * width)
        stack.append(i)

    print(best)


if __name__ == "__main__":
    main()
