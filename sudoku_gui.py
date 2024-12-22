import tkinter as tk
from tkinter import messagebox, Scale
import threading
import queue
import time

from sudoku_solver import SudokuSolver
from sudoku_generator import SudokuGenerator

class SudokuGUI:
    def __init__(self, master):
        """
        Initialize the Sudoku GUI.
        
        Args:
            master (tk.Tk): Main window
        """
        self.master = master
        master.title("Advanced Sudoku Solver")
        master.configure(bg='#f0f0f0')
        master.geometry("600x750")
        
        self.cells = {}
        self.solving_speed = 0.1
        
        self.create_board()
        self.create_controls()
        self.create_buttons()
        self.create_time_label()
        self.create_stats_label()
        
        self.update_queue = queue.Queue()
        self.master.after(100, self.process_queue)

    def create_controls(self):
        """Create speed and difficulty control widgets."""
        controls_frame = tk.Frame(self.master, bg='#f0f0f0')
        controls_frame.pack(pady=10)
        
        speed_label = tk.Label(controls_frame, text="Solving Speed:", bg='#f0f0f0')
        speed_label.pack(side=tk.LEFT, padx=5)
        
        self.speed_slider = Scale(controls_frame, from_=0.01, to=1, resolution=0.01, 
                                  orient=tk.HORIZONTAL, length=200, showvalue=1, 
                                  command=self.update_speed)
        self.speed_slider.set(0.1)
        self.speed_slider.pack(side=tk.LEFT, padx=10)
        
        difficulty_label = tk.Label(controls_frame, text="Difficulty:", bg='#f0f0f0')
        difficulty_label.pack(side=tk.LEFT, padx=5)
        
        self.difficulty_var = tk.StringVar(value='medium')
        difficulties = ['easy', 'medium', 'hard', 'expert']
        difficulty_menu = tk.OptionMenu(controls_frame, self.difficulty_var, *difficulties)
        difficulty_menu.pack(side=tk.LEFT, padx=5)

    def update_speed(self, val):
        """Update solving speed."""
        self.solving_speed = float(val)

    def solve_sudoku_animated(self):
        """Start solving the Sudoku puzzle with animation."""
        sudoku = []
        for i in range(9):
            row = []
            for j in range(9):
                val = self.cells[(i, j)].get()
                row.append(int(val) if val.isdigit() else 0)
            sudoku.append(row)
        
        try:
            solver = SudokuSolver(sudoku, callback=self.update_board)
            solving_thread = threading.Thread(target=self.solve_thread, args=(solver,))
            solving_thread.start()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def solve_thread(self, solver):
        """
        Thread for solving Sudoku to prevent GUI freezing.
        
        Args:
            solver (SudokuSolver): Solver instance
        """
        solved = solver.solve_with_visualization(delay=self.solving_speed)
        if solved is not None:
            self.update_queue.put(('solved', solved, solver.solve_time, solver.attempts, solver.backtrack_count))
        else:
            self.update_queue.put(('error', None, None, None, None))

    def process_queue(self):
        """Process updates from solving thread."""
        try:
            while not self.update_queue.empty():
                status, solved, solve_time, attempts, backtrack_count = self.update_queue.get_nowait()
                
                if status == 'solved':
                    for i in range(9):
                        for j in range(9):
                            self.cells[(i, j)].delete(0, tk.END)
                            self.cells[(i, j)].insert(0, str(solved[i][j]))
                    
                    self.time_label.config(text=f"Solved in {solve_time:.4f} seconds")
                    self.stats_label.config(text=f"Attempts: {attempts}, Backtracks: {backtrack_count}")
                
                elif status == 'error':
                    messagebox.showerror("Error", "No solution exists for this Sudoku!")
        
        except queue.Empty:
            pass
        
        self.master.after(100, self.process_queue)

    def update_board(self, board, status='normal', cell=None, number=None, attempts=0, backtrack_count=0):
        """
        Update board visualization during solving.
        
        Args:
            board (numpy.ndarray): Current Sudoku board state
            status (str): Current solving status
            cell (tuple): Current cell being processed
            number (int): Number being tried
            attempts (int): Number of solving attempts
            backtrack_count (int): Number of backtracks
        """
        for i in range(9):
            for j in range(9):
                try:
                    base_color = '#E0E0FF' if (i // 3 + j // 3) % 2 == 0 else '#FFFFFF'
                    
                    if status == 'trying' and cell and cell == (i, j):
                        base_color = '#FFD700'  # Gold for trying
                    elif status == 'placed':
                        base_color = '#90EE90'  # Light green for placed
                    elif status == 'backtracking' and cell and cell == (i, j):
                        base_color = '#FF6347'  # Tomato red for backtracking
                    
                    self.cells[(i, j)].delete(0, tk.END)
                    if board[i][j] != 0:
                        self.cells[(i, j)].insert(0, str(board[i][j]))
                    
                    self.cells[(i, j)].config(bg=base_color)
                    self.stats_label.config(text=f"Attempts: {attempts}, Backtracks: {backtrack_count}")
                
                except Exception:
                    pass

    def generate_random_sudoku(self):
        """Generate a new random Sudoku puzzle."""
        self.clear_board()
        difficulty = self.difficulty_var.get()
        
        try:
            puzzle = SudokuGenerator.generate_puzzle(difficulty)
            for i in range(9):
                for j in range(9):
                    if puzzle[i][j] != 0:
                        self.cells[(i, j)].insert(0, str(puzzle[i][j]))
                        self.cells[(i, j)].config(state='disabled', fg='#000080')
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def create_board(self):
        """Create Sudoku board grid of Entry widgets."""
        board_frame = tk.Frame(self.master, bg='#f0f0f0')
        board_frame.pack(padx=20, pady=20)
        
        for i in range(9):
            for j in range(9):
                cell = tk.Entry(board_frame, width=3, 
                                font=('Helvetica', 18, 'bold'), 
                                justify='center', 
                                relief=tk.RAISED, 
                                borderwidth=3)
                
                # Alternate background colors to highlight 3x3 boxes
                bg_color = '#E0E0FF' if (i // 3 + j // 3) % 2 == 0 else '#FFFFFF'
                cell.configure(bg=bg_color, 
                               selectbackground='#4682B4', 
                               selectforeground='white')
                
                # Grid layout with extra padding to show 3x3 box divisions
                cell.grid(row=i, column=j, 
                          padx=2 if j % 3 != 0 else 4, 
                          pady=2 if i % 3 != 0 else 4, 
                          ipady=6)
                
                self.cells[(i, j)] = cell
                
                # Validate input to ensure only digits 1-9
                vcmd = (self.master.register(self.validate_input), '%P')
                cell.config(validate='key', validatecommand=vcmd)

    def validate_input(self, new_value):
        """
        Validate user input for Sudoku cells.
        
        Args:
            new_value (str): New cell value
        
        Returns:
            bool: Whether the input is valid
        """
        return len(new_value) <= 1 and (new_value == "" or (new_value.isdigit() and 0 <= int(new_value) <= 9))

    def clear_board(self):
        """Reset the Sudoku board to initial state."""
        for cell in self.cells.values():
            cell.config(state='normal')
            cell.delete(0, tk.END)
            bg_color = '#E0E0FF' if (cell.grid_info()['row'] // 3 + cell.grid_info()['column'] // 3) % 2 == 0 else '#FFFFFF'
            cell.config(bg=bg_color)
        
        self.time_label.config(text="")
        self.stats_label.config(text="Attempts: 0, Backtracks: 0")

    def create_buttons(self):
        """Create control buttons for Sudoku app."""
        button_frame = tk.Frame(self.master, bg='#f0f0f0')
        button_frame.pack(pady=10)
        
        buttons = [
            ("Solve", self.solve_sudoku_animated, '#4CAF50'),  # Green
            ("Generate", self.generate_random_sudoku, '#2196F3'),  # Blue
            ("Clear", self.clear_board, '#f44336')  # Red
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(button_frame, 
                            text=text, 
                            command=command, 
                            font=('Helvetica', 12), 
                            bg=color, 
                            fg='white', 
                            activebackground=color, 
                            relief=tk.RAISED)
            btn.pack(side=tk.LEFT, padx=5)

    def create_time_label(self):
        """Create label to display solving time."""
        self.time_label = tk.Label(self.master, 
                                   text="", 
                                   font=('Helvetica', 12), 
                                   bg='#f0f0f0')
        self.time_label.pack(pady=10)

    def create_stats_label(self):
        """Create label to display solving statistics."""
        self.stats_label = tk.Label(self.master, 
                                    text="Attempts: 0, Backtracks: 0", 
                                    font=('Helvetica', 12), 
                                    bg='#f0f0f0')
        self.stats_label.pack(pady=5)

def main():
    """Create and run the Sudoku GUI application."""
    root = tk.Tk()
    sudoku_gui = SudokuGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()