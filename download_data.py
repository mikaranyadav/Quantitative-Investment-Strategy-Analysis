import yfinance as yf
import pandas as pd

print("Starting data pipeline...")

# Define the tickers
# MBG.DE is the official ticker for Mercedes-Benz Group AG
# ^GSPC is the ticker for the S&P 500 (our benchmark)
tickers = ['MBG.DE', '^GSPC']

# Define the date range (e.g., last 10 years)
start_date = '2015-01-01'
end_date = '2025-01-01'

# --- 1. Ingest Data ---
print(f"Downloading data for {tickers} from {start_date} to {end_date}...")
try:
    # We add auto_adjust=True to try and get 'Adj Close' by default
    data = yf.download(tickers, start=start_date, end=end_date)
except Exception as e:
    print(f"Error during download: {e}")
    exit()

# --- 2. Clean and Prepare Data ---
print("Cleaning and preparing data...")

# Check if the download returned an empty DataFrame
if data.empty:
    print("\n[ERROR] No data was downloaded. The DataFrame is empty.")
    print("This could be a temporary internet issue or a problem with the yfinance API.")
    print("Please try running the script again in a few moments.")
    exit()

# --- UPDATED CHECK ---
# We will use 'Close' as our primary data column
column_to_use = 'Close'

if column_to_use not in data.columns:
    print(f"\n[ERROR] The '{column_to_use}' column was not found in the downloaded data.")
    print("This is unexpected. Available columns are:", data.columns)
    exit()
# --- END OF UPDATED CHECK ---


# Select the 'Close' data
close_df = data[column_to_use]

# Rename columns for clarity
close_df = close_df.rename(columns={'MBG.DE': 'Daimler', '^GSPC': 'SP500'})

# Check for and remove any rows with missing data (e.g., market holidays)
initial_rows = len(close_df)
close_df = close_df.dropna()
final_rows = len(close_df)
print(f"Removed {initial_rows - final_rows} rows with missing data.")

# --- 3. Save to File ---
close_df.to_csv('historical_stock_data.csv')

print("\n--- Phase 1 Complete! ---")
print(f"Data saved to 'historical_stock_data.csv'")
print("\nFirst 5 rows of data:")
print(close_df.head())