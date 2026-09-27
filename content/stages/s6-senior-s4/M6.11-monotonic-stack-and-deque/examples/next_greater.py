import sys


def main() -> None:
    input_data = sys.stdin.read().split()
    n = int(input_data[0])
    arr = list(map(int, input_data[1:n + 1]))

    result = [-1] * n
    stack = []

    for i in range(n):
        while stack and arr[stack[-1]] < arr[i]:
            result[stack.pop()] = i
        stack.append(i)

    print("\n".join(map(str, result)))


if __name__ == "__main__":
    main()
