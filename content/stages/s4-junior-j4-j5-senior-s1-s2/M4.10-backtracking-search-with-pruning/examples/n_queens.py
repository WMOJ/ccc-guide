def solve_n_queens(n):
    result = []
    cols = set()
    diag1 = set()
    diag2 = set()
    
    def backtrack(row, board):
        if row == n:
            result.append([row[:] for row in board])
            return
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            board[row][col] = 1
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            
            backtrack(row + 1, board)
            
            board[row][col] = 0
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)
    
    board = [[0] * n for _ in range(n)]
    backtrack(0, board)
    return len(result)


print(solve_n_queens(4))
print(solve_n_queens(8))
