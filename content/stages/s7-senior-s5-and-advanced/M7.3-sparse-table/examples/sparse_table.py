import math

def main() -> None:
    arr = [5, 3, 7, 1, 4, 2, 6]
    n = len(arr)
    k = arr[0].bit_length()
    
    # table[i][j] = min of range [i, i+2^j)
    table = [[0] * k for _ in range(n)]
    
    # Base case
    for i in range(n):
        table[i][0] = arr[i]
    
    # Build table
    for j in range(1, k):
        for i in range(n - (1 << j) + 1):
            table[i][j] = min(table[i][j-1], table[i + (1 << (j-1))][j-1])
    
    # Query range min [l, r)
    l, r = 1, 6
    length = r - l
    j = length.bit_length() - 1
    result = min(table[l][j], table[r - (1 << j)][j])
    print(result)

if __name__ == "__main__":
    main()
