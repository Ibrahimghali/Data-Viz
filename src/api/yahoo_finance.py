import http.client
import json
import logging
from pathlib import Path

from src.config.config import RAPIDAPI_KEY, RAPIDAPI_HOST, DATA_DIR
from src.models.stock import Stock

logger = logging.getLogger(__name__)

def get_headers():
    """Get API headers using credentials from config."""
    return {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': RAPIDAPI_HOST
    }

def fetch_stock_data(ticker, headers=None):
    """Fetch stock data for a single ticker."""
    if headers is None:
        headers = get_headers()
        
    conn = http.client.HTTPSConnection(RAPIDAPI_HOST)
    
    try:
        conn.request("GET", f"/api/yahoo/qu/quote/{ticker}", headers=headers)
        res = conn.getresponse()
        data = res.read()
        return json.loads(data.decode("utf-8"))
    except Exception as e:
        logger.error(f"Error fetching data for {ticker}: {e}")
        return None
    finally:
        conn.close()

def parse_stock_data(quote, ticker):
    """Parse the API response into a structured format."""
    try:
        q = quote['body'][0]  # Data is in the 'body' array
        return {
            # Basic stock info
            "symbol": q["symbol"],
            "name": q.get("longName"),
            "price": q.get("regularMarketPrice"),
            "change": q.get("regularMarketChange"),
            "percent": q.get("regularMarketChangePercent"),
            "volume": q.get("regularMarketVolume"),
            "range": f"{q.get('regularMarketDayLow')} - {q.get('regularMarketDayHigh')}",
            
            # Additional financial data
            "market_cap": q.get("marketCap"),
            "pe_ratio": q.get("trailingPE"),
            "eps": q.get("epsTrailingTwelveMonths"),
            "52wk_range": f"{q.get('fiftyTwoWeekLow')} - {q.get('fiftyTwoWeekHigh')}",
            "dividend_yield": q.get("dividendYield"),
            "avg_volume": q.get("averageDailyVolume3Month"),
            "analyst_rating": q.get("averageAnalystRating"),
            "currency": q.get("currency")
        }
    except (KeyError, IndexError) as e:
        logger.error(f"Error parsing data for {ticker}: {e}")
        logger.debug(f"Response structure: {quote}")
        return None

def get_stock_data(tickers):
    """Get stock data for a list of tickers."""
    headers = get_headers()
    results = []
    
    for ticker in tickers:
        logger.info(f"Fetching data for {ticker}...")
        quote = fetch_stock_data(ticker, headers)
        if quote:
            stock_data = parse_stock_data(quote, ticker)
            if stock_data:
                results.append(stock_data)
    
    return results

def save_to_json(data, filename="stock_data.json"):
    """Save data to a JSON file."""
    try:
        # Create data directory if it doesn't exist
        data_dir = Path(DATA_DIR)
        data_dir.mkdir(exist_ok=True)
        
        file_path = data_dir / filename
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        logger.info(f"Data saved to {file_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving data to {filename}: {e}")
        return False

def load_from_json(filename="stock_data.json"):
    """Load stock data from JSON file."""
    try:
        file_path = Path(DATA_DIR) / filename
        with open(file_path, 'r') as json_file:
            return json.load(json_file)
    except Exception as e:
        logger.error(f"Error loading data from {filename}: {e}")
        return None

def display_results(results):
    """Display formatted stock data results."""
    for r in results:
        if not r:
            continue
            
        print(f"\n===== {r['symbol']} - {r['name']} =====")
        print(f"Price: {r['price']} {r['currency']} ({r['change']:+.2f}, {r['percent']:+.2f}%)")
        print(f"Volume: {r['volume']:,} (Avg: {r['avg_volume']:,})")
        print(f"Day Range: {r['range']}")
        print(f"52-Week Range: {r['52wk_range']}")
        print(f"Market Cap: ${r['market_cap']:,}")
        print(f"P/E Ratio: {r['pe_ratio']}")
        print(f"EPS: {r['eps']}")
        print(f"Dividend Yield: {r['dividend_yield'] if r['dividend_yield'] is not None else 'N/A'}%")
        print(f"Analyst Rating: {r['analyst_rating']}")