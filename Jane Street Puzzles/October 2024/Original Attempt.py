import itertools

class KnightPuzzleSolver:
    def __init__(self):
        self.board = [
            ["A", "A", "A", "B", "B", "C"],  # row 1
            ["A", "A", "B", "B", "C", "C"],  # row 2
            ["A", "B", "B", "C", "C", "C"],  # row 3
            ["A", "B", "B", "C", "C", "C"],  # row 4
            ["A", "B", "B", "C", "C", "C"],  # row 5
            ["A", "B", "B", "C", "C", "C"]   # row 6
        ]

    def print_board(self):
        for row in self.board[::-1]:
            print(row)

    def initialize_values(self, A, B, C):
        mapping = {"A": A, "B": B, "C": C}
        return [[mapping[cell] for cell in row] for row in self.board]

    def generate_knight_moves(self, x, y):
        # Generate all potential knight moves
        potential_moves = [
            (x + 2, y + 1), (x + 2, y - 1), (x - 2, y + 1), (x - 2, y - 1),
            (x + 1, y + 2), (x + 1, y - 2), (x - 1, y + 2), (x - 1, y - 2)
        ]
        # Filter moves to ensure they remain within the board bounds
        return [(new_x, new_y) for new_x, new_y in potential_moves if 0 <= new_x < 6 and 0 <= new_y < 6]

    def calculate_trip_score(self, path, A, B, C):
        board_values = self.initialize_values(A, B, C)
        score = board_values[path[0][1]][path[0][0]]  # Starting point score
        
        for i in range(1, len(path)):
            prev_x, prev_y = path[i - 1]
            cur_x, cur_y = path[i]
            prev_value = board_values[prev_y][prev_x]
            cur_value = board_values[cur_y][cur_x]
            if prev_value != cur_value:
                score *= cur_value
            else:
                score += cur_value
        
        return score

    def find_knight_trip(self, start, end, A, B, C):
        stack = [(start, [start])]
        visited_positions = set()  # To avoid revisiting the same positions
        
        while stack:
            current_position, path = stack.pop()
            
            # If we reach the end and the path is longer than 1, we have found a solution
            if current_position == end and len(path) > 1:
                return path
            
            # Generate valid knight moves from the current position
            for move in self.generate_knight_moves(*current_position):
                if move not in visited_positions:
                    stack.append((move, path + [move]))
                    visited_positions.add(move)
        
        return None

    def solve_puzzle(self):
        min_sum = float('inf')
        best_values = None
        best_paths = None

        # Iterate over combinations of A, B, and C that are distinct and positive
        for A, B, C in itertools.permutations(range(1, 20), 3):
            if A + B + C >= min_sum:
                continue

            # Find paths from (0, 0) to (5, 5) and from (0, 5) to (5, 0)
            path1 = self.find_knight_trip((0, 0), (5, 5), A, B, C)
            path2 = self.find_knight_trip((0, 5), (5, 0), A, B, C)

            if path1 and path2:
                score1 = self.calculate_trip_score(path1, A, B, C)
                score2 = self.calculate_trip_score(path2, A, B, C)

                if score1 == 2024 and score2 == 2024:
                    current_sum = A + B + C
                    if current_sum < min_sum:
                        min_sum = current_sum
                        best_values = (A, B, C)
                        best_paths = (path1, path2)

        if best_values:
            A, B, C = best_values
            path1, path2 = best_paths
            formatted_path1 = ",".join([f"{chr(97 + x)}{y + 1}" for x, y in path1])
            formatted_path2 = ",".join([f"{chr(97 + x)}{y + 1}" for x, y in path2])
            print(f"Solution: {A},{B},{C},{formatted_path1},{formatted_path2}")
        else:
            print("No solution found.")

# Example usage
solver = KnightPuzzleSolver()
print("Initial Board Configuration:")
solver.print_board()
solver.solve_puzzle()
