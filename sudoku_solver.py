import numpy as np
import time

class SudokuSolver:
    def __init__(self, sudoku, callback=None):
        """
        Initialize the Sudoku solver with advanced strategies.
        
        Args:
            sudoku (numpy.ndarray): Initial Sudoku grid
            callback (function, optional): Function to call during solving for visualization
        """
        self.bitmap = np.ones((9, 9, 9), dtype=bool)
        self.sudoku = np.zeros((9, 9), dtype=int)
        self.callback = callback
        self.attempts = 0
        self.backtrack_count = 0
        
        # Place initial known numbers
        for i in range(9):
            for j in range(9):
                if sudoku[i][j] != 0:
                    self.place_number(i, j, sudoku[i][j])

    def solve_with_visualization(self, visualize=True, delay=0.1):
        """
        Solve the Sudoku puzzle with optional visualization using advanced strategies.
        
        Args:
            visualize (bool): Whether to use visualization
            delay (float): Delay between solving steps
        
        Returns:
            numpy.ndarray or None: Solved Sudoku grid or None if no solution
        """
        start = time.time()
        self.visualize = visualize
        self.attempts = 0
        self.backtrack_count = 0
        
        # Use the advanced backtracking method
        result = self.advanced_backtrack_visualize(delay) if visualize else self.advanced_backtrack()
        
        end = time.time()
        self.solve_time = end - start
        
        return result

    def advanced_least_options_cell(self):
        """
        Select the cell with the least number of options 
        and with the most strategic impact.
        
        Returns:
            tuple: Coordinates of the strategic cell
        """
        # Create an impact matrix
        impact_matrix = np.zeros((9, 9), dtype=float)
        
        for i in range(9):
            for j in range(9):
                if self.sudoku[i][j] == 0:
                    # Count available options
                    options_count = np.sum(self.bitmap[i][j])
                    
                    # Calculate impact based on empty spaces in row, column, and box
                    row_empty = 9 - np.count_nonzero(self.sudoku[i, :])
                    col_empty = 9 - np.count_nonzero(self.sudoku[:, j])
                    
                    # Calculate the 3x3 box
                    box_i, box_j = i // 3 * 3, j // 3 * 3
                    box_empty = 9 - np.count_nonzero(self.sudoku[box_i:box_i+3, box_j:box_j+3])
                    
                    # Calculate an impact score
                    impact_score = (row_empty + col_empty + box_empty) / (options_count + 1)
                    
                    impact_matrix[i, j] = impact_score
        
        # Mask for empty cells
        empty_cells_mask = self.sudoku == 0
        
        # If no empty cells, raise exception
        if not np.any(empty_cells_mask):
            raise ValueError("No empty cells left")
        
        # Find the cell with the highest strategic impact
        impact_matrix[~empty_cells_mask] = -1
        return np.unravel_index(np.argmax(impact_matrix), impact_matrix.shape)

    def smart_number_ordering(self, i, j):
        """
        Order candidate numbers based on their probability of success.
        
        Args:
            i (int): Row of the cell
            j (int): Column of the cell
        
        Returns:
            list: Numbers ordered by probability of success
        """
        # Get possible numbers
        possible_numbers = [num+1 for num in range(9) if self.bitmap[i][j][num]]
        
        # Calculate frequency of numbers in row, column, and box
        def number_frequency_score(number):
            row_freq = np.sum(self.sudoku[i, :] == number)
            col_freq = np.sum(self.sudoku[:, j] == number)
            
            # Calculate frequency in the 3x3 box
            box_i, box_j = i // 3 * 3, j // 3 * 3
            box_freq = np.sum(self.sudoku[box_i:box_i+3, box_j:box_j+3] == number)
            
            return -(row_freq + col_freq + box_freq)
        
        # Sort numbers based on their frequency
        return sorted(possible_numbers, key=number_frequency_score)

    def advanced_backtrack_visualize(self, delay=0.1):
        """
        Advanced backtracking method with intelligent cell and number selection.
        
        Args:
            delay (float): Delay between solving steps
        
        Returns:
            numpy.ndarray or None: Solved Sudoku grid or None if no solution
        """
        self.attempts += 1
        
        if self.is_solved():
            return self.sudoku
        
        if self.callback and self.visualize:
            self.callback(self.sudoku.copy(), status='searching', attempts=self.attempts, backtrack_count=self.backtrack_count)
            time.sleep(delay)
        
        try:
            # Use improved cell selection
            i, j = self.advanced_least_options_cell()
        except ValueError:
            return None
        
        # Get intelligently ordered numbers
        numbers = self.smart_number_ordering(i, j)
        
        for number in numbers:
            if self.can_place_number(i, j, number):
                # Save current state
                curr_bitmap = self.bitmap.copy()
                curr_sudoku = self.sudoku.copy()
                
                if self.callback and self.visualize:
                    self.callback(self.sudoku.copy(), status='trying', cell=(i, j), number=number, attempts=self.attempts, backtrack_count=self.backtrack_count)
                    time.sleep(delay)
                
                # Place number and perform trivial moves
                self.place_number(i, j, number)
                self.trivial_moves()
                
                if self.callback and self.visualize:
                    self.callback(self.sudoku.copy(), status='placed', attempts=self.attempts, backtrack_count=self.backtrack_count)
                    time.sleep(delay)
                
                # Recursively try to solve
                result = self.advanced_backtrack_visualize(delay)
                
                if result is not None:
                    return result
                
                # Backtrack if no solution found
                self.backtrack_count += 1
                
                if self.callback and self.visualize:
                    self.callback(curr_sudoku.copy(), status='backtracking', cell=(i, j), attempts=self.attempts, backtrack_count=self.backtrack_count)
                    time.sleep(delay)
                
                # Restore previous state
                self.bitmap = curr_bitmap
                self.sudoku = curr_sudoku
        
        return None

    def advanced_backtrack(self):
        """
        Advanced backtracking method without visualization.
        
        Returns:
            numpy.ndarray or None: Solved Sudoku grid or None if no solution
        """
        if self.is_solved():
            return self.sudoku
        
        try:
            i, j = self.advanced_least_options_cell()
        except ValueError:
            return None
        
        # Get intelligently ordered numbers
        numbers = self.smart_number_ordering(i, j)
        
        for number in numbers:
            if self.can_place_number(i, j, number):
                # Save current state
                curr_bitmap = self.bitmap.copy()
                curr_sudoku = self.sudoku.copy()
                
                # Place number and perform trivial moves
                self.place_number(i, j, number)
                self.trivial_moves()
                
                # Recursively try to solve
                result = self.advanced_backtrack()
                
                if result is not None:
                    return result
                
                # Backtrack if no solution found
                self.backtrack_count += 1
                
                # Restore previous state
                self.bitmap = curr_bitmap
                self.sudoku = curr_sudoku
        
        return None

    def is_solved(self):
        """Check if the Sudoku is completely filled."""
        return np.sum(self.sudoku == 0) == 0

    def can_place_number(self, i, j, number):
        """
        Check if a number can be placed in a specific cell.
        
        Args:
            i (int): Row index
            j (int): Column index
            number (int): Number to place
        
        Returns:
            bool: Whether the number can be placed
        """
        return self.bitmap[i][j][number-1]

    def place_number(self, i, j, number):
        """
        Place a number in a specific cell and update bitmap.
        
        Args:
            i (int): Row index
            j (int): Column index
            number (int): Number to place
        """
        self.sudoku[i][j] = number
        self.bitmap[i][j] = np.zeros(9, dtype=bool)
        
        # Eliminate number from same row and column
        for k in range(9):
            self.bitmap[i][k][number-1] = False
            self.bitmap[k][j][number-1] = False
        
        # Eliminate number from 3x3 box
        for k in range(3):
            for l in range(3):
                self.bitmap[i//3*3+k][j//3*3+l][number-1] = False

    def trivial_moves(self):
        """Perform trivial moves where only one option exists for a cell."""
        changed = True
        while changed:
            changed = False
            for i in range(9):
                for j in range(9):
                    if self.is_trivial_cell(i, j):
                        changed = True
                        self.place_number(i, j, np.argmax(self.bitmap[i][j]) + 1)

    def is_trivial_cell(self, i, j):
        """
        Check if a cell has only one possible option.
        
        Args:
            i (int): Row index
            j (int): Column index
        
        Returns:
            bool: Whether the cell has only one option
        """
        return self.sudoku[i][j] == 0 and np.sum(self.bitmap[i][j]) == 1