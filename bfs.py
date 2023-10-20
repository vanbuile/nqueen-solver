from queue import Queue
import time

class QueensBFS:
    def __init__(self, size):
        self.size = size

    def solve_bfs(self):
        if self.size < 1:
            return []
        result = []
        queue = Queue()
        queue.put([])
        while not queue.empty():
            solution = queue.get()
            if not self.is_safe(solution):
                continue
            row = len(solution)
            if row == self.size:
                result = solution
                break
            for col in range(self.size):
                queen = col
                queens = solution.copy()
                queens.append(queen)
                queue.put(queens)
        return result

    def is_safe(self, queens):
        for i in range(1, len(queens)):
            for j in range(0, i):
                a, b = i, queens[i]
                c, d = j, queens[j]
                if a == c or b == d or abs(a - c) == abs(b - d):
                    return False
        return True

def main():
    size = 15
    n_queens = QueensBFS(size)

    start_time = time.time()
    bfs_solutions = n_queens.solve_bfs()
    end_time = time.time()

    if len(bfs_solutions):
        print(bfs_solutions)
    else:
        print("No solution")
    print(end_time - start_time)

if __name__ == '__main__':
    main()