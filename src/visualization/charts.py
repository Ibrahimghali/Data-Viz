import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path
import logging

from src.api.yahoo_finance import load_from_json

logger = logging.getLogger(__name__)

def load_stock_data(json_file="stock_data.json"):
    """Load stock data for visualization."""
    data = load_from_json(json_file)
    if not data:
        logger.error("Failed to load stock data")
        return None
    return data

def create_stock_dataframe(data):
    """Convert stock data to pandas DataFrame."""
    if not data:
        return None
    return pd.DataFrame(data)

def plot_price_comparison(stocks_data, save_path=None):
    """Create a bar chart comparing current stock prices."""
    df = create_stock_dataframe(stocks_data)
    if df is None:
        return
    
    plt.figure(figsize=(12, 6))
    
    # Create bar chart
    bars = plt.bar(df['symbol'], df['price'], color=['#2196F3', '#4CAF50', '#FFC107', '#F44336'])
    
    # Add price labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 5,
                f'${height:.2f}', ha='center', va='bottom', fontweight='bold')
    
    # Customize chart
    plt.title('Stock Price Comparison', fontsize=18)
    plt.xlabel('Stock Symbol', fontsize=14)
    plt.ylabel('Price (USD)', fontsize=14)
    plt.grid(axis='y', alpha=0.3)
    
    # Add company names as annotations
    for i, (symbol, name) in enumerate(zip(df['symbol'], df['name'])):
        plt.annotate(name, (i, 0), xytext=(0, -30), 
                    textcoords='offset points', ha='center', fontsize=10)
    
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
        logger.info(f"Chart saved to {save_path}")
    
    plt.tight_layout()
    return plt

def plot_performance_comparison(stocks_data, save_path=None):
    """Create a horizontal bar chart comparing stock performance (% change)."""
    df = create_stock_dataframe(stocks_data)
    if df is None:
        return
    
    plt.figure(figsize=(12, 6))
    
    # Sort by percent change
    df = df.sort_values('percent')
    
    # Define colors based on positive/negative change
    colors = ['#F44336' if x < 0 else '#4CAF50' for x in df['percent']]
    
    # Create horizontal bar chart
    bars = plt.barh(df['symbol'], df['percent'], color=colors)
    
    # Add percent labels
    for bar in bars:
        width = bar.get_width()
        label_x = width + 0.3 if width > 0 else width - 0.3
        plt.text(label_x, bar.get_y() + bar.get_height()/2, 
                f'{width:+.2f}%', ha='center', va='center', fontweight='bold')
    
    # Customize chart
    plt.title('Stock Performance Comparison (% Change)', fontsize=18)
    plt.xlabel('Percent Change (%)', fontsize=14)
    plt.axvline(x=0, color='black', linestyle='-', alpha=0.3)
    plt.grid(axis='x', alpha=0.3)
    
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
        logger.info(f"Chart saved to {save_path}")
    
    plt.tight_layout()
    return plt

def plot_market_cap_comparison(stocks_data, save_path=None):
    """Create a pie chart comparing market capitalization."""
    df = create_stock_dataframe(stocks_data)
    if df is None:
        return
    
    plt.figure(figsize=(10, 8))
    
    # Convert market cap to billions for readability
    market_caps_billions = [cap/1e9 for cap in df['market_cap']]
    
    # Create pie chart
    plt.pie(market_caps_billions, labels=df['symbol'], autopct='%1.1f%%', 
            startangle=90, shadow=False, explode=[0.05]*len(df),
            colors=['#2196F3', '#4CAF50', '#FFC107', '#F44336'])
    
    # Add title and customize
    plt.title('Market Capitalization Comparison (in billions USD)', fontsize=18)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    
    # Add legend with both symbol and full name
    labels = [f"{symbol} - {name}" for symbol, name in zip(df['symbol'], df['name'])]
    plt.legend(labels, loc="best", fontsize=10)
    
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
        logger.info(f"Chart saved to {save_path}")
    
    return plt

def generate_all_charts(output_dir="charts"):
    """Generate all stock charts and save to the specified directory."""
    try:
        # Prepare output directory
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Load stock data
        stocks_data = load_stock_data()
        if not stocks_data:
            return False
        
        # Generate and save charts
        plot_price_comparison(stocks_data, save_path=output_path/"price_comparison.png")
        plot_performance_comparison(stocks_data, save_path=output_path/"performance_comparison.png")
        plot_market_cap_comparison(stocks_data, save_path=output_path/"market_cap_comparison.png")
        
        logger.info(f"All charts generated and saved to {output_dir}")
        return True
    except Exception as e:
        logger.error(f"Error generating charts: {e}")
        return False