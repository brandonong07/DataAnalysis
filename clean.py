import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import yfinance as yf

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
        
        
        

        return self

df = yf.download("AAPL", period="1y")
