import pandas as pd
import numpy as np

print("Starting backtest...")

# --- 1. Load Data ---
try:
    df = pd.read_csv('historical_stock_data.csv', parse_dates=['Date'], index_col='Date')
except FileNotFoundError:
    print("Error: 'historical_stock_data.csv' not found. Did you run download_data.py?")
    exit()

# --- 2. Define Strategy Parameters ---
sma_window = 30 # Our "momentum" window. We'll use 30 days.

# --- 3. Engineer Features (Create Signals) ---
print(f"Generating {sma_window}-day SMA and signals...")

# Calculate the 30-day Simple Moving Average (SMA) for Daimler
df['Daimler_SMA'] = df['Daimler'].rolling(window=sma_window).mean()

# Our signal: 1 if Price > SMA, 0 if Price < SMA
# np.where(condition, value_if_true, value_if_false)
df['Signal'] = np.where(df['Daimler'] > df['Daimler_SMA'], 1, 0)

# We must 'shift' the signal by one day. 
# Why? We can only buy *after* we see the signal. 
# We see the signal at the end of Day 1, so we buy at the start of Day 2.
df['Signal'] = df['Signal'].shift(1)

# --- 4. Calculate Returns ---
print("Calculating strategy returns...")

# Calculate daily percent change for both stocks
df['Daimler_Returns'] = df['Daimler'].pct_change()
df['SP500_Returns'] = df['SP500'].pct_change()

# Calculate our strategy's returns
# Strategy_Returns = Signal (from yesterday) * Today's Returns
df['Strategy_Returns'] = df['Signal'] * df['Daimler_Returns']

# --- 5. Clean Data and Save ---
# Our calculations create NaNs (e.g., the first 30 days)
# Let's drop them
results_df = df.dropna()

# Select only the columns we need for Phase 3
output_columns = ['Daimler_Returns', 'SP500_Returns', 'Strategy_Returns']
results_df[output_columns].to_csv('strategy_returns.csv')

print("\n--- Phase 2 Complete! ---")
print("Backtest finished. Strategy returns saved to 'strategy_returns.csv'")
print("\nFirst 5 rows of results:")
print(results_df[output_columns].head())