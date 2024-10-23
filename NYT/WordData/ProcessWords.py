import requests
import spacy
import pickle
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import *


def download_raw_dictionary():
    # Download raw dictionary from GitHub
    print("Downloading raw dictionary...")
    with requests.get(RAW_DICT_URL, stream=True) as response:
        response.raise_for_status()
        content = []
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE, decode_unicode=True):
            if chunk:
                content.append(chunk)
    return ''.join(content).splitlines()

def is_common_word(word):
    # Check if word is in spaCy's vocabulary
    return word.lower() in nlp.vocab.strings

def process_word(word, min_length, max_length):
    # Process a single word based on length and commonness
    if min_length <= len(word) <= max_length and word.isalpha() and is_common_word(word):
        return word.upper()
    return None

def process_dictionary(game_type):
    # Process the entire dictionary for a specific game type
    print(f"Processing dictionary for {game_type}...")
    raw_words = download_raw_dictionary()
    
    config = GAME_CONFIGS[game_type]
    min_length = config["min_length"]
    max_length = config["max_length"]
    
    DATA_DIR = config["data_dir"]
    
    processed_words = set()
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_word, word, min_length, max_length) for word in raw_words]
        for future in as_completed(futures):
            result = future.result()
            if result:
                processed_words.add(result)
    
    filename = os.path.join(DATA_DIR, config["filename"])
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(filename, 'wb') as f:
        pickle.dump(processed_words, f)
    
    print(f"Processed dictionary for {game_type} saved to {filename}")
    print(f"Total words processed: {len(processed_words)}")

if __name__ == "__main__":
    # Load spaCy model
    print("Loading spaCy model...")
    nlp = spacy.load("en_core_web_sm")

    process_dictionary("LetterBoxed")
    process_dictionary("spelling_bee")
