def rotate_counterclockwise(grid):
    R = len(grid)
    C = len(grid[0])
    transposed = [[grid[i][j] for i in range(R)] for j in range(C)]
    result = transposed[::-1]
    return result


grid = [[1, 2, 3], [4, 5, 6]]
result = rotate_counterclockwise(grid)
for row in result:
    print(' '.join(map(str, row)))
