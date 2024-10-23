import requests
from collections import Counter


# Input variables
MANDATORY_CHAR = 'r'
OPTIONAL_CHARS = 'gulbay'
MAX_CHARS = 11

# URL for the word list
WORD_LIST_URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words.txt"

def download_word_list(url):
    """Download the word list from the given URL."""
    response = requests.get(url)
    if response.status_code == 200:
        return set(word.strip().lower() for word in response.text.split())
    else:
        raise Exception("Failed to download word list")

def filter_nyt_words(words):
    """Filter words to match NYT Spelling Bee criteria."""
    nyt_words = set()
    for word in words:
        # Remove words shorter than 4 letters
        if len(word) < 4:
            continue
        # Remove proper nouns (words starting with a capital letter)
        if word[0].isupper():
            continue
        # Remove obscure words (you might need a separate list of common words)
        # if word not in common_words:
        #     continue
        # Add more filters as needed
        nyt_words.add(word)
    return nyt_words

def is_valid_word(word, mandatory_char, allowed_chars):
    """Check if a word is valid for the Spelling Bee game."""
    return (len(word) >= 4 and
            mandatory_char in word and
            all(char in allowed_chars for char in word))

def find_valid_words(mandatory_char, optional_chars, word_list):
    """Find all valid words for the Spelling Bee game."""
    allowed_chars = set(optional_chars + mandatory_char)
    
    return sorted(
        (word for word in word_list 
         if is_valid_word(word, mandatory_char, allowed_chars)),
        key=len, reverse=True
    )

def main():
    try:
        # Download the word list
        word_list = download_word_list(WORD_LIST_URL)

        # Find all valid words
        valid_words = find_valid_words(MANDATORY_CHAR, OPTIONAL_CHARS, word_list)
        
        # Filter words to match NYT criteria
        nyt_words = filter_nyt_words(valid_words)
        
        # Output the results
        if nyt_words:
            print(f"Found {len(nyt_words)} valid NYT Spelling Bee words:")
            for word in sorted(nyt_words, key=len, reverse=True):
                print(word)
        else:
            print("No valid NYT Spelling Bee words found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def verify_word(word, mandatory_char, allowed_chars):
    """Verify and explain why a word is valid."""
    reasons = []
    if 4 <= len(word) <= MAX_CHARS:
        reasons.append("Length OK")
    else:
        reasons.append("Invalid length")
    
    if mandatory_char in word:
        reasons.append("Contains mandatory char")
    else:
        reasons.append("Missing mandatory char")
    
    if all(char in allowed_chars for char in word):
        reasons.append("All chars allowed")
    else:
        reasons.append("Contains invalid chars")
    
    return ", ".join(reasons)

if __name__ == "__main__":
    main()
