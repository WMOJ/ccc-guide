def rotate_clockwise(grid):
    R = len(grid)
    C = len(grid[0])
    transposed = [[grid[i][j] for i in range(R)] for j in range(C)]
    result = [row[::-1] for row in transposed]
    return result


grid = [[1, 2, 3], [4, 5, 6]]
result = rotate_clockwise(grid)
for row in result:
    print(' '.join(map(str, row)))
