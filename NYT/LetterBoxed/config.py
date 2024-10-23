import os
from datetime import datetime

# Base directory for the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PROCESSED_DICT_PATH = os.path.join(BASE_DIR, "Data", "ProcessedDictionaryLetterBoxed.pkl")
DATE_FORMAT = "%d%m%Y"
DAILY_DATA_DIR = os.path.join(BASE_DIR, "Data", "DailyData")
PUZZLE_SIDES = ['TOP', 'LEFT', 'BOTTOM', 'RIGHT']

# Constant for today's date
TODAY = datetime.now().strftime(DATE_FORMAT)

# Function to generate the correct file path for a given date
def get_daily_data_path(date):
    return os.path.join(DAILY_DATA_DIR, f"LB_{date}.json")
