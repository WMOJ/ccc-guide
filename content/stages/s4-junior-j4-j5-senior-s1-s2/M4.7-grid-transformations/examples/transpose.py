def transpose(grid):
    R = len(grid)
    C = len(grid[0])
    result = [[grid[i][j] for i in range(R)] for j in range(C)]
    return result


grid = [['A', 'B', 'C'], ['D', 'E', 'F']]
result = transpose(grid)
for row in result:
    print(' '.join(row))
