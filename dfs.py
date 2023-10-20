import time

def solve_nqueens(n):
    def is_safe(row, col):
        # Check if it's safe to place a queen in this cell
        if ((ld[row - col + n - 1] != 1 and rd[row + col] != 1) and cl[row] != 1):
            return True
        return False
    
    def dfs(col):
        if col == n:
            # All queens are placed, solution found
            return True
        for row in range(n):
            if is_safe(row, col):
                board[col] = row
                ld[row - col + n - 1] = rd[row + col] = cl[row] = 1
                if dfs(col + 1):
                    return True
                board[col] = 0
                ld[row - col + n - 1] = rd[row + col] = cl[row] = 0
        return False

    board = [0] * n  # Initialize the board
    ld = [0] * (n * 2 - 1)
    rd = [0] * (n * 2 - 1)
    cl = [0] * n
    if dfs(0):
        return board
    else:
        return None

def print_solution(solution):
    if solution is None:
        print("No solution found.")
    else:
        n = len(solution)
        for row in solution:
            board_row = ['Q' if i == row else '.' for i in range(n)]
            print(" ".join(board_row))

if __name__ == "__main__":
    n = 10  # Change 'n' to the desired board size

    start_time = time.time()

    solution = solve_nqueens(n)

    end_time = time.time()

    print("The solution: ", solution)

    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.6f} seconds")
