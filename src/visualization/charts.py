import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path
import logging
import matplotlib.cm as cm
from matplotlib.patches import Rectangle

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

def plot_volume_comparison(stocks_data, save_path=None):
    """Create a bar chart comparing trading volumes."""
    df = create_stock_dataframe(stocks_data)
    if df is None:
        return
    
    plt.figure(figsize=(12, 6))
    
    # Convert volume to millions for readability
    volumes_millions = [vol/1e6 for vol in df['volume']]
    avg_volumes_millions = [vol/1e6 for vol in df['avg_volume']]
    
    # Position bars
    x = np.arange(len(df['symbol']))
    width = 0.35
    
    # Create grouped bar chart
    bars1 = plt.bar(x - width/2, volumes_millions, width, label='Current Volume', color='#2196F3')
    bars2 = plt.bar(x + width/2, avg_volumes_millions, width, label='3-Month Avg Volume', color='#9C27B0', alpha=0.7)
    
    # Add volume labels
    for bar in bars1:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}M', ha='center', va='bottom', fontsize=9)
    
    # Customize chart
    plt.title('Trading Volume Comparison', fontsize=18)
    plt.xlabel('Stock Symbol', fontsize=14)
    plt.ylabel('Volume (Millions)', fontsize=14)
    plt.xticks(x, df['symbol'])
    plt.grid(axis='y', alpha=0.3)
    plt.legend()
    
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
        logger.info(f"Chart saved to {save_path}")
    
    plt.tight_layout()
    return plt

def plot_pe_ratio_comparison(stocks_data, save_path=None):
    """Create a horizontal bar chart comparing P/E ratios."""
    df = create_stock_dataframe(stocks_data)
    if df is None:
        return
    
    plt.figure(figsize=(12, 6))
    
    # Sort by PE ratio
    df = df.sort_values('pe_ratio')
    
    # Create horizontal bar chart with gradient color based on P/E value
    norm = plt.Normalize(df['pe_ratio'].min(), df['pe_ratio'].max())
    colors = cm.viridis(norm(df['pe_ratio']))
    
    bars = plt.barh(df['symbol'], df['pe_ratio'], color=colors)
    
    # Add PE ratio labels
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 1, bar.get_y() + bar.get_height()/2, 
                f'{width:.2f}', ha='left', va='center', fontweight='bold')
    
    # Customize chart
    plt.title('Price-to-Earnings (P/E) Ratio Comparison', fontsize=18)
    plt.xlabel('P/E Ratio', fontsize=14)
    plt.grid(axis='x', alpha=0.3)
    
    # Add industry average reference line
    avg_pe = 20  # Approximate market average
    plt.axvline(x=avg_pe, color='red', linestyle='--', alpha=0.7)
    plt.text(avg_pe + 1, 0.1, f'Market Avg (~{avg_pe})', 
             color='red', ha='left', va='bottom', transform=plt.gca().get_xaxis_transform())
    
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
        logger.info(f"Chart saved to {save_path}")
    
    plt.tight_layout()
    return plt

def plot_analyst_ratings(stocks_data, save_path=None):
    """Visualize analyst ratings for each stock."""
    df = create_stock_dataframe(stocks_data)
    if df is None:
        return
    
    plt.figure(figsize=(12, 6))
    
    # Extract numeric rating from rating string (e.g., "2.1 - Buy" -> 2.1)
    ratings = []
    for rating in df['analyst_rating']:
        if rating and isinstance(rating, str):
            try:
                ratings.append(float(rating.split(' ')[0]))
            except (ValueError, IndexError):
                ratings.append(np.nan)
        else:
            ratings.append(np.nan)
    
    df['rating_value'] = ratings
    df = df.sort_values('rating_value')
    
    # Define color based on rating (1-1.5: Strong Buy, 1.5-2.5: Buy, 2.5-3.5: Hold, etc.)
    colors = []
    labels = []
    for rating in df['rating_value']:
        if np.isnan(rating):
            colors.append('#9E9E9E')  # Gray for N/A
            labels.append('N/A')
        elif rating < 1.5:
            colors.append('#4CAF50')  # Green for Strong Buy
            labels.append('Strong Buy')
        elif rating < 2.5:
            colors.append('#8BC34A')  # Light Green for Buy
            labels.append('Buy')
        elif rating < 3.5:
            colors.append('#FFC107')  # Yellow for Hold
            labels.append('Hold')
        elif rating < 4.5:
            colors.append('#FF9800')  # Orange for Sell
            labels.append('Sell')
        else:
            colors.append('#F44336')  # Red for Strong Sell
            labels.append('Strong Sell')
    
    # Create horizontal bar chart
    bars = plt.barh(df['symbol'], df['rating_value'], color=colors)
    
    # Add rating labels
    for i, (bar, label) in enumerate(zip(bars, labels)):
        width = bar.get_width()
        plt.text(width + 0.1, bar.get_y() + bar.get_height()/2, 
                f'{width:.1f} - {label}', ha='left', va='center')
    
    # Customize chart
    plt.title('Analyst Ratings Comparison', fontsize=18)
    plt.xlabel('Rating (1: Strong Buy to 5: Strong Sell)', fontsize=14)
    plt.xlim(0, 5.5)
    plt.grid(axis='x', alpha=0.3)
    
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
        logger.info(f"Chart saved to {save_path}")
    
    plt.tight_layout()
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
        
        # Generate and save original charts
        plot_price_comparison(stocks_data, save_path=output_path/"price_comparison.png")
        plot_performance_comparison(stocks_data, save_path=output_path/"performance_comparison.png")
        plot_market_cap_comparison(stocks_data, save_path=output_path/"market_cap_comparison.png")
        plot_volume_comparison(stocks_data, save_path=output_path/"volume_comparison.png")
        plot_pe_ratio_comparison(stocks_data, save_path=output_path/"pe_ratio_comparison.png")
        plot_analyst_ratings(stocks_data, save_path=output_path/"analyst_ratings.png")

        logger.info(f"All charts generated and saved to {output_dir}")
        return True
    except Exception as e:
        logger.error(f"Error generating charts: {e}")
        return False