import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

class DataCleaner:

    def __init__(self, ticker_symbol):
        self.ticker = ticker_symbol
        self.data = None
        self.clean_data_frame = None

    def fetch_data(self, start_date, end_date):
        self.data = yf.download(self.ticker, start=start_date, end=end_date)
        if self.data.empty:
            raise ValueError("No data fetched for the given ticker and date range.")
        print("Data fetched successfully.")
        print(self.data.head())
        pass

    def clean_and_prep(self):
        if self.data is None:
            print("No data to clean. Please fetch data.")
            return

        df = self.data.copy()

        # Handle missing values
        df.ffill(inplace=True)
        df.dropna(inplace=True)

        # Ensure Index is Datetime
        if not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index)
        
        # Remove Duplicates
        df = df[~df.index.duplicated(keep='first')]

        self.clean_data_frame = df
        print("Data cleaned.")
        pass

    def aggregate_metrics(self):
        if self.clean_data_frame is None:
            print("No cleaned data to aggregate. Please clean data first.")
            return

        df = self.clean_data_frame

        # Calculate daily returns
        df['Daily Return'] = df['Close'].pct_change()

        # Calculate moving averages (20-day and 50-day)
        df['MA20'] = df['Close'].rolling(window=20).mean()
        df['MA50'] = df['Close'].rolling(window=50).mean()
        self.clean_data_frame = df
        print("Metrics aggregated.")
        pass

    def visualize_trends(self):
        if self.clean_data_frame is None:
            print("No cleaned data to visualize. Please clean data first.")
            return

        df = self.clean_data_frame

        plt.figure(figsize=(14, 7))
    
        # Plotting the raw price and the trends
        plt.plot(df.index, df['Close'], label='Adjusted Close', alpha=0.5)
        plt.plot(df.index, df['MA50'], label='50-Day MA (Trend)', color='orange', linestyle='--')
        plt.plot(df.index, df['MA20'], label='20-Day MA (Trend)', color='red', linestyle='--')

        plt.title(f'{self.ticker} Price Trends & Moving Averages')
        plt.xlabel('Date')
        plt.ylabel('Price (USD)')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        pass

    def summary(self):
        if self.clean_data_frame is None:
            print("No cleaned data to summarize. Please clean data first.")
            return

        df = self.clean_data_frame

        total_return = (df['Close'].iloc[-1] / df['Close'][0] - 1) * 100
        highest_price = df['Close'].max()

        current_price = df['Close'].iloc[-1]
        lowest_price = df['Close'].min()

        print(f"Summary for {self.ticker}:")
        print(f"Total Return: {total_return:.2f}%")
        print(f"Highest Price: ${highest_price:.2f}")
        pass

c = DataCleaner('AAPL')
# 1. Data
c.fetch_data('2020-01-01', '2023-01-01')
# 2. Clean & Prep
c.clean_and_prep()
# 3. Aggregate Metrics
c.aggregate_metrics()
# 4. Visualize Trends
c.visualize_trends()
# 5. Summary
c.summary()
