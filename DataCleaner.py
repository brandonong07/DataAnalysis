import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import yfinance as yf
import math as math

class DataCleaner:
    
    # defining the constructor
    # turning yfinance into pandas dataframe and defining ticker as string
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        pass
    
    # preparing for SQL and turning adj_close to Adj Close
    def standardize(self):
        self.df = self.df.reset_index()
        if isinstance(self.df.index, (pd.DatetimeIndex, pd.Index)):
            self.df = self.df.reset_index()

        # Normalizing column names
        # adj_close -> Adj Close
        self.df.columns = [c.lower().replace(" ", "_") for c in self.df.columns]



        # Renaming datetime column to date if it exists
        if "datetime" in self.df.columns:
            self.df = self.df.rename(columns={"datetime": "date"})
        
        expected_columns = {"date", "open", "high", "low", "close", "adj_close", "volume"}
        missing = expected_columns - set(self.df.columns)
       
        # Raise error if any expected columns are missing
        if missing:
            raise ValueError(f"Missing expected columns: {missing}")
        
        self.df["date"] = pd.to_datetime(self.df["date"])
        # Ensuring correct data types

        self.df["ticker"] = self.ticker
        # ticker column

        # Handling duplicates by keeping the last occurrence
        self.df = self.df.sort_values("date").drop_duplicates(subset=["date"], keep="last").reset_index(drop=True)
        
        return self
    
    def analysis_columns(self, windows=(20,50)):
        if("adj_close" not in self.df.columns):
            raise ValueError("Run standardize() method before analysis_columns()")
        
        # Price as adjusted close
        self.df["price"] = self.df["adj_close"]

        # Returns
        self.df["returns"] = self.df["adj_close"].pct_change()

        # Log Returns
        self.df["log_return"] = self.df["return"].apply(
            lambda r: math.log1p(r) if pd.notna(r) and (1 + r) > 0 else pd.NA
        )

        for w in windows:
            # Moving Averages
            self.df[f"ma_{w}"] = self.df["adj_close"].rolling(window=w).mean()
            # Volatility
            self.df[f"volatility_{w}"] = self.df["returns"].rolling(window=w).std()

        return self

def main():
    # Example usage
    ticker = "AAPL"
    data = yf.download(ticker, start="2020-01-01", end="2023-01-01")
    cleaner = DataCleaner(data)
    cleaner.standardize().analysis_columns()
    print(cleaner.df.head())

main()


