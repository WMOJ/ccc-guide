def reflect_horizontal(grid):
    return [row[::-1] for row in grid]


def reflect_vertical(grid):
    return grid[::-1]


grid = [['A', 'B', 'C'], ['D', 'E', 'F']]

print("Original:")
for row in grid:
    print(' '.join(row))

print("\nHorizontal reflection:")
h_result = reflect_horizontal(grid)
for row in h_result:
    print(' '.join(row))

print("\nVertical reflection:")
v_result = reflect_vertical(grid)
for row in v_result:
    print(' '.join(row))
