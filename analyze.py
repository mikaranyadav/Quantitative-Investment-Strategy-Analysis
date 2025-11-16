import pandas as pd
import numpy as np

print("Starting performance analysis...")

# Define constants
TRADING_DAYS_PER_YEAR = 252  # Standard number of trading days
RISK_FREE_RATE = 0.02  # Assumed 2% annual risk-free rate for Sharpe Ratio

# --- 1. Load Data ---
try:
    df = pd.read_csv('strategy_returns.csv', parse_dates=['Date'], index_col='Date')
except FileNotFoundError:
    print("Error: 'strategy_returns.csv' not found. Did you run backtest.py?")
    exit()

# --- 2. Calculate Equity Curve (Cumulative Returns) ---
# This shows the growth of $1 over time
df['Strategy_Equity'] = (1 + df['Strategy_Returns']).cumprod()
df['Daimler_Equity'] = (1 + df['Daimler_Returns']).cumprod()
df['SP500_Equity'] = (1 + df['SP500_Returns']).cumprod()

# Save the equity curve for our dashboard
equity_curve_df = df[['Strategy_Equity', 'Daimler_Equity', 'SP500_Equity']]
equity_curve_df.to_csv('equity_curve.csv')
print("Equity curve data saved to 'equity_curve.csv'.")

# --- 3. Define Statistical Model Functions ---

def calculate_cagr(equity_curve):
    """Calculates the Compound Annual Growth Rate (CAGR)."""
    total_return = equity_curve.iloc[-1]  # Final value of $1
    num_years = len(equity_curve) / TRADING_DAYS_PER_YEAR
    cagr = (total_return ** (1 / num_years)) - 1
    return cagr

def calculate_sharpe_ratio(returns):
    """Calculates the annualized Sharpe Ratio."""
    daily_risk_free_rate = (1 + RISK_FREE_RATE)**(1/TRADING_DAYS_PER_YEAR) - 1
    excess_returns = returns - daily_risk_free_rate
    
    # Calculate annualized mean and standard deviation of excess returns
    mean_excess_return = excess_returns.mean() * TRADING_DAYS_PER_YEAR
    std_dev_excess_return = excess_returns.std() * np.sqrt(TRADING_DAYS_PER_YEAR)
    
    # Handle division by zero if std_dev is 0
    if std_dev_excess_return == 0:
        return 0.0
        
    sharpe_ratio = mean_excess_return / std_dev_excess_return
    return sharpe_ratio

def calculate_max_drawdown(equity_curve):
    """Calculates the Maximum Drawdown (MDD)."""
    # Calculate the running maximum of the equity curve
    running_max = equity_curve.cummax()
    # Calculate the drawdown (percent drop from the peak)
    drawdown = (equity_curve - running_max) / running_max
    # Find the smallest (most negative) drawdown
    max_drawdown = drawdown.min()
    return max_drawdown

# --- 4. Calculate All Metrics ---
print("Calculating performance metrics...")

metrics = {
    'Strategy': {
        'CAGR': calculate_cagr(df['Strategy_Equity']),
        'Sharpe Ratio': calculate_sharpe_ratio(df['Strategy_Returns']),
        'Max Drawdown': calculate_max_drawdown(df['Strategy_Equity']),
    },
    'Buy & Hold Daimler': {
        'CAGR': calculate_cagr(df['Daimler_Equity']),
        'Sharpe Ratio': calculate_sharpe_ratio(df['Daimler_Returns']),
        'Max Drawdown': calculate_max_drawdown(df['Daimler_Equity']),
    },
    'Benchmark (S&P 500)': {
        'CAGR': calculate_cagr(df['SP500_Equity']),
        'Sharpe Ratio': calculate_sharpe_ratio(df['SP500_Returns']),
        'Max Drawdown': calculate_max_drawdown(df['SP500_Equity']),
    }
}

# Convert metrics dictionary to a DataFrame for easy viewing and saving
metrics_df = pd.DataFrame(metrics).T  # .T transposes the DataFrame

# --- 5. Save and Display Metrics ---
metrics_df.to_csv('performance_metrics.csv')
print("Performance metrics saved to 'performance_metrics.csv'.")

print("\n--- Phase 3 Complete! ---")
print("\nFinal Performance Metrics:")
# Format the output for readability
print(metrics_df.to_string(float_format="{:,.2%}".format))