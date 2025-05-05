# filepath: c:\Users\Ibrahim\Documents\WORK\Faculty-Projects\Data-Viz\src\config.py
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API configuration
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST", "yahoo-finance15.p.rapidapi.com")

# Default stocks to track
DEFAULT_TICKERS = ["AAPL", "GOOG", "MSFT", "TSLA"]

# Data storage
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")