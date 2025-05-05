import sys
import os
from pathlib import Path

# Add the project root to the Python path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from src.utils.logger import setup_logger
from src.api.yahoo_finance import get_stock_data, save_to_json, display_results
from src.visualization.charts import generate_all_charts
from src.config.config import DEFAULT_TICKERS

def main():
    """Main function to run the stock data retrieval and visualization process."""
    # Setup logging
    logger = setup_logger(log_file=root_dir/"logs"/"stock_app.log")
    logger.info("Starting stock data application")
    
    try:
        # Fetch and process stock data
        logger.info(f"Fetching data for tickers: {DEFAULT_TICKERS}")
        results = get_stock_data(DEFAULT_TICKERS)
        
        if not results:
            logger.error("No stock data retrieved")
            return
            
        # Save data
        save_to_json(results)
        
        # Display results
        display_results(results)
        
        # Generate charts
        logger.info("Generating visualization charts")
        charts_dir = root_dir / "charts"
        generate_all_charts(output_dir=charts_dir)
        
        logger.info("Stock data processing completed successfully")
        
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    main()