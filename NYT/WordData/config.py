# Constants
RAW_DICT_URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
CHUNK_SIZE = 1024 * 1024  # 1MB chunks

# Game configurations
GAME_CONFIGS = {
    "LetterBoxed": {
        "min_length": 3,
        "max_length": 15,
        "filename": "ProcessedDictionaryLetterBoxed.pkl",
        "data_dir": "LetterBoxed/Data"
    },
    "spelling_bee": {
        "min_length": 4,
        "max_length": 20,
        "filename": "ProcessedDictionarySpellingBee.pkl",
        "data_dir": "SpellingBee/Data"
    }
}
