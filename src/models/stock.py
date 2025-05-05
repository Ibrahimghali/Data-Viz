class Stock:
    """Stock data model."""
    
    def __init__(self, data):
        self.symbol = data.get("symbol")
        self.name = data.get("longName")
        self.price = data.get("regularMarketPrice")
        self.change = data.get("regularMarketChange")
        self.percent = data.get("regularMarketChangePercent")
        self.volume = data.get("regularMarketVolume")
        self.day_low = data.get("regularMarketDayLow")
        self.day_high = data.get("regularMarketDayHigh")
        self.market_cap = data.get("marketCap")
        self.pe_ratio = data.get("trailingPE")
        self.eps = data.get("epsTrailingTwelveMonths")
        self.week52_low = data.get("fiftyTwoWeekLow")
        self.week52_high = data.get("fiftyTwoWeekHigh")
        self.dividend_yield = data.get("dividendYield")
        self.avg_volume = data.get("averageDailyVolume3Month")
        self.analyst_rating = data.get("averageAnalystRating")
        self.currency = data.get("currency")
        
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            "symbol": self.symbol,
            "name": self.name,
            "price": self.price,
            "change": self.change,
            "percent": self.percent,
            "volume": self.volume,
            "range": f"{self.day_low} - {self.day_high}",
            "market_cap": self.market_cap,
            "pe_ratio": self.pe_ratio,
            "eps": self.eps,
            "52wk_range": f"{self.week52_low} - {self.week52_high}",
            "dividend_yield": self.dividend_yield,
            "avg_volume": self.avg_volume,
            "analyst_rating": self.analyst_rating,
            "currency": self.currency
        }
        
    @classmethod
    def from_dict(cls, data):
        """Create a Stock instance from a dictionary."""
        stock = cls.__new__(cls)
        stock.symbol = data.get("symbol")
        stock.name = data.get("name")
        stock.price = data.get("price")
        stock.change = data.get("change")
        stock.percent = data.get("percent")
        stock.volume = data.get("volume")
        
        # Parse range
        range_str = data.get("range", "").split(" - ")
        stock.day_low = float(range_str[0]) if len(range_str) > 0 and range_str[0] else None
        stock.day_high = float(range_str[1]) if len(range_str) > 1 and range_str[1] else None
        
        stock.market_cap = data.get("market_cap")
        stock.pe_ratio = data.get("pe_ratio")
        stock.eps = data.get("eps")
        
        # Parse 52-week range
        week_range_str = data.get("52wk_range", "").split(" - ")
        stock.week52_low = float(week_range_str[0]) if len(week_range_str) > 0 and week_range_str[0] else None
        stock.week52_high = float(week_range_str[1]) if len(week_range_str) > 1 and week_range_str[1] else None
        
        stock.dividend_yield = data.get("dividend_yield")
        stock.avg_volume = data.get("avg_volume")
        stock.analyst_rating = data.get("analyst_rating")
        stock.currency = data.get("currency")
        return stock