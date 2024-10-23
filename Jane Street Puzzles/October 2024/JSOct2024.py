"""
File: JSOct2024.py
Author: Jack Switzer
Date: October 5th, 2024
Description: This script solves the Knight's Tour puzzle for the Jane Street October 2024 puzzle.
             It finds three distinct positive integers A, B, and C, and two knight's paths on a 6x6 grid,
             both scoring exactly 2024 points according to specific scoring rules.
Version: 1.0
Python Version: 3.x
Dependencies: numpy, collections (deque), itertools (combinations, permutations)
"""

import numpy as np
from collections import deque
from itertools import combinations, permutations


class KnightPuzzleSolver:
    def __init__(self):
        # Initialize the 6x6 board with A, B, and C placements
        self.board = [
            ["A", "A", "A", "B", "B", "C"],  # row 1 (index 0, bottom)
            ["A", "A", "B", "B", "C", "C"],  # row 2 (index 1)
            ["A", "B", "B", "C", "C", "C"],  # row 3 (index 2)
            ["A", "B", "B", "C", "C", "C"],  # row 4 (index 3)
            ["A", "B", "B", "C", "C", "C"],  # row 5 (index 4)
            ["A", "B", "B", "C", "C", "C"]   # row 6 (index 5, top)
        ]
        # Define all possible knight moves as (x, y) offsets
        self.knight_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]

    def generate_paths(self, start, end, max_depth=15):
        """
        Generate all possible knight's paths from start to end within max_depth moves.
        Uses breadth-first search to explore paths.
        """
        paths = []
        queue = deque([(start, [start])])

        while queue:
            current_pos, path = queue.popleft()
            if current_pos == end:
                paths.append(path)
                continue
            if len(path) >= max_depth:
                continue
            for move in self.knight_moves:
                new_x = current_pos[0] + move[0]
                new_y = current_pos[1] + move[1]
                new_pos = (new_x, new_y)
                if 0 <= new_x < 6 and 0 <= new_y < 6 and new_pos not in path:
                    queue.append((new_pos, path + [new_pos]))

        return paths

    def calculate_score(self, path, values):
        """
        Calculate the score for a given path based on the scoring rules.
        """
        score = values['A']  # Start with A points
        for i in range(1, len(path)):
            x_prev, y_prev = path[i - 1]
            x_curr, y_curr = path[i]
            cell_prev = self.board[y_prev][x_prev]
            cell_curr = self.board[y_curr][x_curr]
            value_curr = values[cell_curr]
            if cell_prev != cell_curr:
                score *= value_curr  # Multiply if moving between different integers
            else:
                score += value_curr  # Add if moving within
        return score

    def solve_puzzle(self):
        # From a1 (0, 0) to f6 (5, 5)
        paths_a1_f6 = self.generate_paths((0, 0), (5, 5))

        # From a6 (0, 5) to f1 (5, 0)
        paths_a6_f1 = self.generate_paths((0, 5), (5, 0))

        valid_integers = range(1, 50)
        # Generate all combinations of 3 distinct integers whose sum is less than 50
        for nums in combinations(valid_integers, 3):
            if sum(nums) >= 50:
                continue
            # Consider all permutations (assignments of A, B, C)
            for perm in permutations(nums):
                values = {'A': perm[0], 'B': perm[1], 'C': perm[2]}
                for path1 in paths_a1_f6:
                    score1 = self.calculate_score(path1, values)
                    if score1 != 2024:
                        continue
                    for path2 in paths_a6_f1:
                        if set(path1).isdisjoint(set(path2)):
                            score2 = self.calculate_score(path2, values)
                            if score2 == 2024:
                                A, B, C = values['A'], values['B'], values['C']
                                return A, B, C, path1, path2
        return None

    @staticmethod
    def format_path(path):
        return ",".join(f"{chr(97 + x)}{y + 1}" for x, y in path)

    def visualize_solution(self, A, B, C, path1, path2):
        """
        Visualize the solution on the board with color-coding and consistent alignment.
        """
        # ANSI color codes
        RESET = '\033[0m'
        RED = '\033[91m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        BLUE = '\033[94m'
        MAGENTA = '\033[95m'

        # Create a copy of the board for visualization
        visual_board = [row[:] for row in self.board]
        
        # Check for overlaps
        overlap_exists = any(pos in path2 for pos in path1)

        # Mark the paths on the board
        for i, pos in enumerate(path1):
            x, y = pos
            if i == 0:
                visual_board[y][x] = f"{RED}1-S {RESET}"  # Start of path 1
            elif i == len(path1) - 1:
                visual_board[y][x] = f"{RED}1-E {RESET}"  # End of path 1
            else:
                visual_board[y][x] = f"{RED}1-{i:2}{RESET}"

        for i, pos in enumerate(path2):
            x, y = pos
            if i == 0:
                visual_board[y][x] = f"{BLUE}2-S {RESET}"  # Start of path 2
            elif i == len(path2) - 1:
                visual_board[y][x] = f"{BLUE}2-E {RESET}"  # End of path 2
            else:
                if "1-" in visual_board[y][x]:
                    visual_board[y][x] = f"{MAGENTA}BOTH{RESET}"  # Overlapping path
                else:
                    visual_board[y][x] = f"{BLUE}2-{i:2}{RESET}"
        
        # Prepare the column labels
        column_labels = '      ' + '    '.join(f'{chr(97 + i)}' for i in range(6))
        print(f"\nVisualization (A={YELLOW}{A}{RESET}, B={GREEN}{B}{RESET}, C={BLUE}{C}{RESET}):")
        print(column_labels)
        print("   +" + "----+" * 6)
        for y, row in enumerate(visual_board):
            row_str = f"{y + 1}  |"
            for cell in row:
                if cell == 'A':
                    row_str += f"{YELLOW} A  {RESET}|"
                elif cell == 'B':
                    row_str += f"{GREEN} B  {RESET}|"
                elif cell == 'C':
                    row_str += f"{BLUE} C  {RESET}|"
                else:
                    row_str += f"{cell}|"
            print(row_str)
            print("   +" + "----+" * 6)
        
        # If overlaps exist, add an extra line for better visualization
        if overlap_exists:
            print("\nNote: Overlapping paths are marked as BOTH in magenta.")

    def print_detailed_scoring(self, path1, path2, values):
        """
        Print detailed scoring for both paths side by side, including full mathematical expressions.
        """
        column_width = 45
        separator = "+" + "-" * column_width + "+" + "-" * column_width + "+"
        
        print("\nDetailed scoring for both paths:")
        print(separator)
        print("|{:^{width}}|{:^{width}}|".format("Path 1", "Path 2", width=column_width))
        print(separator)
        
        score1 = score2 = values['A']
        max_moves = max(len(path1), len(path2))
        
        print("|{:<{width}}|{:<{width}}|".format(f"Current Score: {score1}", f"Current Score: {score2}", width=column_width))
        print(separator)
        
        for i in range(1, max_moves):
            move1 = move2 = []
            if i < len(path1):
                x_prev, y_prev = path1[i - 1]
                x_curr, y_curr = path1[i]
                cell_prev = self.board[y_prev][x_prev]
                cell_curr = self.board[y_curr][x_curr]
                value_curr = values[cell_curr]
                if cell_prev != cell_curr:
                    new_score1 = score1 * value_curr
                    move1 = [f"{cell_prev}({x_prev+1},{y_prev+1}) to {cell_curr}({x_curr+1},{y_curr+1}):",
                             f"{score1} * {value_curr} = {new_score1}"]
                else:
                    new_score1 = score1 + value_curr
                    move1 = [f"{cell_prev}({x_prev+1},{y_prev+1}) to {cell_curr}({x_curr+1},{y_curr+1}):",
                             f"{score1} + {value_curr} = {new_score1}"]
                score1 = new_score1
            
            if i < len(path2):
                x_prev, y_prev = path2[i - 1]
                x_curr, y_curr = path2[i]
                cell_prev = self.board[y_prev][x_prev]
                cell_curr = self.board[y_curr][x_curr]
                value_curr = values[cell_curr]
                if cell_prev != cell_curr:
                    new_score2 = score2 * value_curr
                    move2 = [f"{cell_prev}({x_prev+1},{y_prev+1}) to {cell_curr}({x_curr+1},{y_curr+1}):",
                             f"{score2} * {value_curr} = {new_score2}"]
                else:
                    new_score2 = score2 + value_curr
                    move2 = [f"{cell_prev}({x_prev+1},{y_prev+1}) to {cell_curr}({x_curr+1},{y_curr+1}):",
                             f"{score2} + {value_curr} = {new_score2}"]
                score2 = new_score2
            
            for j in range(max(len(move1), len(move2))):
                line1 = move1[j] if j < len(move1) else ""
                line2 = move2[j] if j < len(move2) else ""
                print("|{:<{width}}|{:<{width}}|".format(line1, line2, width=column_width))
            
            print("|{:<{width}}|{:<{width}}|".format(f"Current Score: {score1}", f"Current Score: {score2}", width=column_width))
            print(separator)
        
        print("|{:^{width}}|{:^{width}}|".format(f"Final Score: {score1}", f"Final Score: {score2}", width=column_width))
        print(separator)

def main():
    solver = KnightPuzzleSolver()
    test_solution = "1,3,2,a1,c2,a3,c4,d6,b5,d4,f3,e5,c6,a5,b3,d2,e4,f6,a6,c5,d3,b4,a2,c3,e2,f4,d5,b6,a4,b2,d1,e3,f1"
    
    if test_solution:
        # Parse the test solution
        parts = test_solution.split(',')
        A, B, C = map(int, parts[:3])
        path1_positions = parts[3:3 + len(parts[3:]) // 2]
        path2_positions = parts[3 + len(parts[3:]) // 2:]

        # Convert positions to coordinates
        path1 = [(ord(pos[0]) - ord('a'), int(pos[1:]) - 1) for pos in path1_positions]
        path2 = [(ord(pos[0]) - ord('a'), int(pos[1:]) - 1) for pos in path2_positions]

        print("\nValidating and visualizing the given solution:")
        score1 = solver.calculate_score(path1, {'A': A, 'B': B, 'C': C})
        score2 = solver.calculate_score(path2, {'A': A, 'B': B, 'C': C})
        print(f"Path 1 score: {score1}")
        print(f"Path 2 score: {score2}")
        print(f"Sum of A, B, C: {A + B + C}")

        if score1 == 2024 and score2 == 2024:
            print("The given solution is valid.")
        else:
            print("The given solution is not valid.")

        solver.visualize_solution(A, B, C, path1, path2)
        solver.print_detailed_scoring(path1, path2, {'A': A, 'B': B, 'C': C})
    else:
        result = solver.solve_puzzle()
        if result:
            A, B, C, path1, path2 = result
            formatted_path1 = solver.format_path(path1)
            formatted_path2 = solver.format_path(path2)
            solved_solution = f"{A},{B},{C},{formatted_path1},{formatted_path2}"
            print(f"Solution: {solved_solution}")

            # Proceed to validate and visualize the solution
            positions = (formatted_path1 + ',' + formatted_path2).split(',')

            # Since paths might have different lengths, determine splits based on known start positions
            path1_positions = formatted_path1.split(',')
            path2_positions = formatted_path2.split(',')

            # Convert positions to coordinates
            path1 = [(ord(pos[0]) - ord('a'), int(pos[1:]) - 1) for pos in path1_positions]
            path2 = [(ord(pos[0]) - ord('a'), int(pos[1:]) - 1) for pos in path2_positions]

            print("\nValidating and visualizing the given solution:")
            score1 = solver.calculate_score(path1, {'A': A, 'B': B, 'C': C})
            score2 = solver.calculate_score(path2, {'A': A, 'B': B, 'C': C})
            print(f"Path 1 score: {score1}")
            print(f"Path 2 score: {score2}")
            print(f"Sum of A, B, C: {A + B + C}")

            if score1 == 2024 and score2 == 2024:
                print("The given solution is valid.")
            else:
                print("The given solution is not valid.")

            solver.visualize_solution(A, B, C, path1, path2)
            solver.print_detailed_scoring(path1, path2, {'A': A, 'B': B, 'C': C})
        else:
            print("No solution found.")

if __name__ == "__main__":
    main()