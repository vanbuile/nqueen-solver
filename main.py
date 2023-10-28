import tkinter as tk
from tkinter import ttk
import time
from queue import Queue

# Global variables for step counts
step_count = 0
step_count_dfs = 0

def is_safe(n, row, col, ld, rd, cl):
    if (ld[row - col + n - 1] != 1 and rd[row + col] != 1 and cl[row] != 1):
        return True
    return False

def bfs(n, board, ld, rd, cl, display, display_chessboard_func, root):
    global step_count
    step_count = 0
    queue = Queue()
    queue.put((0, board, ld, rd, cl))

    while not queue.empty():
        col, current_board, current_ld, current_rd, current_cl = queue.get()
        step_count += 1
        if col == n:
            display_chessboard_func(new_board)
            return current_board
        for row in range(n):
            if is_safe(n, row, col, current_ld, current_rd, current_cl):
                new_board = current_board[:]
                new_ld = current_ld[:]
                new_rd = current_rd[:]
                new_cl = current_cl[:]
                new_board[col] = row
                new_ld[row - col + n - 1] = new_rd[row + col] = new_cl[row] = 1
                if display:
                    display_chessboard_func(new_board)
                    root.update()
                    time.sleep(0.5)
                queue.put((col + 1, new_board, new_ld, new_rd, new_cl))
    # display_chessboard_func(board)
    return None

def dfs(n, col, board, ld, rd, cl, display, display_chessboard_func, root):
    global step_count_dfs
    step_count_dfs += 1
    
    if col == n:
        display_chessboard_func(board)
        return True

    for row in range(n):
        if is_safe(n, row, col, ld, rd, cl):
            board[col] = row
            ld[row - col + n - 1] = rd[row + col] = cl[row] = 1
            
            if display:
                display_chessboard_func(board)
                root.update()
                time.sleep(0.5)

            if dfs(n, col + 1, board, ld, rd, cl, display, display_chessboard_func, root):
                return True

            # Backtrack
            board[col] = -1
            ld[row - col + n - 1] = rd[row + col] = cl[row] = 0
            if display:
                display_chessboard_func(board)
                root.update()
                time.sleep(0.5)

    return False

def solve_nqueens(n, display, display_chessboard_func, root, method):
    board = [-1] * n
    ld = [0] * (n * 2 - 1)
    rd = [0] * (n * 2 - 1)
    cl = [0] * n

    if display:
        display_chessboard_func(board)
        root.update()
        time.sleep(0.5)

    if method == "DFS":
        return dfs(n, 0, board, ld, rd, cl, display, display_chessboard_func, root)

def print_solution(solution, display_chessboard_func):
    if solution is None:
        print("No solution found.")
    else:
        n = len(solution)
        for row in solution:
            display_chessboard_func(solution)
            board_row = ['Q' if i == row else '.' for i in range(n)]
            print(" ".join(board_row))


def display_chessboard(board, canvas, square_size, n):
    canvas.delete("all")
    colors = ["#FFCE9E", "#D18B47"]  # Light and dark square colors

    for i in range(n):
        for j in range(n):
            color = colors[(i + j) % 2]
            canvas.create_rectangle(i * square_size, j * square_size, (i + 1) * square_size, (j + 1) * square_size, fill=color, outline="")

    queen_size = square_size*0.13  # Adjust the queen size to fit the square better
    offset = square_size*0.1  # Adjust the offset for proper centering

    queen_icon = tk.PhotoImage(file="queen.png").subsample(int(queen_size), int(queen_size))  # Replace "queen.png" with your queen image file

    for row, col in enumerate(board):
        x = col * square_size + offset
        y = row * square_size + offset
        canvas.create_image(x, y, image=queen_icon, anchor="nw")

    canvas.image = queen_icon

def display_results(method, time_taken, steps, display):
    result_window = tk.Toplevel()
    result_window.title(f"{method} Results")
    if not display: 
        label1 = tk.Label(result_window, text=f"Thời gian thực thi: {time_taken:.2f} seconds")
        label1.pack()
        label2 = tk.Label(result_window, text=f"Số bước đã thực hiện: {steps}")
        label2.pack()
    else:
        label1 = tk.Label(result_window, text="Đã hoàn thành")
        label1.pack()
    exit_button = tk.Button(result_window, text="Đóng", command=result_window.destroy)
    exit_button.pack()

def style_interface(root):
    """Apply styles to the interface"""
    style = ttk.Style()
    style.configure('TButton', font=('Helvetica', 14), padding=5)
    style.configure('TLabel', font=('Helvetica', 12), padding=5)
    style.configure('Title.TLabel', font=('Helvetica', 18))
    root.configure(bg="lightblue")

def create_interface():
    root = tk.Tk()
    root.title("N-Queens Problem Solver")

    style_interface(root)  # Style the interface

    header_frame = ttk.Frame(root)
    header_frame.grid(row=0, column=0, padx=10, pady=10, sticky='w')

    title_label = ttk.Label(header_frame, text="N-Queens Problem Solver", style='Title.TLabel', justify="center")
    title_label.pack(pady=10, anchor='center')

    canvas = tk.Canvas(root, width=400, height=400)
    canvas.grid(row=1, column=0, pady=10, padx=10)

    button_frame = ttk.Frame(root)
    button_frame.grid(row=2, column=0, pady=10)

    def select_method(method):
        method_window = tk.Toplevel(root)
        method_window.title(method)
        method_window.geometry("200x200")

        label = ttk.Label(method_window, text="Enter the value of N:")
        label.pack(pady=10)

        entry = ttk.Entry(method_window)
        entry.pack(pady=10)

        def start_simulation():
            start_time = time.time()
            N = int(entry.get())
            global display
            display = display_var.get()
            method_window.destroy()
            if method == "DFS":
                solution = solve_nqueens(N, display, lambda board: display_chessboard(board, canvas, 400 // N, N), root, method)
                if display:
                    elapsed_time = time.time() - start_time - (0.5 * step_count_dfs)
                else:
                    elapsed_time = time.time() - start_time
                display_results("DFS", elapsed_time, step_count_dfs, display)
            elif method == "BFS":
                solution = bfs(N, [-1] * N, [0] * (2 * N - 1), [0] * (2 * N - 1), [0] * N, display, lambda board: display_chessboard(board, canvas, 400 // N, N), root)
                if display:
                    elapsed_time = time.time() - start_time - (0.5 * step_count)
                else:
                    elapsed_time = time.time() - start_time
                display_results("BFS", elapsed_time, step_count, display)
            print_solution(solution, lambda board: display_chessboard(board, canvas))

        display_var = tk.IntVar()
        display_check = ttk.Checkbutton(method_window, text="Show Animation", variable=display_var)
        display_check.pack(pady=10)

        confirm_button = ttk.Button(method_window, text="Start Simulation", command=start_simulation)
        confirm_button.pack(pady=10)

    dfs_button = ttk.Button(button_frame, text="DFS", command=lambda: select_method("DFS"))
    dfs_button.grid(row=0, column=0, padx=5, pady=5)

    bfs_button = ttk.Button(button_frame, text="BFS", command=lambda: select_method("BFS"))
    bfs_button.grid(row=0, column=1, padx=5, pady=5)

    heuristic_button = ttk.Button(button_frame, text="Heuristic", command=lambda: select_method("Heuristic"))
    heuristic_button.grid(row=0, column=2, padx=5, pady=5)

    exit_button = ttk.Button(root, text="Exit", command=root.destroy)
    exit_button.grid(row=3, column=0, pady=10, sticky='e')

    root.mainloop()


if __name__ == "__main__":
    create_interface()
