import sys


def main() -> None:
    data = sys.stdin.read().split()
    n = int(data[0])
    temps = [int(x) for x in data[1:1 + n]]

    wait = [0] * n
    stack = []  # days still waiting for a warmer day
    for i in range(n):
        while stack and temps[stack[-1]] < temps[i]:
            day = stack.pop()
            wait[day] = i - day
        stack.append(i)

    print(" ".join(str(w) for w in wait))


if __name__ == "__main__":
    main()
