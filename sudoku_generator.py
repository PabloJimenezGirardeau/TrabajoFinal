import numpy as np
import random
from sudoku_solver import SudokuSolver

class SudokuGenerator:
    @staticmethod
    def generate_puzzle(difficulty='medium'):
        """
        Generate a Sudoku puzzle with a specified difficulty level.
        
        Args:
            difficulty (str): Difficulty level - 'easy', 'medium', 'hard', or 'expert'
        
        Returns:
            numpy.ndarray: A 9x9 Sudoku puzzle with some cells removed
        """
        difficulty_settings = {
            'easy': (0.3, 30),
            'medium': (0.5, 40),
            'hard': (0.7, 50),
            'expert': (0.8, 60)
        }
        diff_param, max_attempts = difficulty_settings.get(difficulty, (0.5, 40))
        
        attempts = 0
        while attempts < max_attempts:
            # Create a fully solved Sudoku puzzle
            base_puzzle = np.zeros((9, 9), dtype=int)
            solver = SudokuSolver(base_puzzle)
            solver.solve_with_visualization(False)
            puzzle = solver.sudoku.copy()
            
            # Randomly remove cells
            cells = [(i, j) for i in range(9) for j in range(9)]
            random.shuffle(cells)
            remove_count = int(81 * diff_param)
            
            for i, j in cells[:remove_count]:
                puzzle[i][j] = 0
            
            # Verify the puzzle has a unique solution
            test_solver = SudokuSolver(puzzle)
            if test_solver.solve_with_visualization(False) is not None:
                return puzzle
            
            attempts += 1
        
        raise Exception("Could not generate a valid Sudoku puzzle")