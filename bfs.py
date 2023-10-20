from queue import Queue
import time

class QueensBFS:
    def __init__(self, size):
        self.size = size

    def solve_bfs(self):
        if self.size < 1:
            return []

        def is_safe(queens, row, col):
            for r, c in queens:
                if c == col or abs(row - r) == abs(col - c):
                    return False
            return True

        def convert_result(result): #convert soluiton
            temp = []
            for r, c in result:
                temp.append(c)
            return temp
        
        result = []
        queue = Queue()
        queue.put([])

        while not queue.empty():
            queens = queue.get()
            row = len(queens)
            if row == self.size:
                result = queens
                break
            for col in range(self.size):
                if is_safe(queens, row, col):
                    new_queens = queens + [(row, col)]
                    queue.put(new_queens)

        return convert_result(result)

def main():
    size = 11 #size of board
    n_queens = QueensBFS(size)

    start_time = time.time()
    bfs_solutions = n_queens.solve_bfs()
    end_time = time.time()

    if bfs_solutions:
        print(bfs_solutions)
    else:
        print("No solution found")
    print(end_time - start_time)

if __name__ == '__main__':
    main()