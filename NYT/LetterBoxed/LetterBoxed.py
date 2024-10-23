# Letter Boxed Puzzle Solver by Jack Switzer
import json
from collections import deque
import os
import pickle
import sys
from config import *

def load_lb_data():
    file_path = get_daily_data_path(TODAY)
    if not os.path.exists(file_path):
        print(f"Error: Daily data for {TODAY} is not available at {file_path}", file=sys.stderr)
        sys.exit(1)
    
    with open(file_path, 'r') as f:
        puzzle_data = json.load(f)
    
    return {side: set(puzzle_data[side]) for side in PUZZLE_SIDES}

def load_dictionary():
    if not os.path.exists(PROCESSED_DICT_PATH):
        print(f"Error: Processed dictionary not found at {PROCESSED_DICT_PATH}. Run process_dictionary.py first.", file=sys.stderr)
        sys.exit(1)
    
    with open(PROCESSED_DICT_PATH, 'rb') as f:
        return pickle.load(f)

def get_side(letter, sides):
    return next((side for side, letters in sides.items() if letter in letters), None)

def is_valid_word(word, sides):
    previous_side = None
    for letter in word:
        current_side = get_side(letter, sides)
        if current_side is None or current_side == previous_side:
            return False
        previous_side = current_side
    return True

def find_valid_words(all_letters, sides, valid_words):
    return {word for word in valid_words if set(word).issubset(all_letters) and is_valid_word(word, sides)}

def find_shortest_path(words, all_letters):
    queue = deque([([], set(), '')])
    shortest_solution = None

    while queue:
        current_sequence, used_letters, last_letter = queue.popleft()
        if used_letters == all_letters:
            return current_sequence
        
        for word in words:
            if word[0] == last_letter or not last_letter:
                new_used_letters = used_letters.union(set(word))
                if len(new_used_letters) > len(used_letters):
                    new_sequence = current_sequence + [word]
                    if shortest_solution is None or len(new_sequence) < len(shortest_solution):
                        queue.append((new_sequence, new_used_letters, word[-1]))
                        if len(new_used_letters) == len(all_letters):
                            shortest_solution = new_sequence
                            break

    return shortest_solution

def main():
    lb_data = load_lb_data()
    all_letters = set().union(*lb_data.values())

    print("Loading dictionary...")
    valid_words = load_dictionary()
    print("Dictionary loaded.")

    print("Finding valid words for the puzzle...")
    valid_words_found = find_valid_words(all_letters, lb_data, valid_words)
    print(f"Found {len(valid_words_found)} valid words.")

    print("Searching for the shortest solution...")
    shortest_path = find_shortest_path(valid_words_found, all_letters)

    if shortest_path:
        print("\nShortest sequence of words that uses all letters:")
        print(" -> ".join(f"{word} ({len(word)})" for word in shortest_path))
        print(f"Total words: {len(shortest_path)}")
    else:
        print("\nNo valid sequence found that uses all letters.")

if __name__ == "__main__":
    main()
